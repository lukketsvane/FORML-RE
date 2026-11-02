#!/usr/bin/env python3
"""Generate a stratified probability sample from the *automatic title-included* frame only.

Inclusion probabilities apply only to that incomplete OpenAlex-derived frame,
NOT to all Nordic design research. No article is scored automatically.
"""
import collections
import datetime as dt
import json
import math
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from database import ensure_database

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
FIG=OUT/"figures"
SEED=20261102
N_TARGET=600
FIELDS=["H1","H2","H3","E1","E2","E3","C1","C2","C3","C4","C5"]

def allocate(counts,total,minimum=3):
    # Fixed allocation, floors + largest-remainder, and explicit population caps.
    n=counts.astype(int)
    g=np.zeros(len(n),dtype=int)
    if total>n.sum():raise ValueError("Target exceeds frame size")
    for j in range(len(n)):
        g[j]=min(minimum,n[j])
    remaining=total-g.sum()
    if remaining<0:raise ValueError("Too many strata for minimum allocation")
    spare=n-g
    while remaining>0:
        active=spare>0
        if not active.any():break
        raw=remaining*spare[active]/spare[active].sum()
        proposed=np.floor(raw).astype(int)
        proposed=np.minimum(proposed,spare[active])
        used=proposed.sum()
        ids=np.flatnonzero(active)
        g[ids]+=proposed;spare[ids]-=proposed
        remaining-=int(used)
        if remaining==0:break
        # Largest remaining fractional part, tie-break by stratum order.
        frac=raw-np.floor(raw)
        priority=ids[np.argsort(-frac,kind="stable")]
        for ix in priority:
            if remaining<=0:break
            if spare[ix]>0:
                g[ix]+=1;spare[ix]-=1;remaining-=1
    assert g.sum()==total and np.all(g<=n),("Bad allocation",g.sum(),total)
    return g

