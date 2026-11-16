#!/usr/bin/env python3
"""AutoResearch 004: frosne kontrollar for rettingane i formlaere.tex (sak #32).

Fila vart skriven og køyrd mot urørt manuskript (commit ead4959) før nokon
proposisjon vart endra. Kriteria under er ikkje justerte etterpå.

Tre slag kontrollar, haldne frå kvarandre:

  STRUKTUR  491 adresser, type og rekkjefølgje. Matematiske likningar og
            kjeldemerke i dei seks granska proposisjonane er uendra.
            Litterær revisjon av andre proposisjonar er tillaten.
  FELT      Setningar som kritisk gransking 2026-11 og AutoResearch 003 alt har
            felt med motdøme, skal ikkje stå att. Denne testen feilar på
            baseline; det er det negative kontrolltilfellet for teksten.
  REKNING   Eksakt rasjonal aritmetikk (fractions, heiltalseksponentar med
            grunntal 2, ingen flyttal, ingen frø). Kvar klasse har (a) eksakte
            motdøme mot den gamle formuleringa, (b) uttømmande kontroll av den
            nye formuleringa over ein fastsett endeleg familie, og ein negativ
            kontroll: den naive påstanden må gje brot i same familie, elles kan
            kontrollen ikkje skilje formuleringane.

Rekninga les ikkje manuskriptet, og manuskriptkontrollen krev ikkje at den nye
ordlyden står der. Grøn test provar difor ikkje at ordlyden er rett; han seier
at motdøma og dei endelege familiane oppfører seg slik loggen
revisjon/autoresearch-004-retting.md hevdar. Ingen empiri.
"""

import hashlib
import itertools
import re
import unittest
from fractions import Fraction as F
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
MANUS = ROT / "tekst" / "formlaere.tex"
PROP = re.compile(r"\\begin\{formproposition\}\{([^}]*)\}\{([a-z])\}\n(.*?)\n\\end\{formproposition\}", re.S)
LIKNING = re.compile(r"\\\[.*?\\\]", re.S)
KJELDE = re.compile(r"\\kjelder\{[^}]*\}")

# ---------------------------------------------------------------- frosne verdiar
TAL = 491
FORDELING = {"1": 118, "2": 27, "3": 20, "4": 16, "5": 145, "6": 112, "7": 53}
OPNE = ("6.614", "6.673", "6.674", "6.711", "6.72", "7.1521")
LEGACY_ADRESSE_SHA = "323dd4c1296bda31587c21584401193070fc6e0cb1182e48263617c254258d2a"
ADRESSE_SHA = "94eee2e195dd239d754965173be035e7b551b1d51d9fa91889452e7d490ab663"
LIKNING_SHA = {
    "6.614": "02b9d35b7df25e77b268ce9cac11a74bfcc2edc152eadc4e5ffa700551367f56",
    "6.673": "1ab47a9a2c99d9c56a8f0a0b2a4e4b048fac67bd640fb8ad563e84f658038fcb",
    "6.674": "701c9e4f71a2b69d08971a1315099c1868479c34d4134ac474590ff30076461a",
    "6.711": "cd7494cf16312f59d793052d101e9f002d8e0716cf2fa9477616538500952ace",
    "6.72": "a0eff8bee04fbd29c2e461a5bf7aa4a371036805dd75e26fe2729849d23e7fbb",
    "7.1521": "c23e3a9e4454b39a6e56c3e85cfc602a40d77daba73c07cbb4649f03582fb304",
}
FELTE = (
    ("6.614", "Forholdet mellom sannsyna for to former avheng ikkje av kva andre former som finst:"),
    ("6.614", "Flyttar eit nytt alternativ forholdet mellom to gamle, held ikkje modellen."),
    ("6.673", "Meir prioritering kan ikkje auke det estimerte avviket langs same omsyn."),
    ("6.674", "Meir prioritering betrar det faktiske utfallet"),
    ("6.711", "kan meir omsorg ikkje"),
    ("6.72", "står skade som ingen vinn på, berre att der målet er utan vekt"),
    ("7.1521", "Meir prioritering av eit estimat som ordnar formene rett, kan ikkje auke sviktrisikoen."),
)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def les():
    return MANUS.read_text(encoding="utf-8")


