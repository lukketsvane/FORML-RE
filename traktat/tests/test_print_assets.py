"""Canonical vector figures must stay portable without runtime SVG conversion."""
from __future__ import annotations

import base64
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
import render_latex


class PortableVectorFigures(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.assets = self.root / "nettstad" / "illustrations"
        self.assets.mkdir(parents=True)
        self.work = self.root / "build" / "latex"
        self.work.mkdir(parents=True)
        self.svg = self.assets / "diagram.svg"
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="80" viewBox="0 0 400 80">'
                            '<path d="M5 60H390" stroke="black"/>'
                            '<text x="5" y="35" font-family="DejaVu Serif" font-size="24">𝕄 Π Λ s₀</text></svg>', encoding="utf-8")
        self.raster = self.assets / "raster.png"
        self.raster.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jN1sAAAAASUVORK5CYII="))
        prop = {"kind": "prop", "n": "1", "status": "d", "paragraphs": ["Ei utsegn."], "notes": []}
        self.doc = {"schemaVersion": 1, "title": "Test", "author": "Test", "sourceHash": "a" * 64,
                    "props": [prop], "tokens": [prop], "sources": [], "notes": [], "glossary": [],
                    "figures": [{"after": "1", "file": "diagram.svg", "alt": "Modell"},
                                {"after": "1", "file": "raster.png", "alt": "Raster"}]}
        for module in (build, render_latex):
            patcher = patch.object(module, "ROOT", self.root)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_vector_conversion_preserves_math_and_canonical_source(self):
        canonical = self.svg.read_bytes()
        figures = build.prepare_print_figures(self.doc, self.work)
        self.assertEqual({path.name for path in figures}, {"diagram.pdf", "raster.png"})
        pdf = PdfReader(self.work / "illustrations" / "diagram.pdf")
        self.assertEqual(len(pdf.pages), 1)
        self.assertEqual((float(pdf.pages[0].mediabox.width), float(pdf.pages[0].mediabox.height)), (300, 60))
        self.assertEqual(pdf.pages[0].extract_text().replace(" ", "").replace("\n", ""), "𝕄ΠΛs₀")
        self.assertEqual(pdf.metadata["/CreationDate"], "D:20000101000000Z")
        self.assertEqual(self.svg.read_bytes(), canonical, "Print conversion cannot replace the web's canonical SVG")
        self.assertEqual((self.work / "illustrations" / "raster.png").read_bytes(), self.raster.read_bytes())

    def test_portable_bundle_contains_only_active_ready_to_use_assets(self):
        retired = self.work / "illustrations" / "retired.pdf"
        retired.parent.mkdir()
        retired.write_bytes(b"retired figure")
        figures = build.prepare_print_figures(self.doc, self.work)
        tex = render_latex.Renderer(self.doc).content()
        self.assertIn(r"\bookfigure{illustrations/diagram.pdf}", tex)
        self.assertNotIn("diagram.svg", tex)
        (self.work / "formlaere.tex").write_text(tex, encoding="utf-8")
        bundle = self.root / "formlaere-latex.zip"
        build.package_latex(self.work, figures, bundle)
        with zipfile.ZipFile(bundle) as archive:
            self.assertEqual(set(archive.namelist()), {"formlaere.tex", "illustrations/diagram.pdf", "illustrations/raster.png"})
            self.assertTrue(archive.read("illustrations/diagram.pdf").startswith(b"%PDF-"))
        self.assertFalse(retired.exists(), "Removed placements cannot leak from a previous build")

    def test_portable_bundle_carries_fixed_fonts_licence_and_cover(self):
        layout = self.root / "layout"
        source_fonts = layout / "fonts"
        source_fonts.mkdir(parents=True)
        expected = {"fonts/EBGaramond12-Regular.otf": b"font specimen",
                    "fonts/OFL.txt": b"font licence specimen",
                    "cover-stolar.png": self.raster.read_bytes()}
        for name, data in expected.items():
            (layout / name).write_bytes(data)
        stale = self.work / "fonts" / "removed-font.otf"
        stale.parent.mkdir()
        stale.write_bytes(b"retired font")
        assets = build.prepare_print_layout(self.work)
        (self.work / "formlaere.tex").write_text("Portable edition.", encoding="utf-8")
        bundle = self.root / "formlaere-latex.zip"
        build.package_latex(self.work, assets, bundle)
        with zipfile.ZipFile(bundle) as archive:
            self.assertEqual(set(archive.namelist()), {"formlaere.tex", *expected})
            for name, data in expected.items():
                self.assertEqual(archive.read(name), data)
        self.assertFalse(stale.exists(), "Retired fonts cannot enter the portable book")

    def test_legacy_source_destination_does_not_duplicate_the_printed_reference(self):
        self.doc["sourceAliases"] = {"63": "19"}
        self.doc["sources"] = [{"id": "19", "number": 1, "citation": "One canonical reference."}]
        tex = render_latex.Renderer(self.doc).content()
        self.assertIn(r"\hypertarget{referanse-63}{}", tex)
        self.assertNotIn(r"\begin{referenceentry}{referanse-63}", tex)
        self.assertEqual(tex.count("One canonical reference."), 1)

    def test_source_numbers_are_shared_by_inline_glossary_notes_and_bibliography(self):
        self.doc["sources"] = [{"id": "7", "number": 1, "citation": "First reference."},
                               {"id": "110", "number": 2, "citation": "Second reference."}]
        self.doc["sourceAliases"] = {"63": "7"}
        self.doc["props"][0]["paragraphs"] = ["Ei utsegn.[[kjelde:110]]"]
        self.doc["glossary"] = [{"id": "form", "term": "Form", "definition": "Ei ordning.",
                                 "propositions": ["1"], "sources": ["110"]}]
        self.doc["notes"] = [{"id": "n1", "number": 1, "proposition": "1", "note": "Eit notat.",
                              "sources": ["7", "110"]}]
        tex = render_latex.Renderer(self.doc).content()
        self.assertIn(r"\sourceref{\hyperlink{referanse-110}{2}}", tex)
        self.assertIn(r"Kjelder: \hyperlink{referanse-110}{2}", tex)
        self.assertIn(r"\entrylinks{[\hyperlink{referanse-7}{1}, \hyperlink{referanse-110}{2}]}", tex)
        self.assertIn(r"\begin{referenceentry}{referanse-7}{1}", tex)
        self.assertIn(r"\begin{referenceentry}{referanse-110}{2}", tex)
        self.assertIn(r"\hypertarget{referanse-63}{}", tex)
        self.assertNotIn(r"\hyperlink{referanse-110}{110}", tex)


if __name__ == "__main__":
    unittest.main()
