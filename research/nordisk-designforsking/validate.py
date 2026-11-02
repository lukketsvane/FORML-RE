#!/usr/bin/env python3
"""Integrity and provenance checks for the shareable, metadata-only archive."""
import gzip, hashlib, json, shutil, sqlite3, tempfile
from pathlib import Path
from database import DB, GZ
def main():
    if not GZ.is_file():raise SystemExit("Missing public archive")
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)/"check.sqlite"
        with gzip.open(GZ,"rb") as source,open(t,"wb") as target:
            shutil.copyfileobj(source,target)
        c=sqlite3.connect(t)
        assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        works=c.execute("SELECT count(*) FROM works").fetchone()[0]
        included=c.execute("SELECT count(*) FROM works WHERE in_scope=1").fetchone()[0]
        log=c.execute("SELECT count(*) FROM query_log WHERE error IS NULL").fetchone()[0]
        abstracts=c.execute("SELECT count(*) FROM works WHERE length(abstract)>0").fetchone()[0]
        payloads=c.execute("SELECT count(*) FROM works WHERE length(raw_json)>2").fetchone()[0]
        fts=c.execute("SELECT count(*) FROM works_fts").fetchone()[0]
        assert (works,included,log,abstracts,payloads,fts)==(4869,2889,60,0,0,4869)
        c.close()
    sha=hashlib.sha256(GZ.read_bytes()).hexdigest()
    result={"works":works,"included":included,"search_pages":log,
        "article_abstracts_republished":abstracts,"provider_payloads_republished":payloads,
        "fts_title_records":fts,"compressed_bytes":GZ.stat().st_size,
        "sha256":sha,"sqlite_integrity":"ok"}
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
