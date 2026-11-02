#!/usr/bin/env python3
"""Analyse independent binary coding once actual manual reading has been performed.

NO auto-classification, no simulated labels, no rates for uncoded records.
All estimates apply only to the automatically included OpenAlex frame.
"""
from __future__ import annotations
import argparse,datetime as dt,json,math
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
DEFAULT=HERE/"results"/"probability_sample_600_double_coder.csv"
CODES=["H1","H2","H3","E1","E2","E3","C1","C2","C3","C4","C5"]

def kappa(a,b):
    """Cohen's kappa for two nonmissing binary vectors."""
    a=np.asarray(a,dtype=int);b=np.asarray(b,dtype=int)
    if len(a)==0:return None
    assert set(np.unique(a)).issubset({0,1}) and set(np.unique(b)).issubset({0,1})
    po=float(np.mean(a==b))
    pa=float(np.mean(a));pb=float(np.mean(b))
    pe=pa*pb+(1-pa)*(1-pb)
    return 1.0 if po==1 and pe==1 else ((po-pe)/(1-pe) if pe<1 else None)

def estimate(data,code,min_n=30):
    a=pd.to_numeric(data["coder_A_"+code],errors="coerce")
    b=pd.to_numeric(data["coder_B_"+code],errors="coerce")
    mask=a.isin([0,1])&b.isin([0,1])
    nd=int(mask.sum())
    result={"code":code,"double_coded":nd,"sample_size":len(data),
            "double_coded_share_of_selected":nd/len(data) if len(data) else None,
            "can_interpret":nd>=min_n,"kappa":None,"agreement":None,
            "coder_A_rate_over_double_coded":None,"coder_B_rate_over_double_coded":None,
            "coded_subset_inverse_probability_weighted_rate_A":None,
            "coded_subset_inverse_probability_weighted_rate_B":None}
    if nd<min_n:return result
    av=a[mask].to_numpy(dtype=int);bv=b[mask].to_numpy(dtype=int)
    result["kappa"]=kappa(av,bv)
    result["agreement"]=float((av==bv).mean())
    result["coder_A_rate_over_double_coded"]=float(av.mean())
    result["coder_B_rate_over_double_coded"]=float(bv.mean())
    w=data.loc[mask,"inverse_probability_weight"].to_numpy(dtype=float)
    result["coded_subset_inverse_probability_weighted_rate_A"]=float(np.average(av,weights=w))
    result["coded_subset_inverse_probability_weighted_rate_B"]=float(np.average(bv,weights=w))
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=DEFAULT)
    p.add_argument("--min-doublecoded",type=int,default=30)
    p.add_argument("--out",type=Path,default=HERE/"results"/"CODING_PROGRESS.md")
    args=p.parse_args()
    df=pd.read_csv(args.input,dtype={"id":"str"})
    required={"id","inverse_probability_weight"}
    required.update("coder_"+r+"_"+x for x in CODES for r in "AB")
    missing=required-set(df.columns)
    if missing:raise SystemExit("Invalid code sheet; missing "+str(sorted(missing)))
    if not df.id.is_unique:raise SystemExit("Duplicate work IDs")
    if not np.all(df.inverse_probability_weight>0):raise SystemExit("Invalid nonpositive weights")
    output={"created":dt.datetime.now(dt.timezone.utc).isoformat(),
       "sample_n":len(df),"minimum_doublecoded_per_indicator":args.min_doublecoded,
       "indicators":[estimate(df,k,args.min_doublecoded) for k in CODES],
       "validation":"Only data from the CSV. Missing entries stay missing; no labels inferred.",
       "inference":"Descriptive coding diagnostics. Weighted rates on the coded subset are NOT population estimates without missing-response assumptions."}
    table=[
      "# Uavhengig fulltekstkoding — framdrift og reliabilitet",
      "",
      "Dette er ein prosedyre for å kontrollere *faktiske* kodarvurderingar.",
      "Tomt kodingsskjema genererer ingen oppdikta funn.",
      "",
      "| Indikator | Dobbelkoda | Kappa | Usemje / merknad |",
      "|---|---:|---:|---|"
    ]
    for v in output["indicators"]:
        kapp="ikkje berekna" if v["kappa"] is None else f"{v['kappa']:.3f}"
        note="Minst 30 fullførte vurderingar krevst" if not v["can_interpret"] else "Ikkje lik ein kumulativitetsskår"
        table.append(f"| {v['code']} | {v['double_coded']} | {kapp} | {note} |")
    table.extend([
      "",
      "Utan fagleg validert kodebok, fulltekstar og uavhengig koding er det",
      "ikkje grunnlag for frekvensar av replikasjon eller for generalisering.",
      "",
      "Etter fullført koding må ein kontrollere bortfall per stratum, vekting,",
      "mogeleg skeivskap og faktisk sidetilvising før faglege slutningar.",
    ])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text("\n".join(table)+"\n",encoding="utf-8")
    (args.out.parent/"coding_progress.json").write_text(
       json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"sample_n":len(df),
      "completed_doublecoded_by_indicator":{x["code"]:x["double_coded"] for x in output["indicators"]},
      "claims_inferred_from_blank":0},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
