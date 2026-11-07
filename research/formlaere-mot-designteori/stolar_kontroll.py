#!/usr/bin/env python3
"""Fastsplittkontroll, 199 negative kontrollar og tidsmotprøve for STOLAR.

Køyr: python stolar_kontroll.py api.json --out kontroll.json
Dette er utforskande analysar, ikkje kausal identifisering eller §6.6-data.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit

import stolar_heldut as mod


def losses(train, test, model, feature_data, material_override=None):
    target_cols = ["log_H_W", "log_W_D", "log_size"]
    y_train = train[target_cols].to_numpy()
    center, scale = y_train.mean(0), y_train.std(0)
    tr = (y_train - center) / scale
    te = (test[target_cols].to_numpy() - center) / scale
    terms = {
        "null": (), "year": ("year",),
        "year_materials": ("year", "materials"),
        "materials": ("materials",),
    }[model]
    if not terms:
        prediction = np.zeros_like(te)
    else:
        X = np.column_stack([
            (material_override if term == "materials" and material_override is not None
             else feature_data[term][0]) for term in terms
        ])
        X_test = np.column_stack([feature_data[term][1] for term in terms])
        prediction = Ridge(alpha=20.0).fit(X, tr).predict(X_test)
    return np.mean((te - prediction) ** 2, axis=1)


def run(path: Path):
    sample, source = mod.prepare(path)
    ix_train, ix_test = next(GroupShuffleSplit(
        n_splits=1, test_size=.25, random_state=mod.SEED
    ).split(sample, groups=sample.family_group))
    train, test = sample.iloc[ix_train], sample.iloc[ix_test]
    assert not set(train.family_group) & set(test.family_group)
    f = mod.features(train, test)

    year = losses(train, test, "year", f)
    combined = losses(train, test, "year_materials", f)
    improvements = year - combined
    rng = np.random.default_rng(mod.SEED)

    # Cluster-bootstrap av reelt samregistrerte målebilete.
    grouped = defaultdict(list)
    for key, delta in zip(test.family_group, improvements):
        grouped[key].append(float(delta))
    means = np.array([np.mean(v) for v in grouped.values()])
    sizes = np.array([len(v) for v in grouped.values()])
    choices = rng.integers(0, len(means), size=(4000, len(means)))
    boots = (means[choices]*sizes[choices]).sum(1) / sizes[choices].sum(1)

    # Negativ kontroll: stokking av materiale i trening innan 50-årsbolkar.
    historical_bins = (train.year_from.to_numpy()//50).astype(int)
    mats = f["materials"][0]
    placebo = []
    for repeat in range(199):
        shuffled = np.arange(len(train))
        for era in np.unique(historical_bins):
            ids = np.flatnonzero(historical_bins == era)
            shuffled[ids] = rng.permutation(ids)
        shuffled_loss = losses(train, test, "year_materials", f,
                               material_override=mats[shuffled])
        placebo.append(float(np.mean(year - shuffled_loss)))

    placebo = np.array(placebo)
    observed = float(improvements.mean())

    # Separat negativ test: dette polynomiet vert ekstrapolert i tid.
    transfers = {}
    for name, mask in (("before_1900_to_1900_plus", sample.year_from < 1900),
                       ("1900_plus_to_before_1900", sample.year_from >= 1900)):
        historical, future = sample.loc[mask], sample.loc[~mask]
        feats = mod.features(historical, future)
        transfers[name] = {
            "n_train":len(historical), "n_test":len(future),
            "null_loss":float(losses(historical, future, "null", feats).mean()),
            "year_materials_loss":float(losses(
                historical, future, "year_materials", feats).mean()),
        }

    return {
        "source_sha256":source["input_sha256"],
        "train_objects":len(train), "test_objects":len(test),
        "test_leakage_groups":len(means),
        "year_loss":float(year.mean()),
        "year_materials_loss":float(combined.mean()),
        "material_improvement":observed,
        "bootstrap_ci95_descriptive":[float(x) for x in np.quantile(boots,[.025,.975])],
        "placebo_permutations":len(placebo),
        "placebo_mean":float(placebo.mean()),
        "placebo_ci95":[float(x) for x in np.quantile(placebo,[.025,.975])],
        "placebo_upper_tail_with_plus_one":float(
            (1+(placebo>=observed).sum())/(1+len(placebo))),
        "temporal_negative_transfer":transfers,
        "status":"After data inspection; not preregistered; association only.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = json.dumps(run(args.input), ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(report, encoding="utf8")
    print(report)


if __name__ == "__main__":
    main()
