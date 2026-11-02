#!/usr/bin/env python3
"""Pre-registered literal-language signals in available abstracts, not scientific-quality labels."""
from __future__ import annotations
import json
import re
import sqlite3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from database import ensure_database

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
FIG=OUT/"figures"
PATTERNS={
 "hypothesis_language":r"\b(hypothes[ie]s|hypothesiz\w*|hypothesising|hypotese(?:r|n)?|testable hypothes\w*|predictions?)\b",
 "explicit_testing":r"\b(test(?:ed|ing|s)?|evaluat(?:ed|ion|ing)|experiment(?:s|al)?|kontrollgruppe|randomi[sz](?:ed|ation))\b",
 "replication_language":r"\b(replicat(?:e|ed|ion|ions|ing)|reproducib(?:le|ility)|reproduced|replikasjo\w*|repeterbar(?:het)?)\b",
 "empirical_language":r"\b(empirical|empirisk|interview(?:s|ed)?|survey(?:s|ed)?|participant(?:s)?|case studies|case study|field stud\w*|ethnograph\w*|data set|dataset|datagrunnlag)\b",
 "conceptual_language":r"\b(conceptual|concept stud\w*|theoretical framework|framework|prototype(?:s|d)?|exploratory|design space|scenario(?:s)?|research through design|concept paper|konseptstud\w*)\b",
 "negative_results_language":r"\b(null results?|negative findings?|no significant (?:difference|effect)|failed to replicat\w*|not supported|contrary to our hypothesis|results did not|falsif(?:ied|ication))\b",
 "quantitative_language":r"\b(regression|statistically significant|confidence interval|sample size|effect size|randomi[sz]ation|correlation|anova|bootstrap|likelihood|p-value)\b",
 "qualitative_language":r"\b(qualitative|focus groups?|thematic analysis|interviews?|interpretiv\w*|ethnograph\w*|grounded theory)\b",
}
COMPILED={k:re.compile(v,re.I) for k,v in PATTERNS.items()}
def wilson(x,n,z=1.959964):
    if n==0:return [None,None]
    ph=x/n
    den=1+z*z/n
    center=(ph+z*z/(2*n))/den
    half=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/den
    return [float(center-half),float(center+half)]
