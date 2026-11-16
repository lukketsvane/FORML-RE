import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = (ROOT / "tekst" / "formlaere.tex").read_text(encoding="utf-8")
NOTES = json.loads((ROOT / "kjelder.json").read_text(encoding="utf-8"))["notes"]
SHORT = (ROOT / "nettstad" / "kort.html").read_text(encoding="utf-8")
PROPS = list(re.finditer(r"\\begin\{formproposition\}\{([\d.]+)\}\{([datio])\}", TEX))
IDS = [m.group(1) for m in PROPS]

class DesignerConclusion(unittest.TestCase):
    def test_491_unique_and_new_order(self):
        self.assertEqual(len(IDS), len(set(IDS)))
        self.assertEqual(len(IDS), 491)
        self.assertEqual(IDS[IDS.index("6.01") + 1], "6.1")
        self.assertEqual(IDS[IDS.index("6.76") + 1], "6.8")
        self.assertEqual(IDS[IDS.index("6.87") + 1], "7")
        self.assertFalse(set(("6.02","6.0201","6.021","6.0211","6.022","6.023","6.0231","6.024","6.025","6.026","6.027")) & set(IDS))

    def test_note_and_inline_references(self):
        by_id = {n["id"]: n for n in NOTES}
        self.assertEqual(by_id["prop-6-811"]["proposition"], "6.811")
        self.assertEqual(by_id["prop-6-82"]["proposition"], "6.82")
        self.assertNotIn("prop-6-0211", by_id)
        self.assertNotIn("prop-6-022", by_id)
        for old in ("6.02","6.0201","6.021","6.0211","6.022","6.023","6.0231","6.024","6.025","6.026","6.027"):
            self.assertIsNone(re.search(r"(?<![\d.])" + re.escape(old) + r"(?![\d])", TEX))
        self.assertIn("(6.8, 6.801)", TEX)
        self.assertIn('"6.8"', SHORT)
        self.assertNotIn('"6.02"', SHORT)

if __name__ == "__main__":
    unittest.main()
