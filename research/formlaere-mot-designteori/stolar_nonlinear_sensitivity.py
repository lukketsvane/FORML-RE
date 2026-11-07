#!/usr/bin/env python3
"""Ikkje-lineær kontroll av STOLAR: årstal vs årstal+materiale på same holdouts.

For eksakt same arkiverte api.json som stolar_heldut.py.
Dette er ikkje kausal identifisering og ikkje ei direkte prøve av §6.6.
Krev pandas, numpy, scikit-learn.
"""
from pathlib import Path
import argparse
import json

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.multioutput import MultiOutputRegressor

import stolar_heldut as mod


def run(path):
    df, provenance = mod.prepare(path)
    y = df[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    splits = GroupShuffleSplit(n_splits=12, test_size=0.25, random_state=mod.SEED)
    records = []
    for fold, (train, test) in enumerate(splits.split(df, groups=df.family_group)):
        f = mod.features(df.iloc[train], df.iloc[test])
        center = y[train].mean(0)
        std = y[train].std(0)
        labels = (y[train] - center) / std
        heldout = (y[test] - center) / std
        metrics = {"fold": fold, "train_n": len(train), "test_n": len(test)}
        for name, included in (
            ("year", ("year",)),
            ("year_materials", ("year", "materials")),
        ):
            X = np.column_stack([f[t][0] for t in included])
            Z = np.column_stack([f[t][1] for t in included])
            predictor = MultiOutputRegressor(
                HistGradientBoostingRegressor(
                    max_iter=80, max_leaf_nodes=10, learning_rate=0.05,
                    l2_regularization=2.0, random_state=mod.SEED,
                )
            )
            predictor.fit(X, labels)
            pred = predictor.predict(Z)
            metrics[name] = float(np.mean((heldout-pred)**2))
        records.append(metrics)
    a = np.array([r["year"] for r in records])
    b = np.array([r["year_materials"] for r in records])
    return {
        "study": "exploratory_not_preregistered",
        "provenance": provenance,
        "year_mean_normalized_mse": float(a.mean()),
        "year_material_mean_normalized_mse": float(b.mean()),
        "mean_absolute_improvement": float((a-b).mean()),
        "wins_across_overlapping_splits": int((b < a).sum()),
        "folds": records,
        "limits": [
            "This is observational catalog metadata, not a causal mechanism.",
            "Twelve overlapping splits are not twelve independent replications.",
            "The selected material and geometry schema was inspected before testing.",
            "No agent estimates, choice sets or calibrated generator exist in STOLAR.",
        ],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    contents = json.dumps(run(args.input), ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(contents, encoding="utf8")
    print(contents)
