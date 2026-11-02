#!/usr/bin/env python3
"""Reproduce three-cohort citation-bridge and hub-permutation diagnostics.

Input: published title-screened OpenAlex work list + within-sample citation links.
No full texts and no classification of true theoretical or empirical advancement.
Dependencies: Python 3.11 standard library only.
"""
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
MASK=(1<<32)-1
SEED=20261102
REPETITIONS=2000

def mulberry32(seed):
    state=seed
    def draw():
        nonlocal state
        state=(state+0x6D2B79F5)&MASK
        t=((state^(state>>15))*(1|state))&MASK
        t=((t+(((t^(t>>7))*(61|t))&MASK))&MASK)^t
        return ((t^(t>>14))&MASK)/(2**32)
    return draw

def read_rows(name):
    with (OUT/name).open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream))

def run():
    works=read_rows("semantic_clusters.csv")
    edges=read_rows("internal_citations.csv")
    by_id={w["id"]:w for w in works}
    middle=[w for w in works if 2010<=int(w["year"])<=2019]
    incoming={w["id"]:0 for w in middle}
    outgoing={w["id"]:0 for w in middle}
    adjacency=defaultdict(list)
    direct=0
    for row in edges:
        adjacency[row["citing_id"]].append(row["cited_id"])
        source=by_id.get(row["citing_id"])
        target=by_id.get(row["cited_id"])
        if not source or not target:continue
        if int(source["year"])>=2020 and int(target["year"])<=2009:direct+=1
        if 2020<=int(source["year"])<=2026 and 2010<=int(target["year"])<=2019:
            incoming[target["id"]]+=1
        if 2010<=int(source["year"])<=2019 and 2000<=int(target["year"])<=2009:
            outgoing[source["id"]]+=1
    arr=[{
       "id":w["id"],"title":w["title"],"year":int(w["year"]),"theme":w["theme"],
       "in_recent":incoming[w["id"]],"out_early":outgoing[w["id"]],
       "paths":incoming[w["id"]]*outgoing[w["id"]]
    } for w in middle]
    # Python's stable sort replicates the published JavaScript order at equal scores.
    arr.sort(key=lambda x:-x["paths"])
    observed=sum(w["paths"] for w in arr)
    random=mulberry32(SEED)
    def grouped(key):
        data={}
        for w in arr:
            data.setdefault(key(w),[]).append(w)
        return list(data.values())
    byyear=grouped(lambda w:w["year"])
    byyear_theme=grouped(lambda w:(w["year"],w["theme"]))
    byfive_theme=grouped(lambda w:(w["year"]<2015,w["theme"]))
    def perm(groups,exclude=frozenset()):
        runs=[]
        for _ in range(REPETITIONS):
            total=0
            for group in groups:
                retained=[w for w in group if w["id"] not in exclude]
                shuffled=[w["out_early"] for w in retained]
                for i in range(len(shuffled)-1,0,-1):
                    j=math.floor(random()*(i+1))
                    shuffled[i],shuffled[j]=shuffled[j],shuffled[i]
                total+=sum(w["in_recent"]*shuffled[i] for i,w in enumerate(retained))
            runs.append(total)
        runs.sort()
        obs=sum(w["paths"] for w in arr if w["id"] not in exclude)
        q=lambda v:runs[math.floor(v*(REPETITIONS-1))]
        return {"observed":obs,"null_mean":sum(runs)/REPETITIONS,
          "null_q025":q(.025),"null_median":q(.5),"null_q975":q(.975),
          "p_greater_equal":(1+sum(v>=obs for v in runs))/(REPETITIONS+1)}
    tests={
      "within_middle_year":perm(byyear),
      "within_middle_year_and_search_theme":perm(byyear_theme),
      "within_middle_fiveyear_and_search_theme":perm(byfive_theme),
      "remove_five_largest_middle_hubs_then_year_theme":
          perm(byyear_theme,frozenset(w["id"] for w in arr[:5])),
      "remove_ten_largest_middle_hubs_then_year_theme":
          perm(byyear_theme,frozenset(w["id"] for w in arr[:10]))
    }
    data={"observed":observed,"direct_2020s_to_2000s":direct,
         "middle_papers":len(arr),
         "middle_papers_with_paths":sum(w["paths"]>0 for w in arr),
         "top5_paths":sum(w["paths"] for w in arr[:5]),
         "top10_paths":sum(w["paths"] for w in arr[:10]),
         "permutation_tests":tests}
    # Compare against the frozen, model-independent published output.
    expected=json.loads((OUT/"citation_bridge_hub_sensitivity.json").read_text(encoding="utf-8"))
    assert data["observed"]==expected["observed_two_step_paths"]
    assert data["direct_2020s_to_2000s"]==157
    assert data["top5_paths"]==expected["top5_paths"]
    assert data["top10_paths"]==expected["top10_paths"]
    for key,val in tests.items():
        baseline=expected["permutation_tests"][key]
        for field in ("observed","null_median","null_q025","null_q975"):
            assert val[field]==baseline[field],(key,field,val[field],baseline[field])
        assert abs(val["null_mean"]-baseline["null_mean"])<1e-10
    print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=="__main__":
    run()
