#!/usr/bin/env python3
"""Discover Nordic-affiliated design research. Metadata and abstracts, not PDFs."""
import argparse, datetime as dt, json, os, re, sqlite3, sys, time
from pathlib import Path
import requests
from urllib.parse import urlencode

BASE=Path(__file__).resolve().parent
DB=BASE/"data"/"nordic_design_research.sqlite"
API="https://api.openalex.org/works"
NORDIC={"NO","SE","DK","FI","IS"}
QUERIES=[
"design theory","design research","research through design","design methods",
"design methodology","design philosophy","design epistemology","design aesthetics",
"design history","history of design","design ethics","design justice",
"design thinking","critical design","speculative design","participatory design",
"co-design","user centered design","service design","systemic design",
"systems oriented design","interaction design","industrial design",
"product design","design education","design practice","sustainable design",
"design anthropology","design studies","design processes","design and innovation"
]
FILTER="publication_year:2000-2026,authorships.countries:NO|SE|DK|FI|IS,type:article|book|book-chapter|proceedings-article|review"
FIELDS="id,doi,display_name,publication_year,publication_date,type,cited_by_count,authorships,abstract_inverted_index,referenced_works,primary_topic,keywords,primary_location,open_access,language"
TITLE_TERMS=re.compile(r"\b(?:design|designer|designing|formgiving|formgjeving|gestaltning|arkitektur|architecture|architectural)\b",re.I)
CLINICAL=re.compile(r"\b(?:trial design|study design|design of (?:a|the) (?:cohort|trial|study)|clinical trial protocol|randomi[sz]ed controlled trial)\b",re.I)

def abstract_from_index(idx):
    if not idx or not isinstance(idx,dict): return ""
    pairs=[(pos,word) for word,positions in idx.items() for pos in positions if isinstance(pos,int)]
    return " ".join(word for _,word in sorted(pairs))

def setup(conn):
    conn.executescript("""
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS works (
      id TEXT PRIMARY KEY, doi TEXT, title TEXT, year INTEGER, publication_date TEXT,
      kind TEXT, abstract TEXT, citations INTEGER, source TEXT, source_id TEXT,
      language TEXT, oa_url TEXT, countries TEXT, topic TEXT,
      in_scope INTEGER NOT NULL, decision TEXT, raw_json TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_work_year ON works(year);
    CREATE INDEX IF NOT EXISTS idx_work_doi ON works(doi);
    CREATE TABLE IF NOT EXISTS discoveries(
      id TEXT, query TEXT, page INTEGER, PRIMARY KEY(id,query));
    CREATE TABLE IF NOT EXISTS references_all(
      citing_id TEXT, cited_id TEXT, PRIMARY KEY(citing_id,cited_id));
    CREATE INDEX IF NOT EXISTS idx_ref_cited ON references_all(cited_id);
    CREATE TABLE IF NOT EXISTS authorships(
      work_id TEXT, author_id TEXT, author_name TEXT, institution_id TEXT,
      institution_name TEXT, country TEXT, author_position TEXT);
    CREATE INDEX IF NOT EXISTS idx_author_work ON authorships(work_id);
    CREATE TABLE IF NOT EXISTS query_log(
      query TEXT, page INTEGER, url TEXT, total_hits INTEGER,
      returned INTEGER, fetched_at TEXT, error TEXT, PRIMARY KEY(query,page));
    """)

def ingest(conn, w, query, page):
    wid=(w.get("id") or "").rsplit("/",1)[-1]
    if not wid: return
    aus=w.get("authorships") or []
    cs=sorted(({c for a in aus for c in (a.get("countries") or [])}
       |{i.get("country_code") for a in aus for i in (a.get("institutions") or [])}) & NORDIC)
    title=w.get("display_name") or "(untitled)"
    include=int(bool(cs) and bool(TITLE_TERMS.search(title)) and not CLINICAL.search(title))
    decision="Nordic affiliation and design-related title" if include else "Needs manual eligibility review"
    loc=w.get("primary_location") or {}; source=loc.get("source") or {}
    topic=w.get("primary_topic") or {}; oa=w.get("open_access") or {}
    record=(wid,w.get("doi"),title,w.get("publication_year"),w.get("publication_date"),
      w.get("type"),abstract_from_index(w.get("abstract_inverted_index")),
      w.get("cited_by_count",0),source.get("display_name"),source.get("id"),
      w.get("language"),oa.get("oa_url"),json.dumps(cs),topic.get("display_name"),
      include,decision,json.dumps(w,ensure_ascii=False,separators=(",",":")))
    conn.execute("""INSERT INTO works VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(id) DO UPDATE SET
      doi=excluded.doi,title=excluded.title,year=excluded.year,
      publication_date=excluded.publication_date,kind=excluded.kind,
      abstract=excluded.abstract,citations=excluded.citations,
      source=excluded.source,source_id=excluded.source_id,
      language=excluded.language,oa_url=excluded.oa_url,
      countries=excluded.countries,topic=excluded.topic,
      in_scope=excluded.in_scope,decision=excluded.decision,raw_json=excluded.raw_json""",record)
    conn.execute("INSERT OR IGNORE INTO discoveries VALUES (?,?,?)",(wid,query,page))
    conn.executemany("INSERT OR IGNORE INTO references_all VALUES (?,?)",
       [(wid,r.rsplit("/",1)[-1]) for r in w.get("referenced_works") or [] if r])
    conn.execute("DELETE FROM authorships WHERE work_id=?",(wid,))
    rows=[]
    for a in aus:
        author=a.get("author") or {}; insts=a.get("institutions") or [{}]
        for i in insts:
            rows.append((wid,(author.get("id") or "").rsplit("/",1)[-1],
              author.get("display_name"),(i.get("id") or "").rsplit("/",1)[-1],
              i.get("display_name"),i.get("country_code"),a.get("author_position")))
    conn.executemany("INSERT INTO authorships VALUES (?,?,?,?,?,?,?)",rows)

