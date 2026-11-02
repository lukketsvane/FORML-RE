#!/usr/bin/env python3
"""Reproducible *access and citation-locator* audit of OA metadata.

This program DOES NOT adjudicate what a citation means, nor whether a
theoretical claim was validated. It records whether a *candidate citation
location* can be located in a legitimately accessible PDF.
PDFs and extracted text stay in local gitignored caches. Public exports
contain bibliographic IDs and page numbers, never fulltext reproduction.
"""
from __future__ import annotations
import argparse,csv,datetime as dt,hashlib,json,random,re,sqlite3,time,urllib.parse
from collections import Counter
from pathlib import Path
import requests
import fitz

ROOT=Path(__file__).resolve().parent
CACHE=ROOT/"data"/"oa_fulltexts_private"
OUT=ROOT/"results"
DB=ROOT/"data"/"nordic_design_research.sqlite"
URL_DENY={"localhost","127.0.0.1","0.0.0.0","::1"}
AGENT="FormlaereNordicResearchEvidenceAudit/1.0 (noncommercial academic fulltext access)"
KEYS=["paper_id","doi","title","year","oa_link","http_status","pdf_available",
      "local_pdf_sha256","pdf_page_count","fulltext_chars","has_text_layer",
      "citation_locator","possible_bibliographic_page_1based","candidate_body_pages_1based",
      "body_author_year_mentions","cited_work_id","cited_first_author","cited_year",
      "document_screening_notes","date_utc"]

def validate_https(url):
    try: o=urllib.parse.urlsplit(url or "")
    except Exception:return False
    if o.scheme!="https" or not o.hostname:return False
    if o.username or o.password:return False
    host=o.hostname.lower()
    if host in URL_DENY or host.endswith(".local") or host.endswith(".internal"):return False
    if host.startswith("10.") or host.startswith("192.168.") or host.startswith("172.16."):return False
    return True

def extract_paper_info(conn,work_id):
    r=conn.execute("SELECT doi,title,year,oa_url,raw_json FROM works WHERE id=?",(work_id,)).fetchone()
    if not r:return None
    try: raw=json.loads(r[4])
    except Exception:raw={}
    authorlist=(raw.get("authorships") or [])
    author_name=((authorlist[0].get("author") or {}).get("display_name") or "") if authorlist else ""
    surname=author_name.split()[-1] if author_name else ""
    if len(surname)<3 or surname.lower() in ("jr.","sr."):surname=""
    return {"id":work_id,"doi":r[0],"title":r[1],"year":r[2],"url":r[3],"surname":surname}

def retrieve_pdf(session,work,url,bytes_limit=14_000_000):
    CACHE.mkdir(parents=True,exist_ok=True)
    target=CACHE/(work["id"]+".pdf")
    if target.exists() and target.stat().st_size>500:
        b=target.read_bytes()
        if b[:4]==b"%PDF":return b,200,"cached"
        target.unlink()
    if not validate_https(url):
        return None,None,"invalid or non-HTTPS source"
    try:
        res=session.get(url,timeout=(8,22),headers={"Accept":"application/pdf,*/*;q=0.6"},
             stream=True,allow_redirects=True)
        if not validate_https(res.url):
            res.close()
            return None,None,"redirect target denied"
        status=res.status_code
        res.raise_for_status()
        chunks=[];count=0
        for chunk in res.iter_content(chunk_size=65536):
            if not chunk:continue
            count+=len(chunk)
            if count>bytes_limit:
                res.close()
                return None,status,"download larger than 14 MB"
            chunks.append(chunk)
        res.close()
        data=b"".join(chunks)
        if len(data)<400 or not data[:16].lstrip().startswith(b"%PDF"):
            return None,status,"not a direct PDF (may be article HTML)"
        target.write_bytes(data)
        return data,status,"pdf ok"
    except requests.RequestException as e:
        return (None, getattr(getattr(e,"response",None),"status_code",None),
                type(e).__name__+": "+str(e)[:80])
    except Exception as e:
        return None,None,type(e).__name__+": "+str(e)[:100]

