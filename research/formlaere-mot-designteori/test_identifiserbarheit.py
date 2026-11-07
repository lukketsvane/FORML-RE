"""Syntetiske motprøver til Formlæra §6.6.

Desse testane viser modellgrenser og identifiserbarheit, ikkje empirisk styrke.
Køyr med: python test_identifiserbarheit.py
"""
from __future__ import annotations

from math import exp, fsum, isclose, log
import unittest


def gibbs(mu, phi, beta, allowed=None):
    """Normalisert valfordeling for eit endeleg formrom."""
    if len(mu) != len(phi) or not mu:
        raise ValueError("mu og phi må ha same positive lengd")
    if beta < 0 or not all(m > 0 for m in mu):
        raise ValueError("positiv grunnvekt og beta >= 0 er påkravde")
    allowed = set(range(len(mu))) if allowed is None else set(allowed)
    if not allowed:
        raise ValueError("D må vere ikkje-tom")
    weights = [mu[i] * exp(-beta * phi[i]) if i in allowed else 0.0 for i in range(len(mu))]
    z = fsum(weights)
    if z <= 0:
        raise ValueError("Z må vere positiv")
    return tuple(w / z for w in weights)


def saturating_landscape(target, mu, beta):
    """Eit etterpåtilpassa landskap som gjev eksakt målfordeling.

    Dette er nett grunnen til at tilpassing ikkje er ei kausal forklaring.
    """
    if not beta > 0:
        raise ValueError("beta må vere strengt positiv")
    if len(target) != len(mu) or not all(t > 0 and m > 0 for t, m in zip(target, mu)):
        raise ValueError("både target og mu må ha full positiv støtte")
    if not isclose(fsum(target), 1.0, abs_tol=1e-12):
        raise ValueError("target må vere ei sannsynsfordeling")
    return tuple(-log(t / m) / beta for t, m in zip(target, mu))


class StructuralCountertests(unittest.TestCase):
    def test_friteftertilpassa_landskap_kan_imitere_alle_positive_fordelingar(self):
        target = (0.08, 0.17, 0.21, 0.54)
        mu = (0.4, 0.3, 0.2, 0.1)
        beta = 1.7
        phi = saturating_landscape(target, mu, beta)
        for actual, expected in zip(gibbs(mu, phi, beta), target):
            self.assertAlmostEqual(actual, expected, places=12)

    def test_skalaen_beta_gonger_phi_er_ikkje_identifiserbar(self):
        mu = (1.0, 2.0, 3.0)
        phi = (0.1, 0.6, 1.3)
        p1 = gibbs(mu, phi, 2.0)
        p2 = gibbs(mu, tuple(x / 5.0 for x in phi), 10.0)
        self.assertTrue(all(isclose(a, b, abs_tol=1e-12) for a, b in zip(p1, p2)))

    def test_konstant_tillegg_til_phi_flyttar_berre_normaliseringa(self):
        mu = (1.0, 2.0, 3.0)
        phi = (0.1, 0.6, 1.3)
        p1 = gibbs(mu, phi, 2.0)
        p2 = gibbs(mu, tuple(x + 200.0 for x in phi), 2.0)
        self.assertTrue(all(isclose(a, b, abs_tol=1e-12) for a, b in zip(p1, p2)))

    def test_grunnfordeling_og_landskap_kan_bytte_effekt(self):
        # mu'(x) = mu(x)*exp(h(x)); phi'(x)=phi(x)+h(x)/beta.
        # Same observerte P trass ulik generativ grunnvekt/landskap.
        mu = (1.0, 2.0, 3.0)
        phi = (0.2, 0.5, 0.9)
        h = (0.0, 0.2, -0.3)
        beta = 1.5
        tilted = tuple(m * exp(x) for m, x in zip(mu, h))
        corrected = tuple(x + hi / beta for x, hi in zip(phi, h))
        p1 = gibbs(mu, phi, beta)
        p2 = gibbs(tilted, corrected, beta)
        self.assertTrue(all(isclose(a, b, abs_tol=1e-12) for a, b in zip(p1, p2)))

    def test_materielt_mogleg_men_normativt_utestengt_er_ikkje_fysisk_veto(self):
        mu = (1.0, 1.0, 1.0)
        phi = (0.0, 0.0, 0.0)
        material = {0, 1, 2}
        admissible_by_legitimate_decision = {0, 1}
        p_physical = gibbs(mu, phi, 1.0, material)
        p_decision = gibbs(mu, phi, 1.0, material & admissible_by_legitimate_decision)
        self.assertGreater(p_physical[2], 0.0)
        self.assertEqual(p_decision[2], 0.0)
        # Alternativ 2 forsvann frå vedtaket, ikkje frå naturens moglegheiter.

    def test_stasjonær_gammal_grammatikk_kan_ikkje_gje_sannsyn_til_ny_form(self):
        old_distribution = gibbs((1.0, 1.0), (0.0, 0.0), 1.0)
        self.assertEqual(len(old_distribution), 2)
        new_distribution = gibbs((1.0, 1.0, 1.0), (0.0, 0.0, -1.0), 1.0)
        self.assertEqual(len(new_distribution), 3)
        self.assertGreater(new_distribution[2], 0.0)
        # Overgangen til større rom er ein ekstra modellert operasjon.

    def test_tidsvariasjon_krev_ei_tidsforklaring(self):
        # To aktørar prioriterer motsatt. Kven som har innverknad
        # varierer over tid. Tida er ikkje årsak; den endra vekta er det.
        mu = (1.0, 1.0)
        e_a = (0.0, 2.0)
        e_b = (2.0, 0.0)
        def model(wa):
            phi = tuple(wa*a + (1-wa)*b for a, b in zip(e_a, e_b))
            return gibbs(mu, phi, beta=2.0)
        p_first, p_last = model(0.9), model(0.1)
        self.assertGreater(p_first[0], p_first[1])
        self.assertLess(p_last[0], p_last[1])
        # Ein modell med faste weights+estimat kan ikkje føreseie
        # begge desse fordelingsskifta utan eit nytt forklaringsledd.


if __name__ == "__main__":
    unittest.main(verbosity=2)
