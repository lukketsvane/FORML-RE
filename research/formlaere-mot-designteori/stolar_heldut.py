#!/usr/bin/env python3
"""Utforskande held-ut-prognose av STOLAR-kataloggeometri, ikkje av §§6.6-val.

Køyr med: python stolar_heldut.py api.json --out stolar_resultat.json
Krev numpy, pandas og scikit-learn. Skriptet endrar ikkje kjeldearkivet.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit

SEED = 20261107
DIMENSIONS = ("height_cm", "width_cm", "depth_cm")


def prepare(path: Path):
    source = json.loads(path.read_text(encoding="utf8"))
    if not isinstance(source, dict) or not isinstance(source.get("chairs"), list):
        raise ValueError("Forventa STOLAR api.json")
    df = pd.DataFrame(source["chairs"])
    required = {"id", "year_from", "materials", *DIMENSIONS}
    if not required <= set(df.columns):
        raise ValueError("Manglar felt: " + repr(required - set(df.columns)))

    # Dokumenter ei kanonisk rad per museums-ID. Ingen konfliktar vert løyste.
    df["nonempty_fields"] = df.notna().sum(axis=1)
    df = (df.sort_values(["id", "nonempty_fields"], ascending=[True, False], kind="stable")
            .drop_duplicates("id", keep="first").copy())
    unique_count = len(df)
    for col in (*DIMENSIONS, "year_from", "year_to"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for field, low, high in (("height_cm", 30, 220),
                             ("width_cm", 20, 200),
                             ("depth_cm", 15, 150),
                             ("year_from", 1500, 2026)):
        df = df.loc[df[field].between(low, high)].copy()

    df = df.loc[~df["keywords"].fillna("").str.contains(
        "Arkitekturfotografi|Dekorativ gjenstand|Sportsutstyr",
        regex=True, case=False)].copy()

    # Eksakt målebilete + same år og materiale = same lekkasjekontrollgruppe.
    df["family_group"] = [
        f"{int(y)}|{h:.1f}|{w:.1f}|{d:.1f}|{m}"
        for y, h, w, d, m in zip(
            df.year_from, df.height_cm, df.width_cm,
            df.depth_cm, df.materials)
    ]
    df["source"] = np.where(df["id"].str.startswith("O"), "V&A", "Nasjonalmuseet")
    df["log_H_W"] = np.log(df.height_cm / df.width_cm)
    df["log_W_D"] = np.log(df.width_cm / df.depth_cm)
    df["log_size"] = np.log((df.height_cm * df.width_cm * df.depth_cm)**(1/3))
    df = df.reset_index(drop=True)

    provenance = {
        "source_generated": source.get("generated"),
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "input_rows": len(source["chairs"]),
        "unique_object_ids": unique_count,
        "included_objects": len(df),
        "distinct_leakage_groups": int(df.family_group.nunique()),
        "included_style_labelled": int(df["style"].notna().sum()),
        "source_counts": df.source.value_counts().to_dict(),
        "measurement_bounds": {"H_cm": [30, 220], "W_cm": [20, 200],
                               "D_cm": [15, 150], "year_from": [1500, 2026]},
    }
    return df, provenance


def material_sets(df):
    return [set(s.strip().lower() for s in str(m).split(",") if s.strip())
            for m in df["materials"]]


def features(train, test):
    z_train = (train.year_from.to_numpy() - 1800) / 100
    z_test = (test.year_from.to_numpy() - 1800) / 100
    years = (np.stack([z_train, z_train**2, z_train**3], 1),
             np.stack([z_test, z_test**2, z_test**3], 1))

    tr_m = material_sets(train)
    te_m = material_sets(test)
    counter = Counter(s for terms in tr_m for s in terms)
    vocab_m = sorted(s for s, n in counter.items() if n >= 20)

    def encode_material(values):
        return np.array([[float(v in values_i) for v in vocab_m]
                         for values_i in values], dtype=float)

    materials = (encode_material(tr_m), encode_material(te_m))
    styles = train["style"].fillna("UNRECORDED").astype(str).tolist()
    st_counts = Counter(styles)
    vocab_s = sorted(s for s, n in st_counts.items() if n >= 5)

    def encode_style(values):
        return np.array([[float(s == v) for v in vocab_s]
                         for s in values], dtype=float)

    style = (encode_style(styles),
             encode_style(test["style"].fillna("UNRECORDED").astype(str)))
    return {"year": years, "materials": materials, "style": style}


def evaluate(df, n_splits=12):
    groups = df.family_group
    folds = GroupShuffleSplit(n_splits=n_splits, test_size=.25, random_state=SEED)
    y = df[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    models = {
        "null": (), "year": ("year",), "materials": ("materials",),
        "year_materials": ("year", "materials"), "style": ("style",),
        "year_style": ("year", "style"),
        "year_style_materials": ("year", "style", "materials"),
    }
    results = []
    for k, (train_ids, test_ids) in enumerate(folds.split(df, groups=groups)):
        train, test = df.iloc[train_ids], df.iloc[test_ids]
        assert not (set(train.family_group) & set(test.family_group))
        f = features(train, test)
        center, scale = y[train_ids].mean(0), y[train_ids].std(0)
        if (scale <= 0).any():
            raise ValueError("Degenerert utfall")
        train_y = (y[train_ids] - center) / scale
        test_y = (y[test_ids] - center) / scale

        for name, terms in models.items():
            if "style" in terms and df["style"].isna().any():
                continue
            if not terms:
                predicted = np.zeros_like(test_y)
            else:
                x_train = np.concatenate([f[t][0] for t in terms], axis=1)
                x_test = np.concatenate([f[t][1] for t in terms], axis=1)
                predicted = Ridge(alpha=20.0).fit(x_train, train_y).predict(x_test)
            loss = float(((test_y - predicted)**2).mean())
            results.append({"fold": k, "model": name,
                            "n_test": len(test_ids), "loss": loss})

    result = {}
    df_results = pd.DataFrame(results)
    for model, group in df_results.groupby("model"):
        values = group["loss"].to_numpy()
        result[model] = {
            "mean_loss": float(values.mean()),
            "std_across_overlapping_splits": float(values.std(ddof=1)),
            "losses": [round(float(x), 6) for x in values],
        }

    changes = {}
    for challenger, baseline in (
        ("year_materials", "year"), ("materials", "null"),
        ("year", "null"), ("year_style", "year"),
        ("year_style_materials", "year_style"),
        ("year_materials", "year_style"),
    ):
        if challenger not in result or baseline not in result:
            continue
        a = np.array(result[challenger]["losses"])
        b = np.array(result[baseline]["losses"])
        changes[f"{challenger}_vs_{baseline}"] = {
            "mean_delta_loss": float((a-b).mean()),
            "wins": int((a < b).sum()),
            "split_count": len(a),
        }
    return {"n_objects": len(df), "models": result, "comparisons": changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Eksakt kjeldekopi av STOLAR api.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    full, provenance = prepare(args.input)
    out = {
        "provenance": provenance,
        "all_objects": evaluate(full),
        "style_labelled": evaluate(full.loc[full["style"].notna()].reset_index(drop=True)),
        "vam_only": evaluate(full.loc[full.source == "V&A"].reset_index(drop=True)),
        "warning": "Utforskande assosiasjonar, ikkje valmekanisme, kausalitet eller evidens for heile Formlæra.",
    }
    contents = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(contents, encoding="utf8")
    print(contents)


if __name__ == "__main__":
    main()