def proposisjonar(tekst):
    return [(m.group(1), m.group(2), m.group(3)) for m in PROP.finditer(tekst)]


def adresse_sha(tekst):
    return sha("\n".join(f"{n}\t{t}" for n, t, _ in proposisjonar(tekst)))


def likning_sha(kropp):
    return sha("\n".join(LIKNING.findall(kropp) + KJELDE.findall(kropp)))


# ---------------------------------------------------------------- eksakt rekning
def heiltal(x):
    x = F(x)
    if x.denominator != 1:
        raise ValueError("eksponenten må vere eit heiltal: %s" % x)
    return x.numerator


def vekter(mu, eksp):
    """Heiltal proporsjonale med mu(x) * 2^(-eksp(x))."""
    e = [heiltal(x) for x in eksp]
    topp = max(e)
    return [m * (1 << (topp - x)) for m, x in zip(mu, e)]


def forv(v, f):
    return F(sum(a * F(b) for a, b in zip(v, f)), sum(v))


def kov(v, f, g):
    return forv(v, [F(a) * F(b) for a, b in zip(f, g)]) - forv(v, f) * forv(v, g)


def lin(*ledd):
    n = len(ledd[0][1])
    return [sum(F(c) * F(vec[i]) for c, vec in ledd) for i in range(n)]


def stig(v):
    return any(b > a for a, b in zip(v, v[1:]))


def fell(v):
    return any(b < a for a, b in zip(v, v[1:]))


def los(A, b):
    """Eksakt Gauss-eliminasjon. Kastar ZeroDivisionError ved singulær matrise."""
    n = len(A)
    M = [[F(x) for x in rad] + [F(y)] for rad, y in zip(A, b)]
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            raise ZeroDivisionError("singulær")
        M[k], M[p] = M[p], M[k]
        piv = M[k][k]
        M[k] = [x / piv for x in M[k]]
        for i in range(n):
            if i != k and M[i][k] != 0:
                f = M[i][k]
                M[i] = [a - f * c for a, c in zip(M[i], M[k])]
    return [M[i][n] for i in range(n)]


TRI = list(itertools.product((0, 1, 2), repeat=3))
BIN3 = list(itertools.product((0, 1), repeat=3))
GRUNN3 = ((1, 1, 1), (1, 2, 5), (7, 1, 1))


