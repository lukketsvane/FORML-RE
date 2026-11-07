"""Deterministisk, lesande PDF-proveniens-audit for designteori-korpuset.

Flaggar moglege feilkoplingar. Utgjeving av 'suspect' er aldri det same
som ein stadfesta feil. Skriptet skriv ikkje til korpus eller PDF-mapper.

Køyr:
  python audit_pdf_manifest.py C:/Users/Iver/Documents/github/designteori --sample 220
Krev PyMuPDF: pip install pymupdf
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import random
import re
import unicodedata

try:
    import fitz
except ImportError as exc:
    raise SystemExit("Installer pymupdf for å lese PDF: pip install pymupdf") from exc

STOP = set(
    "the and for with from this that into over under between toward towards "
    "where what which when design research study analysis an a is are of on "
    "to in at it by using through".split()
)


def normalize(value):
    low = unicodedata.normalize("NFKD", str(value).lower())
    letters = "".join(ch for ch in low if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", letters))


def classify(title, first_pages):
    needle = normalize(title)
    haystack = normalize(first_pages)
    if needle and needle in haystack:
        return "exact", 1.0
    tokens = set(t for t in needle.split() if len(t) > 3 and t not in STOP)
    if not tokens or not haystack:
        return "unreadable", 0.0
    share = len(tokens & set(haystack.split())) / len(tokens)
    if share >= 0.7:
        return "likely", round(share, 3)
    if share >= 0.45:
        return "ambiguous", round(share, 3)
    return "suspect", round(share, 3)


def inspect(corpus, *, sample=220, seed=20261107, max_pages=3):
    pub = {r["id"]: r for r in json.loads((corpus / "docs/data/publications.json").read_text(encoding="utf8"))}
    manifest = json.loads((corpus / "pdf/manifest.json").read_text(encoding="utf8"))["items"]
    eligible = sorted(
        x for x in manifest if x in pub and
        (corpus / manifest[x]["file"]).is_file()
    )
    if sample <= 0 or sample >= len(eligible):
        selected = eligible
    else:
        selected = random.Random(seed).sample(eligible, sample)
    rows = []
    for work_id in selected:
        rec = pub[work_id]
        entry = manifest[work_id]
        path = corpus / entry["file"]
        try:
            with fitz.open(path) as pdf:
                page_text = " ".join(pdf[i].get_text() for i in range(min(max_pages, len(pdf))))
        except Exception:
            page_text = ""
        status, share = classify(rec.get("title", ""), page_text)
        rows.append({
            "id": work_id,
            "status": status,
            "title_token_share": share,
            "metadata_title": rec.get("title", ""),
            "metadata_doi": rec.get("doi", ""),
            "source_url": entry.get("source_url", ""),
        })
    return {"tested": len(rows), "eligible": len(eligible),
            "sample_seed": seed, "counts": dict(Counter(r["status"] for r in rows)),
            "flags": [r for r in rows if r["status"] in {"ambiguous", "suspect", "unreadable"}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="Rotmappa for lokal designteori-checkout")
    parser.add_argument("--sample", type=int, default=220, help="0 = alle PDF-ar")
    parser.add_argument("--seed", type=int, default=20261107)
    parser.add_argument("--max-pages", type=int, default=3)
    args = parser.parse_args()
    result = inspect(args.corpus, sample=args.sample, seed=args.seed, max_pages=args.max_pages)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\nMerk: Flagga krev kjeldekontroll. Eit uleseleg PDF-tekstlag er ikkje prov på feil fil.")


if __name__ == "__main__":
    main()
