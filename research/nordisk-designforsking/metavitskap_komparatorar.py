#!/usr/bin/env python3
"""Source-grounded comparator register; never pool heterogeneous sample counts."""
from __future__ import annotations
import csv,datetime as dt,json,sqlite3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
REFS=[
 {"id":"cash2023","year":2023,"doi":"10.1016/j.destud.2023.101204",
  "title":"Evaluating the efficacy and effectiveness of design methods: A systematic review and assessment framework",
  "scope":"Design methods papers in six selected journals, 2020","method":"systematic review","screened_n":348,"included_n":18,
  "outcome":"No included individual paper consistently documented all five evidence-chain links.",
  "interpretation":"Critique of documented method evidence, not of all design fields.",
  "relevance":"Use five independent M1-M5 coding dimensions.",
  "url":"https://www.sciencedirect.com/science/article/pii/S0142694X23000455"},
 {"id":"alaie2025","year":2025,"doi":"10.1017/dsj.2025.10027",
  "title":"Evaluation of the relationship between studies of design research and design process in the field of architecture: a systematic review",
  "scope":"Architectural and related design-research studies, peer-reviewed","method":"systematic review; PRISMA/CASP","screened_n":94,"included_n":70,
  "outcome":"Four research-orientation clusters and five research-actor modes in selected studies.",
  "interpretation":"Typology of inquiry, not measurement of replication frequency.",
  "relevance":"Code time of inquiry (pre/during/post) and actor configuration.",
  "url":"https://www.cambridge.org/core/journals/design-science/article/evaluation-of-the-relationship-between-studies-of-design-research-and-design-process-in-the-field-of-architecture-a-systematic-review/D77AABAC5F42C734AADEFF78FB941184"},
 {"id":"bonnin2026","year":2026,"doi":"10.1177/19375867261454386",
  "title":"A Critical Assessment of Evidence-Based Design's Knowledge Base and Inspiration: A Systematic Review",
  "scope":"Philosophy of evidence-based design and its analogy with evidence-based medicine","method":"systematic review","screened_n":None,"included_n":31,
  "outcome":"Questions the general transfer of medicine's hierarchical best-evidence model to heterogeneous design inquiries.",
  "interpretation":"Argues for epistemic pluralism rather than rejecting empirical evidence.",
  "relevance":"Do not score an exploratory concept study as failed experiment.",
  "url":"https://pubmed.ncbi.nlm.nih.gov/42429553/"},
 {"id":"brendel2021","year":2021,"doi":"10.1177/02683962211006429",
  "title":"Toward replication study types for design science research",
  "scope":"Design science research in information systems","method":"conceptual replication taxonomy","screened_n":None,"included_n":None,
  "outcome":"Proposes eight forms of replication and distinguishes utility-oriented design claims.",
  "interpretation":"Domain-specific conceptual framework, not a counted replication dataset.",
  "relevance":"Code replicate artifact utility separately from claims about truth.",
  "url":"https://journals.sagepub.com/doi/10.1177/02683962211006429"},
 {"id":"rode2024","year":2024,"doi":"10.1017/pds.2024.14",
  "title":"Replication studies in engineering design – a feasibility study",
  "scope":"Engineering design case replication of a previous design-behaviour study","method":"empirical replication feasibility study","screened_n":None,"included_n":None,
  "outcome":"Demonstrates practical adaptation and uncertainty in attempts to replicate design-research measures.",
  "interpretation":"One replication case, not a fieldwide rate.",
  "relevance":"Separate within-study significance from between-study effect differences.",
  "url":"https://www.cambridge.org/core/journals/proceedings-of-the-design-society/article/replication-studies-in-engineering-design-a-feasibility-study/F3A32DC9C940254CAFE6529A7C7C80A1"},
 {"id":"pedgley2025","year":2025,"doi":"10.1177/30497671251392169",
  "title":"Considerations for planning, conducting, and disseminating research through design (RTD)",
  "scope":"Research through design as scholarly inquiry","method":"methodological position paper","screened_n":None,"included_n":None,
  "outcome":"Distinguishes RTD as an approach to inquiry rather than one fixed research method.",
  "interpretation":"Methodological guidance, not an evidence synthesis with a denominator.",
  "relevance":"Separate design acts, documentation and claims about scholarly contribution.",
  "url":"https://journals.sagepub.com/doi/10.1177/30497671251392169"},
 {"id":"hoffmann2025","year":2025,"doi":"10.1177/25152459251328273",
  "title":"The Design of Current Replication Studies: A Systematic Literature Review on the Variation of Study Characteristics",
  "scope":"Replications in social and cognitive psychology, 2017–2022","method":"systematic review of replication designs","screened_n":1312,"included_n":134,
  "analytic_sample_n":60,"outcome":"Replications often keep treatments and outcome definitions but vary or underreport population, time and setting.",
  "interpretation":"External comparator on replication reporting, not directly comparable design research prevalence.",
  "relevance":"Code treatment, outcome, analysis, recruitment, time, location, population and setting.",
  "url":"https://journals.sagepub.com/doi/10.1177/25152459251328273"},
 {"id":"hou2024","year":2024,"doi":None,
  "title":"Two decades of design research on lessons-learned systems: a systematic review and future research agenda",
  "scope":"Information systems design of lessons-learned systems","method":"systematic literature review","screened_n":None,"included_n":None,
  "outcome":"Synthesizes design features and identifies projectability and knowledge-transfer gaps.",
  "interpretation":"Domain-specific information-systems design; no verified scope N used here.",
  "relevance":"Code whether a published method transfers to another setting.",
  "url":"https://scholar.dsu.edu/bispapers/419/"}
]
def main():
    OUT.mkdir(exist_ok=True)
    c=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    data=[]
    for ref in REFS:
        x=dict(ref)
        x["found_in_auto_title_screened_nordic_corpus"]=None
        if ref["doi"]:
            doi="https://doi.org/"+ref["doi"].lower().strip()
            rows=c.execute("SELECT id,in_scope,year FROM works WHERE lower(doi)=?",(doi,)).fetchall()
            x["found_in_nordic_openalex_candidate_corpus"]=len(rows)>0
            x["found_in_auto_title_screened_nordic_corpus"]=any(v[1]==1 for v in rows)
            x["matching_openalex_ids"]=[v[0] for v in rows]
        else:
            x["found_in_nordic_openalex_candidate_corpus"]=None
            x["matching_openalex_ids"]=[]
        data.append(x)
    out={"date_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "population":"External methodological checks, not observations added to the 7,300 Nordic works",
      "pooling_forbidden":"Sample counts concern different populations; never add them or estimate a combined proportion.",
      "sources":data}
    (OUT/"external_methodological_benchmarks.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    cols=["id","year","doi","method","scope","included_n","analytic_sample_n",
          "relevance","found_in_nordic_openalex_candidate_corpus","found_in_auto_title_screened_nordic_corpus","url"]
    with (OUT/"external_methodological_benchmarks.csv").open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=cols);wr.writeheader();wr.writerows([{k:x.get(k) for k in cols} for x in data])
    lines=[
      "# Eksterne vitskapsteoretiske kontrollstudiar, 2021–2026",
      "",
      "Kvar rad er kjeldekontrollert, men datagjennomgangen er **ikkje** ein ny systematisk review.",
      "Tala gjeld ulike populasjonar og kan **ikkje** summerast eller direkte samanliknast",
      "som prevalensestimat for kvalitet eller kumulativitet.",
      "",
      "| Studie | Fagleg omfang | Undersøkt i sluttrunde | Kva analysen faktisk kan brukast til |",
      "|---|---|---:|---|"
    ]
    for x in data:
        n=str(x["included_n"]) if x["included_n"] is not None else "—"
        lines.append(f"| [{x['id']}]({x['url']}) | {x['scope']} | {n} | {x['relevance']} |")
    lines.extend([
      "",
      "## Prinsipp for vidare analyse",
      "",
      "1. **Ikkje flytt metodekriterium mellom sjangrar.** Eit arbeid gjennom design er ikkje",
      "   mangelfullt berre fordi det ikkje er eit randomisert eksperiment.",
      "2. **Test konkrete påstandar.** Målelikskap, data, samanlikning, replikerbarheit",
      "   og konseptuell overføring skal registrerast som ulike dimensjonar.",
      "3. **Rett komparatormåling.** Ei ekstern 2025-oversikt over psykologisk",
      "   replikasjonspraksis er informativ for rapporteringskvalitet, men korkje",
      "   same designpopulasjon eller same forskingstype.",
      "4. **Kan teorien feile?** Hovudhypotesen om låg kumulativitet må kunne",
      "   utfordrast av funn om replikasjon, prediktiv vidareprøving og kontrollerte",
      "   metodeoverføringar.",
      "",
      "## Forankring i kodeboka",
      "",
      "M1–M5: evidenskjeda frå Cash mfl. (2023).",
      "Tidsplassering og forskarrolle: Alaie mfl. (2025).",
      "Evidenspluralisme og metodepassande kriterium: Bonnin (2026).",
      "Replikasjon som nytte, kontekst og effekt: Brendel mfl. (2021), Rode mfl. (2024),",
      "Hoffmann mfl. (2025).",
      "Kunnskap gjennom skaping: Pedgley (2025).",
      "",
      "Det kjem fram av CSV-en kva av desse eksterne DOI-ane som også er indekserte",
      "i den nordiske databasen; det er ein dedupliseringskontroll, ikkje ei",
      "automatisk utviding av nordisk populasjon.",
    ])
    (OUT/"KOMPARATORAR_2026.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"sources":len(data),"nordic_indexed":sum(x["found_in_nordic_openalex_candidate_corpus"] is True for x in data),
                      "within_auto_screened":sum(x["found_in_auto_title_screened_nordic_corpus"] is True for x in data)},
                     indent=2))
    c.close()
if __name__=="__main__":main()
