"""Compile a small real book so page format, cover and fonts cannot drift."""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build
from render_latex import Renderer


@unittest.skipUnless(shutil.which("xelatex"), "Book integration test needs XeLaTeX")
class CompiledBookLayout(unittest.TestCase):
    def test_real_template_retains_book_cover_geometry_and_searchable_garamond(self):
        props = [
            {"kind": "prop", "n": "1", "status": "d", "notes": [],
             "paragraphs": ["Thompson Kauffman Mifflin skifte. ÆØÅ æøå."]},
            {"kind": "prop", "n": "1.01", "status": "t", "notes": ["test-note"],
             "paragraphs": ["*Ei kursiv utsegn.* Ei kjelde.[[kjelde:7]]"]},
        ]
        document = {
            "schemaVersion": 1, "sourceHash": "a" * 64,
            "title": "formlære", "author": "Testforfattar",
            "tokens": [
                {"kind": "title", "text": "formlære"},
                {"kind": "paragraph", "text": "*Ei prøve av bokforma*\nTestforfattar · 2026"},
                {"kind": "heading", "text": "Føreord"},
                {"kind": "paragraph", "text": "Bokprøva byrjar på sida etter omslaget."},
                {"kind": "heading", "text": "Lesekode"},
                {"kind": "paragraph", "text": "Definisjon og følgje har kvar sin status."},
                *props,
            ],
            "props": props, "figures": [], "sourceAliases": {}, "mathematics": {},
            "glossary": [{"id": "prove", "term": "Prøve", "definition": "Ei lita bokprøve.",
                          "propositions": ["1"], "sources": ["7"]}],
            "notes": [{"id": "test-note", "number": 1, "proposition": "1.01",
                       "note": "Eit notat i den same bokforma.", "sources": ["7"]}],
            "sources": [{"id": "7", "number": 1, "citation": "Thompson Kauffman Mifflin skifte."}],
        }
        # Use the active template and its actual vendored cover/fonts, without
        # mocking paths or depending on installed Garamond variants.
        with tempfile.TemporaryDirectory(prefix="formlaere-book-") as directory:
            work = Path(directory)
            build.prepare_print_layout(work)
            (work / "formlaere.tex").write_text(Renderer(document).render(), encoding="utf-8")
            env = dict(os.environ, SOURCE_DATE_EPOCH="946684800", FORCE_SOURCE_DATE="1")
            for _ in range(2):
                result = subprocess.run(
                    ["xelatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "formlaere.tex"],
                    cwd=work, env=env, capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout[-5000:] + result.stderr[-1000:])
            reader = PdfReader(work / "formlaere.pdf")
            self.assertGreaterEqual(len(reader.pages), 3)
            for page in reader.pages:
                self.assertAlmostEqual(float(page.mediabox.width), 125 / 25.4 * 72, delta=0.02)
                self.assertAlmostEqual(float(page.mediabox.height), 200 / 25.4 * 72, delta=0.02)
            cover_text = reader.pages[0].extract_text() or ""
            self.assertIn("formlære", cover_text)
            self.assertIn("Testforfattar", re.sub(r"\s+", "", cover_text))
            self.assertGreater(len(reader.pages[0].images), 0, "The cover must contain the chair mosaic")
            second_page = reader.pages[1].extract_text() or ""
            self.assertIn("Bokprøvabyrjar", re.sub(r"\s+", "", second_page), "No blank page may separate cover and foreword")
            searchable = re.sub(r"\s+", "", "".join(page.extract_text() or "" for page in reader.pages))
            for label in ("[d]", "[t]"):
                self.assertIn(label, searchable, "Status must remain separate from decimal proposition numbers")
            for word in ("Thompson", "Kauffman", "Mifflin", "skifte", "ÆØÅ", "æøå"):
                self.assertIn(word, searchable, "Letters and ligatures must retain their Unicode text")
            fonts = {
                str(font.get_object().get("/BaseFont", ""))
                for page in reader.pages
                for font in page["/Resources"].get_object().get("/Font", {}).get_object().values()
            }
            self.assertTrue(any("EBGaramond12-Regular" in font for font in fonts), fonts)
            self.assertTrue(any("EBGaramond12-Italic" in font for font in fonts), fonts)
            self.assertTrue(any("EBGaramond08-Regular" in font for font in fonts), fonts)
            self.assertFalse(any("DejaVuSerif" in font for font in fonts), fonts)


if __name__ == "__main__":
    unittest.main()