def main():
    p=argparse.ArgumentParser();p.add_argument("--pages",type=int,default=2)
    p.add_argument("--limit-queries",type=int,default=0);p.add_argument("--force",action="store_true")
    args=p.parse_args();DB.parent.mkdir(exist_ok=True,parents=True)
    from database import ensure_database
    ensure_database(DB)
    c=sqlite3.connect(DB);setup(c)
    sess=requests.Session()
    sess.headers["User-Agent"]="NordicDesignResearchAudit/1.0 (noncommercial bibliography)"
    queries=QUERIES[:args.limit_queries] if args.limit_queries else QUERIES
    fail=0;halt=False
    for ix,q in enumerate(queries,1):
        for page in range(1,args.pages+1):
            if not args.force and c.execute(
                  "SELECT error FROM query_log WHERE query=? AND page=?",(q,page)).fetchone()==(None,):
                print("SKIP",q,page,flush=True);continue
            params={"filter":FILTER,"search":'"'+q+'"',"per_page":100,"page":page,"select":FIELDS}
            url=API+"?"+urlencode(params)
            error=None; works=[]; total=0
            for attempt in range(3):
                try:
                    response=sess.get(API,params=params,timeout=40)
                    response.raise_for_status()
                    j=response.json()
                    works=j.get("results",[]);total=j.get("meta",{}).get("count",0)
                    error=None
                    break
                except (requests.RequestException,ValueError) as e:
                    error=f"{type(e).__name__} {str(e)[:180]}"
                    print("REQUEST_ERROR",q,page,error,flush=True)
                    if any(str(s) in error for s in ("400","401","403","429")):break
                    time.sleep(1.5*(attempt+1))
            for w in works:ingest(c,w,q,page)
            c.execute("INSERT OR REPLACE INTO query_log VALUES (?,?,?,?,?,?,?)",
              (q,page,url,total,len(works),dt.datetime.now(dt.timezone.utc).isoformat(),error))
            c.commit()
            n=c.execute("SELECT count(*) FROM works").fetchone()[0]
            y=c.execute("SELECT count(*) FROM works WHERE in_scope=1").fetchone()[0]
            print(f"{ix}/{len(queries)} {q} page={page} returned={len(works)} total_hits={total} unique={n} included={y} {error or ''}",flush=True)
            if error:
                fail+=1
                if any(s in error for s in ("401","403","429")):halt=True
                break
            if len(works)<100:break
            time.sleep(0.15)
        if halt:break
    try:
        c.execute("DROP TABLE IF EXISTS works_fts")
        c.execute("CREATE VIRTUAL TABLE works_fts USING fts5(title,abstract,content='works',content_rowid='rowid')")
        c.execute("INSERT INTO works_fts(rowid,title,abstract) SELECT rowid,title,abstract FROM works")
    except sqlite3.OperationalError as e: print("FTS5 unavailable",e)
    c.commit()
    print("FINAL",{"candidates":c.execute("SELECT count(*) FROM works").fetchone()[0],
      "title_included":c.execute("SELECT count(*) FROM works WHERE in_scope=1").fetchone()[0],
      "abstracts":c.execute("SELECT count(*) FROM works WHERE length(abstract)>40").fetchone()[0],
      "pages_successful":c.execute("SELECT count(*) FROM query_log WHERE error IS NULL").fetchone()[0]},flush=True)
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)");c.close()
    return int(fail>0)
if __name__=="__main__":raise SystemExit(main())
