#!/usr/bin/env python3
"""Semantic continuity in observed citation pairs against age/topic matched alternatives.

This is an exploratory *linkage* study, NOT a determination of confirmation,
replication, truth, refutation, or scientific accumulation.
"""
from __future__ import annotations
from pathlib import Path
import json, sqlite3, datetime as dt
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from database import ensure_database

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
FIG=OUT/"figures"
SEED=20261102

def main():
    OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
    ensure_database()
    con=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    wk=pd.read_sql_query("SELECT id,title,doi,year,source,citations,abstract FROM works WHERE in_scope=1",con)
    topics=pd.read_csv(OUT/"semantic_clusters.csv",dtype={"id":str})[["id","theme"]]
    wk=wk.merge(topics,on="id",how="left")
    vecfile=np.load(OUT/"lsa_vectors.npz")
    vecids=vecfile["ids"].astype(str)
    vectors=vecfile["vectors"].astype(np.float32)
    # Canonical alignment to semantic model work IDs
    wk=wk.set_index("id").loc[vecids].reset_index()
    assert len(wk)==len(vectors)
    ids=wk.id.to_numpy(dtype=str)
    index={v:i for i,v in enumerate(ids)}
    years=wk.year.to_numpy(dtype=int)
    themes=wk.theme.fillna("anna").to_numpy(dtype=str)
    cited_counts=wk.citations.fillna(0).to_numpy(dtype=float)
    binpop=pd.qcut(pd.Series(cited_counts).rank(method="average"),q=4,labels=False,duplicates="drop").to_numpy(dtype=int)
    available=wk.abstract.fillna("").str.len().to_numpy()>59
    aa=pd.read_sql_query("SELECT DISTINCT work_id,author_id FROM authorships WHERE author_id IS NOT NULL AND author_id!=''",con)
    authors=aa.groupby("work_id").author_id.agg(set).to_dict()
    ref=pd.read_sql_query("""SELECT r.citing_id,r.cited_id FROM references_all r
      JOIN works a ON a.id=r.citing_id AND a.in_scope=1
      JOIN works b ON b.id=r.cited_id AND b.in_scope=1
      WHERE r.citing_id!=r.cited_id""",con)
    ref=ref[(ref.citing_id.isin(index))&(ref.cited_id.isin(index))].copy()
    ref["i"]=ref.citing_id.map(index);ref["j"]=ref.cited_id.map(index)
    ref["same_author"]=[bool(authors.get(a,set())&authors.get(b,set())) for a,b in zip(ref.citing_id,ref.cited_id)]
    ref["gap_years"]=years[ref.i.to_numpy(dtype=int)]-years[ref.j.to_numpy(dtype=int)]
    ref["same_theme"]=themes[ref.i.to_numpy(dtype=int)]==themes[ref.j.to_numpy(dtype=int)]
    ref["both_abstracts"]=available[ref.i.to_numpy(dtype=int)] & available[ref.j.to_numpy(dtype=int)]
    ref["cosine"]=np.sum(vectors[ref.i.to_numpy(dtype=int)]*vectors[ref.j.to_numpy(dtype=int)],axis=1)
    ref["matched_cosine"]=np.nan
    ref["matched_n"]=0
    rng=np.random.default_rng(SEED)
    # The matched alternative controls for topic, referenced-paper age and citation popularity.
    # Relax only the cited-paper year window, never substitute unknown fields silently.
    alt_cos=[]
    alt_quality=[]
    for row in ref.itertuples():
        i=int(row.i); j=int(row.j)
        mask=(np.abs(years-years[j])<=2)&(themes==themes[j])&(binpop==binpop[j])&(np.arange(len(wk))!=i)&(np.arange(len(wk))!=j)
        tier="year2_theme_pop"
        if mask.sum()<7:
            mask=(np.abs(years-years[j])<=3)&(themes==themes[j])&(np.arange(len(wk))!=i)&(np.arange(len(wk))!=j)
            tier="year3_theme"
        if mask.sum()<7:
            mask=(np.abs(years-years[j])<=4)&(np.arange(len(wk))!=i)&(np.arange(len(wk))!=j)
            tier="year4_any"
        cands=np.flatnonzero(mask)
        if not len(cands):
            alt_cos.append(np.nan);alt_quality.append("unmatched")
            continue
        sampled=rng.choice(cands,size=min(30,len(cands)),replace=len(cands)<30)
        alt_cos.append(float(np.mean(vectors[sampled]@vectors[i])))
        alt_quality.append(tier)
    ref["matched_cosine"]=alt_cos
    ref["match_stratum"]=alt_quality
    ref["delta_vs_matched"]=ref.cosine-ref.matched_cosine
    ref["cosine_semantic_only_not_replication"]=ref.cosine
    ref["citing_year"]=years[ref.i.to_numpy(dtype=int)]
    ref["cited_year"]=years[ref.j.to_numpy(dtype=int)]
    ref["citing_theme"]=themes[ref.i.to_numpy(dtype=int)]
    ref["cited_theme"]=themes[ref.j.to_numpy(dtype=int)]
    # Release only structured signals and bibliographic titles; no article abstract copied.
    keep=["citing_id","cited_id","citing_year","cited_year","gap_years",
          "citing_theme","cited_theme","same_theme","same_author","both_abstracts",
          "cosine_semantic_only_not_replication","matched_cosine","delta_vs_matched","match_stratum"]
    ref[keep].to_csv(OUT/"citation_semantic_links.csv",index=False)
    matched=ref[ref.matched_cosine.notna()].copy()
    nonself=matched[~matched.same_author].copy()
    both=nonself[nonself.both_abstracts & (nonself.gap_years>=0)].copy()

    def cluster_boot(df,reps=800):
        if len(df)==0:return None
        by=df.groupby("citing_id").delta_vs_matched.agg(["sum","count"])
        numerator=by["sum"].to_numpy()
        denominator=by["count"].to_numpy()
        values=np.empty(reps)
        for k in range(reps):
            ind=rng.integers(0,len(by),size=len(by))
            values[k]=numerator[ind].sum()/denominator[ind].sum()
        return {"mean_delta":float(df.delta_vs_matched.mean()),
           "cluster_bootstrap_95pct":[float(x) for x in np.quantile(values,[.025,.975])],
           "citing_paper_clusters":len(by),"edges":len(df)}

    strata=matched.match_stratum.value_counts().to_dict()
    groups={"all_observed_edges":matched,
        "exclude_shared_author":nonself,
        "exclude_shared_author_both_abstracts_nonnegative_year":both,
        "same_theme_only":nonself[nonself.same_theme],
        "cross_theme_only":nonself[~nonself.same_theme],
        "ten_or_more_year_gap":nonself[nonself.gap_years>=10]}
    result={"generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "semantic_definition":"Cosine in 40-dimensional title+abstract LSA; NOT claim content, validation or full text.",
        "matching_definition":"cited paper same year +/-2, same search topic, similar global citation count; fallback +/-3 same topic or +/-4 year only.",
        "matched_tier_counts":{str(k):int(v) for k,v in strata.items()},
        "groups":{k:cluster_boot(v) for k,v in groups.items()},
        "critical_limit":"This is an exploratory, incomplete citation graph with search-based topic labels and corpus-specific LSA. Similarity != independent confirmation."}
    (OUT/"citation_semantic_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

    # Candidate papers for a *manual* check of whether a citation continued a substantive theory.
    # Exclude shared authors and year-inverted pairs. Ranking combines cosine and matched novelty only.
    cand=both[(both.gap_years>=1)&(both.gap_years<=20)&(both.cosine>=.32)].copy()
    cand=cand.sort_values(["delta_vs_matched","cosine"],ascending=False).head(200)
    paper=wk.set_index("id")
    cand["citing_title"]=cand.citing_id.map(paper.title)
    cand["cited_title"]=cand.cited_id.map(paper.title)
    cand["citing_doi"]=cand.citing_id.map(paper.doi)
    cand["cited_doi"]=cand.cited_id.map(paper.doi)
    cand["replication_verified"]=None
    cand["theory_updated_verified"]=None
    cand["human_review_notes"]=None
    cand[["citing_id","cited_id","citing_title","citing_doi","cited_title","cited_doi",
          "citing_year","cited_year","cosine","delta_vs_matched",
          "replication_verified","theory_updated_verified","human_review_notes"]].to_csv(
          OUT/"lineage_review_queue.csv",index=False,encoding="utf-8")
    # Plot explicit baseline, not just pairwise point similarity.
    fig,ax=plt.subplots(figsize=(9,4))
    vals=matched.delta_vs_matched.to_numpy(dtype=float)
    ax.hist(vals,bins=55)
    ax.axvline(0,linestyle="--",linewidth=2,label="Matched null expectation")
    ax.set_xlabel("Observed cosine minus matched-paper mean cosine")
    ax.set_ylabel("Citation edges")
    ax.set_title("Semantic continuity in referenced literature (not replication)")
    ax.legend()
    fig.tight_layout();fig.savefig(FIG/"15-siteringssemantikk-mot-nullmodell.png",dpi=170,bbox_inches="tight");plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    byperiod=matched.assign(period=(matched.citing_year//5)*5).groupby("period").agg(
        mean_delta=("delta_vs_matched","mean"),n=("citing_id","size")).reset_index()
    ax.plot(byperiod.period,byperiod.mean_delta,marker="o")
    ax.axhline(0,linestyle="--")
    ax.set_xlabel("Citing-paper five-year cohort start")
    ax.set_ylabel("Semantic delta vs matched baseline")
    ax.set_title("Cohorts within a biased ranking sample")
    fig.tight_layout();fig.savefig(FIG/"16-siteringssemantikk-over-tid.png",dpi=170,bbox_inches="tight");plt.close(fig)
    byperiod.to_csv(OUT/"citation_semantic_cohorts.csv",index=False)
    report=[
      "# Semantiske koplingar langs observerte siteringar",
      "",
      "Generert "+result["generated_utc"]+".",
      "",
      "Prosjektet måler kontinuitet i tekstsemantikk, ikkje om ei hypotese er testa,",
      "stadfesta, falsifisert eller vidareutvikla. Resultat kan ha metadata- og utvalsskeivskap.",
      "",
      "| Delutval | Siteringskantar | Gjennomsnittleg cosine-differanse | 95 % bootstrap (siterande artiklar) |",
      "|---|---:|---:|---|"]
    for name,row in result["groups"].items():
        if row is None:continue
        a,b=row["cluster_bootstrap_95pct"]
        report.append(f"| {name} | {row['edges']} | {row['mean_delta']:+.3f} | [{a:+.3f}, {b:+.3f}] |")
    report.extend([
      "",
      "## Avgrensingar",
      "- Begge semantiske tekstrepresentasjonar kan mangle samandrag.",
      "- Siteringslenkjer til arbeid utanfor det innhenta utvalet er ikkje med i paranalysen.",
      "- Matchestrata vert utvida når det er få samanlikningskandidatar; fordelinga er rapportert i JSON.",
      "- Felles forfattar kan vere teikn på eit utviklingsprogram, ikkje uavhengig replikasjon.",
      "- Nullmodellen er ein intern samanlikning, ikkje ein publisert epistemisk referansestandard.",
      "",
      "## Fulltekstutval til reell prøving",
      f"{len(cand)} siteringspar med høg tekstlikskap er lagt i ein kandidat-CSV. "
      "Alle tolkingsfelt er blanke; menneskeleg fulltekstgransking er enno ikkje utført.",
      "",
      "![Semantisk nullmodell](figures/15-siteringssemantikk-mot-nullmodell.png)",
      "",
      "![Kohortanalyse](figures/16-siteringssemantikk-over-tid.png)"
    ])
    (OUT/"SITERINGSLINJER.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    con.close()
    print(json.dumps({"edges":len(ref),"matched_edges":len(matched),
       "human_queue":len(cand),"results":result["groups"],"tiers":strata},
       ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":main()
