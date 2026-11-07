"""Fire syntetiske prøver av identifiserbarheit i Formlæra §6.665.

Dette er lineær-algebraiske kontrollar, ikkje empiriske valresultat.
Krev NumPy.
"""
import unittest
import numpy as np


def probability(mu, estimated, beta, weights):
    theta = beta * np.asarray(weights, dtype=float)
    raw = np.asarray(mu, dtype=float) * np.exp(-np.asarray(estimated) @ theta)
    return raw / raw.sum()


def inverse(mu, estimated, p):
    values = np.asarray(estimated)
    X = values[1:] - values[0]
    g = -np.log((p[1:] / p[0]) / (mu[1:] / mu[0]))
    return np.linalg.matrix_rank(X), np.linalg.lstsq(X, g, rcond=None)[0]


class RankTests(unittest.TestCase):
    def setUp(self):
        self.mu = np.array([0.1, 0.2, 0.3, 0.4])
        self.est = np.array([[0, 0], [1, 0], [2, 1], [0, 3]], dtype=float)
        self.beta = 1.7
        self.weights = np.array([0.35, 0.65])

    def test_full_rank_identifies_strength_and_weights(self):
        p = probability(self.mu, self.est, self.beta, self.weights)
        rank, theta = inverse(self.mu, self.est, p)
        self.assertEqual(rank, 2)
        self.assertAlmostEqual(theta.sum(), self.beta, places=12)
        self.assertTrue(np.allclose(theta / theta.sum(), self.weights))

    def test_collinear_estimates_cannot_separate_influence(self):
        estim = np.column_stack((self.est[:, 0], 2*self.est[:, 0]))
        a, b = np.array([0.595, 1.105]), np.array([2.805, 0.0])
        p_a = self.mu * np.exp(-estim @ a); p_a /= p_a.sum()
        p_b = self.mu * np.exp(-estim @ b); p_b /= p_b.sum()
        self.assertEqual(np.linalg.matrix_rank(estim[1:]-estim[0]), 1)
        self.assertTrue(np.allclose(p_a, p_b))
        self.assertFalse(np.allclose(a, b))

    def test_zero_beta_has_no_information_about_weights(self):
        for w in ([0.1, 0.9], [0.8, 0.2], [0.5, 0.5]):
            self.assertTrue(np.allclose(
                probability(self.mu, self.est, 0.0, w), self.mu/self.mu.sum()
            ))

    def test_alternatives_must_outnumber_agent_dimensions(self):
        E = np.array([[0, 0, 0], [1, 1, 0], [2, 0, 1]], dtype=float)
        self.assertLess(np.linalg.matrix_rank(E[1:]-E[0]), E.shape[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
