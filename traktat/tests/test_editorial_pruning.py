import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "tekst" / "formlaere.tex").read_text(encoding="utf-8")
GLOSSARY = json.loads((ROOT / "ordliste.json").read_text(encoding="utf-8"))
PROPOSITIONS = dict(re.findall(r"\\begin\{formproposition\}\{([\d.]+)\}\{[datio]\}\s*([\s\S]*?)\\end\{formproposition\}", TEXT))


class EditorialPruning(unittest.TestCase):
    def test_redundant_propositions_are_removed(self):
        self.assertEqual(len(PROPOSITIONS), 488)
        for number in ("5.7221", "6.201", "6.5111"):
            self.assertNotIn(number, PROPOSITIONS)

    def test_glossary_references_survive(self):
        entry = next(e for e in GLOSSARY["entries"] if e["id"] == "negativ-tilbakekopling")
        self.assertIn("6.1213", entry["propositions"])
        self.assertNotIn("6.201", entry["propositions"])

    def test_unjustified_certainties_and_defence_are_gone(self):
        self.assertNotIn("krev lause koplingar", PROPOSITIONS["6.131"])
        self.assertIn("kan", PROPOSITIONS["6.1211"])
        self.assertNotIn("Arkivet er ikkje ei skulding", PROPOSITIONS["7.13"])


if __name__ == "__main__":
    unittest.main()
