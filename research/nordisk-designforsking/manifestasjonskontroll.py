#!/usr/bin/env python3
"""Find possible different manifestations of one work in a bibliometric corpus.

Candidate grouping requires *same normalized title* and the same OpenAlex
first-author identity. This produces review candidates, NOT automatic merges.
"""
from __future__ import annotations
import collections,csv,datetime as dt,json,re,sqlite3,unicodedata
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
DB=ROOT/"data"/"nordic_design_research.sqlite"
OUT=ROOT/"results"
def titlekey(s):
    x=unicodedata.normalize("NFKD",s or "").casefold()
    x="".join(ch for ch in x if not unicodedata.combining(ch))
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9]+"," ",x)).strip()
def first_author(j):
    try: data=json.loads(j)
    except Exception:return ("","")
    authors=data.get("authorships") or []
    a=(authors[0].get("author") or {}) if authors else {}
    return ((a.get("id") or "").rsplit("/",1)[-1],a.get("display_name") or "")
def main():
    OUT.mkdir(exist_ok=True)
    c=sqlite3.connect(DB)
    raw=c.execute("SELECT id,doi,title,year,kind,source,raw_json,in_scope FROM works").fetchall()
    works=[]
    for row in raw:
        au,name=first_author(row[6])
        works.append({"id":row[0],"doi":row[1] or "","title":row[2],"year":int(row[3]),
          "kind":row[4],"source":row[5],"author_id":au,"first_author":name,
          "in_scope":row[7],"title_key":titlekey(row[2])})
    grouped=collections.defaultdict(list)
    for w in works:
        if len(w["title_key"])>=22 and w["author_id"]:
            grouped[(w["title_key"],w["author_id"])].append(w)
    cand=[v for v in grouped.values() if len(v)>1]
    # Unambiguous within OpenAlex-ID match is guaranteed by DB primary key; nothing else assumed.
    pairs=[]
    for g in cand:
        for i in range(len(g)):
            for j in range(i+1,len(g)):
                a,b=g[i],g[j]
                pairs.append({
                    "work_id_a":a["id"],"work_id_b":b["id"],
                    "first_author_name":a["first_author"],
                    "normalized_title":a["title_key"],
                    "year_a":a["year"],"year_b":b["year"],
                    "year_gap":abs(a["year"]-b["year"]),
                    "type_a":a["kind"],"type_b":b["kind"],
                    "doi_a":a["doi"],"doi_b":b["doi"],
                    "same_doi":int(bool(a["doi"]) and a["doi"]==b["doi"]),
                    "different_doi":int(bool(a["doi"] and b["doi"]) and a["doi"]!=b["doi"]),
                    "both_included":int(a["in_scope"]==1 and b["in_scope"]==1),
                    "manual_same_underlying_study": "",
                    "manual_status":"unreviewed",
                    "manual_notes":""})
    fields=(list(pairs[0].keys()) if pairs else [
        "work_id_a","work_id_b","first_author_name","normalized_title",
        "year_a","year_b","year_gap","type_a","type_b",
        "doi_a","doi_b","same_doi","different_doi","both_included",
        "manual_same_underlying_study","manual_status","manual_notes"])
    with (OUT/"candidate_same_title_same_author_manifestations.csv").open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(pairs)
    # Report the actual known case separately, without silently merging the graph.
    au="W1595005902"; bu="W2971882061"
    a=next((w for w in works if w["id"]==au),None)
    b=next((w for w in works if w["id"]==bu),None)
    known={"work_A":a,"work_B":b,
       "sources":[
         "https://researchportal.helsinki.fi/fi/publications/towards-primary-school-physics-teaching-and-learning-design-resea-2/",
         "https://doi.org/10.5617/nordina.456",
         "https://files.eric.ed.gov/fulltext/ED489993.pdf",
       ],
       "interpretation":"2005 University of Helsinki doctoral thesis, subsequently represented in a 2012 journal record under the same title; journal record is not independent evidence of a replicated experiment. This is a manual bibliographic caution, not a globally validated equivalence rule."}
    (OUT/"juuti_2005_2012_manifestation.json").write_text(json.dumps(known,indent=2,ensure_ascii=False),encoding="utf-8")
    incident=c.execute("""SELECT citing_id,cited_id FROM references_all
        WHERE cited_id IN (?,?) AND citing_id IN (SELECT id FROM works WHERE in_scope=1)""",(au,bu)).fetchall()
    from_works=collections.defaultdict(set)
    for citing,cited in incident:from_works[citing].add(cited)
    overlap=[citing for citing,group in from_works.items() if len(group)>1]
    report={
      "timestamp_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "database_work_records":len(works),
      "candidate_title_author_groups":len(cand),
      "candidate_pairs":len(pairs),
      "crossyear_pairs":sum(x["year_gap"]>0 for x in pairs),
      "different_doi_pairs":sum(x["different_doi"] for x in pairs),
      "same_doi_pairs":sum(x["same_doi"] for x in pairs),
      "both_autoincluded_pairs":sum(x["both_included"] for x in pairs),
      "case_example":"Juuti thesis 2005 and journal manifestation 2012",
      "case_citing_papers_for_either":len(from_works),
      "case_citing_papers_with_both_ids_as_references":len(overlap),
      "case_overlapping_citing_ids":overlap,
      "important_caveat":"Title+author matches can be genuine revised editions, separate chapters, corrections or versions. No automatic merge, deletion, citation discounting or inference of replicability."
    }
    (OUT/"manifestation_audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    gaps=collections.Counter("Same år" if x["year_gap"]==0 else "1–4 år" if x["year_gap"]<=4 else "5–9 år" if x["year_gap"]<=9 else "10+ år" for x in pairs)
    labels=["Same år","1–4 år","5–9 år","10+ år"]
    fig,ax=plt.subplots(figsize=(7.5,4))
    ax.bar(labels,[gaps.get(l,0) for l in labels])
    ax.set_ylabel("Moglege publikasjonpar, ikkje stadfesta duplikat")
    ax.set_title("Sams tittel og fyrsteforfattar på tvers av år")
    fig.tight_layout()
    fig.savefig(OUT/"figures"/"21-manifestasjonar-aarsskilje.png",dpi=170,bbox_inches="tight")
    plt.close(fig)
    lines=[
      "# Korpus- og manifestasjonskontroll: same verk, fleire publikasjonspostar",
      "",
      f"Kontrollert {len(works)} unike OpenAlex-postar. Automatisk kandidatsøk gav",
      f"**{len(cand)}** tittel+forfattar-grupper med minst to rekordar,",
      f"**{len(pairs)}** kandidatpar, og **{sum(x['year_gap']>0 for x in pairs)}**",
      "kandidatpar med ulike publikasjonsår.",
      "",
      "**Dette er berre metadata-kandidatar.** Lik tittel og fyrsteforfattar er",
      "ikkje prov for at to publikasjonar er same underliggjande studie.",
      "",
      "## Dokumentert døme: Juuti",
      "",
      "Kalle Juuti gav ut doktoravhandlinga *Towards Primary School Physics",
      "Teaching and Learning: Design Research Approach* ved Helsinki-universitetet",
      "i 2005. Den same tittelen finst i *Nordic Studies in Science Education*",
      "registrert under DOI 10.5617/nordina.456 med eit seinare publikasjonsår.",
      "Eit tidlegare forskingsresultat kan difor få fleire bibliografiske former.",
      "Det ville vere metodisk feil å telje seinare gjengjevinga som ei",
      "uavhengig replikasjon berre fordi ho har ein eigen register-ID.",
      "",
      f"I dette avgrensa siteringsutvalet viser {len(from_works)} inkluderte",
      f"publikasjonar til minst éin av dei to rekordane. {len(overlap)}",
      "siterande publikasjonar viser til begge ID-ane. Ingen rågraf er",
      "automatisk omarbeidd som resultat av denne observasjonen.",
      "",
      "Kjelder:",
      "- [Universitetet i Helsinki, originalavhandling 2005](https://researchportal.helsinki.fi/fi/publications/towards-primary-school-physics-teaching-and-learning-design-resea-2/)",
      "- [Seinare DOI-register 10.5617/nordina.456](https://doi.org/10.5617/nordina.456)",
      "- [Avhandlings-PDF i ERIC](https://files.eric.ed.gov/fulltext/ED489993.pdf)",
      "",
      "## Vitskapleg metode",
      "Alle kandidatpar ligg i candidate_same_title_same_author_manifestations.csv.",
      "Den manuelle kodekolonnen er blank, slik at ikkje ordlikskap vert",
      "omgjord til oppdikta journal-versjonar eller replikasjonar.",
      "Dette treng separat dokumentkontroll av referansen sitt ISBN, DOI,",
      "utgjevingstype, tekstlikskap, forfattarskap og tidspunkt.",
    ]
    (OUT/"MANIFESTASJONAR.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    c.close()
if __name__=="__main__":main()
