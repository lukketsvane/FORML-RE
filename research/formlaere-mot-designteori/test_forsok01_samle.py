"""Sju SYNTHETISKE kontrakttestar for forsok01_samle.py.

Desse testar integriteten i datarøyrleidninga. Ingen reelle
menneskevurderingar eller designval er skapte/rapporterte.
"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest

from forsok01_samle import (
    OUTPUT, compile_data, manifest_check, new_roster, responses_check,
)

BEFORE = datetime(2026, 11, 7, 9, 0, tzinfo=timezone.utc)
AFTER = datetime(2026, 11, 7, 10, 0, tzinfo=timezone.utc)


def dummy_manifest():
    """Fiktivt, berre for programtest. Ikkje faktiske 50×50×50-objekt."""
    study = "syntetisk-kontrakttest"
    sets = []
    for i in range(8):
        sets.append({
            "case_id": study + ":" + str(i),
            "weights": {"agent1":0.75 if i%2==0 else 0.25,
                        "agent2":0.25 if i%2==0 else 0.75},
            "options": [
                {"option_id":str(i)+":"+str(j),"mu":0.25,
                 "hard_rule_flags": [],"display_code":"ABCD"[j]}
                for j in range(4)
            ],
        })
    return {
        "schema_version":"formlaere-pilot-manifest-v1",
        "study_id":study,
        "manifest_sha256":"a"*64,
        "sets":sets,
    }


def write_roles(manifest, roster, folder):
    for pan in roster:
        panel = pan["panel_id"]
        for role in ("agent1","agent2","decision"):
            actor = panel + "-" + role
            out = {
                "schema_version":"formlaere-pilot-response-v1",
                "study_id":manifest["study_id"],
                "manifest_sha256":manifest["manifest_sha256"],
                "panel_id":panel,"actor_id":actor,"role":role,
                "voluntary":True,"consent_confirmed_at":BEFORE.isoformat(),
                "answers":[],
            }
            for c in manifest["sets"]:
                ans = {"case_id":c["case_id"],
                       "recorded_at":(AFTER if role=="decision" else BEFORE).isoformat()}
                if role=="decision":
                    ans["chosen_option_id"]=c["options"][0]["option_id"]
                else:
                    ans["scores"]={
                        x["option_id"]:float(i) for i,x in enumerate(c["options"])
                    }
                out["answers"].append(ans)
            (folder/(panel+"_"+role+".json")).write_text(json.dumps(out), encoding="utf8")


class IndependentDataTests(unittest.TestCase):
    def setUp(self):
        self.m=dummy_manifest()
        self.roster=new_roster(self.m, 6)
        self.tmp=tempfile.TemporaryDirectory()
        self.folder=Path(self.tmp.name)
        write_roles(self.m,self.roster,self.folder)

    def tearDown(self):
        self.tmp.cleanup()

    def get_file(self,pan,role):
        return self.folder/(pan["panel_id"]+"_"+role+".json")

    def edit_file(self,path,edit):
        d=json.loads(path.read_text(encoding="utf8"))
        edit(d)
        path.write_text(json.dumps(d),encoding="utf8")

    def test_frozen_roster_balanced_and_deterministic(self):
        self.assertEqual(self.roster,new_roster(self.m,6))
        self.assertEqual([x["split"] for x in self.roster].count("train"),2)
        self.assertEqual([x["split"] for x in self.roster].count("validation"),2)
        self.assertEqual([x["split"] for x in self.roster].count("test"),2)

    def test_complete_compilation_respects_groups(self):
        rows=compile_data(self.m,self.roster,self.folder)
        self.assertEqual(len(rows),6*8*4)
        self.assertEqual(tuple(rows[0]),OUTPUT)
        groups={}
        for row in rows:
            group=row["group_id"]
            groups.setdefault(group,set()).add(row["split"])
        self.assertTrue(all(len(s)==1 for s in groups.values()))
        for pan in self.roster:
            p=[r for r in rows if r["group_id"]==pan["panel_id"]]
            self.assertEqual(sum(r["chosen"]=="1" for r in p),8)

    def test_after_the_fact_rating_is_rejected(self):
        p=self.get_file(self.roster[0],"agent1")
        self.edit_file(p,lambda d: d["answers"][0].update(recorded_at=(AFTER+timedelta(hours=1)).isoformat()))
        with self.assertRaisesRegex(ValueError,"oppdaga"):
            compile_data(self.m,self.roster,self.folder)

    def test_conflicting_manifest_is_rejected(self):
        p=self.get_file(self.roster[0],"agent1")
        self.edit_file(p,lambda d: d.update(manifest_sha256="b"*64))
        with self.assertRaisesRegex(ValueError,"feil manifest"):
            compile_data(self.m,self.roster,self.folder)

    def test_role_conflict_is_rejected(self):
        p=self.get_file(self.roster[0],"agent2")
        self.edit_file(p,lambda d: d.update(actor_id=self.roster[0]["panel_id"]+"-agent1"))
        with self.assertRaisesRegex(ValueError,"krevst"):
            compile_data(self.m,self.roster,self.folder)

    def test_cross_panel_actor_leakage_is_rejected(self):
        other = self.roster[0]["panel_id"] + "-agent1"
        p=self.get_file(self.roster[1],"agent1")
        self.edit_file(p,lambda d: d.update(actor_id=other))
        with self.assertRaisesRegex(ValueError,"fleire train/test-panel"):
            compile_data(self.m,self.roster,self.folder)

    def test_missing_consent_rejected(self):
        p=self.get_file(self.roster[0],"agent1")
        self.edit_file(p,lambda d: d.update(voluntary=False))
        with self.assertRaisesRegex(ValueError,"samtykke"):
            compile_data(self.m,self.roster,self.folder)

    def test_missing_rating_rejected(self):
        p=self.get_file(self.roster[0],"agent1")
        self.edit_file(p,lambda d: d["answers"][0]["scores"].pop(next(iter(d["answers"][0]["scores"]))))
        with self.assertRaisesRegex(ValueError,"Manglande vurderingar"):
            compile_data(self.m,self.roster,self.folder)


if __name__=="__main__":
    unittest.main(verbosity=2)
