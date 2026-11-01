"""The editable TeX manuscript must drive both renderers without content loss."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

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
            renderer = Renderer({"schemaVersion": 1, "props": props, "sources": [{"id": "1"}], "notes": [], "mathematics": math})
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
        from render_kortversjon import short_source_hash, require_fresh_short
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nettstad").mkdir()
            source = root / "nettstad/kortversjon.tex"
            source.write_text("first manuscript")
            (root / "nettstad/kortversjon.html").write_text("<!-- form-source: " + short_source_hash(root) + " -->")
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


if __name__ == "__main__":
    unittest.main()
