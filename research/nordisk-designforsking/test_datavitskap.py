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

    def test_oa_retrievability_audit(self):
        import csv
        summary=json.loads((O/"oa_retrievability_quality.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["sample_pairs"],162)
        self.assertEqual(summary["readable_pdf_pair_attempts"],32)
        self.assertEqual(summary["unique_citing_pdfs_downloaded"],26)
        self.assertEqual(sum(summary["reasons"].values()),162)
        with (O/"oa_citation_locator_audit.csv").open(encoding="utf-8",newline="") as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),162)
        self.assertEqual(sum(r["pdf_available"]=="1" for r in rows),32)

    def test_oa_reference_crosscheck_is_not_labelled_reproduction(self):
        import csv
        with (O/"oa_reference_crosscheck.csv").open(encoding="utf-8",newline="") as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),32)
        self.assertEqual(sum(r["validation_tier"]=="bibliography-and-intext-candidate" for r in rows),13)
        self.assertTrue(all("replication" not in r["validation_tier"] for r in rows))

    def test_year_sensitivity_preserves_three_period_count(self):
        years=json.loads((O/"year_basis_sensitivity.json").read_text(encoding="utf-8"))["scenarios"]
        self.assertEqual(years["openalex_year_baseline"]["two_step_paths"],712)
        self.assertEqual(years["both_journal_volume_years"]["two_step_paths"],712)
        self.assertEqual(years["openalex_year_baseline"]["future_dated_references"],15)
        self.assertEqual(years["both_journal_volume_years"]["late_to_early_direct_edges"],156)

    def test_manual_pdf_pilot_is_preliminary(self):
        import csv
        with (O/"oa_manual_pilot.csv").open(encoding="utf-8",newline="") as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),7)
        self.assertTrue(all(r["coder_status"]=="single_reader_preliminary" for r in rows))
        self.assertTrue(all(r["provisional_L_code"] in {"L0","L1","LNA"} for r in rows))
        self.assertIn("data/oa_fulltexts_private/",(R/".gitignore").read_text(encoding="utf-8"))

    def test_manifestation_candidates_not_automatically_deduplicated(self):
        manifest=json.loads((O/"manifestation_audit.json").read_text(encoding="utf-8"))
        pairs=pd.read_csv(O/"candidate_same_title_same_author_manifestations.csv")
        self.assertEqual(manifest["database_work_records"],self.summary["unique_candidates"])
        self.assertEqual(manifest["candidate_title_author_groups"],59)
        self.assertEqual(manifest["candidate_pairs"],79)
        self.assertEqual(manifest["crossyear_pairs"],58)
        self.assertEqual(len(pairs),79)
        self.assertTrue(pairs.manual_same_underlying_study.isna().all())
        self.assertEqual(manifest["case_citing_papers_with_both_ids_as_references"],1)

    def test_oa_locator_calibration_nonrepresentative(self):
        c=json.loads((O/"citation_locator_calibration_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(c["verified_positive_contexts_from_purposive_sample"],15)
        self.assertEqual(c["positive_contexts_also_detected_by_strict_auto_heuristic"],12)
        self.assertEqual(c["unverified_or_ambiguous_cases_not_treated_as_negatives"],2)
        frame=pd.read_csv(O/"citation_locator_positive_calibration.csv")
        self.assertEqual(len(frame),17)
        self.assertTrue(frame.not_an_epistemic_quality_label.all())

    def test_second_manual_context_pilot_is_not_blind(self):
        r=pd.read_csv(O/"oa_manual_pilot_round2.csv")
        self.assertEqual(len(r),10)
        self.assertTrue((r.coder_status=="single_reader_context_pilot").all())
        self.assertEqual(int((r.provisional_L_code=="L3").sum()),2)
        self.assertTrue(set(r.provisional_L_code).issubset({"L0","L1","L3","LNA"}))

    def test_open_access_url_safety(self):
        from oa_fulltext_audit import validate_https
        self.assertTrue(validate_https("https://doi.org/10.1017/dsj.2025.10027"))
        self.assertTrue(validate_https("https://researchportal.helsinki.fi/publications/test"))
        for url in ("http://example.com/a","https://localhost/a","https://127.0.0.1/a",
                    "https://172.28.1.3/file","https://169.254.169.254/latest/meta-data/",
                    "https://[::1]/a","https://example.com:8080/","https://a.local/file",
                    "https://u:p@example.org/s"):
            with self.subTest(url=url):
                self.assertFalse(validate_https(url))

    def test_external_meta_benchmarks_not_pooled(self):
        d=json.loads((O/"external_methodological_benchmarks.json").read_text(encoding="utf-8"))
        self.assertEqual(len(d["sources"]),8)
        self.assertEqual(sum(x["found_in_nordic_openalex_candidate_corpus"] is True for x in d["sources"]),1)
        self.assertEqual([x["included_n"] for x in d["sources"] if x["id"]=="alaie2025"],[70])
        self.assertEqual([x["included_n"] for x in d["sources"] if x["id"]=="bonnin2026"],[31])
        self.assertIn("never add",d["pooling_forbidden"])

    def test_research_reports(self):
        expected=["RAPPORT.md","AVANSERT_ANALYSE.md","DASHBOARD.md",
             "SITERINGSLINJER.md","UTVALSPLAN.md","DATAKVALITET.md",
             "OA_TILGANG.md","OA_MANUELL_PILOT.md","AARSKJELDEKRITIKK.md",
             "OA_MANUELL_PILOT_2.md","LOKALISERING_VALIDERING.md","MANIFESTASJONAR.md","KOMPARATORAR_2026.md"]
        for name in expected:
            with self.subTest(name=name):
                self.assertTrue((O/name).exists(),name)
                self.assertGreater((O/name).stat().st_size,600)
        for j in range(1,22):
            files=list((O/"figures").glob(f"{j:02d}-*.png"))
            self.assertEqual(len(files),1,f"Missing or duplicated plot {j}")
            self.assertGreater(files[0].stat().st_size,3000)

if __name__=="__main__":
    unittest.main(verbosity=2)
