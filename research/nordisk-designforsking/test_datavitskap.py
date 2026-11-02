#!/usr/bin/env python3
"""Regression checks for the published Nordic design-research analysis."""
from __future__ import annotations
import gzip
import io
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from database import DB,GZ,ensure_database
R=Path(__file__).resolve().parent
O=R/"results"

class Reproducibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_database()
        cls.c=sqlite3.connect(DB)
        cls.summary=json.loads((O/"summary.json").read_text(encoding="utf-8"))
    @classmethod
    def tearDownClass(cls):
        cls.c.close()

    def test_source_database(self):
        integrity=self.c.execute("PRAGMA integrity_check").fetchone()[0]
        self.assertEqual(integrity,"ok")
        count,valid=self.c.execute("SELECT COUNT(*),SUM(in_scope) FROM works").fetchone()
        self.assertEqual(count,self.summary["unique_candidates"])
        self.assertEqual(valid,self.summary["provisionally_included"])
        self.assertEqual(self.c.execute(
            "SELECT COUNT(*) FROM query_log WHERE error IS NULL").fetchone()[0],
            self.summary["successful_search_pages"])
        self.assertEqual(self.c.execute(
            "SELECT COUNT(*) FROM query_log WHERE error LIKE '%429%'").fetchone()[0],1)

    def test_years(self):
        lo,hi=self.c.execute("SELECT MIN(year),MAX(year) FROM works").fetchone()
        self.assertGreaterEqual(lo,2000);self.assertLessEqual(hi,2026)

    def test_public_gzip_omits_provider_text(self):
        with tempfile.TemporaryDirectory() as path:
            dst=Path(path)/"archive.sqlite"
            with gzip.open(GZ,"rb") as src,dst.open("wb") as out:
                import shutil
                shutil.copyfileobj(src,out)
            conn=sqlite3.connect(dst)
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(conn.execute("SELECT count(*) FROM works").fetchone()[0],
                             self.summary["unique_candidates"])
            self.assertEqual(conn.execute("SELECT count(*) FROM works WHERE length(abstract)>0").fetchone()[0],0)
            self.assertEqual(conn.execute("SELECT count(*) FROM works WHERE length(raw_json)>2").fetchone()[0],0)
            conn.close()

    def test_public_tables(self):
        t=pd.read_csv(O/"included_publications.csv")
        self.assertEqual(len(t),self.summary["provisionally_included"])
        self.assertTrue(t["id"].is_unique)
        self.assertNotIn("abstract",t.columns)
        t2=pd.read_csv(O/"candidates_for_manual_review.csv")
        self.assertEqual(len(t)+len(t2),self.summary["unique_candidates"])

    def test_lsa_matrix_alignment(self):
        data=np.load(O/"lsa_vectors.npz")
        ids=data["ids"].astype(str)
        m=data["vectors"]
        self.assertEqual(len(ids),len(m))
        self.assertEqual(len(ids),self.summary["provisionally_included"])
        self.assertTrue(pd.Series(ids).is_unique)
        self.assertFalse(np.isnan(m).any())

    def test_internal_citations(self):
        refs=pd.read_csv(O/"internal_citations.csv")
        self.assertEqual(len(refs),self.summary["cited_edges_within_retrieved_sample"])
        self.assertTrue({"citing_id","cited_id"}.issubset(refs.columns))
        self.assertEqual(len(refs),len(refs[["citing_id","cited_id"]].drop_duplicates()))

    def test_semantic_citation_controls(self):
        csv=pd.read_csv(O/"citation_semantic_links.csv")
        self.assertEqual(len(csv),self.summary["cited_edges_within_retrieved_sample"])
        self.assertGreater(csv.matched_cosine.notna().mean(),.9)
        v=json.loads((O/"citation_semantic_results.json").read_text(encoding="utf-8"))
        self.assertEqual(v["groups"]["all_observed_edges"]["edges"],len(csv))
        self.assertGreaterEqual(v["groups"]["exclude_shared_author"]["edges"],500)

    def test_stratified_sample(self):
        sample=pd.read_csv(O/"probability_sample_600_double_coder.csv")
        alloc=pd.read_csv(O/"probability_sample_allocation.csv")
        info=json.loads((O/"probability_sample_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(len(sample),600)
        self.assertTrue(sample.id.is_unique)
        self.assertEqual(int(alloc.draw_n.sum()),len(sample))
        self.assertEqual(int(alloc.frame_n.sum()),info["automatic_title_screened_frame"])
        # Sample weights reconstruct the exact finite automatic frame by stratum.
        self.assertAlmostEqual(float(sample.inverse_probability_weight.sum()),
             info["automatic_title_screened_frame"],delta=.01)
        self.assertTrue(sample.coder_A_C2.isna().all())
        self.assertTrue(sample.coder_B_C3.isna().all())

    def test_browser_review_no_fulltext(self):
        s=(O/"review.html").read_text(encoding="utf-8")
        m=re.search(r'<script id="paperData" type="application/json">(.*?)</script>',s,re.S)
        self.assertIsNotNone(m)
        records=json.loads(m.group(1))
        self.assertEqual(len(records),200)
        self.assertEqual(len({p["id"] for p in records}),200)
        self.assertTrue(all(p["citing_id"]!=p["cited_id"] for p in records))
        self.assertTrue(all("abstract" not in p for p in records))

    def test_coding_analysis_does_not_infer_from_blanks(self):
        import kodingsanalyse
        self.assertEqual(kodingsanalyse.kappa([0,1],[0,1]),1.0)
        self.assertEqual(kodingsanalyse.kappa([0,1],[1,0]),-1.0)
        self.assertIsNone(kodingsanalyse.kappa([],[]))
        status=json.loads((O/"coding_progress.json").read_text(encoding="utf-8"))
        self.assertTrue(all(v["double_coded"]==0 for v in status["indicators"]))

    def test_review_javascript_parses(self):
        import shutil,subprocess,tempfile
        node=shutil.which("node")
        if not node:self.skipTest("Node executable unavailable")
        s=(O/"review.html").read_text(encoding="utf-8")
        match=re.findall(r"<script(?:[^>]*)>(.*?)</script>",s,re.S)
        self.assertGreater(len(match),1)
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"review.js"
            target.write_text(match[-1],encoding="utf-8")
            chk=subprocess.run([node,"--check",str(target)],capture_output=True,text=True)
            self.assertEqual(chk.returncode,0,chk.stderr)

    def test_research_reports(self):
        expected=["RAPPORT.md","AVANSERT_ANALYSE.md","DASHBOARD.md",
             "SITERINGSLINJER.md","UTVALSPLAN.md","DATAKVALITET.md"]
        for name in expected:
            with self.subTest(name=name):
                self.assertTrue((O/name).exists(),name)
                self.assertGreater((O/name).stat().st_size,600)
        for j in range(1,19):
            files=list((O/"figures").glob(f"{j:02d}-*.png"))
            self.assertEqual(len(files),1,f"Missing or duplicated plot {j}")
            self.assertGreater(files[0].stat().st_size,3000)

if __name__=="__main__":
    unittest.main(verbosity=2)
