#!/usr/bin/env python3
"""Exploratory: materiale utover produksjonsår og registrert teknikk i STOLAR.

Køyr: python teknikk_sensitivitet.py api.json --out kontroll.json
Ikkje direkte test av Formlæra §6.6; association, ikkje kausalitet.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import HistGradientBoostingRegressor

import stolar_heldut as mod


def tokens(value):
    if value is None or (isinstance(value,float) and np.isnan(value)):
        return set()
    return {t.strip().lower() for t in str(value).split(",") if t.strip()}


def technique_features(train, test, minimum_training_count=10):
    tr = [tokens(x) for x in train.technique]
    te = [tokens(x) for x in test.technique]
    counts = Counter(t for row in tr for t in row)
    vocab = sorted(k for k, v in counts.items() if v >= minimum_training_count)
    def encode(rows):
        return np.array([[float(t in x) for t in vocab]+[float(not x)] for x in rows])
    return encode(tr), encode(te)


def evaluate(df):
    y = df[["log_H_W","log_W_D","log_size"]].to_numpy()
    splitter = GroupShuffleSplit(n_splits=12,test_size=0.25,random_state=mod.SEED)
    scores = []
    for fold,(itr,ite) in enumerate(splitter.split(df,groups=df.family_group)):
        train,test=df.iloc[itr],df.iloc[ite]
        assert not set(train.family_group) & set(test.family_group)
        features=mod.features(train,test)
        tech=technique_features(train,test)
        center,scale=y[itr].mean(0),y[itr].std(0)
        target=(y[itr]-center)/scale
        truth=(y[ite]-center)/scale
        Xbase=np.column_stack((features["year"][0],tech[0]))
        Zbase=np.column_stack((features["year"][1],tech[1]))
        Xext=np.column_stack((Xbase,features["materials"][0]))
        Zext=np.column_stack((Zbase,features["materials"][1]))
        loss=[]
        for X,Z in ((Xbase,Zbase),(Xext,Zext)):
            learner=MultiOutputRegressor(HistGradientBoostingRegressor(
                max_iter=80,max_leaf_nodes=10,learning_rate=0.05,
                l2_regularization=2.0,random_state=mod.SEED
            ))
            learner.fit(X,target)
            loss.append(float(np.mean((learner.predict(Z)-truth)**2)))
        scores.append(loss)
    a=np.asarray(scores)
    return {
        "n_objects":len(df),
        "mean_year_tech":float(a[:,0].mean()),
        "mean_year_tech_materials":float(a[:,1].mean()),
        "added_material_improvement":float((a[:,0]-a[:,1]).mean()),
        "wins_in_12_overlapping_splits":int(sum(a[:,1]<a[:,0])),
        "losses_by_fold":a.tolist(),
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    df,provenance=mod.prepare(args.input)
    result={
        "source_sha256":provenance["input_sha256"],
        "all_objects":evaluate(df),
        "technique_documented":evaluate(df.loc[df.technique.notna()].reset_index(drop=True)),
        "warning":"Exploratory, not preregistered, not causal. Missing technique labels are not random; repeated splits are overlapping.",
    }
    content=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.out:args.out.write_text(content,encoding="utf8")
    print(content)
