#!/usr/bin/env python3
"""Nonlinear STOLAR sensitivity to materials after time, technique and origin.

Exploratory held-out metadata prediction, not a direct test of Formlære §6.6.
Run: python stolar_ikkjelinear.py api.json --out nonlinear_result.json
"""
from pathlib import Path
import argparse
import json

import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import HistGradientBoostingRegressor

from stolar_heldut import prepare, features, SEED
from stolar_robusthet import technique_features, category_features


def evaluate(df, splits=6):
    df = df.reset_index(drop=True)
    y = df[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    results = []
    for train_idx, test_idx in GroupShuffleSplit(n_splits=splits,test_size=.25,random_state=SEED).split(df,groups=df.family_group):
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        assert not set(train.family_group) & set(test.family_group)
        f = features(train,test)
        f["technique"] = technique_features(train,test)
        f["origin"] = category_features(train,test,"origin")
        center, scale = y[train_idx].mean(0), y[train_idx].std(0)
        train_y = (y[train_idx]-center)/scale
        actual = (y[test_idx]-center)/scale
        losses = []
        for cols in [
            ("year","technique","origin"),
            ("year","technique","origin","materials"),
        ]:
            X = np.column_stack([f[name][0] for name in cols])
            Z = np.column_stack([f[name][1] for name in cols])
            reg = MultiOutputRegressor(HistGradientBoostingRegressor(
                max_iter=60,max_leaf_nodes=10,learning_rate=.05,
                l2_regularization=2.0,random_state=SEED
            ))
            reg.fit(X,train_y)
            forecast = reg.predict(Z)
            losses.append(float(np.mean((forecast-actual)**2)))
        results.append(losses)
    score = np.array(results)
    return {
        "n":len(df), "folds":splits,
        "without_material":float(score[:,0].mean()),
        "with_material":float(score[:,1].mean()),
        "material_improvement":float(np.mean(score[:,0]-score[:,1])),
        "positive_folds":int(sum(score[:,1] < score[:,0])),
        "per_fold":score.tolist(),
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    df,p = prepare(args.input)
    report = {
        "source_sha256":p["input_sha256"],
        "full":evaluate(df),
        "since_1900":evaluate(df.loc[df.year_from>=1900]),
        "scope":"Exploratory: more flexible rival model. Cannot prove causality or §6.6.",
    }
    result=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.out:args.out.write_text(result,encoding="utf8")
    print(result)


if __name__=="__main__":
    main()