class Struktur(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tekst = les()
        cls.props = proposisjonar(cls.tekst)
        cls.kropp = {n: k for n, _, k in cls.props}

    def test_491_adresser_type_og_rekkjefolgje(self):
        self.assertEqual(len(self.props), TAL)
        self.assertEqual(len(self.kropp), TAL)
        self.assertEqual(self.tekst.count("\\begin{formproposition}"), TAL)
        self.assertEqual(self.tekst.count("\\end{formproposition}"), TAL)
        teljing = {}
        for n, _, _ in self.props:
            teljing[n.split(".")[0]] = teljing.get(n.split(".")[0], 0) + 1
        self.assertEqual(teljing, FORDELING)
        self.assertEqual(adresse_sha(self.tekst), ADRESSE_SHA)

    def test_likningar_og_kjeldemerke_er_urorte(self):
        for n in OPNE:
            with self.subTest(n):
                self.assertEqual(likning_sha(self.kropp[n]), LIKNING_SHA[n])

    def test_felte_setningar_er_borte(self):
        # Feilar på baseline (negativ kontroll for teksten).
        for n, setning in FELTE:
            with self.subTest(n + ": " + setning[:40]):
                self.assertNotIn(setning, self.kropp[n])


class Vektforskyving(unittest.TestCase):
    """6.673, 6.674, 7.1521: fri vekt mot flytting under sum 1."""

    def test_e1_eksakt(self):
        mu, lk, lm = (1, 1), (0, 4), (0, 8)
        bunden = [forv(vekter(mu, lin((F(q, 4), lk), (1 - F(q, 4), lm))), lk) for q in range(5)]
        self.assertEqual(bunden, [F(4, 257), F(4, 129), F(4, 65), F(4, 33), F(4, 17)])
        fri = [forv(vekter(mu, lin((F(q, 4), lk), (F(3, 4), lm))), lk) for q in range(1, 5)]
        self.assertEqual(fri, [F(4, 129), F(4, 257), F(4, 513), F(4, 1025)])
        v = vekter(mu, lin((F(1, 4), lk), (F(3, 4), lm)))
        self.assertEqual(kov(v, lk, lk), F(2048, 16641))
        self.assertEqual(kov(v, lk, lm), F(4096, 16641))
        d = [a - b for a, b in zip(lk, lm)]
        # 6.6742 med estimatet i staden for e_j: forteiknet er -(Var - Cov) = -Cov(lk, lk - lm) > 0.
        self.assertEqual(-kov(v, lk, d), F(2048, 16641))

    def test_fri_vekt_kan_ikkje_auke(self):
        brot = brot_risiko = brot_transform = feilvendt = n = 0
        for mu in GRUNN3:
            for lk in TRI:
                ind = [1 if a > 1 else 0 for a in lk]      # 1[e > toleranse] når e = lk
                kvadrat = [a * a for a in lk]              # faktisk avvik ordna som estimatet
                omvendt = [2 - a for a in lk]              # estimatet er feilvendt
                for lm in TRI:
                    for tm in (0, 2):
                        vs = [vekter(mu, lin((tk, lk), (tm, lm))) for tk in range(4)]
                        n += 1
                        brot += stig([forv(v, lk) for v in vs])
                        brot_risiko += stig([forv(v, ind) for v in vs])
                        brot_transform += stig([forv(v, kvadrat) for v in vs])
                        feilvendt += stig([forv(v, omvendt) for v in vs])
        self.assertEqual(n, 4374)
        self.assertEqual(brot, 0)            # 6.673, første setning
        self.assertEqual(brot_transform, 0)  # 6.674/6.6741 med rett ordna estimat
        self.assertEqual(brot_risiko, 0)     # 7.1521 med rett ordna estimat
        self.assertGreater(feilvendt, 0)     # «eit feilvendt estimat kan»

    def test_bunden_vekt_negativ_kontroll(self):
        naiv = naiv_risiko = differanse = n = 0
        for mu in GRUNN3:
            for lk in TRI:
                ind = [1 if a > 1 else 0 for a in lk]
                for lm in TRI:
                    d = [a - b for a, b in zip(lk, lm)]
                    vs = [vekter(mu, lin((q, lk), (4 - q, lm))) for q in range(5)]
                    n += 1
                    naiv += stig([forv(v, lk) for v in vs])
                    naiv_risiko += stig([forv(v, ind) for v in vs])
                    differanse += stig([forv(v, d) for v in vs])
        self.assertEqual(n, 2187)
        self.assertGreater(naiv, 0)          # den gamle setninga i 6.673/6.674 held ikkje under sum 1
        self.assertGreater(naiv_risiko, 0)   # den gamle setninga i 7.1521 held ikkje under sum 1
        self.assertEqual(differanse, 0)      # E[lk - lm] stig aldri ved flytting m -> k

    def test_to_tilstandar_forteiknsregel(self):
        # E[lk] stig ved flytting m -> k nett når avvika har same forteikn og |lm| > |lk|.
        for mu in ((1, 1), (1, 3), (5, 1)):
            for a in (-8, -4, 0, 4, 8):
                for b in (-8, -4, 0, 4, 8):
                    lk, lm = (0, a), (0, b)
                    verdiar = [forv(vekter(mu, lin((F(q, 4), lk), (1 - F(q, 4), lm))), lk) for q in range(5)]
                    ventar_stiging = a * b > 0 and abs(b) > abs(a)
                    for x, y in zip(verdiar, verdiar[1:]):
                        self.assertEqual(y > x, ventar_stiging, (mu, a, b))

    def test_beta_null(self):
        # Utan seleksjon flyttar inga omfordeling noko: «kan stige» krev beta*w > 0.
        for mu in GRUNN3:
            verdiar = {forv(vekter(mu, lin((0 * q, (0, 1, 2)), (0 * (4 - q), (2, 2, 0)))), (0, 1, 2)) for q in range(5)}
            self.assertEqual(len(verdiar), 1)


def svarkurve(v, bilete, e):
    h = {}
    for u in sorted(set(bilete)):
        idx = [i for i, b in enumerate(bilete) if b == u]
        h[u] = F(sum(v[i] * e[i] for i in idx), sum(v[i] for i in idx))
    return h


class Svarkurve(unittest.TestCase):
    """6.711: fri vekt på biletet mot omsorgsdelen gamma_A i 6.701."""

    EIGNE = ((0, 0, 0), (0, 1, 2), (2, 0, 1), (0, 2, 0))

    def test_e2_eksakt(self):
        mu, eigne, bilete = (1, 1, 1), (0, 10, 20), (0, 2, 4)
        e = bilete  # feilfritt bilete, h(u) = u
        gamma = [forv(vekter(mu, lin((1 - g, eigne), (g, bilete))), e) for g in (F(0), F(1, 2), F(1))]
        self.assertEqual(gamma, [F(684, 349867), F(44, 1387), F(4, 7)])
        fri = [forv(vekter(mu, lin((1, eigne), (t, bilete))), e) for t in range(4)]
        self.assertFalse(stig(fri))
        self.assertTrue(fell(fri))

    def test_fri_vekt_paa_biletet(self):
        flytta = brot = stigande = fallande = n = 0
        for mu in ((1, 1, 1), (1, 2, 5)):
            for eigne in self.EIGNE:
                for bilete in TRI:
                    for e in TRI:
                        vs = [vekter(mu, lin((1, eigne), (t, bilete))) for t in range(4)]
                        hs = [svarkurve(v, bilete, e) for v in vs]
                        n += 1
                        flytta += any(h != hs[0] for h in hs)
                        kurve = [hs[0][u] for u in sorted(hs[0])]
                        middel = [forv(v, e) for v in vs]
                        if not fell(kurve):
                            stigande += 1
                            brot += stig(middel)
                        if not stig(kurve):
                            fallande += 1
                            brot += fell(middel)
        self.assertEqual(n, 5832)
        self.assertEqual(flytta, 0)
        self.assertGreater(stigande, 0)
        self.assertGreater(fallande, 0)
        self.assertEqual(brot, 0)

    def test_omsorgsdelen_negativ_kontroll(self):
        flytta = mot = brot_flate_eigne = 0
        for mu in ((1, 1, 1), (1, 2, 5)):
            for eigne in self.EIGNE:
                for bilete in TRI:
                    for e in TRI:
                        vs = [vekter(mu, lin((2 - g, eigne), (g, bilete))) for g in range(3)]
                        hs = [svarkurve(v, bilete, e) for v in vs]
                        flytta += any(h != hs[0] for h in hs)
                        alle_stigande = all(not fell([h[u] for u in sorted(h)]) for h in hs)
                        if alle_stigande and stig([forv(v, e) for v in vs]):
                            mot += 1
                            brot_flate_eigne += len(set(eigne)) == 1
        self.assertGreater(flytta, 0)             # kurva flyttar seg når gamma_A endrar seg
        self.assertGreater(mot, 0)                # «meir omsorg» lesen som gamma_A held ikkje
        self.assertEqual(brot_flate_eigne, 0)     # skil ikkje eigne omsyn formene, er gamma_A ei fri vekt


def naboar(nodar, kantar):
    nab = {x: [] for x in nodar}
    for a, b in kantar:
        nab[a].append(b)
        nab[b].append(a)
    return nab


def kjerne(nodar, nab, mu, phi, beta):
    """5.7 med r_A frå 5.702 og like sannsyn for kvart ope steg."""
    T = {x: {} for x in nodar}
    for x in nodar:
        rest = F(1)
        for y in nab[x]:
            q_xy, q_yx = F(1, len(nab[x])), F(1, len(nab[y]))
            r = F(mu[y]) * q_yx / (F(mu[x]) * q_xy)
            aksept = min(F(1), r * F(2) ** (-(beta * (phi[y] - phi[x]))))
            T[x][y] = q_xy * aksept
            rest -= T[x][y]
        T[x][x] = rest
    return T


def stasjonaer(nodar, T):
    n = len(nodar)
    A = [[T[nodar[j]].get(nodar[i], F(0)) - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    A[-1] = [F(1)] * n
    return dict(zip(nodar, los(A, [F(0)] * (n - 1) + [F(1)])))


GRAFAR = (
    (("x", "y"), (("x", "y"),)),
    (("x", "y", "w"), (("x", "y"), ("y", "w"))),
    (("x", "y", "w"), (("x", "y"), ("y", "w"), ("w", "x"))),
    (("x", "y", "w", "u"), (("w", "x"), ("w", "y"), ("w", "u"))),
)


def fordeling(nodar, kantar, phi, beta, mu=None):
    """Stasjonær fordeling løyst frå kjernen, ikkje frå Gibbs-formelen."""
    nab = naboar(nodar, kantar)
    if mu is None:
        mu = {x: len(nab[x]) for x in nodar}  # 5.711
    return stasjonaer(list(nodar), kjerne(nodar, nab, mu, phi, beta)), mu


class Uavhengigheit(unittest.TestCase):
    """6.614 mot 5.711: nye alternativ og grunnvekter."""

    def test_5711_grunnfordelinga_er_talet_paa_opne_steg(self):
        for nodar, kantar in GRAFAR:
            P, mu = fordeling(nodar, kantar, {x: 0 for x in nodar}, 0)
            total = sum(mu.values())
            self.assertEqual(P, {x: F(mu[x], total) for x in nodar})

    def test_gammal_paastand_felt_i_kjeda(self):
        phi = {"x": 0, "y": 1, "z": 5}
        P, _ = fordeling(("x", "y"), (("x", "y"),), phi, 1)
        Q, _ = fordeling(("x", "y", "z"), (("x", "y"), ("x", "z")), phi, 1)
        self.assertEqual(P["x"] / P["y"], 2)
        self.assertEqual(Q["x"] / Q["y"], 4)  # dobla av z, med uendra Phi(x) og Phi(y)

    def familie(self):
        for nodar, kantar in GRAFAR:
            for slag in (0, 1):
                phi = {x: (0 if slag == 0 else (i * i + 1) % 3) for i, x in enumerate(nodar)}
                for beta in (0, 1, 2):
                    for r in range(1, len(nodar) + 1):
                        for feste in itertools.combinations(nodar, r):
                            for phi_z in (0, 2):
                                ny_phi = dict(phi, z=phi_z)
                                yield nodar, kantar, phi, beta, nodar + ("z",), kantar + tuple((a, "z") for a in feste), ny_phi

    def test_flytting_folgjer_grunnvektene(self):
        # 5.711: mu_SG = N(x). Forholdet mellom to gamle former flyttar seg nett så mykje
        # som forholdet mellom grunnvektene deira, og ikkje i det heile når det står fast.
        flytta = fast = n = 0
        for nodar, kantar, phi, beta, nodar2, kantar2, phi2 in self.familie():
            P, mu = fordeling(nodar, kantar, phi, beta)
            Q, mu2 = fordeling(nodar2, kantar2, phi2, beta)
            n += 1
            for a, b in itertools.combinations(nodar, 2):
                self.assertEqual(P[a] / P[b], F(mu[a], mu[b]) * F(2) ** (-(beta * (phi[a] - phi[b]))))
                rho_p = (Q[a] / Q[b]) / (P[a] / P[b])
                rho_mu = F(mu2[a], mu2[b]) / F(mu[a], mu[b])
                self.assertEqual(rho_p, rho_mu)
                if rho_mu == 1:
                    fast += 1
                else:
                    flytta += 1
        self.assertEqual(n, 384)
        self.assertGreater(flytta, 0)
        self.assertGreater(fast, 0)

    def test_fast_ikkje_flat_grunnfordeling(self):
        # Grunnvektene til dei gamle formene er gjevne og haldne faste (ikkje flate, ikkje N(x)).
        # Då flyttar ikkje noko nytt alternativ forholdet, kvar det enn vert festa.
        for nodar, kantar, phi, beta, nodar2, kantar2, phi2 in self.familie():
            mu = {x: 1 + 2 * i for i, x in enumerate(nodar)}
            P, _ = fordeling(nodar, kantar, phi, beta, mu)
            Q, _ = fordeling(nodar2, kantar2, phi2, beta, dict(mu, z=3))
            for a, b in itertools.combinations(nodar, 2):
                self.assertEqual(P[a] / P[b], Q[a] / Q[b])
                self.assertEqual(P[a] / P[b], F(mu[a], mu[b]) * F(2) ** (-(beta * (phi[a] - phi[b]))))


def minimum(phi):
    m = min(phi)
    return [i for i, p in enumerate(phi) if p == m]


def dominerer(est, y, x):
    return all(f[y] <= f[x] for f in est) and any(f[y] < f[x] for f in est)


class SterkSeleksjon(unittest.TestCase):
    """6.72: estimert skade, faktisk skade og kva som har vekt."""

    def test_dominert_minimum_berre_langs_estimat_utan_vekt(self):
        dominerte = brot = brot_alle_vekter = n = 0
        for est in itertools.product(BIN3, repeat=3):
            for theta in itertools.product((0, 1, 2), repeat=3):
                phi = [sum(t * f[i] for t, f in zip(theta, est)) for i in range(3)]
                n += 1
                for x in minimum(phi):
                    for y in range(3):
                        if dominerer(est, y, x):
                            dominerte += 1
                            brot += any(theta[k] > 0 for k, f in enumerate(est) if f[y] < f[x])
                            brot_alle_vekter += all(t > 0 for t in theta)
        self.assertEqual(n, 13824)
        self.assertGreater(dominerte, 0)
        self.assertEqual(brot, 0)
        self.assertEqual(brot_alle_vekter, 0)

    def test_sterk_seleksjon_samlar_massen_ogsaa_med_skeiv_grunnfordeling(self):
        mu = (1, 5, 25)
        for est in itertools.product(BIN3, repeat=3):
            for theta in ((1, 1, 0), (2, 0, 1), (1, 2, 1)):
                phi = [sum(t * f[i] for t, f in zip(theta, est)) for i in range(3)]
                v = vekter(mu, [40 * p for p in phi])
                ute = sum(v[i] for i in range(3) if i not in minimum(phi))
                self.assertLessEqual(ute * 2 ** 30, sum(v))

    def test_beta_null_gjev_ingen_garanti(self):
        # Alle vekter positive, men utan seleksjon står den dominerte forma med grunnvekta si.
        est, mu = ((0, 1, 1),), (1, 5, 25)
        v = vekter(mu, [0, 0, 0])
        self.assertTrue(dominerer(est, 0, 1))
        self.assertEqual(F(v[1], sum(v)), F(5, 31))

    def test_faktisk_skade_negativ_kontroll(self):
        # Estimatet har vekt, men ordnar formene feil: e^ = (0, 1), e = (1, 0).
        est, faktisk = ((0, 1),), (1, 0)
        valt = minimum([1 * est[0][i] for i in range(2)])
        self.assertEqual(valt, [0])
        self.assertEqual(faktisk[0], 1)
        self.assertEqual(faktisk[1], 0)  # betre for målet, og ingen andre estimat skil formene

    def test_bilete_mot_eige_estimat(self):
        # B utan innverknad; A (w = 1) har omsorg 1/2 for målet til B gjennom eit bilete (0, 1).
        # B sitt eige estimat er (1, 0) og har inga vekt. Målvekta etter 6.702 er positiv,
        # likevel står skaden B estimerer. «Der målet er utan vekt» er difor ikkje presist nok.
        w_a, w_b, gamma_a = F(1), F(0), F(1, 2)
        bilete, eige_b, eigne_a = (0, 1), (1, 0), (0, 0)
        maalvekt = w_b * 1 + w_a * gamma_a
        self.assertGreater(maalvekt, 0)
        phi = lin((w_a * (1 - gamma_a), eigne_a), (w_a * gamma_a, bilete), (w_b, eige_b))
        self.assertEqual(minimum(phi), [0])
        est = (eigne_a, bilete, eige_b)
        theta = (w_a * (1 - gamma_a), w_a * gamma_a, w_b)
        self.assertFalse(dominerer(est, 1, 0))  # biletet med vekt seier at form 0 er best for B
        self.assertEqual(eige_b[0], 1)          # estimatet utan vekt seier det motsette
        self.assertEqual(theta[2], 0)


RADER = ((F(0), F(0)), (F(1, 2), F(0)), (F(0), F(1, 2)), (F(1, 2), F(1, 2)), (F(1), F(0)), (F(0), F(1)))
INNVERKNAD = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)),
              (F(1, 2), F(1, 2), F(0)), (F(1, 3), F(1, 3), F(1, 3)))


