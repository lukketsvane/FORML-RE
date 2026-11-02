#!/usr/bin/env python3
"""Search deliberately for possible counterexamples to low cumulative theory.

Use available metadata, no unverified claims about actual replication.
"""
import datetime as dt
import json
import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from database import ensure_database

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
FLAGS={
 "direct_test_words":r"\b(test(?:ing|ed|s)?|validat(?:e|ion|ed|ing)|experiment(?:al|s)?|evaluat(?:e|ion|ed|ing)|assess(?:ment|ed)?)\b",
 "explicit_replication_words":r"\b(replicat(?:e|ed|ion|ions|ing)|reproducib(?:le|ility)|reproduced|reproduce)\b",
 "theory_development_words":r"\b(theory development|theory building|theory construction|theoretical advance|developing theory|extending(?: a)? theory|model extension)\b",
 "criticism_words":r"\b(critique|criticism|critical reassessment|challenge(?:d|s)?|contradict(?:s|ed|ion)?|refut(?:e|ed|ation)|fail(?:ed|s)? to reproduce|limitation(?:s)?)\b"
}
CHECK={k:re.compile(v,re.I) for k,v in FLAGS.items()}

def main():
    ensure_database()
    conn=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    work=pd.read_sql_query("SELECT id,doi,title,abstract,year,source FROM works WHERE in_scope=1",conn)
    byid=work.set_index("id")
    refs=pd.read_csv(OUT/"citation_semantic_links.csv",dtype={"citing_id":str,"cited_id":str})
    refs=refs[(~refs.same_author)&refs.both_abstracts&(refs.gap_years>=0)].copy()
    if refs.empty:raise SystemExit("No compatible citation pairs")
    for name,pattern in CHECK.items():
        refs[name]=[
          bool(pattern.search(str(byid.loc[k,"title"])+" "+str(byid.loc[k,"abstract"])))
          for k in refs.citing_id
        ]
    refs["citing_title"]=refs.citing_id.map(byid.title)
    refs["cited_title"]=refs.cited_id.map(byid.title)
    refs["citing_doi"]=refs.citing_id.map(byid.doi)
    refs["cited_doi"]=refs.cited_id.map(byid.doi)
    refs["publication_year"]=refs.citing_id.map(byid.year)
    # A deliberately counterevidence-friendly ranking for follow-up, not a quality score.
    refs["priority"]=(
       refs["direct_test_words"].astype(int)
       +3*refs["explicit_replication_words"].astype(int)
       +2*refs["theory_development_words"].astype(int)
       +refs["criticism_words"].astype(int)
       +np.clip(refs["delta_vs_matched"],-1,1)
    )
    relevant=refs[refs[list(CHECK)].any(axis=1)].sort_values(
       ["priority","cosine_semantic_only_not_replication"],ascending=False).head(150)
    signals=pd.DataFrame([
      {"signal":name,"detected_pairs":int(refs[name].sum()),
       "denominator_nonself_both_abstracts":len(refs)}
      for name in CHECK
    ])
    signals.to_csv(OUT/"counterexample_signal_counts.csv",index=False)
    fig,ax=plt.subplots(figsize=(9,4))
    ax.barh(signals.signal.iloc[::-1],signals.detected_pairs.iloc[::-1])
    ax.set_xlabel("Par med minst eitt språkleg treff")
    ax.set_title("Moglege motdøme: automatisk ordtreff, ikkje stadfesta funn")
    fig.tight_layout()
    fig.savefig(OUT/"figures"/"18-motprovesignal.png",dpi=170,bbox_inches="tight")
    plt.close(fig)
    cols=["citing_id","cited_id","citing_title","citing_doi","cited_title","cited_doi",
          "citing_year","cited_year","gap_years","priority",
          "cosine_semantic_only_not_replication","delta_vs_matched"]+list(CHECK)
    if relevant.empty:raise SystemExit("No candidate metadata signals")
    selected=relevant[cols].copy()
    selected["independent_fulltext_validation"]=""
    selected["confirmed_counterexample_to_non_cumulativity"]=""
    selected["documentation_page"]=""
    selected["coder_notes"]=""
    selected.to_csv(OUT/"possible_counterexamples_to_non_cumulative_design.csv",
       index=False,encoding="utf-8")
    report={
     "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
     "eligible_nonself_links_both_abstracts":len(refs),
     "selected_for_manual_counterevidence_audit":len(selected),
     "automated_term_flags":{name:int(refs[name].sum()) for name in CHECK},
     "confirmed_replicated_findings":0,
     "confirmation_performed":False,
     "limitation":"Regex and text similarity identify candidates only; no claims about factually verified cumulative design research."
    }
    (OUT/"counterexample_screen_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    note=[
      "# Aktiv leiting etter motbevis — ikkje berre stadfesting",
      "",
      f"**{len(refs)}** uavhengige, tekstdekte siteringspar vart undersøkte.",
      f"**{len(selected)}** vart prioriterte for manuell, sidetilvist lesing.",
      "",
      "## Avgrensing",
      "Ord i tittel og samandrag kan vise til *annan* forsking enn den siterte",
      "publikasjonen. Korkje 'replicate', 'test', 'validation' eller semantisk likskap",
      "dokumenterer kva som faktisk er replisert. Det gjeld særleg breie",
      "designord som 'evaluation'. Ingen av par er kvalitetssikra i fulltekst.",
      "",
      "## Overflatiske språksignal (kan overlappe)",
      "",
      "| Søkjemønster | Par med ordtreff |",
      "|---|---:|"
    ]
    for key in CHECK:note.append(f"| {key} | {report['automated_term_flags'][key]} |")
    note +=[
     "",
     "## Protokoll",
     "Opne DOI for båe artiklane. Finn konkret sitat eller referanse i den nyare",
     "artikkelen. Dokumenter kva påstand eller metode som vert eksplisitt prøvd,",
     "kva slags datagrunnlag eller prov som vert ført, og kva for utfall som er",
     "rapportert. Kodinga kan motbevise den overordna hypotesen.",
     "",
     "CSV: possible_counterexamples_to_non_cumulative_design.csv.",
     "Alle kontrollkolonnar er tomme. Ein semantisk kandidat er ikkje eit positivt",
     "fagleg funn før uavhengig manuell vurdering."
    ]
    (OUT/"MOTPROVER.md").write_text("\n".join(note)+"\n",encoding="utf-8")
    conn.close()
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
