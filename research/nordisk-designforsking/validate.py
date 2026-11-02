#!/usr/bin/env python3
"""Check the publication-safe database, source-to-archive counts and SQLite integrity."""
import gzip
import hashlib
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path
from database import DB, GZ

HERE=Path(__file__).resolve().parent
SUMMARY=HERE/"results"/"summary.json"
def main():
    if not GZ.is_file():raise SystemExit("Missing public archive")
    expected=json.loads(SUMMARY.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)/"check.sqlite"
        with gzip.open(GZ,"rb") as source,open(t,"wb") as target:
            shutil.copyfileobj(source,target)
        conn=sqlite3.connect(t)
        assert conn.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        works=conn.execute("SELECT COUNT(*) FROM works").fetchone()[0]
        included=conn.execute("SELECT COUNT(*) FROM works WHERE in_scope=1").fetchone()[0]
        log=conn.execute("SELECT COUNT(*) FROM query_log WHERE error IS NULL").fetchone()[0]
        failed=conn.execute("SELECT COUNT(*) FROM query_log WHERE error IS NOT NULL").fetchone()[0]
        abstracts=conn.execute("SELECT COUNT(*) FROM works WHERE LENGTH(abstract)>0").fetchone()[0]
        payloads=conn.execute("SELECT COUNT(*) FROM works WHERE LENGTH(raw_json)>2").fetchone()[0]
        fts=conn.execute("SELECT COUNT(*) FROM works_fts").fetchone()[0]
        assert works==expected["unique_candidates"],(works,expected["unique_candidates"])
        assert included==expected["provisionally_included"]
        assert log==expected["successful_search_pages"]
        assert (abstracts,payloads,fts)==(0,0,works)
        conn.close()
    from csv import reader
    with open(HERE/"results"/"included_publications.csv",encoding="utf-8",newline="") as f:
        csv_n=sum(1 for _ in reader(f))-1
    assert csv_n==included,(csv_n,included)
    digest=hashlib.sha256(GZ.read_bytes()).hexdigest()
    result={
      "works":works,"included":included,"successful_search_pages":log,
      "failed_search_pages":failed,"abstracts_republished":abstracts,
      "raw_provider_payloads_republished":payloads,
      "title_search_records":fts,
      "csv_included_rows":csv_n,
      "archive_bytes":GZ.stat().st_size,
      "sha256":digest,"sqlite_integrity":"ok"
    }
    (HERE/"results"/"release_validation.json").write_text(
       json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
