#!/usr/bin/env python3
"""Sensitivity statistics and bibliographic coupling for a non-representative OpenAlex corpus."""
import datetime as dt
import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, triu
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from database import ensure_database

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
FIG=OUT/"figures"
RNG=np.random.default_rng(20261102)
VENUES={
 "the design journal","design studies","design issues","codesign",
 "formakademisk - forskningstidsskrift for design og designdidaktikk",
 "journal of design history","international journal of design","she ji",
 "design and culture","design science","journal of engineering design",
 "international journal of technology and design education",
}
def save(name):
    plt.tight_layout()
    plt.savefig(FIG/name,dpi=165,bbox_inches="tight")
    plt.close()
def summarize_subset(frame,ed,authors,label):
    if frame.empty:return {"subset":label,"works":0}
    ids=frame.id.to_numpy(dtype=str)
    key={w:i for i,w in enumerate(ids)}
    e=ed[ed.citing_id.isin(key)&ed.cited_id.isin(key)]
    if e.empty:return {"subset":label,"works":len(frame),"edges":0}
    source=e.citing_id.map(key).to_numpy(dtype=int)
    target=e.cited_id.map(key).to_numpy(dtype=int)
    themes=frame.theme.fillna("anna").to_numpy(dtype=str)
    years=frame.year.to_numpy(dtype=int)
    popularity=np.log1p(frame.citations.fillna(0).to_numpy(dtype=float))
    rank=pd.Series(popularity).rank(pct=True).to_numpy()
    strata=((years-2000)//5)*4+np.minimum(3,(rank*4).astype(int))
    groups=[np.flatnonzero(strata==v) for v in np.unique(strata)]
    match=themes[source]==themes[target]
    selfmask=np.array([bool(authors.get(a,set()) & authors.get(b,set()))
                       for a,b in zip(e.citing_id,e.cited_id)],dtype=bool)
    def randomise(mask,rounds=500):
        observed=float(np.mean(match[mask]))
        simulated=np.empty(rounds)
        for round in range(rounds):
            lab=themes.copy()
            for g in groups:
                if len(g)>1:lab[g]=lab[RNG.permutation(g)]
            simulated[round]=np.mean(lab[source[mask]]==lab[target[mask]])
        qs=np.quantile(simulated,[.025,.5,.975])
        return {"observed_fraction":observed,
           "null_2_5pct":float(qs[0]),"null_median":float(qs[1]),
           "null_97_5pct":float(qs[2]),
           "one_sided_permutation_p":float((1+sum(simulated>=observed))/(rounds+1)),
           "n_permutations":rounds}
    # Citation edges from one paper are correlated; bootstrap citing-paper clusters.
    by=e.assign(same=match.astype(int)).groupby("citing_id").same.agg(["sum","count"])
    num=by["sum"].to_numpy(dtype=int);den=by["count"].to_numpy(dtype=int)
    boot=np.empty(600)
    for j in range(len(boot)):
        s=RNG.integers(0,len(by),size=len(by))
        boot[j]=num[s].sum()/den[s].sum()
    return {
       "subset":label,"works":len(frame),"edges":len(e),
       "unique_citing_papers":len(by),"same_theme_edges":int(match.sum()),
       "shared_author_edges":int(selfmask.sum()),
       "same_theme_rate_cluster_bootstrap_95pct":[float(x) for x in np.quantile(boot,[.025,.975])],
       "all_edges":randomise(np.ones(len(e),dtype=bool)),
       "excluding_shared_authors":randomise(~selfmask) if sum(~selfmask)>=20 else None,
    }
def main():
    OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
    ensure_database()
    con=sqlite3.connect(HERE/"data"/"nordic_design_research.sqlite")
    works=pd.read_sql_query(
      "SELECT id,doi,title,year,kind,abstract,citations,source FROM works WHERE in_scope=1",con)
    topic=pd.read_csv(OUT/"semantic_clusters.csv",dtype={"id":str})[["id","theme","cluster"]]
    works=works.merge(topic,on="id")
    works["core_venue"]=works.source.fillna("").str.strip().str.lower().isin(VENUES)
    works["has_abstract"]=works.abstract.fillna("").str.len()>=60
    first=pd.read_sql_query("SELECT id,MIN(page) AS first_page FROM discoveries GROUP BY id",con)
    works=works.merge(first,on="id",how="left")
    works["selection"]=np.where(works.first_page<=2,"initial_top_200","expanded_ranked_pages")
    authors_df=pd.read_sql_query("SELECT DISTINCT work_id,author_id FROM authorships WHERE author_id!='' AND author_id IS NOT NULL",con)
    authors=authors_df.groupby("work_id").author_id.agg(set).to_dict()
    edges=pd.read_sql_query("""SELECT r.citing_id,r.cited_id,a.year citing_year,b.year cited_year
      FROM references_all r JOIN works a ON a.id=r.citing_id AND a.in_scope=1
      JOIN works b ON b.id=r.cited_id AND b.in_scope=1 WHERE r.citing_id!=r.cited_id""",con)
    categories=dict(zip(works.id,works.theme))
    edges["source_theme"]=edges.citing_id.map(categories)
    edges["target_theme"]=edges.cited_id.map(categories)
    edges["same_theme"]=edges.source_theme==edges.target_theme
    edges["shared_author"]=[bool(authors.get(a,set()) & authors.get(b,set())) for a,b in zip(edges.citing_id,edges.cited_id)]
    edges["lag"]=edges.citing_year-edges.cited_year

    groups={
     "all_auto_included":works,
     "curated_design_venues":works[works.core_venue],
     "works_with_abstract":works[works.has_abstract],
     "original_top200":works[works.first_page<=2],
     "since_2010":works[works.year>=2010],
     "before_2015":works[works.year<2015]
    }
    output={}
    for k,g in groups.items():
        output[k]=summarize_subset(g,edges,authors,k)
        print("ROBUST",k,output[k].get("works"),output[k].get("edges"),flush=True)
    (OUT/"robustness.json").write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding="utf-8")

    # Bias audit: different-ranked search pages are not a random cross-section.
    source_bias=works.groupby("selection").agg(
      works=("id","size"),abstract_coverage=("has_abstract","mean"),
      core_venue_fraction=("core_venue","mean"),
      median_citations=("citations","median"),median_publication_year=("year","median")
    ).reset_index()
    source_bias.to_csv(OUT/"selection_bias.csv",index=False)
    pd.crosstab(works.selection,works.theme).to_csv(OUT/"selection_bias_themes.csv")
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    axs[0].bar(source_bias.selection,source_bias.works)
    axs[0].set_title("Tal på arbeid, etter rangering")
    axs[0].tick_params(axis="x",rotation=18)
    axs[1].bar(source_bias.selection,100*source_bias.abstract_coverage,label="Samandrag")
    axs[1].bar(source_bias.selection,100*source_bias.core_venue_fraction,alpha=.7,label="Kjernetidsskrift")
    axs[1].set_title("Datasamansetnad (%)");axs[1].legend()
    axs[1].tick_params(axis="x",rotation=18)
    save("09-rangering-og-bias.png")

    edges["period"]=(edges.citing_year//5)*5
    cohorts=edges.groupby("period").agg(
      reference_edges=("same_theme","size"),
      within_theme_fraction=("same_theme","mean"),
      same_author_fraction=("shared_author","mean"),
      median_lag_years=("lag","median")).reset_index()
    cohorts.to_csv(OUT/"citation_cohorts.csv",index=False)
    plt.figure(figsize=(9,4.2))
    plt.plot(cohorts.period,cohorts.within_theme_fraction,marker="o",label="Same tema")
    plt.plot(cohorts.period,cohorts.same_author_fraction,marker="o",label="Felles forfattar")
    plt.title("Interne siteringsmønster etter kohort")
    plt.xlabel("Femårsstart for siterande artikkel")
    plt.ylabel("Del av internt observerte siteringar")
    plt.ylim(0,1);plt.legend()
    save("10-sitering-kohortar.png")

    # Bibliographic coupling: works sharing at least 3 distinct referenced works.
    refs=pd.read_sql_query("""SELECT r.citing_id,r.cited_id FROM references_all r
       JOIN works w ON w.id=r.citing_id AND w.in_scope=1""",con)
    i_map={v:i for i,v in enumerate(works.id)}
    refs=refs[refs.citing_id.isin(i_map)].copy()
    freq=refs.groupby("cited_id").size()
    maxfreq=max(50,round(len(works)*.08))
    keep=set(freq[(freq>=2)&(freq<=maxfreq)].index)
    refs2=refs[refs.cited_id.isin(keep)].copy()
    r_map={v:i for i,v in enumerate(refs2.cited_id.unique())}
    ii=refs2.citing_id.map(i_map).to_numpy(dtype=int)
    jj=refs2.cited_id.map(r_map).to_numpy(dtype=int)
    matrix=coo_matrix((np.ones(len(ii),dtype=np.int32),(ii,jj)),
        shape=(len(works),len(r_map))).tocsr()
    matrix.sum_duplicates();matrix.data[:]=1
    nrefs=np.asarray(matrix.sum(axis=1)).ravel()
    shared=triu(matrix @ matrix.T,k=1).tocoo()
    mask=shared.data>=3
    aa=shared.row[mask];bb=shared.col[mask];common=shared.data[mask]
    jaccard=common/np.maximum(1,nrefs[aa]+nrefs[bb]-common)
    bib=pd.DataFrame({
      "a":works.id.to_numpy()[aa],"b":works.id.to_numpy()[bb],
      "common_references":common,"jaccard":jaccard,
      "year_a":works.year.to_numpy()[aa],"year_b":works.year.to_numpy()[bb],
      "theme_a":works.theme.to_numpy()[aa],"theme_b":works.theme.to_numpy()[bb]})
    bib["same_theme"]=bib.theme_a==bib.theme_b
    bib["shared_author"]=[bool(authors.get(a,set()) & authors.get(b,set())) for a,b in zip(bib.a,bib.b)]
    bib["year_gap"]=abs(bib.year_a-bib.year_b)
    strong=bib[(bib.common_references>=4)&(bib.jaccard>=.12)]
    strong.sort_values(["jaccard","common_references"],ascending=False).head(1000).to_csv(
       OUT/"strong_bibliographic_coupling.csv",index=False)
    stats={
      "included_works":len(works),
      "distinct_cited_external_or_internal_work_ids":int(refs.cited_id.nunique()),
      "reference_mentions":int(len(refs)),
      "reference_filter":"include refs mentioned by >=2 and <=8% of included works",
      "after_filter_cited_work_ids":len(r_map),
      "pairs_with_at_least_3_shared_refs":int(len(bib)),
      "strong_pairs_4_refs_and_jaccard_0_12":int(len(strong)),
      "strong_pair_within_theme_rate":float(strong.same_theme.mean()) if len(strong) else None,
      "strong_pair_shared_author_rate":float(strong.shared_author.mean()) if len(strong) else None,
      "strong_pair_median_year_gap":float(strong.year_gap.median()) if len(strong) else None,
      "caveat":"Co-citation overlap is not proof of replication or theory improvement."
    }
    (OUT/"bibliographic_coupling.json").write_text(json.dumps(stats,indent=2,ensure_ascii=False),encoding="utf-8")
    if len(bib):
        hist=bib.common_references.clip(upper=12).value_counts().sort_index()
        plt.figure(figsize=(8,4));plt.bar(hist.index.astype(str),hist.values)
        plt.title("Bibliografisk kopling: felles referansar")
        plt.xlabel("Felles referansar, 12 = 12 eller meir")
        plt.ylabel("Par publikasjonar")
        save("11-bibliografisk-kopling.png")

    # Are the latent-topic clusters algorithmically stable?
    data=np.load(OUT/"lsa_vectors.npz")
    embeddings=data["vectors"]
    n_clusters=len(works.cluster.unique())
    trials=[KMeans(n_clusters=n_clusters,random_state=seed,
        n_init=3,max_iter=160).fit_predict(embeddings)
        for seed in [7,13,23,31,43,57,73,101]]
    ari=[float(adjusted_rand_score(trials[i],trials[j]))
         for i in range(len(trials)) for j in range(i+1,len(trials))]
    stability={
       "seeds":len(trials),"k":n_clusters,
       "median_adjusted_rand_index":float(np.median(ari)),
       "range_5_to_95pct":[float(x) for x in np.quantile(ari,[.05,.95])],
       "caveat":"Algorithm reproducibility is not human topic validation."
    }
    (OUT/"cluster_stability.json").write_text(json.dumps(stability,indent=2,ensure_ascii=False),encoding="utf-8")
    plt.figure(figsize=(7,4));plt.hist(ari,bins=12)
    plt.title("Kor stabil er K-means på same LSA-data?")
    plt.xlabel("Justert Rand-indeks mellom to initialiseringar")
    plt.ylabel("Antal par køyringar")
    save("12-klynge-stabilitet.png")

    lines=[
      "# Avansert data science: robustheit, sitering og bibliografisk kopling",
      "",
      "Generert: "+dt.datetime.now(dt.timezone.utc).isoformat(),
      "",
      f"Utval: {len(works)} automatisk tittelinkluderte postar. Ikkje representativt for all designforsking.",
      "",
      "## Sensitivitetsanalysar",
      "| Utval | Publikasjonar | Interne siteringar | Del same tema | Nullmedian |",
      "|---|---:|---:|---:|---:|"
    ]
    for k,v in output.items():
        m=v.get("all_edges") or {}
        lines.append(f"| {k} | {v.get('works',0)} | {v.get('edges',0)} | {100*m.get('observed_fraction',0):.1f} % | {100*m.get('null_median',0):.1f} % |")
    lines.extend([
      "",
      "Permutasjonsnullmodellen held siteringskantar faste og stokkar om på temamerkelappar innan "
      "femårs- og siteringspopularitetsstrata. Kode og eksakte tal er i robustness.json.",
      "",
      "## Bibliografisk kopling",
      f"- {stats['reference_mentions']} referansetilvisingar til {stats['distinct_cited_external_or_internal_work_ids']} ulike arbeid.",
      f"- {stats['pairs_with_at_least_3_shared_refs']} publikasjonpar deler minst tre av dei bevarte referansane.",
      f"- {stats['strong_pairs_4_refs_and_jaccard_0_12']} par deler minst fire og har Jaccard 0,12 eller meir.",
      "Bibliografisk kopling viser felles kunnskapsgrunnlag, ikkje replikasjon eller kumulativ teorianalyse.",
      "",
      "## Sensitivitet for søkjerangering",
      source_bias.to_string(index=False),
      "",
      "## Klyngestabilitet",
      f"Median justert Rand-indeks over åtte initialiseringar: {stability['median_adjusted_rand_index']:.3f}.",
      "",
      "## Konklusjon",
      "Dette er robustheits- og strukturmålingar for eit ufullstendig metadatakorpus. "
      "Manglande kumulativitet er framleis ei hypotese som krev uavhengig fulltekstkoding "
      "av prøvbare påstandar, replikerte resultat og eksplisitt teorirevisjon. "
      "Den utvida API-innsamlinga stoppa ved rategrense, ikkje ved uttømmande dekning.",
    ])
    (OUT/"AVANSERT_ANALYSE.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    con.close()
    print("SUMMARY",json.dumps({"total":len(works),"edges":len(edges),
       "core_n":int(works.core_venue.sum()),"bibliographic":stats,"stability":stability},
       indent=2,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
