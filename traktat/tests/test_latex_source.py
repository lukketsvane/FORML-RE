"""The editable TeX manuscript must drive both renderers without content loss."""
from __future__ import annotations

import sys
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from content import CANONICAL, parse_source
from latex_source import group, inline, legacy_inline_to_latex, migrate_to_latex, parse_latex, render_mathml, validate_mathml
from render_latex import Renderer


class CanonicalLatex(unittest.TestCase):
    def test_latex_is_the_only_active_manuscript_input(self):
        self.assertIn("tekst/formlaere.tex", CANONICAL)
        self.assertNotIn("tekst/formlaere.txt", CANONICAL)

    def test_historical_manuscript_migrates_without_losing_prose_math_or_addresses(self):
        source = (ROOT / "archive/2026-11-01/formlaere.txt").read_text()
        old_tokens, old_props = parse_source(source)
        tokens, props, math = parse_latex(migrate_to_latex(source))
        self.assertEqual([(p["n"], p["status"]) for p in props], [(p["n"], p["status"]) for p in old_props])
        self.assertEqual([t["kind"] for t in tokens], [t["kind"] for t in old_tokens])
        renderer = Renderer({"schemaVersion": 1, "props": props, "sources": [], "notes": [], "mathematics": math})
        # Compare what the print renderer receives, including every math atom.
        # The new source uses native delimiters where the old renderer inserted ensuremath.
        for old, new in zip(old_tokens, tokens):
            old_texts = old.get("paragraphs", [old.get("text", "")])
            new_texts = new.get("paragraphs", [new.get("text", "")])
            self.assertEqual(len(old_texts), len(new_texts))
            for original, migrated in zip(old_texts, new_texts):
                expected = renderer.prose(original)
                normalized, cursor = [], 0
                while True:
                    index = expected.find(r"\ensuremath{", cursor)
                    if index < 0:
                        normalized.append(expected[cursor:])
                        break
                    normalized.append(expected[cursor:index])
                    value, cursor = group(expected, index + len(r"\ensuremath"))
                    normalized.append(r"\(" + value + r"\)")
                self.assertEqual(renderer.prose(migrated), "".join(normalized), original)

    def test_native_formula_and_edit_reach_mathml_and_pdf_from_same_source(self):
        source = r"""\section{Føreord}
Ei innleiing.
\section{Lesekode}
Ei følgje krev premiss.
\begin{formproposition}{1}{t}
\emph{Verdien er \(\frac{a}{b}\).}\kjelder{1}
\end{formproposition}
"""
        def both(text):
            tokens, props, math = parse_latex(text)
            render_mathml(math)
            renderer = Renderer({"schemaVersion": 1, "props": props, "sources": [{"id": "1", "number": 1}], "notes": [], "mathematics": math})
            return props, math, renderer.prose(props[0]["paragraphs"][0])
        before, old_math, print_before = both(source)
        after, new_math, print_after = both(source.replace(r"\frac{a}{b}", r"\frac{a}{c}"))
        self.assertNotEqual(before, after)
        self.assertIn(r"\frac{a}{b}", print_before)
        self.assertIn(r"\frac{a}{c}", print_after)
        self.assertIn(r"\textit{Verdien er \(\frac{a}{c}\).}", print_after)
        self.assertIn("<mfrac>", next(iter(new_math.values()))["mathml"])
        self.assertIn("<mi>c</mi>", next(iter(new_math.values()))["mathml"])
        self.assertNotEqual(old_math, new_math)

    def test_source_line_wrapping_is_whitespace_and_explicit_breaks_are_retained(self):
        self.assertEqual(inline("Eit langt\navsnitt", {}), "Eit langt avsnitt")
        self.assertEqual(inline(r"Eit langt\newline{}avsnitt", {}), "Eit langt\navsnitt")
        tokens, _, _ = parse_latex("Eit% comment\navsnitt")
        self.assertEqual(tokens[0]["text"], "Eitavsnitt")

    def test_unknown_or_unbalanced_source_fails_instead_of_diverging(self):
        for fragment in (r"\input{secret}", r"\emph{unfinished", r"\(\write{18}\)", r"a_b", r"\(a+b"):
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                inline(fragment, {})
        with self.assertRaisesRegex(ValueError, "Nested"):
            parse_latex(r"\begin{formproposition}{1}{d}\section{Oops}\end{formproposition}")

    def test_explicit_citations_notes_and_comments_keep_their_meaning(self):
        tokens, props, _ = parse_latex(r"""% comment
\section{Føreord}
Ein tekst\notat{intro-1}. 50\%.
\begin{formproposition}{1}{d}
\textbf{Form}.\kjelder{1,3}% ignored
\end{formproposition}
""")
        self.assertEqual(tokens[1]["text"], "Ein tekst[[notat:intro-1]]. 50%.")
        self.assertEqual(props[0]["paragraphs"], ["**Form**.[[kjelde:1,3]]"])


