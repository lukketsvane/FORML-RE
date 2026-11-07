#!/usr/bin/env python3
"""Exploratory group hold-out with linked museum IDs and named designers.

Run: python stolar_designar_holdut.py /path/to/api.json
No attempt to estimate causal influence or choice probabilities.
"""
import argparse
from collections import Counter
from pathlib import Path
import json

import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import Ridge

from stolar_heldut import prepare, features, SEED
from stolar_robusthet import technique_features, category_features


def artist_clusters(data):
    """Union exact measurement families and identifiable same-maker objects."""
    rows = data.reset_index(drop=True)
    parent = list(range(len(rows)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def union(i, j):
        parent[root(i)] = root(j)
    first = {}
    unknown = {"", "unknown", "ukjent", "ikkje registrert", "anonymous", "anonym"}
    for i, (_, row) in enumerate(rows.iterrows()):
        raw_maker = row.get("designer")
        maker = raw_maker.strip().lower() if isinstance(raw_maker, str) else ""
        keys = ["family:" + row["family_group"]]
        if maker not in unknown:
            keys.append("maker:" + maker)
        for key in keys:
            if key in first:
                union(i, first[key])
            else:
                first[key] = i
    return np.array([root(i) for i in range(len(rows))])


def evaluate(df, folds=12):
    df = df.reset_index(drop=True)
    groups = artist_clusters(df)
    y = df[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    out = []
    for train_ids, test_ids in GroupShuffleSplit(
        n_splits=folds, test_size=0.25, random_state=SEED
    ).split(df, groups=groups):
        train, test = df.iloc[train_ids], df.iloc[test_ids]
        assert not set(groups[train_ids]) & set(groups[test_ids])
        f = features(train, test)
        f["technique"] = technique_features(train, test)
        f["origin"] = category_features(train, test, "origin")
        mean, scale = y[train_ids].mean(0), y[train_ids].std(0)
        yt = (y[train_ids] - mean)/scale
        obs = (y[test_ids] - mean)/scale
        fold = []
        for terms in (("year", "technique", "origin"),
                      ("year", "technique", "origin", "materials")):
            X = np.column_stack([f[k][0] for k in terms])
            Z = np.column_stack([f[k][1] for k in terms])
            pred = Ridge(alpha=20).fit(X, yt).predict(Z)
            fold.append(float(np.mean((pred-obs)**2)))
        out.append(fold)
    results = np.array(out)
    return {
        "n":len(df), "independent_holdout_groups":len(set(groups)),
        "baseline_loss":float(results[:,0].mean()),
        "plus_material_loss":float(results[:,1].mean()),
        "improvement":float(np.mean(results[:,0]-results[:,1])),
        "winning_splits":int(sum(results[:,1] < results[:,0])),
        "splits":folds,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    df,prov=prepare(args.input)
    result={
        "source_sha256":prov["input_sha256"],
        "all":evaluate(df),
        "before_1900":evaluate(df.loc[df.year_from<1900]),
        "since_1900":evaluate(df.loc[df.year_from>=1900]),
        "scope":"Exploratory observed chair metadata, not choice model or causal proof.",
    }
    content=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.out:args.out.write_text(content,encoding="utf8")
    print(content)


if __name__=="__main__":main()
