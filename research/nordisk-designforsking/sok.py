#!/usr/bin/env python3
"""Local semantic search of titles + available abstracts; also SQLite FTS5."""
import argparse, json, sqlite3
from pathlib import Path
import numpy as np
from joblib import load
from sklearn.preprocessing import normalize
ROOT=Path(__file__).resolve().parent
DB=ROOT/"data"/"nordic_design_research.sqlite"
OUT=ROOT/"results"
def main():
    p=argparse.ArgumentParser(description="Search the locally harvested Nordic design bibliographic database")
    p.add_argument("query");p.add_argument("--limit",type=int,default=12)
    p.add_argument("--mode",choices=["semantic","fts"],default="semantic")
    args=p.parse_args()
    from database import ensure_database
    ensure_database(DB)
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    if args.mode=="fts":
        q='"'+'" AND "'.join(args.query.replace('"',"").split())+'"'
        try:
            rows=c.execute("""SELECT w.id,w.title,w.year,w.doi
             FROM works_fts f JOIN works w ON w.rowid=f.rowid
             WHERE works_fts MATCH ? AND w.in_scope=1 ORDER BY bm25(works_fts)
             LIMIT ?""",(q,args.limit)).fetchall()
        except sqlite3.OperationalError as ex: raise SystemExit(f"FTS error: {ex}")
        for r in rows:print(f"{r['year']}  {r['title']}  {r['doi'] or r['id']}")
    else:
        v=np.load(OUT/"lsa_vectors.npz")
        model=load(OUT/"lsa_model.joblib")
        ids=v["ids"];data=v["vectors"]
        q=normalize(model["svd"].transform(model["tfidf"].transform([args.query])))[0]
        vals=data@q
        ix=np.argsort(vals)[::-1][:args.limit]
        for j in ix:
            row=c.execute("SELECT title,year,doi FROM works WHERE id=?",(str(ids[j]),)).fetchone()
            if row:print(f"{vals[j]:.3f}  {row['year']}  {row['title']}  {row['doi'] or ids[j]}")
    c.close()
if __name__=="__main__":main()
