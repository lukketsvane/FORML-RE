#!/usr/bin/env python3
"""One fixed STOLAR held-out split with paired cluster-bootstrap intervals.

Run: python stolar_parvis_intervall.py /path/to/api.json
Exploratory uncertainty conditional on this pre-chosen seed and model family.
Not causal inference, and not a preregistered independent replication.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit

from stolar_heldut import prepare, features, SEED
from stolar_robusthet import technique_features, category_features


def evaluate(df, seed=SEED):
    df=df.reset_index(drop=True)
    train_ids,test_ids=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=seed).split(df,groups=df.family_group))
    train,test=df.iloc[train_ids],df.iloc[test_ids]
    assert not set(train.family_group)&set(test.family_group)
    f=features(train,test)
    f["technique"]=technique_features(train,test)
    f["origin"]=category_features(train,test,"origin")

    y=df[["log_H_W","log_W_D","log_size"]].to_numpy()
    center,scale=y[train_ids].mean(0),y[train_ids].std(0)
    ytrain=(y[train_ids]-center)/scale
    ytest=(y[test_ids]-center)/scale
    losses=[]
    for cols in [
        ("year","technique","origin"),
        ("year","technique","origin","materials"),
    ]:
        X=np.column_stack([f[k][0] for k in cols])
        Z=np.column_stack([f[k][1] for k in cols])
        pred=Ridge(alpha=20).fit(X,ytrain).predict(Z)
        losses.append(np.mean((ytest-pred)**2,axis=1))
    diff=losses[0]-losses[1]
    by_group=defaultdict(list)
    for name,val in zip(test.family_group,diff):
        by_group[name].append(float(val))
    sums=np.array([sum(v) for v in by_group.values()])
    sizes=np.array([len(v) for v in by_group.values()])
    rng=np.random.default_rng(seed)
    ix=rng.integers(0,len(sums),size=(4000,len(sums)))
    boot=sums[ix].sum(1)/sizes[ix].sum(1)
    return {
        "train":len(train),"test":len(test),"test_groups":len(by_group),
        "baseline_mean_mse":float(np.mean(losses[0])),
        "plus_materials_mean_mse":float(np.mean(losses[1])),
        "mean_improvement":float(np.mean(diff)),
        "paired_cluster_bootstrap95_descriptive":[float(x) for x in np.quantile(boot,[.025,.975])],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    df,provenance=prepare(args.input)
    out={
        "source_sha256":provenance["input_sha256"],
        "all":evaluate(df),
        "before_1900":evaluate(df.loc[df.year_from<1900]),
        "since_1900":evaluate(df.loc[df.year_from>=1900]),
        "qualifier":"Conditional and exploratory; no preregistered or causal claim.",
    }
    s=json.dumps(out,ensure_ascii=False,indent=2)+"\n"
    if args.out:args.out.write_text(s,encoding="utf8")
    print(s)


if __name__=="__main__":
    main()
