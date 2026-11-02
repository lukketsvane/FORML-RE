#!/usr/bin/env python3
"""Restore/pack the SQLite research archive with deterministic gzip metadata."""
import argparse, gzip, os, shutil, sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DB=ROOT/"data"/"nordic_design_research.sqlite"
GZ=DB.with_suffix(".sqlite.gz")
def ensure_database(path=DB):
    path=Path(path)
    if path.exists():return path
    archive=path.with_suffix(".sqlite.gz")
    if not archive.exists():return path
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(".restoring")
    with gzip.open(archive,"rb") as inp,open(tmp,"wb") as out:
        shutil.copyfileobj(inp,out)
    conn=sqlite3.connect(tmp)
    result=conn.execute("PRAGMA integrity_check").fetchone()[0]
    conn.close()
    if result!="ok":
        tmp.unlink(missing_ok=True)
        raise RuntimeError("Invalid compressed SQLite database: "+result)
    os.replace(tmp,path)
    return path
def archive_database(path=DB):
    path=Path(path)
    if not path.exists():raise FileNotFoundError(path)
    conn=sqlite3.connect(path)
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    result=conn.execute("PRAGMA integrity_check").fetchone()[0]
    conn.close()
    if result!="ok":raise RuntimeError(result)
    # Public archive includes bibliographic metadata, citations and search provenance.
    # Reconstructed article abstracts and provider payloads are intentionally excluded
    # because OpenAlex metadata access does not grant republication rights to abstracts.
    public=path.with_name("public_metadata.sqlite")
    shutil.copy2(path,public)
    safe=sqlite3.connect(public)
    safe.execute("UPDATE works SET abstract='', raw_json='{}'")
    safe.execute("DROP TABLE IF EXISTS works_fts")
    safe.execute("CREATE VIRTUAL TABLE works_fts USING fts5(title,abstract,content='works',content_rowid='rowid')")
    safe.execute("INSERT INTO works_fts(rowid,title,abstract) SELECT rowid,title,abstract FROM works")
    safe.commit();safe.execute("VACUUM")
    safe.close()
    archive=path.with_suffix(".sqlite.gz")
    tmp=archive.with_suffix(".gz.tmp")
    with open(public,"rb") as src,open(tmp,"wb") as target:
        with gzip.GzipFile(filename="",mode="wb",fileobj=target,mtime=0,compresslevel=9) as out:
            shutil.copyfileobj(src,out,1024*1024)
    os.replace(tmp,archive)
    public.unlink()
    print(f"Archived public metadata {path.stat().st_size:,} bytes locally -> {archive.stat().st_size:,} compressed bytes")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--archive",action="store_true")
    args=p.parse_args()
    if args.archive:archive_database()
    else:print(ensure_database())
