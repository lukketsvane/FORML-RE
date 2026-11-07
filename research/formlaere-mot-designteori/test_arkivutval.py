"""Six synthetic algebra checks for FORMLÆRE §6.668 (archive observation).

These are mathematical consistency checks, not historical or empirical
validation of real archive-inclusion probabilities.
"""
import unittest
import math


def normalize(a):
    s = sum(a)
    if s <= 0:
        raise ValueError("no observed support")
    return tuple(v / s for v in a)


def world(mu, phi, beta):
    return normalize([m * math.exp(-beta * v) for m, v in zip(mu, phi)])


def observed(p, r):
    return normalize([v * s for v, s in zip(p, r)])


class ArchiveSelectionTests(unittest.TestCase):
    def setUp(self):
        self.mu = (0.2, 0.3, 0.5)
        self.phi = (0.0, 1.0, 2.0)
        self.beta = 1.4
        self.p = world(self.mu, self.phi, self.beta)
        self.r = (0.2, 0.5, 0.9)

    def test_observed_matches_effective_energy(self):
        q = observed(self.p, self.r)
        phi_obs = [v - math.log(t) / self.beta for v, t in zip(self.phi, self.r)]
        predicted = world(self.mu, phi_obs, self.beta)
        self.assertTrue(all(math.isclose(a, b, abs_tol=1e-13) for a, b in zip(q, predicted)))

    def test_archive_observation_does_not_identify_world(self):
        q = observed(self.p, self.r)
        world2, selection2 = q, (1.0, 1.0, 1.0)
        self.assertTrue(all(math.isclose(a, b, abs_tol=1e-13)
                            for a, b in zip(q, observed(world2, selection2))))
        self.assertFalse(all(math.isclose(a, b, abs_tol=1e-5)
                             for a, b in zip(self.p, world2)))

    def test_known_positive_inclusion_recovers_world(self):
        q = observed(self.p, self.r)
        recovered = normalize([v / t for v, t in zip(q, self.r)])
        self.assertTrue(all(math.isclose(a, b, abs_tol=1e-13)
                            for a, b in zip(self.p, recovered)))

    def test_zero_capture_erases_possible_form(self):
        q = observed(self.p, (0.0, 0.5, 0.9))
        self.assertGreater(self.p[0], 0.0)
        self.assertEqual(q[0], 0.0)

    def test_beta_zero_can_still_give_nonuniform_archive(self):
        p = world(self.mu, self.phi, 0.0)
        q = observed(p, self.r)
        self.assertFalse(all(math.isclose(a, b, abs_tol=1e-6)
                             for a, b in zip(p, q)))

    def test_no_detection_at_finite_sample_is_not_impossibility(self):
        p, n = 0.001, 100
        self.assertGreater((1 - p)**n, 0.90)


if __name__ == "__main__":
    unittest.main(verbosity=2)
