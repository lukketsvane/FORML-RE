#!/usr/bin/env python3
"""Explicit journal-vs-index-year sensitivity for the nonexhaustive citation graph.

Keep raw OpenAlex publication_year intact. Publication-year policies are
sensitivity assumptions, not silently modified metadata.
"""
from __future__ import annotations
import csv,datetime as dt,json,sqlite3
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"

def readcsv(name):
 with (OUT/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def assess(works,edges,alternate_ids):
 ys={w["id"]:int(w["year"]) for w in works}
 for x in alternate_ids:ys[x["work_id"]]=int(x["alternate_year"])
 # Basic year-horizon cross-validation
 future=sum(ys[e["citing_id"]]<ys[e["cited_id"]] for e in edges)
 adj=defaultdict(list)
 for e in edges:adj[e["citing_id"]].append(e["cited_id"])
 paths=0
 starts=set();middle=set();ends=set()
 for a in works:
  if not 2020<=ys[a["id"]]<=2026:continue
  for bid in adj.get(a["id"],[]):
   if not 2010<=ys[bid]<=2019:continue
   for cid in adj.get(bid,[]):
    if not 2000<=ys[cid]<=2009:continue
    paths+=1;starts.add(a["id"]);middle.add(bid);ends.add(cid)
 old_to_new=sum(2020<=ys[e["citing_id"]]<=2026 and 2000<=ys[e["cited_id"]]<=2009 for e in edges)
 return {"two_step_paths":paths,"late_to_early_direct_edges":old_to_new,
  "future_dated_references":future,"paths_middle_nodes":len(middle),
  "paths_early_nodes":len(ends),"paths_late_nodes":len(starts)}

def main():
 works=readcsv("semantic_clusters.csv")
 edges=readcsv("internal_citations.csv")
 corrections=readcsv("year_basis_sensitivity.csv")
 ids={w["id"] for w in works}
 if len(ids)!=len(works):raise AssertionError("Duplicate paper ids")
 for row in corrections:
  if row["work_id"] not in ids:raise AssertionError("Unknown paper "+row["work_id"])
 base=assess(works,edges,[])
 # Independent sensitivity scenarios, no hidden interpolation.
 scenarios={"openalex_year_baseline":base}
 for row in corrections:scenarios["journal_year_"+row["work_id"]]=assess(works,edges,[row])
 scenarios["both_journal_volume_years"]=assess(works,edges,corrections)
 assert base["two_step_paths"]==712,base
 report={
   "date_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
   "sample":"3729 auto-title-screened works with 3159 observed within-sample citation edges",
   "baseline_policy":"OpenAlex publication_year; source record and years preserved",
   "scenarios":scenarios,
   "curated_overrides":corrections,
   "policy_warning":"Journal volume year, online-first year and institutional reporting year differ. Neither should be substituted without a declared analysis policy.",
   "interpretation_warning":"Network year changes do not measure retractions, replicability or substantive theoretical continuity."
 }
 (OUT/"year_basis_sensitivity.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
 md=[
 "# Årsgrunnlag og tidskjeldekritikk",
 "",
 f"Analysedato: {report['date_utc']}. Ingen metadata eller råpostar er overskrivne.",
 "",
 "OpenAlex-år er ikkje alltid lik tidsskriftets volumår. Dette er ein særleg relevant",
 "feilkjelde i nettverk som deler publikasjonane i femårsbolkar eller tiår.",
 "",
 "| Utgåve | 2020–26 → 2010–19 → 2000–09 | Direkte 2020–26 → 2000–09 | Referansar som ser framtidsdaterte ut |",
 "|---|---:|---:|---:|"
 ]
 for key,x in scenarios.items():
  md.append(f"| {key} | {x['two_step_paths']} | {x['late_to_early_direct_edges']} | {x['future_dated_references']} |")
 md.extend([
  "",
  "## Dokumenterte kjelder",
  "- *Practicing Design Judgement through Intention-Focused Course Curricula*: original tidsskriftvolum 20(1) er frå **2015**,",
  "  sjølv om OpenAlex-indeksen i arbeidsdatabasen har **2023**.",
  "  [Open PDF frå ERIC](https://files.eric.ed.gov/fulltext/EJ1119540.pdf).",
  "- *Emerging human-technology relationships in a co-design process with generative AI*: registrert som **2024**",
  "  i tidlege rapporteringsregister, medan trykt tidsskriftvolum er **56 (juni 2025)**.",
  "  [Forlagspost](https://www.sciencedirect.com/science/article/pii/S1871187124002803).",
  "",
  "Å definere eit einaste «korrekt år» på tvers av tilgjengeleggjering,",
  "publiseringsdato, rapporteringsdato og tidsskriftvolum kan vere misvisande.",
  "Registrer fleire årsfelt og analyser konsekvensane av eksplisitt årspolicy.",
  "",
  "## Vurdering",
  "Dette er **eit utval på to kjende tilfelle**, ikkje eit representativt estimat på",
  "metadatafeil i OpenAlex. Framtidsdaterte referansar kan også kome av førehandsversjonar,",
  "forfattarmanuskript, rapporteringsskilje eller feilkoplingar.",
  "Siteringsanalyse som vert brukt til fagkritikk må gje lesaren denne usikkerheita.",
 ])
 (OUT/"AARSKJELDEKRITIKK.md").write_text("\n".join(md)+"\n",encoding="utf-8")
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
