#!/usr/bin/env python3
"""Quality checks and public, non-textual audit outputs for an OpenAlex corpus."""
import datetime as dt
import json
import re
import sqlite3
from pathlib import Path
import pandas as pd
from database import ensure_database

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"

def main():
    ensure_database()
    con=sqlite3.connect(HERE/"data"/"nordic_design_research.sqlite")
    assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    included=pd.read_sql_query(
     "SELECT id,doi,title,year,kind,source,citations,abstract,oa_url,countries FROM works WHERE in_scope=1",con)
    all_count=con.execute("SELECT count(*) FROM works").fetchone()[0]
    excluded=all_count-len(included)
    logs=pd.read_sql_query(
     "SELECT query,page,total_hits,returned,fetched_at,error FROM query_log",con)
    log_success=logs.error.isna()
    doi=included[included.doi.notna()].copy()
    doi_dupes=doi[doi.duplicated("doi",keep=False)].sort_values("doi")
    doi_dupes[["id","doi","title","year"]].to_csv(OUT/"audit_duplicate_doi.csv",index=False)
    included["title_norm"]=included.title.fillna("").str.lower().str.replace(r"[^\w]+"," ",regex=True).str.strip()
    normalized=included[included.title_norm.str.len()>12]
    dups=normalized[normalized.duplicated(["title_norm","year"],keep=False)].sort_values(["title_norm","year"])
    dups[["id","doi","title","year","source"]].to_csv(OUT/"audit_duplicate_titles.csv",index=False)
    citations=pd.read_sql_query("""SELECT r.citing_id,r.cited_id,
      a.title AS citing_title,b.title AS cited_title,
      a.year AS citing_year,b.year AS cited_year
      FROM references_all r JOIN works a ON a.id=r.citing_id AND a.in_scope=1
      JOIN works b ON b.id=r.cited_id AND b.in_scope=1
      WHERE r.citing_id!=r.cited_id AND a.year<b.year""",con)
    citations.to_csv(OUT/"audit_future_dated_references.csv",index=False)
    early=logs[logs.page<=2]
    late=logs[logs.page>2]
    source=included.source.fillna("(ukjend)").value_counts().head(25)
    source.rename_axis("publishing_source").reset_index(name="records").to_csv(
        OUT/"top_25_sources.csv",index=False)
    included["has_abstract"]=included.abstract.fillna("").str.len()>=60
    bin_stats=included.assign(period=(included.year//5)*5).groupby("period").agg(
      total=("id","size"),abstracts=("has_abstract","sum"),
      median_citations=("citations","median"),open_access_urls=("oa_url","count")
    ).reset_index()
    bin_stats["abstract_coverage"]=bin_stats.abstracts/bin_stats.total
    bin_stats.to_csv(OUT/"completeness_by_period.csv",index=False)
    bykind=included.groupby("kind").agg(
     total=("id","size"),abstracts=("has_abstract","sum")).reset_index()
    bykind["abstract_coverage"]=bykind.abstracts/bykind.total
    bykind.to_csv(OUT/"completeness_by_kind.csv",index=False)
    countries=pd.read_sql_query(
     "SELECT country,count(DISTINCT work_id) AS works FROM authorships WHERE country IN ('NO','SE','DK','FI','IS') GROUP BY country ORDER BY works DESC",con)
    countries.to_csv(OUT/"country_affiliations_distinct.csv",index=False)
    overrepresentation=included.copy()
    overrepresentation["suspicious_clinical"]=overrepresentation.title.str.contains(
      r"\b(?:clinical trial|cohort study|randomized controlled trial|study design for|protocol for a)\b",
      case=False,regex=True,na=False)
    overrepresentation["engineering_design"]=overrepresentation.title.str.contains(
      r"\b(?:bridge design|fuselage design|rotor design|reactor design|antenna design|circuit design|filter design)\b",
      case=False,regex=True,na=False)
    flagged=overrepresentation[overrepresentation.suspicious_clinical | overrepresentation.engineering_design].copy()
    flagged[["id","doi","title","year","suspicious_clinical","engineering_design"]].to_csv(
       OUT/"manual_scope_review.csv",index=False)
    index_pages={r["page"]:1 for _,r in logs.iterrows()}
    info={
     "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
     "sqlite_integrity":"ok",
     "unique_records":int(all_count),
     "provisionally_included":int(len(included)),
     "auto_not_included":int(excluded),
     "openalex_queries":int(logs["query"].nunique()),
     "successful_query_pages":int(log_success.sum()),
     "failed_query_pages":int((~log_success).sum()),
     "api_rate_limit_detected":bool(logs.error.fillna("").str.contains("429").any()),
     "papers_with_abstract":int(included.has_abstract.sum()),
     "missing_abstract_count":int((~included.has_abstract).sum()),
     "duplicate_DOI_rows":int(len(doi_dupes)),
     "duplicate_normalized_title_year_rows":int(len(dups)),
     "negative_reference_year_links":int(len(citations)),
     "manual_scope_flags":int(len(flagged)),
     "not_quality_labels":True,
    }
    (OUT/"data_quality.json").write_text(json.dumps(info,indent=2,ensure_ascii=False),encoding="utf-8")
    notes=[
      "# Datakvalitet og revisjonsspor",
      "",
      f"Utgåve: {info['generated_utc']}. SQLite integrity: ok.",
      "",
      f"- Unike postar: {all_count}. Automatisk tittelinkluderte: {len(included)}.",
      f"- API-sider utan feil: {info['successful_query_pages']}. Sider med feil: {info['failed_query_pages']}.",
      "- API 429 registrert: "+("ja" if info["api_rate_limit_detected"] else "nei")+".",
      f"- Inkluderte postar med samandrag: {info['papers_with_abstract']}.",
      f"- DOI-duplikat-rader: {len(doi_dupes)}. Normaliserte tittel/år-duplikat-rader: {len(dups)}.",
      f"- Siteringar der referert arbeid er datert seinare enn siterande: {len(citations)}.",
      f"- Autogenererte flagg for mogleg feil fagavgrensing: {len(flagged)}. Ingen er manuelt koda.",
      "",
      "Søkjemotoren returnerer rangsorterte treff. Ein negativ siteringslag eller tittelduplikat",
      "kan skuldast metadata, versjonar eller faktisk inkonsistens; revisjon er påkravd.",
      "Flagga for mogleg feilkategori er diagnostikk og skal ikkje utan kontroll brukast",
      "som automatisk eksklusjon. Konklusjonar om vitskapleg kumulativitet krev eigne prøver.",
    ]
    (OUT/"DATAKVALITET.md").write_text("\n".join(notes)+"\n",encoding="utf-8")
    print(json.dumps(info,indent=2,ensure_ascii=False))
    con.close()
if __name__=="__main__":main()
