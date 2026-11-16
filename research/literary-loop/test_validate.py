import unittest
from pathlib import Path

from validate import TEXT, check

ORIGINAL = TEXT.read_text(encoding="utf-8")


class LiteraryInvariants(unittest.TestCase):
    def test_unchanged_canon(self):
        self.assertEqual(check(ORIGINAL, ORIGINAL)["count"], 0)

    def test_change_plain_prose_allowed(self):
        old = "Dette tomrommet vert halde oppe av to sirkelslutningar."
        self.assertIn(old, ORIGINAL)
        with self.assertRaisesRegex(ValueError, "outside propositions"):
            check(ORIGINAL, ORIGINAL.replace(old, old + " Ny prosa.", 1))

    def test_math_cannot_move(self):
        target = r"\(\beta\Phi(x)"
        self.assertIn(target, ORIGINAL)
        with self.assertRaisesRegex(ValueError, "Mathematics altered"):
            check(ORIGINAL, ORIGINAL.replace(target, r"\(\Phi(x)", 1))

    def test_citations_cannot_disappear(self):
        import re
        m = re.search(r"\\begin\{formproposition\}.*?\\kjelder\{\d+[^}]*\}", ORIGINAL, re.S)
        self.assertIsNotNone(m)
        token = re.search(r"\\kjelder\{[^}]+\}", m.group()).group()
        text = ORIGINAL[:m.start()] + m.group().replace(token, "", 1) + ORIGINAL[m.end():]
        with self.assertRaisesRegex(ValueError, "Citations altered"):
            check(ORIGINAL, text)

    def test_no_extra_proposition(self):
        old = r"\begin{formproposition}{1.01}{d}"
        self.assertIn(old, ORIGINAL)
        with self.assertRaisesRegex(ValueError, "491 proposition"):
            check(ORIGINAL, ORIGINAL.replace(old, old.replace("{1.01}", "{1.0100}"), 1))


if __name__ == "__main__":
    unittest.main()
