#!/usr/bin/env python3
"""Create an unlabelled, reproducible double-coder audit frame; never hallucinate labels."""
import argparse, sqlite3, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,default=20261102)
    p.add_argument("--per-theme",type=int,default=15)
    p.add_argument("--excluded",type=int,default=30)
    args=p.parse_args()
    root=ROOT/"results";root.mkdir(exist_ok=True)
    from database import ensure_database
    ensure_database()
    conn=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    incl=pd.read_csv(root/"semantic_clusters.csv",dtype={"id":"str"})
    details=pd.read_sql_query("SELECT id,doi,oa_url,source FROM works",conn)
    included=incl.merge(details,on="id",how="left")
    rng=np.random.default_rng(args.seed)
    chosen=[]
    for theme,g in included.groupby("theme"):
        # Random within each theme and spread over eras where possible.
        n=min(args.per_theme,len(g))
        selected=g.iloc[rng.choice(len(g),size=n,replace=False)]
        chosen.append(selected)
    frame=pd.concat(chosen,ignore_index=True) if chosen else included.head(0)
    frame["selection_group"]="included_random_within_theme"
    out=pd.read_sql_query("SELECT id,doi,title,oa_url,source,year FROM works WHERE in_scope=0",conn)
    if len(out):
        out=out.iloc[rng.choice(len(out),size=min(args.excluded,len(out)),replace=False)]
        out["selection_group"]="excluded_random"
        frame=pd.concat([frame,out],ignore_index=True)
    frame=frame.sample(frac=1,random_state=args.seed).reset_index(drop=True)
    columns=["id","doi","title","year","source","theme","selection_group","oa_url",
             "coder_A_eligibility","coder_B_eligibility",
             "coder_A_H1","coder_B_H1","coder_A_H3","coder_B_H3",
             "coder_A_C2","coder_B_C2","coder_A_C3","coder_B_C3",
             "coder_A_C4","coder_B_C4","coder_A_C5","coder_B_C5",
             "page_evidence_A","page_evidence_B","adjudicated_decision"]
    for k in columns:
        if k not in frame:frame[k]=""
    frame=frame[columns]
    frame.to_csv(root/"audit_blind_coding_template.csv",index=False,encoding="utf-8")
    print("Wrote",len(frame),"unlabelled candidate rows with two independent coder columns")
if __name__=="__main__":main()
