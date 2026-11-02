#!/usr/bin/env python3
"""Conditional citation-topic assortativity test within the deliberately capped sample."""
import json, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;OUT=ROOT/"results"
def main():
    works=pd.read_csv(OUT/"included_publications.csv",low_memory=False)
    labels=pd.read_csv(OUT/"semantic_clusters.csv")[["id","theme"]]
    works=works.drop(columns=["theme"],errors="ignore").merge(labels,on="id")
    edges=pd.read_csv(OUT/"internal_citations.csv")
    works["popularity_bin"]=pd.qcut(np.log1p(works.citations.fillna(0)),
        q=4,labels=False,duplicates="drop").fillna(0).astype(int)
    paper=works.set_index("id")
    if edges.empty:raise SystemExit("No internal references")
    allyears=works.year.to_numpy(dtype=int)
    allbins=works.popularity_bin.to_numpy(dtype=int)
    allthemes=works.theme.to_numpy(dtype=str)
    p=[]
    for edge in edges.itertuples():
        b=paper.loc[edge.cited_id]
        age=int(b.year)
        pop=int(b.popularity_bin)
        pool=(np.abs(allyears-age)<=1)&(allbins==pop)
        if pool.sum()<10:pool=(np.abs(allyears-age)<=2)
        if pool.sum()<10:pool=allyears<=int(edge.citing_year)
        # Exclude exact citing paper; single-sample null estimates not generalizable.
        prob=float((allthemes[pool]==edge.citing_theme).mean())
        p.append(prob)
    p=np.asarray(p)
    observed=int((edges.citing_theme==edges.cited_theme).sum())
    obs_fraction=observed/len(edges)
    null_expected=float(p.mean())
    rng=np.random.default_rng(20261102)
    simulated=np.zeros(2000,dtype=int)
    for i in range(len(simulated)):
        simulated[i]=np.count_nonzero(rng.random(len(p))<p)
    pvalue=float((np.count_nonzero(simulated>=observed)+1)/(len(simulated)+1))
    cited_lag=(edges.citing_year-edges.cited_year).dropna()
    # Co-authorship overlaps within observed citation edges, separate from semantic self-citation.
    conn=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    ac=pd.read_sql_query("SELECT DISTINCT work_id,author_id FROM authorships WHERE length(author_id)>2",conn)
    authors=ac.groupby("work_id").author_id.agg(set).to_dict()
    selfedges=sum(bool(authors.get(row.citing_id,set())&authors.get(row.cited_id,set()))
            for row in edges.itertuples())
    conn.close()
    stats={
       "conditioning":"For each observed citation, sample alternative cited works from same cited year +/-1 and citation-count quartile; fallback +/-2 years when fewer than 10; titlescreened OpenAlex sample.",
       "edges":len(edges),"observed_same_topic_edges":observed,
       "observed_same_topic_rate":obs_fraction,
       "conditional_null_mean_rate":null_expected,
       "observed_minus_null_percentage_points":100*(obs_fraction-null_expected),
       "permutation_draws":len(simulated),"one_sided_monte_carlo_p":pvalue,
       "median_reference_lag_years":float(cited_lag.median()),
       "negative_reference_lag_edges":int((cited_lag<0).sum()),
       "shared_author_edges":int(selfedges),
       "shared_author_rate":float(selfedges/len(edges)),
       "limitation":"Internal-graph comparison only. Search ranking, missing full text, discipline misclassification and omitted nodes preclude population-wide cumulativity inference."
    }
    (OUT/"conditional_citation_null.json").write_text(json.dumps(stats,indent=2,ensure_ascii=False),encoding="utf-8")
    plt.figure(figsize=(8,4))
    plt.hist(simulated/len(edges),bins=36)
    plt.axvline(obs_fraction,linestyle="--",linewidth=2,label="Observerte")
    plt.axvline(null_expected,linestyle=":",linewidth=2,label="Nullsnitt")
    plt.title("Temalikskap i interne siteringar mot betinga nullmodell")
    plt.xlabel("Del internt siterande avsendar–mottakar med same søkjetema")
    plt.ylabel("Tal simuleringar");plt.legend()
    plt.tight_layout()
    fig=OUT/"figures"/"08-siterings-nullmodell.png"
    plt.savefig(fig,dpi=165,bbox_inches="tight");plt.close()
    report=OUT/"RAPPORT.md"
    if report.exists():
        body=report.read_text(encoding="utf-8").split("\n## Betinga siteringsnullmodell")[0]
        add=("\n## Betinga siteringsnullmodell\n"
             +f"Same temagruppe: {100*obs_fraction:.1f} % observerte mot {100*null_expected:.1f} % i referansemodellen. "
             +f"Internsiteringar med felles forfattar: {100*selfedges/len(edges):.1f} %. "
             +"Nullmodellen er ei eksplorativ permutasjon samanlikna med alternativ i dette ikkje-representative utvalet; han validerer korkje dei operative temamerkelappane eller påstanden om vitskapleg kumulativitet.\n")
        report.write_text(body+add,encoding="utf-8")
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
