#!/usr/bin/env python3
"""Exploratory STOLAR held-out sensitivity: time, technique, geography, material.

Run beside stolar_heldut.py:
    python stolar_robusthet.py /path/to/api.json --out robusthet.json

Uses the independently archived STOLAR JSON and its SHA-256. Models do NOT
observe design alternatives, agent evaluations or the form-grammar generator.
Therefore no result here can be described as a direct test of Formlære §6.6.
Requires numpy, pandas, scikit-learn.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit

from stolar_heldut import prepare, features, SEED


def tokenize(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return set()
    return {x.strip().lower() for x in str(value).split(",") if x.strip()}


def technique_features(train, test, threshold=10):
    tr, te = [tokenize(v) for v in train.technique], [tokenize(v) for v in test.technique]
    freq = Counter(token for values in tr for token in values)
    vocab = sorted(token for token, n in freq.items() if n >= threshold)
    def encoded(values):
        return np.array([[float(t in row) for t in vocab] + [float(not row)] for row in values])
    return encoded(tr), encoded(te)


def category_features(train, test, column, threshold=15):
    tr = train[column].fillna("UNRECORDED").astype(str).str.lower().str.strip().tolist()
    te = test[column].fillna("UNRECORDED").astype(str).str.lower().str.strip().tolist()
    freq = Counter(tr)
    vocab = sorted(v for v, n in freq.items() if n >= threshold)
    def encoded(values):
        return np.array([[float(v == label) for label in vocab] for v in values])
    return encoded(tr), encoded(te)


def compare(df, folds=12):
    Y = df[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    splits = GroupShuffleSplit(n_splits=folds, test_size=.25, random_state=SEED)
    sets = {
        "year": ("year",),
        "year_materials": ("year", "materials"),
        "year_technique": ("year", "technique"),
        "year_technique_materials": ("year", "technique", "materials"),
        "year_technique_origin": ("year", "technique", "origin"),
        "year_technique_origin_materials": ("year", "technique", "origin", "materials"),
        "year_technique_nationality": ("year", "technique", "nationality"),
        "year_technique_nationality_materials": ("year", "technique", "nationality", "materials"),
    }
    fold_scores = {name: [] for name in sets}
    fold_axes = {name: [] for name in sets}
    for train_ids, test_ids in splits.split(df, groups=df.family_group):
        train, test = df.iloc[train_ids], df.iloc[test_ids]
        assert not set(train.family_group) & set(test.family_group), "held-out group leakage"
        f = features(train, test)
        f["technique"] = technique_features(train, test)
        f["origin"] = category_features(train, test, "origin")
        f["nationality"] = category_features(train, test, "nationality")
        center, scale = Y[train_ids].mean(0), Y[train_ids].std(0)
        if np.any(scale <= 0):
            raise ValueError("degenerate outcome")
        ytrain = (Y[train_ids] - center) / scale
        ytest = (Y[test_ids] - center) / scale
        for label, terms in sets.items():
            X = np.column_stack([f[t][0] for t in terms])
            Z = np.column_stack([f[t][1] for t in terms])
            forecast = Ridge(alpha=20).fit(X, ytrain).predict(Z)
            axes_loss = ((forecast - ytest)**2).mean(0)
            fold_scores[label].append(float(axes_loss.mean()))
            fold_axes[label].append([float(v) for v in axes_loss])

    models = {label: {
        "mean_normalized_mse": float(np.mean(values)),
        "axes_mean_normalized_mse": np.mean(fold_axes[label], 0).tolist(),
        "folds": [round(float(v), 6) for v in values],
    } for label, values in fold_scores.items()}
    comparisons = {}
    for base, after in [
        ("year", "year_materials"),
        ("year_technique", "year_technique_materials"),
        ("year_technique_origin", "year_technique_origin_materials"),
        ("year_technique_nationality", "year_technique_nationality_materials"),
    ]:
        a = np.asarray(fold_scores[base])
        b = np.asarray(fold_scores[after])
        comparisons[after + "_vs_" + base] = {
            "mean_improvement": float((a - b).mean()),
            "wins": int(sum(b < a)), "folds": len(a),
            "per_axis_mean_improvement": (
                np.mean(np.array(fold_axes[base])-np.array(fold_axes[after]), 0).tolist()
            ),
        }
    return {"n_objects": len(df), "n_leakage_groups": int(df.family_group.nunique()),
            "models": models, "comparisons": comparisons}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--expected-sha256", default=None)
    args = parser.parse_args()
    df, provenance = prepare(args.input)
    if args.expected_sha256 and provenance["input_sha256"] != args.expected_sha256:
        raise ValueError("Input file differs from the locked source")
    populations = {
        "all": df, "before_1900": df.loc[df.year_from < 1900],
        "since_1900": df.loc[df.year_from >= 1900],
        "technique_known": df.loc[df.technique.notna()],
        "vam_only": df.loc[df.source == "V&A"],
    }
    report = {
        "provenance": provenance,
        "analyses": {key: compare(value.copy()) for key, value in populations.items()},
        "scope": "Exploratory metadata prediction. Not causal; not a §6.6 choice-model test.",
        "overlapping_folds": "Twelve group splits are not independent replicates or a confirmatory CI.",
    }
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(content, encoding="utf8")
    print(content)


if __name__ == "__main__":
    main()
