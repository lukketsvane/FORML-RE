import re
import unittest
from fractions import Fraction
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "tekst" / "formlaere.tex").read_text(encoding="utf-8")


def proposition(number):
    pattern = re.compile(
        r"\\begin\{formproposition\}\{" + re.escape(number)
        + r"\}\{[^}]+\}(.*?)\\end\{formproposition\}", re.S
    )
    matches = pattern.findall(SOURCE)
    if len(matches) != 1:
        raise AssertionError(number)
    return matches[0]


class ClaimConsistency(unittest.TestCase):
    def test_cardinality(self):
        self.assertEqual(SOURCE.count(r"\begin{formproposition}"), 488)

    def test_6673_free_not_normalized(self):
        text = proposition("6.673")
        self.assertIn("Meir fri vekt", text)
        self.assertIn("Summerer omhugsvektene seg til 1", text)
        self.assertIn("kovariansen mellom estimatet og skilnaden", text)
        self.assertIn("kan stige", text)
        self.assertNotIn("Meir prioritering kan ikkje", text)

    def test_6711_free_not_care_transfer(self):
        text = proposition("6.711")
        self.assertEqual(text.count("meir fri vekt på biletet"), 2)
        self.assertNotIn("meir omsorg", text)

    def test_6614_fixed_base_distribution(self):
        text = proposition("6.614")
        self.assertIn(r"forholdet mellom grunnvektene \(\mu_{SG}(x)/\mu_{SG}(y)\) står fast", text)
        self.assertIn("annleis enn det flyttar forholdet mellom grunnvektene deira", text)

    def test_672_predicted_not_actual_harm(self):
        text = proposition("6.72")
        self.assertIn("estimert skade", text)
        self.assertIn("langs estimat eller bilete utan vekt", text)
        self.assertIn("Faktisk skade kan stå att", text)
        self.assertIn("når estimatet ordnar formene feil", text)

    def test_normalized_weight_counterexample(self):
        def expected(weight):
            mass = Fraction(1, 2) ** (8 - 4 * weight)
            return 4 * mass / (1 + mass)
        self.assertLess(expected(Fraction(1, 4)), expected(Fraction(1, 2)))
        self.assertEqual(expected(Fraction(1, 4)), Fraction(4, 129))
        self.assertEqual(expected(Fraction(1, 2)), Fraction(4, 65))


if __name__ == "__main__":
    unittest.main()