def main():
    ensure_database();OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
    con=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    works=pd.read_sql_query("SELECT id,doi,title,year,source,abstract FROM works WHERE in_scope=1",con)
    topic=pd.read_csv(OUT/"semantic_clusters.csv",dtype={"id":str})[["id","theme"]]
    works=works.merge(topic,on="id",how="left")
    works["has_abstract"]=works.abstract.fillna("").str.len()>=60
    texts=works.abstract.fillna("").tolist()
    for name,rgx in COMPILED.items():
        works[name]=[bool(rgx.search(text)) for text in texts]
    valid=works[works.has_abstract].copy()
    n=len(valid)
    bysignal=[]
    for name in PATTERNS:
        count=int(valid[name].sum())
        bysignal.append({"signal":name,"n_abstracts":n,"n_with_phrase":count,
          "prevalence_within_available_abstracts":count/n if n else None,
          "wilson_95pct_given_this_sample":wilson(count,n)})
    (OUT/"abstract_signal_summary.json").write_text(
        json.dumps(bysignal,ensure_ascii=False,indent=2),encoding="utf-8")
    works["period"]=(works.year//5)*5
    yearrows=[]
    for period,group in works.groupby("period"):
        val=group[group.has_abstract]
        entry={"five_year_start":int(period),"total_included":len(group),
            "available_abstracts":len(val),"abstract_coverage":len(val)/len(group)}
        for name in PATTERNS:entry[name]=val[name].mean() if len(val) else None
        yearrows.append(entry)
    pd.DataFrame(yearrows).to_csv(OUT/"abstract_signal_by_period.csv",index=False)
    topicrows=[]
    for theme,group in works.groupby("theme"):
        val=group[group.has_abstract]
        entry={"theme":theme,"total_included":len(group),
            "available_abstracts":len(val),"abstract_coverage":len(val)/len(group)}
        for name in PATTERNS:entry[name]=val[name].mean() if len(val) else None
        topicrows.append(entry)
    pd.DataFrame(topicrows).to_csv(OUT/"abstract_signal_by_theme.csv",index=False)
    # No quoted abstract text in published output; all tags and candidate IDs remain auditable.
    keepcols=["id","doi","title","year","theme","has_abstract"]+list(PATTERNS)
    works[keepcols].to_csv(OUT/"abstract_signal_flags.csv",index=False,encoding="utf-8")
    sample=[]
    for name in PATTERNS:
        positives=valid[valid[name]]
        negatives=valid[~valid[name]]
        for group,flag in [(positives,True),(negatives,False)]:
            if len(group)==0:continue
            picked=group.sample(n=min(8,len(group)),random_state=20261102)
            for row in picked.itertuples():
                sample.append({"work_id":row.id,"doi":row.doi,
                  "signal":name,"regex_detected":flag,
                  "manual_fulltext_or_abstract_validation":"","coders_notes":""})
    pd.DataFrame(sample).drop_duplicates(["work_id","signal"]).to_csv(
        OUT/"abstract_signal_manual_review.csv",index=False,encoding="utf-8")
    fig,ax=plt.subplots(figsize=(10,4.5))
    names=[r["signal"] for r in bysignal]
    values=[100*r["prevalence_within_available_abstracts"] for r in bysignal]
    ax.barh(names[::-1],values[::-1])
    ax.set_xlabel("Prosent av tilgjengelege samandrag med ord/frasar")
    ax.set_title("Mønster i samandrag — ordtreff, ikkje dokumentert metode")
    fig.tight_layout();fig.savefig(FIG/"13-metodeord-i-samandrag.png",dpi=170,bbox_inches="tight");plt.close(fig)
    temporal=pd.DataFrame(yearrows)
    fig,ax=plt.subplots(figsize=(9,4.2))
    for name in ["hypothesis_language","replication_language","conceptual_language","empirical_language"]:
        ax.plot(temporal.five_year_start,temporal[name]*100,marker="o",label=name)
    ax.set_ylabel("Prosent av samandrag i same søkjeutval")
    ax.set_xlabel("Femårsstart");ax.legend(fontsize=8)
    ax.set_title("Utforskande ordtreff etter tid — utvalsavhengig")
    fig.tight_layout();fig.savefig(FIG/"14-metodeord-over-tid.png",dpi=170,bbox_inches="tight");plt.close(fig)
    report=[
     "# Språksignal i samandrag: pilot, ikkje kvalitetsdom",
     "",
     f"Tilgjengelege samandrag: {n} av {len(works)} inkluderte postar.",
     "",
     "Dette er presise streng-/regulæruttrykkssøk i samandrag, ikkje verifisert",
     "identifikasjon av hypotesetest, replikasjon, data eller kunnskap.",
     "Ingen fråvær av ord kan tolkast som fråvær av forskingsmetode.",
     "",
     "| Signal | Trefftall | Del |",
     "|---|---:|---:|"
    ]
    for row in bysignal:
        report.append(f"| {row['signal']} | {row['n_with_phrase']} | {100*row['prevalence_within_available_abstracts']:.1f} % |")
    report.extend([
       "",
       "Faglege feilkjelder: nordiske språk, ulike abstraktsjangrar, sjangerforskjellar",
       "mellom tidsskrift, søkjeordsvridning, manglande samandrag og ord brukt om",
       "tidlegare forsking snarare enn eiga metode. Alt krev manuell kodingskontroll.",
       "",
       "Resultatfilene inneheld berre arbeids-ID, tittel, DOI og boolske ordtreff.",
       "Artikkelsamandraga er ikkje republiserte.",
       "",
       "Sjå auditfila abstract_signal_manual_review.csv for uavhengig kvalitetskontroll."
    ])
    (OUT/"ABSTRAKT_SIGNAL.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    print(json.dumps({"available_abstracts":n,"signals":bysignal},ensure_ascii=False,indent=2))
    con.close()
if __name__=="__main__":main()
