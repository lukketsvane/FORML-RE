#!/usr/bin/env python3
"""Describe OA link retrievability conditional on a deliberately selected queue.

No inference to the field's open-access share or scientific quality.
"""
from __future__ import annotations
import collections,csv,datetime as dt,json,math,urllib.parse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parent
RES=ROOT/"results"
def read(name):
    with (RES/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))
def pct(a,b):
    return 100*a/b if b else 0
def main():
    rows=read("oa_citation_locator_audit.csv")
    check=read("oa_reference_crosscheck.csv")
    domains=collections.defaultdict(lambda:{"attempted":0,"retrieved":0})
    reasons=collections.Counter()
    for row in rows:
        host=urllib.parse.urlsplit(row["oa_link"]).hostname or "(unknown)"
        host=host.removeprefix("www.")
        k="other"
        if any(s in host for s in ("tandfonline","sciencedirect","sagepub","emerald","wiley","mdpi","scup","intellectdiscovery")):
            k="major_publisher_endpoint"
        elif any(s in host for s in ("oslomet","diva-portal","dtu.dk","hioa.no","qip-journal","springeropen","frontiersin","openjournals","repository","cambridge","research","orbit")):
            k="repository_or_other_open_portal"
        else:k="mixed_or_other_endpoint"
        domains[k]["attempted"]+=1
        domains[k]["retrieved"]+=int(row["pdf_available"] or 0)
        reason=row["document_screening_notes"]
        if "403" in reason:reasons["HTTP 403"]+=1
        elif "not a direct PDF" in reason:reasons["HTML / non-PDF"]+=1
        elif "larger" in reason:reasons["over 14 MB"]+=1
        elif "denied" in reason:reasons["blocked redirect"]+=1
        elif row["pdf_available"]=="1":reasons["readable PDF"]+=1
        else:reasons["other"]+=1
    unique_pdf=len({row["paper_id"] for row in rows if row["pdf_available"]=="1"})
    tier=collections.Counter(row["validation_tier"] for row in check)
    totals={
        "created_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "sample_definition":"First 100 pairs from a fixed-seed purposive shortlist of the 200 top semantic candidate citations; available HTTPS OpenAlex links; two-sided OA candidates prioritized.",
        "sample_pairs":len(rows),
        "readable_pdf_pair_attempts":sum(int(row["pdf_available"]) for row in rows),
        "unique_citing_pdfs_downloaded":unique_pdf,
        "link_retrievability_in_this_audit_pct":pct(sum(int(row["pdf_available"]) for row in rows),len(rows)),
        "failed_or_nonpdf":sum(int(row["pdf_available"])==0 for row in rows),
        "reasons":dict(reasons),
        "validation_tiers":dict(tier),
        "url_classes":dict(domains),
        "nonrandom_sample":True,
        "fulltext_epistemic_labels_assigned_automatically":0,
        "limitation":"A 403, paywall, non-PDF or missing text layer is an access/extraction event, not evidence against scientific content; author/year matches are not verified semantic citation functions."
    }
    (RES/"oa_retrievability_quality.json").write_text(json.dumps(totals,indent=2,ensure_ascii=False),encoding="utf-8")
    hosts=sorted(domains)
    lab=[{"major_publisher_endpoint":"Større forlagsendepunkt","repository_or_other_open_portal":"Arkiv/opne portalar","mixed_or_other_endpoint":"Blanda/andre"}[x] for x in hosts]
    observed=[domains[x]["retrieved"] for x in hosts]
    missed=[domains[x]["attempted"]-domains[x]["retrieved"] for x in hosts]
    fig,ax=plt.subplots(figsize=(9,4.1))
    x=np.arange(len(hosts))
    ax.bar(x,observed,label="PDF henta")
    ax.bar(x,missed,bottom=observed,label="Ikkje henta")
    ax.set_xticks(x,lab,rotation=20,ha="right")
    ax.set_ylabel("Par i det ikkje-tilfeldige søkjeutvalet")
    ax.set_title("Open-access-lenkjer: retrieval er ikkje det same som tilgang")
    ax.legend()
    fig.tight_layout();fig.savefig(RES/"figures"/"19-pdf-tilgjenge.png",dpi=170,bbox_inches="tight");plt.close(fig)
    lines=[
       "# PDF-tilgang og tekstfunn — kontroll av OpenAlex-arbeidslista",
       "",
       f"Generert {totals['created_utc']}. Dette er eit **målretta utval**, ikkje tilfeldig utval av alle nordiske forskingsartiklar.",
       "",
       f"- {totals['sample_pairs']} siteringspar undersøkte.",
       f"- {totals['readable_pdf_pair_attempts']} par hadde ei lesbar PDF på den registrerte HTTPS-lenkja.",
       f"- {unique_pdf} unike siterande PDF-dokument vart henta; nokre dokument opptrer i fleire par.",
       f"- {totals['failed_or_nonpdf']} par gav tilkomstfeil, HTML, for store filer eller andre avvik.",
       "",
       "## Tilkomsttilstand",
       "",
       "| Tilstand | Par |",
       "|---|---:|",
       *[f"| {k} | {v} |" for k,v in reasons.most_common()],
       "",
       "![Lenkjer mot lesbare PDF-ar](figures/19-pdf-tilgjenge.png)",
       "",
       "## Finne ei konkret referanse",
       "",
       f"Automatisk andrepass fann {tier.get('bibliography-and-intext-candidate',0)} par med både bibliografisk og in-text *kandidat*,",
       f"{tier.get('bibliographic-entry-only',0)} med berre bibliografisk kandidat og",
       f"{tier.get('not-located',0)} utan kandidat.",
       "",
       "Verken namn–år-nærleik eller registrert DOI/tittel kan åleine vise **korleis ein",
       "sitering vert brukt**. Dette krev kontroll av referansen, sjølve avsnittet og",
       "originalarbeidet sitt argument. Bibliografisk tittel kan nemnast andre stader",
       "enn i referanselista. Ein kontekst kan vere kritikk, lån, metode, test eller",
       "replikasjon, og meir enn éin kategori kan vere relevant.",
       "",
       "## Viktige feilkjelder",
       "",
       "- OpenAlex sitt OA-felt peikar ofte på ein forlagslandingsside eller direkte lenkje",
       "  som gjev HTTP 403; ikkje omdefiner dette til betalt, lukka eller uvitskapleg.",
       "- Filsstorleik er avgrensa til 14 MB per dokument for kontrollen.",
       "- Ulike årsfelt er ikkje harmoniserte før indeksering; sjå AARSKJELDEKRITIKK.md.",
       "- Eitt etternamn kan peike til fleire studiar; forfattaren sin oppførte årgang",
       "  kan vise til online-first versus tidsskriftvolum. Bruk DOI/tittel som eksterne",
       "  kontrollar, og dokumenter kva som står i referanselista.",
       "- Automatiske treff er ikkje brukt som kodingsfasit for C2–C5 eller L4–L7.",
       "",
       "## Data og personvern",
       "Dei 14 nedlasta fulltekstdokumenta er lokale, under data/oa_fulltexts_private/",
       "på CYGNUS, og vert ikkje pusha til GitHub. Offentlege filer inneheld berre DOI,",
       "OA-lenkjer, hash-verdiar, kontrollstatus og PDF-sidetilvisingar.",
       "",
       "Analyser: oa_citation_locator_audit.csv, oa_reference_crosscheck.csv,",
       "oa_retrievability_quality.json. Ver obs på at PDF-hash identifiserer eit",
       "lokalt nedlasta dokument, ikkje nødvendigvis kanonisk utgåve.",
    ]
    (RES/"OA_TILGANG.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(totals,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
