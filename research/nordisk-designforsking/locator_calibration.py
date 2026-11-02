#!/usr/bin/env python3
"""Small positive-set audit of in-body locator recall (non-probability sample).

Only explicitly located, human-inspected citation contexts are marked as
positives. Unconfirmed citations are UNKNOWN, not negative evidence.
"""
from __future__ import annotations
import csv,datetime as dt,json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
# These page markers come from read citation contexts in locally available PDFs.
POSITIVE={
 ("W2908349601","W2750861048"):"2",
 ("W4416250669","W4405439335"):"2",
 ("W1877690414","W1968718690"):"3",
 ("W2919057183","W1872643186"):"2;3",
 ("W7155508854","W3205778302"):"3;11",
 ("W4389099516","W3035254258"):"1;2;11",
 ("W4322492190","W1830093444"):"2",
 ("W2899361681","W2159255554"):"4",
 ("W2982281212","W2528473844"):"3;4",
 ("W2098856852","W2141989798"):"1;12",
 ("W2995635751","W2971882061"):"7",
 ("W4311715142","W2076426378"):"2;3;4",
 ("W4307994144","W2076426378"):"17",
 ("W4283392104","W1492164359"):"3",
 # Table 1 of this 2017 synthesis includes Deckers et al. 2012 on
 # perceptual crossing (rather than a narrative sentence).
 ("W2774875954","W2102042280"):"11",
}
UNKNOWN={
 ("W7155508854","W4306369153"),
 ("W3191732044","W2047927201")
}
def main():
    with (OUT/"oa_reference_crosscheck.csv").open(encoding="utf-8",newline="") as f:
        candidates=list(csv.DictReader(f))
    keys={(x["citing_work_id"],x["cited_work_id"]):x for x in candidates}
    records=[]
    for pair,pages in POSITIVE.items():
        if pair not in keys:raise AssertionError(pair)
        r=keys[pair]
        detection=int(r["validation_tier"]=="bibliography-and-intext-candidate")
        records.append({"citing_id":pair[0],"cited_id":pair[1],
            "human_inspected_body_page_numbers":pages,
            "review_status":"positive_context_located_single_reader",
            "algorithm_detected_candidate":detection,
            "algorithm_tier":r["validation_tier"],
            "not_an_epistemic_quality_label":True})
    for pair in UNKNOWN:
        if pair not in keys:raise AssertionError(pair)
        r=keys[pair]
        records.append({"citing_id":pair[0],"cited_id":pair[1],
            "human_inspected_body_page_numbers":"",
            "review_status":"not_verified_insufficient_context",
            "algorithm_detected_candidate":int(r["validation_tier"]=="bibliography-and-intext-candidate"),
            "algorithm_tier":r["validation_tier"],
            "not_an_epistemic_quality_label":True})
    fields=list(records[0].keys())
    with (OUT/"citation_locator_positive_calibration.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
    found=sum(x["algorithm_detected_candidate"] for x in records if x["review_status"].startswith("positive"))
    report={
      "created_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "verified_positive_contexts_from_purposive_sample":len(POSITIVE),
      "positive_contexts_also_detected_by_strict_auto_heuristic":found,
      "observed_detection_fraction_among_positive_contexts":found/len(POSITIVE),
      "unverified_or_ambiguous_cases_not_treated_as_negatives":len(UNKNOWN),
      "validation_scope":"Manual sighting of cited author/context in citing PDF, not testing that source's hypothesis or validating cited fulltext.",
      "important_limit":"15 preselected positive contexts from a purposive sample are not a population sensitivity or specificity estimate; the rule can have both false negatives and false positives."
    }
    (OUT/"citation_locator_calibration_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    fig,ax=plt.subplots(figsize=(7.5,4))
    ax.bar(["Automatisk funne","Oversett av regelen"],[found,len(POSITIVE)-found])
    ax.set_ylabel("Tekststader i førebels positivt kontrollutval")
    ax.set_title("Kalibrering av heuristisk sitatlokalisering")
    fig.tight_layout()
    fig.savefig(OUT/"figures"/"20-lokaliseringskalibrering.png",dpi=170,bbox_inches="tight")
    plt.close(fig)
    doc=[
      "# Kontroll av automatisk sitatlokalisering mot konkrete tekststader",
      "",
      f"På {len(POSITIVE)} siteringspar der ein lesar lokaliserte relevant",
      f"tekststad, gav den strengare automatiske regelen treff for {found}.",
      f"Det er {100*found/len(POSITIVE):.1f} % *innanfor denne positive, målretta testmengda*,",
      "ikkje eit generaliserbart anslag på sensitivitet.",
      "",
      "To andre par har utilstrekkeleg dokumentert sitatsamanheng og er merkte",
      "som uavklara, ikkje som negative kontrollar.",
      "",
      "Eit særleg viktig døme er Cash & Kreye (2017) si samanstilling av",
      "«perceptual crossing» frå Deckers mfl. (2012) i ein tabell.",
      "Regelen fann ikkje denne som ei vanleg author–year-setning, men",
      "kjelda er relevant for syntesen av teoriar om designaktivitet.",
      "Å leite berre etter fortløpande setningar ville difor oversjå",
      "ein faktisk bibliografisk og konseptuell samanheng.",
      "",
      "Fulltekstkontroll kan òg avdekkje falske positive søkjemønster.",
      "Algoritmen skal difor aldri tildele L3–L7 utan at den faglege",
      "relasjonen vert dokumentert og kontrollert av uavhengige kodarar.",
      "",
      "Data: citation_locator_positive_calibration.csv.",
    ]
    (OUT/"LOKALISERING_VALIDERING.md").write_text("\n".join(doc)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
