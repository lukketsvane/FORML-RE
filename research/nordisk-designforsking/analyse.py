#!/usr/bin/env python3
"""Descriptive bibliometrics and exploratory metadata text/network science."""
from __future__ import annotations
import argparse, collections, datetime as dt, json, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
DB=ROOT/"data"/"nordic_design_research.sqlite"
OUT=ROOT/"results"; PLOTS=OUT/"figures"
THEMES={
 "grunnlagsteori":["design theory","design philosophy","design epistemology","design aesthetics"],
 "forsking/metode":["design research","research through design","design methods","design methodology","design practice","design processes","design studies"],
 "historie":["design history","history of design"],
 "etikk/kritikk":["design ethics","design justice","critical design","speculative design","sustainable design"],
 "deltaking":["participatory design","co-design","user centered design"],
 "teneste/system":["service design","systemic design","systems oriented design","design thinking","design and innovation"],
 "interaksjon":["interaction design"],
 "produkt":["industrial design","product design"],
 "utdanning/antropologi":["design education","design anthropology"]
}
QUERY2THEME={q:k for k,vals in THEMES.items() for q in vals}
PERIODS=[2000,2005,2010,2015,2020,2025,2027]
PERIOD_NAMES=["2000–04","2005–09","2010–14","2015–19","2020–24","2025–26"]

def fmt(v):return f"{int(v):,}".replace(","," ")
def pct(n,d):return round(100*n/d,1) if d else 0.0
def save(name):
    plt.tight_layout();plt.savefig(PLOTS/name,dpi=160,bbox_inches="tight");plt.close()

def load(conn):
    df=pd.read_sql_query("SELECT id,doi,title,year,publication_date,kind,abstract,citations,source,language,oa_url,countries,topic FROM works WHERE in_scope=1",conn)
    dis=pd.read_sql_query("SELECT id,query FROM discoveries",conn)
    byid=dis.groupby("id")["query"].agg(list).to_dict()
    df["queries"]=df.id.map(lambda x:byid.get(x,[]))
    def choose(row):
        queries=row.queries
        exact=[q for q in queries if q in row.title.lower()]
        q=sorted(exact or queries or [""])[0]
        return QUERY2THEME.get(q,"anna")
    df["theme"]=df.apply(choose,axis=1)
    df["country_list"]=df.countries.fillna("[]").apply(json.loads)
    df["has_abstract"]=df.abstract.fillna("").str.len()>=60
    df["period"]=pd.cut(df.year,bins=PERIODS,labels=PERIOD_NAMES,right=False)
    return df

