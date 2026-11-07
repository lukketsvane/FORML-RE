"""Fem syntetiske kontrollar av §6.663–6.664 (ikkje empiriske funn)."""
from math import exp, log, fsum
import unittest


def dist(mu, phi, beta, allowed=None):
    allowed = set(range(len(mu))) if allowed is None else set(allowed)
    if not allowed or not all(mu[i] > 0 for i in allowed):
        raise ValueError("D må vere ikkje-tom med positive grunnvekter")
    raw = [mu[i] * exp(-beta * phi[i]) if i in allowed else 0.0 for i in range(len(mu))]
    z = fsum(raw)
    return tuple(v / z for v in raw)


def mean(values, p):
    return fsum(v * mass for v, mass in zip(values, p))


def variance(values, p):
    e = mean(values, p)
    return fsum(mass * (v - e)**2 for v, mass in zip(values, p))


def kl(p, mu):
    return fsum(x * log(x / y) for x, y in zip(p, mu) if x > 0)


def entropy(p):
    return -fsum(x * log(x) for x in p if x > 0)


class InformationTests(unittest.TestCase):
    def test_mean_landscape_slope(self):
        mu, phi, h = (0.5, 0.3, 0.2), (0.3, 1.2, 1.7), 1e-5
        for b in (0.0, 0.3, 1.8):
            numerical = (mean(phi, dist(mu, phi, b+h)) - mean(phi, dist(mu, phi, b-h))) / (2*h)
            self.assertAlmostEqual(numerical, -variance(phi, dist(mu, phi, b)), places=8)

    def test_kl_slope(self):
        mu, phi, h = (0.5, 0.3, 0.2), (0.3, 1.2, 1.7), 1e-5
        for b in (0.3, 1.8):
            numerical = (kl(dist(mu, phi, b+h), mu) - kl(dist(mu, phi, b-h), mu)) / (2*h)
            self.assertAlmostEqual(numerical, b * variance(phi, dist(mu, phi, b)), places=8)

    def test_plain_entropy_can_increase(self):
        mu, phi = (0.95, 0.05), (1.0, 0.0)
        self.assertLess(entropy(dist(mu, phi, 0.0)), entropy(dist(mu, phi, log(19))))
        self.assertAlmostEqual(dist(mu, phi, log(19))[0], 0.5, places=10)

    def test_support_requires_independent_veto(self):
        mu, phi = (0.3, 0.2, 0.5), (100.0, 3.0, 0.0)
        self.assertGreater(dist(mu, phi, 1.0)[0], 0.0)
        self.assertEqual(dist(mu, phi, 1.0, allowed=(1, 2))[0], 0.0)

    def test_kl_zero_at_beta_zero(self):
        mu, phi = (0.2, 0.3, 0.5), (1.0, 2.0, 0.0)
        self.assertAlmostEqual(kl(dist(mu, phi, 0.0), mu), 0.0, places=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