class ShortLatexFreshness(unittest.TestCase):
    def test_editing_short_tex_invalidates_committed_html(self):
        from render_kortversjon import short_source_hash, require_fresh_short, stamped_html
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nettstad").mkdir()
            source = root / "nettstad/kortversjon.tex"
            source.write_text("first manuscript")
            content = "<!-- form-source: " + short_source_hash(root) + " -->\n<p>First page.</p>"
            (root / "nettstad/kortversjon.html").write_bytes(stamped_html(content))
            require_fresh_short(root)
            source.write_text("changed manuscript")
            with self.assertRaisesRegex(ValueError, "stale"):
                require_fresh_short(root)

    def test_mathml_alignment_is_preserved_and_error_nodes_are_rejected(self):
        markup = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mtable><mtr><mtd columnalign="right" style="text-align: right"><mi>a</mi></mtd></mtr></mtable></math>'
        normalized = validate_mathml(markup)
        self.assertIn('columnalign="right"', normalized)
        self.assertNotIn('style=', normalized)
        with self.assertRaisesRegex(ValueError, "error"):
            validate_mathml('<math xmlns="http://www.w3.org/1998/Math/MathML"><merror>invalid</merror></math>')


class ShortEditionIntegrity(unittest.TestCase):
    def setUp(self):
        import render_kortversjon
        self.renderer = render_kortversjon
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "nettstad").mkdir()
        self.source = self.root / "nettstad/kortversjon.tex"
        self.source.write_text(r"\begin{document}First manuscript.\end{document}", encoding="utf-8")
        self.target = self.root / "nettstad/kortversjon.html"
        self.body = "<p>Converted manuscript.</p>" + '<math><mi>a</mi></math>' * 35
        self.success = subprocess.CompletedProcess(["pandoc"], 0, stdout=self.body, stderr="")
        with patch.object(self.renderer.subprocess, "run", return_value=self.success):
            self.renderer.render_short(self.root)
        self.previous = self.target.read_bytes()

    def assert_previous_preserved(self):
        self.assertEqual(self.target.read_bytes(), self.previous)
        self.assertFalse(list(self.target.parent.glob(".kortversjon-*.tmp")))

    def test_verified_generated_page_needs_no_converter_for_publication(self):
        with patch.object(self.renderer.subprocess, "run", side_effect=AssertionError("Publication must not need Pandoc")):
            self.renderer.require_fresh_short(self.root)

    def test_body_wrapper_and_truncation_cannot_keep_a_valid_source_stamp(self):
        for modified in (
            self.previous.replace(b"Converted manuscript.", b"Manually edited content."),
            self.previous.replace("<title>formlære".encode("utf-8"), "<title>feil formlære".encode("utf-8")),
            self.previous.split(b"<p>Converted manuscript.")[0],
        ):
            with self.subTest(modified=modified[:70]):
                self.target.write_bytes(modified)
                with self.assertRaisesRegex(ValueError, "stale or modified"):
                    self.renderer.require_fresh_short(self.root)

    def test_missing_or_duplicate_generation_markers_are_rejected(self):
        source_stamp = self.renderer.SOURCE_STAMP.search(self.previous)[0]
        output_stamp = self.renderer.OUTPUT_STAMP.search(self.previous)[0]
        for modified in (
            self.previous.replace(output_stamp, b""),
            self.previous + source_stamp,
            self.previous + output_stamp,
        ):
            self.target.write_bytes(modified)
            with self.assertRaisesRegex(ValueError, "stale or modified"):
                self.renderer.require_fresh_short(self.root)

    def test_source_edit_during_conversion_preserves_previous_page(self):
        def convert_then_edit(*args, **kwargs):
            self.assertIn("First manuscript.", kwargs["input"])
            self.source.write_text(r"\begin{document}New manuscript.\end{document}", encoding="utf-8")
            return self.success

        with patch.object(self.renderer.subprocess, "run", side_effect=convert_then_edit):
            with self.assertRaisesRegex(ValueError, "source changed during rendering"):
                self.renderer.render_short(self.root)
        self.assert_previous_preserved()

    def test_renderer_edit_during_conversion_preserves_previous_page(self):
        original_read = Path.read_bytes
        changed = False

        def read_snapshot(path):
            data = original_read(path)
            return data + b"\n# Renderer changed.\n" if changed and path == Path(self.renderer.__file__) else data

        def convert_then_edit(*args, **kwargs):
            nonlocal changed
            changed = True
            return self.success

        with patch.object(Path, "read_bytes", read_snapshot), patch.object(self.renderer.subprocess, "run", side_effect=convert_then_edit):
            with self.assertRaisesRegex(ValueError, "source changed during rendering"):
                self.renderer.render_short(self.root)
        self.assert_previous_preserved()

    def test_converter_or_invalid_output_failure_preserves_previous_page(self):
        with patch.object(self.renderer.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "pandoc")):
            with self.assertRaises(subprocess.CalledProcessError):
                self.renderer.render_short(self.root)
        self.assert_previous_preserved()
        invalid = subprocess.CompletedProcess(["pandoc"], 0, stdout="<p>No mathematics.</p>", stderr="")
        with patch.object(self.renderer.subprocess, "run", return_value=invalid):
            with self.assertRaisesRegex(ValueError, "lost its mathematical"):
                self.renderer.render_short(self.root)
        self.assert_previous_preserved()

    def test_failed_install_keeps_previous_html_and_removes_temporary_file(self):
        replace = Path.replace

        def failed_install(path, destination):
            if Path(destination) == self.target:
                raise OSError("HTML replacement failed")
            return replace(path, destination)

        with patch.object(self.renderer.subprocess, "run", return_value=self.success), patch.object(Path, "replace", failed_install):
            with self.assertRaisesRegex(OSError, "HTML replacement failed"):
                self.renderer.render_short(self.root)
        self.assert_previous_preserved()


if __name__ == "__main__":
    unittest.main()
