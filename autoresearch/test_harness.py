import json
import tempfile
import unittest
from pathlib import Path
from autoresearch import harness


class HarnessTests(unittest.TestCase):
    def test_propositions(self):
        props = harness.propositions()
        self.assertEqual(len(props), 491)
        self.assertEqual(props["1"], "d")
        self.assertEqual(props["7.34"], "t")

    def test_candidate_provenance(self):
        audit = harness.status()
        self.assertEqual(audit["candidate_citation_pairs"], 150)
        self.assertEqual(audit["independent_fulltext_validations"], 0)
        self.assertEqual(audit["confirmed_counterexamples"], 0)

    def test_seed(self):
        record = Path(__file__).parent / "experiments/0001-kumulativitet.json"
        result = harness.check(record)
        self.assertTrue(result["structurally_valid"])
        self.assertEqual(result["evidence_items"], 0)

    def test_reject_unfounded_verdict(self):
        record = json.loads((Path(__file__).parent / "experiments/0001-kumulativitet.json").read_text(encoding="utf-8"))
        record["status"] = "supported"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "attempt.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaises(ValueError):
                harness.check(path)

    def test_candidate_search_does_not_claim_verification(self):
        matches = harness.search("design", limit=3)
        self.assertTrue(matches)
        self.assertTrue(all(x["status"] == "ikkje_fulltekstverifisert" for x in matches))


if __name__ == "__main__":
    unittest.main()