def page_types(doc):
    # Conservative: if references heading is identifiable, count only preceding pages as body.
    heads=[]
    for i,page in enumerate(doc):
        txt=page.get_text("text",sort=True)
        match=re.search(r"(?im)^\s*(?:\d{1,2}(?:[.]|\s+))?(?:references|bibliography|referansar|litteratur|works cited)\s*$",txt)
        if match and i>=max(1,len(doc)//3):heads.append(i)
    stop=heads[-1] if heads else max(len(doc)-2,1)
    return stop

def find_citation_pages(doc,older):
    if not older:return [],[],0
    stop=page_types(doc)
    surname=older.get("surname","")
    year=str(older.get("year") or "")
    if not surname or len(year)!=4:return [],[],0
    pattern=re.compile(re.escape(surname)+r"[\s\S]{0,145}"+re.escape(year)+
                      r"|"+re.escape(year)+r"[\s\S]{0,145}"+re.escape(surname),re.I)
    matched_body=[];matched_ref=[];count=0
    for i,page in enumerate(doc):
        text=page.get_text("text",sort=True)
        if not text:continue
        number=len(pattern.findall(text))
        if number:
            if i<stop:
                matched_body.append(i+1);count+=number
            else:matched_ref.append(i+1)
    return matched_body,matched_ref,count

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--limit-pairs",type=int,default=30)
    parser.add_argument("--seed",type=int,default=20261102)
    parser.add_argument("--resume",action="store_true")
    args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(DB)
    with (OUT/"lineage_review_queue.csv").open(encoding="utf-8",newline="") as stream:
        queue=list(csv.DictReader(stream))
    pairs=[]
    for p in queue:
        younger=extract_paper_info(conn,p["citing_id"])
        older=extract_paper_info(conn,p["cited_id"])
        if younger and older and validate_https(younger["url"]):
            pairs.append((younger,older))
    both=[p for p in pairs if validate_https(p[1]["url"])]
    one=[p for p in pairs if not validate_https(p[1]["url"])]
    rng=random.Random(args.seed)
    rng.shuffle(both);rng.shuffle(one)
    chosen=(both+one)[:args.limit_pairs]
    print("QUEUE",{"200_review_pairs":len(queue),"citing_oa":len(pairs),"both_oa":len(both),
                   "selected":len(chosen)},flush=True)
    prev={}
    path=OUT/"oa_citation_locator_audit.csv"
    if args.resume and path.exists():
        with path.open(encoding="utf-8",newline="") as stream:
            prev={(row["paper_id"],row["cited_work_id"]):row for row in csv.DictReader(stream)}
    session=requests.Session();session.headers["User-Agent"]=AGENT
    results=[]
    for n,(young,older) in enumerate(chosen,1):
        key=young["id"],older["id"]
        if key in prev:
            results.append(prev[key]);print("SKIP",n,*key,flush=True);continue
        content,status,note=retrieve_pdf(session,young,young["url"])
        now=dt.datetime.now(dt.timezone.utc).isoformat()
        result=dict.fromkeys(KEYS,"")
        result.update({
          "paper_id":young["id"],"doi":young["doi"],"title":young["title"],
          "year":young["year"],"oa_link":young["url"],"http_status":status or "",
          "pdf_available":int(bool(content)),
          "citation_locator":"unavailable", "cited_work_id":older["id"],
          "cited_first_author":older["surname"],"cited_year":older["year"],
          "document_screening_notes":note,"date_utc":now,
        })
        if content:
            try:
                with fitz.open(stream=content,filetype="pdf") as doc:
                    texts=[page.get_text("text") for page in doc]
                    result["local_pdf_sha256"]=hashlib.sha256(content).hexdigest()
                    result["pdf_page_count"]=len(doc)
                    result["fulltext_chars"]=sum(len(v) for v in texts)
                    result["has_text_layer"]=int(result["fulltext_chars"]>=700)
                    if result["has_text_layer"]:
                        body,refs,count=find_citation_pages(doc,older)
                        result["candidate_body_pages_1based"]=";".join(map(str,body))
                        result["possible_bibliographic_page_1based"]=";".join(map(str,refs))
                        result["body_author_year_mentions"]=count
                        result["citation_locator"]=(
                          "body-candidate" if body else
                          "reference-only-candidate" if refs else
                          "not-located-by-author-year-heuristic")
                    else: result["citation_locator"]="no text layer"
            except Exception as e:
                result["pdf_available"]=0
                result["citation_locator"]="invalid PDF"
                result["document_screening_notes"]="PDF extraction failed "+type(e).__name__
        results.append(result)
        with path.open("w",encoding="utf-8",newline="") as file:
            writer=csv.DictWriter(file,fieldnames=KEYS);writer.writeheader();writer.writerows(results)
        print(f"{n}/{len(chosen)} {young['id']} {result['citation_locator']} {result['pdf_page_count']} pg ({str(result['document_screening_notes'])[:70]})",flush=True)
        time.sleep(.22)
    counts=Counter(row["citation_locator"] for row in results)
    report={
      "date_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "sampling":"Targeted, non-probability subset of top-200 high-LSA-citation pairs, randomized among valid OA links",
      "seed":args.seed,
      "review_pairs":len(queue),"citing_oa_pairs":len(pairs),"both_oa_pairs":len(both),
      "audited_pairs":len(results),
      "retrieved_pdf_count":sum(int(r["pdf_available"]) for r in results),
      "locator_status_counts":dict(counts),
      "copyright":"PDFs and all extracted text are stored on CYGNUS, outside GitHub, not republished",
      "limits":"Author-year cooccurrence and reference heading patterns do not establish correct citation identity or any epistemic function. Some PDF links yield HTML, require permissions, or differ from the canonical version."
    }
    (OUT/"oa_citation_locator_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    conn.close()
    print("FINAL",json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=="__main__":main()
