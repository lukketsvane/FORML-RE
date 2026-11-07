#!/usr/bin/env python3
"""FORMLÆRE / FORSØK 01: frys panelfordeling og bygg val-CSV frå RÅ svar.

Køyr:
  python forsok01_samle.py roster formlaere-kandidatar.json --out panel.csv --panels 12
  python forsok01_samle.py compile formlaere-kandidatar.json panel.csv svar/ --out choices.csv

Svar kjem frå forsok01.html med to uavhengige vurderarar og eitt
avgjerdspanel per panelkode. Ingen syntetiske val vert genererte her.
Ingenting vert skrive utan at --out er oppgjeve. Råfiler vert aldri endra.

VIKTIG: Mu=0,25 i dette pilotmanifestet er presentasjonsdesign, IKKJE ein
uavhengig estimert genereringsprior for den naturlege formgrammatikken.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import random

SEED = 20261107
ROLES = ("agent1", "agent2", "decision")
SPLITS = ("train", "validation", "test")
OUTPUT = ("case_id", "group_id", "split", "option_id", "chosen",
          "feasible", "mu", "e1", "e2", "w1", "w2")


def read_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def manifest_check(m):
    if m.get("schema_version") != "formlaere-pilot-manifest-v1":
        raise ValueError("Feil manifestversjon")
    h = m.get("manifest_sha256", "")
    if len(h) != 64 or not all(c in "0123456789abcdef" for c in h):
        raise ValueError("Manifest manglar gyldig sha256")
    sets = m.get("sets")
    if not isinstance(sets, list) or len(sets) < 5:
        raise ValueError("Må ha minst fem valsett")
    ids = set()
    for case in sets:
        cid = case["case_id"]
        if cid in ids:
            raise ValueError("Dupliserte valsett")
        ids.add(cid)
        options = case["options"]
        if len(options) != 4 or len({x["option_id"] for x in options}) != 4:
            raise ValueError("Kvar prøve må ha fire ulike alternativ")
        if any("chosen" in x or "e1" in x or "e2" in x for x in options):
            raise ValueError("Utfall vart ulovleg lagt inn i generatoren")
        if any(x.get("hard_rule_flags") or float(x.get("mu", -1)) <= 0
               for x in options):
            raise ValueError("Kandidat med hardt brot eller ikkje-positiv mu")
        if abs(sum(float(x["mu"]) for x in options)-1.0) > 1e-8:
            raise ValueError("Presentasjonsprior summerer ikkje til 1")
        w = case["weights"]
        if not all(0 <= float(w[a]) <= 1 for a in ("agent1", "agent2")):
            raise ValueError("Ugyldige vekter")
        if abs(float(w["agent1"])+float(w["agent2"])-1.0) > 1e-8:
            raise ValueError("Vektene summerer ikkje til éin")
    return h


def new_roster(m, panels=12):
    manifest_check(m)
    if panels < 3 or panels % 3:
        raise ValueError("Tal panel må vere positivt multiplum av tre")
    rng = random.Random(SEED)
    splits = list(SPLITS) * (panels // 3)
    rng.shuffle(splits)
    rows = []
    for index in range(panels):
        token = hashlib.sha256((m["manifest_sha256"] + "/" +
                                str(index+1)).encode()).hexdigest()[:6]
        rows.append({
            "panel_id": "P" + str(index + 1).zfill(2) + "-" + token,
            "split": splits[index],
            "manifest_sha256": m["manifest_sha256"],
        })
    return rows


def roster_check(m, path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) < 3:
        raise ValueError("For få panel")
    ids = set()
    for item in rows:
        if item.get("manifest_sha256") != m["manifest_sha256"]:
            raise ValueError("Panelroster har feil manifest")
        if item["split"] not in SPLITS or item["panel_id"] in ids:
            raise ValueError("Rosteren har ugyldig split/duplikat")
        ids.add(item["panel_id"])
    return rows


def timestamp(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("Tidsstempel må ha tidssone")
    return d


def responses_check(m, files, roster):
    valid_panels = {r["panel_id"] for r in roster}
    collected = defaultdict(dict)
    for file in sorted(Path(files).glob("*.json")):
        response = read_json(file)
        if response.get("schema_version") != "formlaere-pilot-response-v1":
            raise ValueError("Ukjend svarfil " + str(file))
        if response.get("study_id") != m["study_id"]:
            raise ValueError("Svarfil frå feil studie " + str(file))
        if response.get("manifest_sha256") != m["manifest_sha256"]:
            raise ValueError("Svarfil med feil manifest " + str(file))
        panel = response.get("panel_id")
        role = response.get("role")
        actor = response.get("actor_id")
        if panel not in valid_panels or role not in ROLES:
            raise ValueError("Svarfil har ukjent panel/rolle " + str(file))
        if not actor or not isinstance(actor, str) or len(actor) > 48:
            raise ValueError("Manglande/ugyldig aktørkode " + str(file))
        if role in collected[panel]:
            raise ValueError("Fleire filer frå same rolle i same panel")
        responses = response.get("answers")
        if not isinstance(responses, list) or len(responses) != len(m["sets"]):
            raise ValueError("Ufullstendig svarfil " + str(file))
        answer_by_id = {}
        for a in responses:
            cid = a.get("case_id")
            if cid in answer_by_id:
                raise ValueError("Duplikat-svar")
            timestamp(a.get("recorded_at",""))
            answer_by_id[cid] = a
        if set(answer_by_id) != {s["case_id"] for s in m["sets"]}:
            raise ValueError("Manglande eller framande valsett")
        collected[panel][role] = {**response, "by_case": answer_by_id}
    return collected


def compile_data(m, roster, data_dir):
    manifest_check(m)
    collected = responses_check(m, data_dir, roster)
    output = []
    used_actors = {}
    for entry in roster:
        panel = entry["panel_id"]
        if set(collected.get(panel,{})) != set(ROLES):
            raise ValueError("Mangler dei tre sjølvstendige rollene i panel " + panel)
        group = collected[panel]
        actors = [group[role]["actor_id"] for role in ROLES]
        if len(set(actors)) != 3:
            raise ValueError("Tre ulike aktørar krevst i " + panel)
        for actor in actors:
            if actor in used_actors and used_actors[actor] != panel:
                raise ValueError("Aktør deltek i fleire train/test-panel: " + actor)
            used_actors[actor] = panel
        for case in m["sets"]:
            cid = case["case_id"]
            a = group["agent1"]["by_case"][cid]
            b = group["agent2"]["by_case"][cid]
            d = group["decision"]["by_case"][cid]
            if not (timestamp(a["recorded_at"]) < timestamp(d["recorded_at"])
                    and timestamp(b["recorded_at"]) < timestamp(d["recorded_at"])):
                raise ValueError("Etterpåvurdering oppdaga i " + panel + ":" + cid)
            options = case["options"]
            option_ids = {o["option_id"] for o in options}
            if set(a.get("scores",{})) != option_ids or set(b.get("scores",{})) != option_ids:
                raise ValueError("Manglande vurderingar for " + cid)
            selected = d.get("chosen_option_id")
            if selected not in option_ids:
                raise ValueError("Valt alternativ finst ikkje")
            if "scores" in d or "chosen_option_id" in a or "chosen_option_id" in b:
                raise ValueError("Rolleforveksling i rådata")
            for opt in options:
                e1,e2 = a["scores"][opt["option_id"]],b["scores"][opt["option_id"]]
                for e in (e1,e2):
                    if (type(e) not in (int,float) or not 0 <= e <= 10 or
                            round(e*2) != e*2):
                        raise ValueError("Vurdering utanfor 0–10 eller i feil steg")
                output.append({
                    "case_id": panel + "::" + cid,
                    "group_id": panel,
                    "split": entry["split"],
                    "option_id": opt["option_id"],
                    "chosen": "1" if opt["option_id"] == selected else "0",
                    "feasible": "1",
                    "mu": repr(float(opt["mu"])),
                    "e1": str(e1),
                    "e2": str(e2),
                    "w1": repr(float(case["weights"]["agent1"])),
                    "w2": repr(float(case["weights"]["agent2"])),
                })
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="mode",required=True)
    ro=sub.add_parser("roster",help="Frys panel og datasplitt før responsar")
    ro.add_argument("manifest",type=Path)
    ro.add_argument("--panels",type=int,default=12)
    ro.add_argument("--out",type=Path,required=True)
    co=sub.add_parser("compile",help="Kombiner daterte, uavhengige svar")
    co.add_argument("manifest",type=Path)
    co.add_argument("roster",type=Path)
    co.add_argument("responses_dir",type=Path)
    co.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    manifest=read_json(args.manifest)
    manifest_check(manifest)
    if args.mode=="roster":
        records=new_roster(manifest,args.panels)
        columns=("panel_id","split","manifest_sha256")
        dest=args.out
    else:
        roster=roster_check(manifest,args.roster)
        records=compile_data(manifest,roster,args.responses_dir)
        columns=OUTPUT
        dest=args.out
    with dest.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader();writer.writerows(records)
    print("Skrive",len(records),"rader til",dest)
    if args.mode=="compile":
        print("OBS: Pilot på fire stratifiserte typologiar med uniform presentasjonsprior.")
        print("Det er ikkje ei empirisk identifisering av den naturlege mu_SG.")


if __name__=="__main__":
    main()
