"""Finitte kontrollar av Formlære 6.6 og 6.673–6.674.

Dette er analytiske programtestar med syntetiske verdiar, ikkje empirisk
validering eller ei samanlikning med andre teoriar.
"""
from math import exp, fsum, isclose
import unittest

ESTIMATED = (0.0, 1.0, 2.0)
ACTUAL = (2.0, 1.0, 0.0)
BASE = (1.0, 1.0, 1.0)


def distribution(theta: float, estimated=ESTIMATED, base=BASE, allowed=None):
    """P_theta(x) ∝ base(x) exp(-theta * estimated(x)); veto excludes x."""
    allowed = tuple(range(len(base))) if allowed is None else tuple(allowed)
    if not allowed:
        raise ValueError("D må vere ikkje-tom")
    weights = {i: base[i] * exp(-theta * estimated[i]) for i in allowed}
    z = fsum(weights.values())
    if not z:
        raise ValueError("Ugyldig normalisering")
    return tuple(weights.get(i, 0.0) / z for i in range(len(base)))


def mean(values, probabilities):
    return fsum(v * p for v, p in zip(values, probabilities))


def covariance(x, y, probabilities):
    return mean(tuple(a * b for a, b in zip(x, y)), probabilities) - mean(x, probabilities) * mean(y, probabilities)


class ModelChecks(unittest.TestCase):
    def test_beta_zero_returns_base(self):
        self.assertEqual(distribution(0.0), (1.0 / 3.0,) * 3)

    def test_veto_removes_unreachable_position(self):
        p = distribution(1.0, allowed=(0, 1))
        self.assertEqual(p[2], 0.0)
        self.assertTrue(isclose(sum(p), 1.0))

    def test_synthetic_harm_increases_with_misleading_estimate(self):
        p0 = distribution(0.0)
        p1 = distribution(1.0)
        p2 = distribution(2.0)
        self.assertLess(mean(ESTIMATED, p2), mean(ESTIMATED, p1))
        self.assertLess(mean(ESTIMATED, p1), mean(ESTIMATED, p0))
        self.assertGreater(mean(ACTUAL, p2), mean(ACTUAL, p1))
        self.assertGreater(mean(ACTUAL, p1), mean(ACTUAL, p0))

    def test_derivative_is_negative_covariance(self):
        # Samanlikn analytisk derivasjon med sentral differanse.
        for theta in (0.0, 0.5, 2.0):
            h = 1.0e-5
            p = distribution(theta)
            numerical = (mean(ACTUAL, distribution(theta + h)) - mean(ACTUAL, distribution(theta - h))) / (2 * h)
            theoretical = -covariance(ACTUAL, ESTIMATED, p)
            self.assertAlmostEqual(numerical, theoretical, places=8)
            self.assertLess(covariance(ACTUAL, ESTIMATED, p), 0.0)

    def test_symmetric_mh_satisfies_detailed_balance(self):
        p = distribution(1.5)
        n = len(p)
        transition = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    q = 1 / (n - 1)
                    transition[i][j] = q * min(1.0, p[j] / p[i])
            transition[i][i] = 1.0 - fsum(transition[i])
        for i in range(n):
            self.assertTrue(isclose(fsum(transition[i]), 1.0, abs_tol=1e-12))
            for j in range(n):
                self.assertTrue(isclose(p[i] * transition[i][j], p[j] * transition[j][i], abs_tol=1e-12))


if __name__ == "__main__":
    unittest.main()