def main():
    p=argparse.ArgumentParser();p.add_argument("--min-records",type=int,default=1);args=p.parse_args()
    OUT.mkdir(exist_ok=True);PLOTS.mkdir(exist_ok=True)
    from database import ensure_database
    ensure_database(DB)
    conn=sqlite3.connect(DB);df=load(conn)
    if len(df)<args.min_records:raise SystemExit(f"Only {len(df)} records")
    qlog=pd.read_sql_query("SELECT query,page,total_hits,returned,error FROM query_log",conn)
    qlog.to_csv(OUT/"query_log.csv",index=False)
    cols=["id","doi","title","year","kind","citations","source","countries","topic","theme","oa_url"]
    df.sort_values(["year","title"]).to_csv(OUT/"included_publications.csv",columns=cols,index=False,encoding="utf-8")
    excluded=pd.read_sql_query("SELECT id,doi,title,year,decision FROM works WHERE in_scope=0",conn)
    excluded.to_csv(OUT/"candidates_for_manual_review.csv",index=False,encoding="utf-8")
    byyear=df.groupby("year").agg(n=("id","size"),median_citations=("citations","median"),with_abstract=("has_abstract","sum")).reset_index()
    byyear.to_csv(OUT/"by_year.csv",index=False)
    bytheme=df.groupby(["period","theme"],observed=True).size().unstack(fill_value=0).reindex(PERIOD_NAMES,fill_value=0)
    bytheme.to_csv(OUT/"by_period_and_theme.csv")
    countries=collections.Counter(v for vals in df.country_list for v in vals)
    pd.DataFrame(sorted(countries.items()),columns=["country_code","works_with_affiliation"]).to_csv(OUT/"by_country.csv",index=False)
    plt.figure(figsize=(8,4));plt.plot(byyear.year,byyear.n,marker=".",lw=1)
    plt.title("Publikasjonar i rangsortert søkjeutval, ikkje heile feltet")
    plt.xlabel("Publikasjonsår");plt.ylabel("Innhenta postar");save("01-sokjeutval-per-aar.png")
    fig,ax=plt.subplots(figsize=(9,4.6));bytheme.plot(kind="bar",stacked=True,ax=ax)
    ax.set_title("Søkjetema i innsamla utval");ax.set_xlabel("Femårsbolk");ax.set_ylabel("Postar")
    ax.legend(fontsize=7,bbox_to_anchor=(1.01,1),loc="upper left");save("02-sokjetema.png")
    plt.figure(figsize=(8,4));plt.plot(byyear.year,byyear.median_citations,marker=".")
    plt.title("Globalt siteringstal etter publikasjonsår (aldersskeivt)")
    plt.xlabel("År");plt.ylabel("Median OpenAlex-siteringar");save("03-sitering-per-aar.png")
    plt.figure(figsize=(7,4));plt.bar(list(countries),list(countries.values()))
    plt.title("Forfattartilknyting (ein publikasjon kan telje i fleire land)")
    plt.ylabel("Publikasjonar");save("04-land.png")
    # All observed within-sample direct references; missing works imply missing edges.
    refs=pd.read_sql_query("""SELECT r.citing_id,r.cited_id,
       a.year AS citing_year,b.year AS cited_year FROM references_all r
       JOIN works a ON r.citing_id=a.id AND a.in_scope=1
       JOIN works b ON r.cited_id=b.id AND b.in_scope=1
       WHERE r.citing_id!=r.cited_id""",conn)
    tm=dict(zip(df.id,df.theme))
    refs["citing_theme"]=refs.citing_id.map(tm)
    refs["cited_theme"]=refs.cited_id.map(tm)
    refs["citation_age_years"]=refs.citing_year-refs.cited_year
    refs.to_csv(OUT/"internal_citations.csv",index=False)
    graph=nx.Graph();graph.add_nodes_from(df.id.tolist())
    if not refs.empty:graph.add_edges_from(refs[["citing_id","cited_id"]].itertuples(index=False,name=None))
    isolates=nx.number_of_isolates(graph)
    comps=sorted(nx.connected_components(graph),key=len,reverse=True)
    giant=len(comps[0]) if comps else 0; modularity=None
    if 4<=giant<=2500:
        g=graph.subgraph(comps[0])
        communities=list(nx.community.greedy_modularity_communities(g))
        modularity=float(nx.community.modularity(g,communities))
    themes=sorted(df.theme.unique())
    cross=pd.crosstab(refs.citing_theme,refs.cited_theme).reindex(index=themes,columns=themes,fill_value=0)
    cross.to_csv(OUT/"citation_theme_matrix.csv")
    if len(themes)>1:
        mat=cross.to_numpy(dtype=float)
        den=mat.sum(axis=1,keepdims=True)
        mat=np.divide(mat,den,out=np.zeros_like(mat),where=den>0)
        plt.figure(figsize=(9,7));plt.imshow(mat,aspect="auto",cmap="Blues",vmin=0,vmax=1)
        plt.xticks(range(len(themes)),themes,rotation=35,ha="right",fontsize=8)
        plt.yticks(range(len(themes)),themes,fontsize=8)
        plt.colorbar(label="Del av interne referansar")
        plt.title("Kryssitering mellom operasjonelle temagrupper")
        save("05-kryssitering.png")
    # Language-limited LSA; title plus available abstracts (never PDFs).
    texts=(df.title.fillna("")+". "+df.abstract.fillna("").str.slice(0,4500)).tolist()
    tf=TfidfVectorizer(stop_words="english",ngram_range=(1,2),min_df=3,max_df=.85,max_features=16000,sublinear_tf=True)
    sparse=tf.fit_transform(texts)
    dims=min(40,sparse.shape[0]-2,sparse.shape[1]-2)
    svd=TruncatedSVD(n_components=dims,n_iter=5,random_state=42)
    vectors=normalize(svd.fit_transform(sparse))
    from joblib import dump
    dump({"tfidf":tf,"svd":svd},OUT/"lsa_model.joblib",compress=3)
    np.savez_compressed(OUT/"lsa_vectors.npz",ids=df.id.to_numpy(dtype=str),vectors=vectors.astype("float32"))
    nc=9
    clustering=KMeans(n_clusters=nc,random_state=42,n_init=5,max_iter=160)
    labels=clustering.fit_predict(vectors);df["cluster"]=labels
    silhouette=float(silhouette_score(vectors,labels,sample_size=min(800,len(df)),random_state=42))
    words=tf.get_feature_names_out()
    clusters=[]
    for n in range(nc):
        inds=np.flatnonzero(labels==n)
        scores=np.asarray(sparse[inds].mean(axis=0)).ravel()
        top=[str(words[i]) for i in np.argsort(scores)[-8:][::-1]]
        clusters.append({"cluster":n,"count":len(inds),"descriptive_top_terms":top})
    (OUT/"latent_topics.json").write_text(json.dumps(clusters,ensure_ascii=False,indent=2),encoding="utf-8")
    df[["id","title","year","theme","cluster"]].to_csv(OUT/"semantic_clusters.csv",index=False)
    plt.figure(figsize=(9,6))
    for k in range(nc):
        mask=labels==k
        plt.scatter(vectors[mask,0],vectors[mask,1],s=5,alpha=.5,label=f"{k} ({sum(mask)})")
    plt.title("Latent tekstrom — titlar og tilgjengelege samandrag")
    plt.xlabel("LSA dimensjon 1");plt.ylabel("LSA dimensjon 2")
    plt.legend(fontsize=7,markerscale=2,ncol=3);save("06-lsa-tekstrom.png")
    near=NearestNeighbors(n_neighbors=6,algorithm="brute",metric="cosine").fit(vectors)
    distances,neighbours=near.kneighbors(vectors)
    nearrows=[]
    for i,workid in enumerate(df.id):
        for j,distance in zip(neighbours[i,1:],distances[i,1:]):
            nearrows.append((workid,df.id.iloc[j],float(1-distance)))
    pd.DataFrame(nearrows,columns=["id","similar_id","text_cosine"]).to_csv(OUT/"semantic_neighbours.csv",index=False)
    distributions=[]
    for label in PERIOD_NAMES:
        xs=df.loc[df.period==label,"cluster"].to_numpy(dtype=int)
        hist=np.bincount(xs,minlength=nc).astype(float)
        if hist.sum():hist/=hist.sum()
        distributions.append(hist)
    drift=[]
    for i in range(1,len(distributions)):
        x,y=distributions[i-1:i+1]
        val=float(jensenshannon(x,y,base=2)**2) if x.sum()>0 and y.sum()>0 else None
        drift.append((PERIOD_NAMES[i-1],PERIOD_NAMES[i],val))
    pd.DataFrame(drift,columns=["from","to","JS_divergence_bits"]).to_csv(OUT/"semantic_drift.csv",index=False)
    plt.figure(figsize=(8,3.7))
    plt.bar([a+"–"+b for a,b,_ in drift],[v or 0 for _,_,v in drift])
    plt.title("Endring i latente tekstklynger mellom årsbolkar")
    plt.xticks(rotation=35,ha="right",fontsize=8);plt.ylabel("Jensen–Shannon (bit)")
    save("07-tekstdynamikk.png")
    df.sort_values("citations",ascending=False).head(100).to_csv(OUT/"top_cited.csv",
      columns=["id","doi","title","year","citations","theme"],index=False)
    total=int(pd.read_sql_query("SELECT count(*) as n FROM works",conn).iloc[0]["n"])
    same=int((refs.citing_theme==refs.cited_theme).sum())
    summary={
      "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "sample_definition":"Nordic-affiliated OpenAlex 2000-2026, top two relevance-ranked pages per search, automatically screened by title",
      "unique_candidates":total,"provisionally_included":len(df),"manual_review_pending":len(excluded),
      "successful_search_pages":int(qlog.error.isna().sum()),
      "with_abstract":int(df.has_abstract.sum()),"abstract_coverage_pct":pct(int(df.has_abstract.sum()),len(df)),
      "duplicate_dois_in_included":int(df.doi.dropna().duplicated().sum()),
      "publication_sources":int(df.source.nunique(dropna=True)),
      "country_memberships":dict(countries),
      "cited_edges_within_retrieved_sample":len(refs),
      "internal_citation_graph_isolates":int(isolates),
      "internal_citation_graph_largest_component":int(giant),
      "network_modularity_largest_component":modularity,
      "internal_same_theme_edges":same,"internal_cross_theme_edges":int(len(refs)-same),
      "lsa_components":dims,"lsa_explained_variance_ratio":float(svd.explained_variance_ratio_.sum()),
      "cluster_count":nc,"cluster_silhouette_exploratory":silhouette,
      "full_text_pdfs_collected":0,
      "methodological_limit":"Descriptive, capped search sample; no validated inference about scientific cumulativity."
    }
    (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=[
    "# Nordisk designforsking 2000–2026 — datarapport",
    "",
    "Uttrekksdato: "+summary["generated_utc"]+". Kjelde: OpenAlex. Kun metadata og tilgjengelege samandrag.",
    "",
    "## Omfang",
    f"- {fmt(total)} ulike kandidatar innhenta; {fmt(len(df))} er automatisk tittelavgrensa for vidare analyse.",
    f"- {fmt(len(excluded))} kandidatar står att til manuell gjennomgang.",
    f"- {summary['successful_search_pages']} søkjesider, {summary['publication_sources']} ulike publiseringskjelder.",
    f"- {fmt(summary['with_abstract'])} postar med minst 60 teikn i samandraget ({summary['abstract_coverage_pct']} %).",
    f"- {fmt(len(refs))} observerte interne referansekanter mellom inkluderte postar.",
    f"- {summary['duplicate_dois_in_included']} DOI-duplikat i det inkluderte utvalet.",
    "",
    "## Analyser",
    "Publikasjonar per år, temakategoriar over tid, nordiske institusjonstilknytingar, siteringstal, "
    "direkte siteringsnettverk, krysstematiske referansar, LSA-tekstrom, KMeans, nærnaboar og Jensen–Shannon-drift.",
    f"- Tekstmodellen: {dims} LSA-dimensjonar; {nc} klynger; utforskande silhuett={silhouette:.3f}.",
    f"- Nettverket: {isolates} isolerte nodar; største komponent {giant}; modularitet {modularity}.",
    "",
    "## Kva dette IKKJE beviser",
    "Det rangsorterte søkjeutvalet er ikkje representativt for all nordisk designforsking. "
    "Sitering er ikkje replikasjon, tekstlikskap er ikkje testing, og fragmentering er ikkje i seg sjølv bevis på "
    "manglande kumulativ vitskap. Tidstrendar er skeive av søkjerangering, siteringsalder og endringar i indeksering.",
    "Analysen kan ikkje støtte påstanden om at faget ikkje har produsert reproduserbare funn.",
    "",
    "## Neste vitskaplege prøve",
    "Utvikle kodebok for eksplisitte hypotesar, operasjonalisering, negative resultat, replikasjon, motseiingar og "
    "teoretisk vidarebygging. Trekk eit sannsynsutval og bruk to uavhengige kodarar, med usemje og reliabilitet rapportert. "
    "Samanlikn mot ein referansedisiplin med same kriterium og korriger for publikasjonsår og sjanger.",
    "",
    "## Figurar",
    *["- "+x.name for x in sorted(PLOTS.glob("*.png"))],
    "",
    "Datafiler og figurane står i results/. Databasefil og søkjelogg er lagra i data/ og results/.",
    ""
    ]
    (OUT/"RAPPORT.md").write_text("\n".join(lines),encoding="utf-8")
    conn.close()
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
