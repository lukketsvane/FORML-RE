#!/usr/bin/env python3
"""Conservative second-pass validation of in-text citation locators in cached PDFs.

Metadata aliases are not full-text interpretations. All results are evidence
location *candidates* and require human confirmation of referent/claim context.
No PDF content or substantial extracts are republished.
"""
from __future__ import annotations
import csv,datetime as dt,json,re,sqlite3,unicodedata
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parent
IN=ROOT/"results"/"oa_citation_locator_audit.csv"
OUT=ROOT/"results"
CONN=ROOT/"data"/"nordic_design_research.sqlite"
FIELDS=["citing_work_id","cited_work_id","citing_doi","cited_doi",
        "cited_metadata_year","cited_author_alias","bibliography_title_exact",
        "cited_doi_in_text","body_author_year_candidate_pages",
        "reference_title_pages","reference_doi_pages",
        "source_pdf_pages","validation_tier","notes"]
def basic(s):
    norm=unicodedata.normalize("NFKD",s or "").lower()
    norm="".join(ch for ch in norm if not unicodedata.combining(ch))
    return re.sub(r"\s+"," ",re.sub("[^a-z0-9]+"," ",norm)).strip()
def author_alias(raw):
    try: j=json.loads(raw)
    except Exception:return ""
    au=(j.get("authorships") or [{}])[0]
    full=((au.get("author") or {}).get("display_name") or "").strip()
    if "," in full:
        # OpenAlex can return "Deckers, EJL Eva", where the first comma part
        # is the family name. A naïve .split()[-1] would incorrectly give Eva.
        family=full.split(",",1)[0].strip()
    else:
        pieces=full.split()
        family=pieces[-1] if pieces else ""
    return family if len(family)>=3 else ""
def content_pages(doc,phrase,normalize=True):
    matches=[]
    for i,page in enumerate(doc):
        raw=page.get_text("text",sort=True)
        text=basic(raw) if normalize else raw.lower()
        if phrase and phrase in text:matches.append(i+1)
    return matches
def title_probe(title):
    words=basic(title).split()
    # Reference entries may have truncated subtitles, so prefer the first 6 words.
    return " ".join(words[:min(6,len(words))]) if len(words)>=4 else ""
def find_body(doc,surname,year):
    if not surname or not year:return []
    family=re.escape(surname)
    if not family:return []
    # Do not scan across a different four-digit year, a semicolon separating
    # references, or a line break. The earlier punctuation-stripped version
    # accidentally allowed nearby *other* references to satisfy this match.
    between=r"(?:(?!\b(?:19|20)\d{2}\b|;|\n).){0,90}?"
    phrase=re.compile(r"\b"+family+r"\b"+between+r"\b"+re.escape(str(year))+r"\b",re.I)
    # Bibliography is often in last quarter, but use headings to infer beginning.
    first_reference=len(doc)
    for i,page in enumerate(doc):
        txt=page.get_text("text",sort=True)
        if re.search(r"(?im)^\s*(?:\d{1,2}[.]?\s*)?(?:references|bibliography|litteratur|works cited)\s*$",txt):
            if i>max(1,len(doc)//3):first_reference=min(first_reference,i)
    pages=[]
    for i,page in enumerate(doc):
        if i>=first_reference:break
        s=page.get_text("text",sort=True)
        if phrase.search(s):pages.append(i+1)
    return pages

def main():
    conn=sqlite3.connect(CONN)
    rows=list(csv.DictReader(IN.open(encoding="utf-8",newline="")))
    audited=[]
    for r in rows:
        if str(r["pdf_available"])!="1":continue
        citing=r["paper_id"];cited=r["cited_work_id"]
        match=conn.execute("SELECT doi,title,year,raw_json FROM works WHERE id=?",(cited,)).fetchone()
        newer=conn.execute("SELECT doi FROM works WHERE id=?",(citing,)).fetchone()
        if not match:continue
        doi,title,year,raw=match
        family=author_alias(raw)
        pdf=ROOT/"data"/"oa_fulltexts_private"/(citing+".pdf")
        if not pdf.exists():continue
        with fitz.open(pdf) as doc:
            ref_title=title_probe(title)
            matches=content_pages(doc,ref_title)
            DOI=(doi or "").split("doi.org/")[-1].lower()
            doi_pages=content_pages(doc,DOI,normalize=False) if DOI and DOI.startswith("10.") else []
            author_year=find_body(doc,family,year)
            has_bib=bool(matches or doi_pages)
            if author_year and has_bib:
                tier="bibliography-and-intext-candidate"
            elif has_bib:
                tier="bibliographic-entry-only"
            elif author_year:
                tier="unresolved-intext-year-only"
            else:tier="not-located"
            note=(
                "Reference-title/DOI may occur outside bibliography; manual check required"
                if has_bib else
                "Neither title nor DOI corroborates the person-year match; do not accept as verified citation"
            )
            audited.append({
              "citing_work_id":citing,"cited_work_id":cited,
              "citing_doi":newer[0] if newer else "","cited_doi":doi or "",
              "cited_metadata_year":year,"cited_author_alias":family,
              "bibliography_title_exact":int(bool(matches)),"cited_doi_in_text":int(bool(doi_pages)),
              "body_author_year_candidate_pages":";".join(map(str,author_year)),
              "reference_title_pages":";".join(map(str,matches)),
              "reference_doi_pages":";".join(map(str,doi_pages)),
              "source_pdf_pages":len(doc),"validation_tier":tier,"notes":note
            })
    out=OUT/"oa_reference_crosscheck.csv"
    with out.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(audited)
    bytier={}
    for a in audited:bytier[a["validation_tier"]]=bytier.get(a["validation_tier"],0)+1
    report={
      "utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "audited_pairs_with_retrieved_pdf":len(audited),
      "validation_tiers":bytier,
      "method":"First-author family name plus recorded publication year near each other in body; additionally first six normalized title words or DOI anywhere in PDF",
      "not_verified":"This script does not verify the exact bibliography entry, context, replicability, scientific effect or argument. Positive text matches are candidates only.",
      "manual_review_required":True
    }
    (OUT/"oa_reference_crosscheck_summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    for a in audited:print(a["citing_work_id"],a["cited_work_id"],a["validation_tier"],a["body_author_year_candidate_pages"],a["reference_title_pages"],a["reference_doi_pages"])
    conn.close()

if __name__=="__main__":main()