def chi_matrise(C):
    """6.731: chi = (I - C)^-1 diag(1 - gamma)."""
    n = len(C)
    gamma = [sum(rad) for rad in C]
    IC = [[(1 if i == j else 0) - C[i][j] for j in range(n)] for i in range(n)]
    kolonnar = [los(IC, [(1 - gamma[j]) if i == j else 0 for i in range(n)]) for j in range(n)]
    return [[kolonnar[j][i] for j in range(n)] for i in range(n)], gamma


def rekk(C):
    n = len(C)
    R = [[C[i][j] > 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return R


class Omsorgsveg(unittest.TestCase):
    """6.76 er ikkje retta. Testane dokumenterer kvifor «viss og berre viss» ikkje følgjer."""

    def test_gir_alt_bort(self):
        # 6.702: B har all innverknad, gamma_B = 1. Vekta på B sitt eige mål er 0.
        w, gamma, omega_j = (F(0), F(1)), (F(0), F(1)), (F(1), F(1))
        c_j = ((F(0), F(0)), (F(0), F(0)))  # ingen har omsorg for B langs j
        W_Bj = w[1] * (1 - gamma[1]) * omega_j[1] + w[0] * c_j[0][1]
        self.assertGreater(w[1], 0)
        self.assertEqual(W_Bj, 0)

    def test_omsorg_langs_eit_anna_maal(self):
        # 6.701: omsorgsvektene er per mål. A (w = 1) har omsorg for B langs j', ikkje langs j.
        w_a, w_b = F(1), F(0)
        c_til_b = {"j": F(0), "j'": F(1, 2)}
        W = {j: w_b * 1 + w_a * c for j, c in c_til_b.items()}
        self.assertGreater(W["j'"], 0)
        self.assertEqual(W["j"], 0)

    def test_6731_berre_viss_held_viss_held_ikkje(self):
        singulaere = brot_berre_viss = brot_viss = brot_eksakt = n = 0
        for rader in itertools.product(RADER, repeat=3):
            C = [[F(0), rader[0][0], rader[0][1]], [rader[1][0], F(0), rader[1][1]], [rader[2][0], rader[2][1], F(0)]]
            try:
                chi, gamma = chi_matrise(C)
            except ZeroDivisionError:
                singulaere += 1  # 6.732: omsorga endar ikkje i noko eige omsyn
                continue
            for rad in chi:
                self.assertEqual(sum(rad), 1)
                self.assertTrue(all(x >= 0 for x in rad))
            R = rekk(C)
            for w in INNVERKNAD:
                for B in range(3):
                    for omega in (0, 1):
                        n += 1
                        vekt = omega * sum(w[A] * chi[A][B] for A in range(3))
                        ordlyd = w[B] > 0 or any(w[A] > 0 and R[A][B] for A in range(3) if A != B)
                        eksakt = omega > 0 and gamma[B] < 1 and ordlyd
                        brot_berre_viss += vekt > 0 and not ordlyd
                        brot_viss += ordlyd and not vekt > 0
                        brot_eksakt += (vekt > 0) != eksakt
        self.assertGreater(singulaere, 0)
        self.assertGreater(n, 0)
        self.assertEqual(brot_berre_viss, 0)   # «berre viss» følgjer
        self.assertGreater(brot_viss, 0)       # «viss» følgjer ikkje
        self.assertEqual(brot_eksakt, 0)       # med gamma_B < 1 og omega_j(B) > 0 i tillegg held begge vegar

    def test_dei_to_modellane_gjev_ulike_svar(self):
        # A (w = 1) har omsorg 1/2 for B langs j. B har ikkje omsynet sjølv: omega_j(B) = 0.
        w_a, c, omega_jb = F(1), F(1, 2), F(0)
        etter_6702 = F(0) * omega_jb + w_a * c          # bilete av avviket: vekt 1/2
        chi, _ = chi_matrise([[F(0), c], [F(0), F(0)]])
        etter_6731 = omega_jb * w_a * chi[0][1]          # heile vurderinga til B: vekt 0
        self.assertEqual(chi[0][1], F(1, 2))
        self.assertGreater(etter_6702, 0)
        self.assertEqual(etter_6731, 0)


if __name__ == "__main__":
    unittest.main()