def main():
    ensure_database()
    OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
    conn=sqlite3.connect(ROOT/"data"/"nordic_design_research.sqlite")
    frame=pd.read_sql_query(
      "SELECT id,doi,title,year,source,oa_url,kind,language FROM works WHERE in_scope=1",conn)
    tags=pd.read_csv(OUT/"semantic_clusters.csv",dtype={"id":str})[["id","theme"]]
    frame=frame.merge(tags,on="id")
    assert frame.id.is_unique
    frame["period"]=(frame.year//5)*5
    frame["stratum"]=frame.theme.astype(str)+"|"+frame.period.astype(str)
    grouped=frame.groupby("stratum").size().sort_index()
    counts=grouped.to_numpy(dtype=int)
    draw=allocate(counts,N_TARGET,minimum=3)
    alloc=pd.DataFrame({"stratum":grouped.index,"frame_n":counts,"draw_n":draw})
    alloc["inclusion_probability"]=alloc.draw_n/alloc.frame_n
    alloc["design_weight"]=alloc.frame_n/alloc.draw_n
    alloc["theme"]=alloc.stratum.str.rsplit("|",n=1).str[0]
    alloc["period"]=alloc.stratum.str.rsplit("|",n=1).str[1]
    alloc.to_csv(OUT/"probability_sample_allocation.csv",index=False)
    rng=np.random.default_rng(SEED)
    records=[]
    for row in alloc.itertuples():
        sub=frame[frame.stratum==row.stratum]
        index=rng.choice(sub.index.to_numpy(),size=row.draw_n,replace=False)
        items=sub.loc[index].copy()
        items["stratum_frame_n"]=row.frame_n
        items["stratum_sample_n"]=row.draw_n
        items["inclusion_probability"]=row.inclusion_probability
        items["inverse_probability_weight"]=row.design_weight
        records.append(items)
    selected=pd.concat(records,ignore_index=True)
    selected=selected.sample(frac=1,random_state=SEED).reset_index(drop=True)
    selected["case_id"]=selected.index.map(lambda i:f"DS-{i+1:04d}")
    # Every variable is blank; prior automatic selection must never act as a method label.
    for f in FIELDS:selected["coder_A_"+f]="";selected["coder_B_"+f]=""
    for c in ["coder_A_eligibility","coder_B_eligibility",
              "coder_A_fulltext_read","coder_B_fulltext_read",
              "coder_A_evidence_pages","coder_B_evidence_pages",
              "coder_A_notes","coder_B_notes","adjudication","adjudication_reason"]:
        selected[c]=""
    columns=["case_id","id","doi","title","year","source","kind","language",
       "oa_url","theme","period","stratum","stratum_frame_n","stratum_sample_n",
       "inclusion_probability","inverse_probability_weight"]+[
        "coder_A_eligibility","coder_B_eligibility","coder_A_fulltext_read",
        "coder_B_fulltext_read"]+[
        x for f in FIELDS for x in ("coder_A_"+f,"coder_B_"+f)
    ]+["coder_A_evidence_pages","coder_B_evidence_pages",
       "coder_A_notes","coder_B_notes","adjudication","adjudication_reason"]
    assert len(selected)==N_TARGET and selected.id.is_unique
    selected[columns].to_csv(OUT/"probability_sample_600_double_coder.csv",index=False,encoding="utf-8")
    bin_=(pd.crosstab(frame.period,frame.theme).fillna(0).astype(int))
    chosen=(pd.crosstab(selected.period,selected.theme).fillna(0).astype(int))
    bin_.to_csv(OUT/"population_frame_by_stratum.csv")
    chosen.to_csv(OUT/"sample_by_stratum.csv")
    pd.DataFrame([
       {"stratum":r.stratum,"n":int(r.frame_n),"sample_n":int(r.draw_n),
        "inclusion_probability":float(r.inclusion_probability)}
       for r in alloc.itertuples()
    ]).to_csv(OUT/"design_weights.csv",index=False)
    fig,ax=plt.subplots(figsize=(10,5))
    agg=alloc.groupby("period").agg(frame=("frame_n","sum"),selected=("draw_n","sum")).reset_index()
    periods=agg.period.tolist()
    x=np.arange(len(periods))
    ax.bar(x-.2,agg.frame,width=.4,label="Automatisk inklusjonsramme")
    ax.bar(x+.2,agg.selected,width=.4,label="Stratifisert fulltekstutval")
    ax.set_xticks(x,periods)
    ax.set_title("Kva forskingsmateriale skal gjennomgåast i fulltekst?")
    ax.set_ylabel("Publikasjonar");ax.legend()
    fig.tight_layout()
    fig.savefig(FIG/"17-sannsynsutval-600.png",dpi=170,bbox_inches="tight")
    plt.close(fig)
    # Precision target is NOT a post-hoc guarantee: worst-case 95% CI +/-4.0pp
    # for simple random sampling n600 without design effect, nonresponse, exclusions.
    moe=1.96*math.sqrt(.25/N_TARGET)
    weights=selected.inverse_probability_weight.to_numpy(dtype=float)
    kish_effective_n=float(weights.sum()**2/(weights**2).sum())
    approximate_design_effect=float(N_TARGET/kish_effective_n)
    summary={
       "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
       "selection_seed":SEED,
       "target":N_TARGET,"automatic_title_screened_frame":len(frame),
       "strata":len(alloc),
       "min_inclusion_probability":float(alloc.inclusion_probability.min()),
       "max_inclusion_probability":float(alloc.inclusion_probability.max()),
       "max_design_weight":float(alloc.design_weight.max()),
       "min_design_weight":float(alloc.design_weight.min()),
       "ideal_SRS_worst_case_MOE_fraction_without_design_effect":moe,
       "kish_effective_sample_size_due_to_weight_dispersion":kish_effective_n,
       "weight_dispersion_approx_design_effect":approximate_design_effect,
       "coding_complete":0,
       "population_covered":"The retrieved title-screened OpenAlex records ONLY; not Nordic design science",
       "purpose":"Manual fulltext validation of claim and replication indicators with two blinded coders"
    }
    (OUT/"probability_sample_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=[
       "# Sannsynsutval og fulltekstprotokoll for kumulativitet",
       "",
       "Dette er ein tilfeldig, stratifisert **600-postars prøve av den automatisk inkluderte databaseramma**.",
       "Det er ikkje eit sannsynsutval av all nordisk designforsking og kan difor ikkje utan",
       "ytterlegare registrering og kontroll generaliserast til heile faget.",
       "",
       f"Trekkseed {SEED}; {len(alloc)} ikkje-tomme strata etter søkjetema og femårsbolk.",
       "Minimum tre testar per stratum når mogleg; resten fordelt etter rammevolum.",
       "Sannsynet for å verte trekt og inverse utvalsvekter er lagra per post.",
       "Søkjekategoriane er automatiske hjelpestrata og må ikkje forvekslast med valide fagdisiplinar.",
       "",
       "## Koding",
       "To uavhengige kodarar skal bruke CODEBOOK.md, og skal ikkje sjå kvarandre sine",
       "vurderingar før kodinga er avslutta. Alle C/H/E-felt er medvite blanke.",
       "Uleselege eller utilgjengelege fulltekstar skal kodast som manglande, ikkje 0.",
       "Slutning om replikasjon krev spesifikke metodar og konkrete dokumenterte",
       "sidetilvisingar. Cohen kappa og inter-rater-reliabilitet skal rapporterast",
       "for kvar indikator før eventuelle generaliseringar.",
       "",
       "## Presisjon",
       f"Eit tenkt enkelt tilfeldig utval n={N_TARGET} ville ved 50 % og 95 %",
       f"ha normaltilnærma feilmargin om lag +/-{100*moe:.1f} prosentpoeng.",
       "Den faktiske stratifiseringa, ulik vekting, ikkje-svar og skjermingsfeil",
       "gjev andre usikkerheiter. Berekn ikkje dette som den faktiske studien si feilmargin.",
       "",
       "![Stratifisert utval](figures/17-sannsynsutval-600.png)",
       "",
       "Sjå: probability_sample_600_double_coder.csv, probability_sample_allocation.csv,",
       "probability_sample_summary.json og CODEBOOK.md i overordna mappe.",
       "",
       "Ingen fulltekstar er koda. Det er ikkje laga fabrikkerte funn."
    ]
    (OUT/"UTVALSPLAN.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    conn.close()
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
