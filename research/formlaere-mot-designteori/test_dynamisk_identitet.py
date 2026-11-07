"""Endelege motprøver av dynamikk og seleksjonsodds i §§6.666–6.667.

Matematiske kontrollar. INGEN empirisk validering. Krev numpy.
"""
from math import log, isclose
import unittest
import numpy as np


def gibbs(mu, phi, beta):
    weights = np.array(mu, dtype=float)
    energies = np.array(phi, dtype=float)
    logweights = np.log(weights) - beta * energies
    logweights -= logweights.max()
    z = np.exp(logweights)
    return z / z.sum()


class SameMarginalDifferentDynamics(unittest.TestCase):
    def setUp(self):
        self.pi = np.array([0.7, 0.3])
        self.T = np.array([[0.85, 0.15], [0.35, 0.65]])

    def test_stationary_distribution_identical_with_different_kernels(self):
        self.assertTrue(np.allclose(self.pi @ self.T, self.pi))
        for alpha in [0.04, 0.1, 0.25, 0.75, 1.0]:
            T_alpha = (1-alpha)*np.eye(2) + alpha*self.T
            self.assertTrue(np.allclose(T_alpha.sum(axis=1), 1))
            self.assertTrue(np.allclose(self.pi @ T_alpha, self.pi))
            self.assertEqual(np.allclose(T_alpha, self.T), alpha == 1)

    def test_first_hitting_time_scales_inversely_with_alpha(self):
        t = 1/self.T[0, 1]
        for alpha in [0.05, 0.1, 0.5, 1.0]:
            Ta = (1-alpha)*np.eye(2) + alpha*self.T
            self.assertTrue(isclose(1/Ta[0, 1], t/alpha, rel_tol=1e-12))

    def test_serial_dependence_not_identified_by_stationary_pi(self):
        Ta = 0.9*np.eye(2) + 0.1*self.T
        self.assertGreater(Ta[0, 0], self.T[0, 0])


class PairwiseOddsInvariant(unittest.TestCase):
    def setUp(self):
        self.mu = np.array([0.1, 0.3, 0.6])
        self.phi = np.array([1.9, 0.2, 2.8])

    def test_pairwise_log_odds_exactly_linear_in_beta(self):
        x, y = 0, 1
        slope = -(self.phi[x]-self.phi[y])
        intercept = log(self.mu[x]/self.mu[y])
        for beta in [0, 0.2, 1, 2]:
            p = gibbs(self.mu, self.phi, beta)
            self.assertTrue(isclose(log(p[x]/p[y]), intercept + beta*slope, abs_tol=1e-12))

    def test_log_odds_second_difference_zero_for_fixed_landscape(self):
        f = lambda b: log(gibbs(self.mu, self.phi, b)[0]/gibbs(self.mu, self.phi, b)[1])
        h = 0.2
        for b in [0.3, 0.7, 1.2]:
            self.assertAlmostEqual(f(b+h)-2*f(b)+f(b-h), 0, places=12)

    def test_controlled_beta_difference_cancels_the_generator(self):
        b1, b2 = 0.5, 1.4
        p1, p2 = gibbs(self.mu, self.phi, b1), gibbs(self.mu, self.phi, b2)
        for x, y in [(0,1),(0,2),(1,2)]:
            actual = log(p2[x]/p2[y]) - log(p1[x]/p1[y])
            expected = -(b2-b1)*(self.phi[x]-self.phi[y])
            self.assertTrue(isclose(actual, expected, abs_tol=1e-12))


if __name__ == "__main__":
    unittest.main(verbosity=2)
