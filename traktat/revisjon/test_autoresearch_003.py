#!/usr/bin/env python3
"""AutoResearch forsøk 003: vektforskyving ved fri og ved normalisert vekt.

Køyr: python traktat/revisjon/test_autoresearch_003.py
Berre standardbiblioteket. Protokollen står i autoresearch-003-vektforskyving.md.

Gjeld proposisjon 6.673, 6.674, 6.6742, 6.71 og 6.711 i formlaere.tex, lesne
saman med normaliseringa i 6.61 og 6.701.

H_fri          dE[f]/dtheta_k = -Cov(f, e^_k) når berre theta_k endrar seg.
H_normalisert  d/dt E[f] = -beta w Cov(f, e^_k - e^_m) når t vert flytta frå
               omsyn m til omsyn k. E[e^_k] kan då stige.
Naiv rival     E[e^_k] kan ikkje stige når omega_k aukar under sum 1.

Utskrifta har tre slag liner:
  PROV-KONTROLL  eksakt brøkrekning (fractions), ingen flyttal
  NUMERISK       sentraldifferanse mot kovariansformelen, med toleranse
  TELJING        skildrande teljing utan krav
Sluttkode 0 = alle frosne kriterium fall ut som H_fri og H_normalisert seier.
"""
import math
import random
import sys
from collections import Counter
from fractions import Fraction

# --- Frosen protokoll. Skal ikkje endrast etter første køyring. -------------
FRO_TILFELDIG = 2026   # same frø som kontrollrekning-2026-11.py
FRO_KOMONOTON = 2027
FRO_SVARKURVE = 2028
N_TILFELDIG = 300
N_KOMONOTON = 300
N_SVARKURVE = 200
H_STEG = 1e-5          # sentraldifferanse: h = H_STEG / max(1, spenn(retning))
TOL = 1e-6             # |numerisk - formel| <= TOL * max(1, max|f| * spenn(retning))
ENDELEG_MARGIN = 1e-9  # minste skilnad som tel som stiging ved endelege steg
PAR_MARGIN = 0.05      # minste |df * dg| for eit par som skal bryte komonotoni
FRIE_STEG = (0.1, 1.0, 10.0)
FLYTT = 0.25           # endeleg omfordeling: min(FLYTT, tilgjengeleg vekt)

UVENTA = []


def meld(slag, kriterium, ok, tekst):
    if not ok:
        UVENTA.append(kriterium)
    print(f"{slag if ok else 'UVENTA'} | {kriterium} | {tekst}")


def gibbs(mu, eksp):
    lagast = min(eksp)
    w = [m * math.exp(-(p - lagast)) for m, p in zip(mu, eksp)]
    z = sum(w)
    return [x / z for x in w]


def E(P, f):
    return sum(p * x for p, x in zip(P, f))


def cov(P, f, g):
    ef, eg = E(P, f), E(P, g)
    return sum(p * (a - ef) * (b - eg) for p, a, b in zip(P, f, g))


def spenn(f):
    return max(f) - min(f)


def maksabs(f):
    return max(abs(x) for x in f)


def eksponent(M, omega):
    return [M["fast"][x] + M["bw"] * sum(o * e[x] for o, e in zip(omega, M["est"]))
            for x in range(len(M["mu"]))]


def forventning(mu, base, d, t, f):
    return E(gibbs(mu, [b + t * dx for b, dx in zip(base, d)]), f)


def samanlikn(mu, base, d, f):
    """Numerisk derivert av E[f] langs eksponentretninga d, mot -Cov(f, d)."""
    h = H_STEG / max(1.0, spenn(d))
    num = (forventning(mu, base, d, h, f) - forventning(mu, base, d, -h, f)) / (2 * h)
    formel = -cov(gibbs(mu, base), f, d)
    return num, formel, TOL * max(1.0, maksabs(f) * spenn(d))


def granske(M, T):
    """Alle frie og normaliserte retningar i éin modell. Tel i T."""
    mu, est, om, bw = M["mu"], M["est"], M["omega"], M["bw"]
    K, n = len(est), len(mu)
    funksjonar = est + [M["faktisk"]]
    base = eksponent(M, om)
    P0 = gibbs(mu, base)
    for k in range(K):
        e0 = E(P0, est[k])
        skala = max(1.0, maksabs(est[k]))
        # Fri vekt: berre theta_k endrar seg (6.673, 6.674).
        for f in funksjonar:
            num, formel, tol = samanlikn(mu, base, est[k], f)
            T["K1_fri_n"] += 1
            T["K1_fri_avvik"] += abs(num - formel) > tol
        num, formel, tol = samanlikn(mu, base, est[k], est[k])
        T["K2_n"] += 1
        T["K2_brot"] += num > tol
        for steg in FRIE_STEG:
            T["K2_endeleg_n"] += 1
            T["K2_endeleg_brot"] += forventning(mu, base, est[k], steg, est[k]) > e0 + ENDELEG_MARGIN * skala
        # Normalisert vekt: sum omega = 1 (6.61). Parvis flytting og proporsjonal nedskalering.
        retningar = [("par", [bw * (a - b) for a, b in zip(est[k], est[m])], min(FLYTT, om[m]))
                     for m in range(K) if m != k]
        if om[k] < 1:
            rest = [sum(om[m] * est[m][x] for m in range(K) if m != k) / (1 - om[k]) for x in range(n)]
            retningar.append(("prop", [bw * (a - b) for a, b in zip(est[k], rest)], min(FLYTT, 1 - om[k])))
        for slag, d, t in retningar:
            for f in funksjonar:
                num, formel, tol = samanlikn(mu, base, d, f)
                T["K1_norm_n"] += 1
                T["K1_norm_avvik"] += abs(num - formel) > tol
                # Negativ kontroll: den frie formelen brukt uendra på normalisert vekt.
                T["naivformel_n"] += 1
                T["naivformel_avvik"] += abs(num + bw * cov(P0, f, est[k])) > tol
            num, formel, tol = samanlikn(mu, base, d, est[k])
            T[f"K3_{slag}_n"] += 1
            T[f"K3_{slag}_stig"] += num > tol
            if abs(formel) > 10 * tol:
                T["K4_n"] += 1
                T["K4_mistilpassing"] += (num > 0) != (formel > 0)
            if t > 0:
                T[f"K3_{slag}_endeleg_n"] += 1
                T[f"K3_{slag}_endeleg_stig"] += forventning(mu, base, d, t, est[k]) - e0 > ENDELEG_MARGIN * skala
            # N2: differansen langs flytteretninga kan ikkje stige.
            num, formel, tol = samanlikn(mu, base, d, d)
            T["N2_n"] += 1
            T["N2_brot"] += num > tol
            if t > 0:
                T["N2_endeleg_n"] += 1
                T["N2_endeleg_brot"] += (forventning(mu, base, d, t, d) - E(P0, d)
                                         > ENDELEG_MARGIN * max(1.0, maksabs(d)))


def tilfeldig_modell(rng, i):
    n, K = (2, 3, 5, 8)[i % 4], (2, 3, 4)[i % 3]
    raa = [rng.uniform(0.05, 1) for _ in range(K)]
    return {
        "mu": [rng.uniform(0.2, 2) for _ in range(n)],
        "est": [[rng.uniform(0, 3) for _ in range(n)] for _ in range(K)],
        "faktisk": [rng.uniform(0, 3) for _ in range(n)],
        "fast": [rng.uniform(0, 2) for _ in range(n)],   # andre agentar og omsyn, haldne faste
        "omega": [r / sum(raa) for r in raa],
        "bw": rng.uniform(0.2, 4) * rng.uniform(0.1, 1),  # beta * w_i
    }


# Adversarielle modellar, fastsette for hand før køyring.
ADVERSARIELLE = [
    ("A1 motdømet i kontrollrekninga", {"mu": [1, 1], "est": [[0, 1], [0, 2]], "faktisk": [0, 1],
                                         "fast": [0, 0], "omega": [0.2, 0.8], "bw": 2.0}),
    ("A2 motstridande omsyn", {"mu": [1, 1], "est": [[0, 1], [2, 0]], "faktisk": [0, 1],
                                "fast": [0, 0], "omega": [0.2, 0.8], "bw": 2.0}),
    ("A3 identiske estimat", {"mu": [1, 3], "est": [[0, 1], [0, 1]], "faktisk": [1, 0],
                               "fast": [0, 0], "omega": [0.5, 0.5], "bw": 1.5}),
    ("A4 omsorg etter 6.701", {"mu": [1, 1, 1], "est": [[0, 1, 2], [0, 5, 10]], "faktisk": [0, 1, 2],
                                "fast": [0, 0, 0], "omega": [0.2, 0.8], "bw": 1.0}),
    ("A5 kolineære estimat", {"mu": [0.01, 5, 0.3, 2, 1], "est": [[0, 1, 2, 3, 4], [0, 3, 6, 9, 12]],
                               "faktisk": [4, 3, 2, 1, 0], "fast": [1, 0, 2, 0, 1],
                               "omega": [0.6, 0.4], "bw": 0.7}),
    ("A6 nær deterministisk, beta w = 50", {"mu": [1, 1, 1], "est": [[0.0, 0.1, 3], [1, 0.0, 0.2], [0.3, 2, 0.0]],
                                             "faktisk": [1, 2, 3], "fast": [0, 0, 0],
                                             "omega": [0.5, 0.3, 0.2], "bw": 50.0}),
    ("A7 beta = 0", {"mu": [0.5, 1, 2, 4], "est": [[0, 1, 2, 3], [3, 1, 0, 2]], "faktisk": [1, 0, 1, 0],
                     "fast": [0, 0, 0, 0], "omega": [0.5, 0.5], "bw": 0.0}),
    ("A8 konstant estimat", {"mu": [1, 2, 3], "est": [[1, 1, 1], [0, 1, 2]], "faktisk": [2, 0, 1],
                              "fast": [0, 0, 0], "omega": [0.3, 0.7], "bw": 1.0}),
    ("A9 stort spenn, skeiv grunnfordeling", {"mu": [1e-6, 1, 1e-3, 0.5],
                                               "est": [[0, 1000, 250, 3], [500, 0, 999, 1]],
                                               "faktisk": [1, 1000, 0, 10], "fast": [0, 0, 0, 0],
                                               "omega": [0.3, 0.7], "bw": 0.01}),
    ("A10 forteiknet snur langs vegen", {"mu": [1, 1, 1], "est": [[0, 1, 2], [0, 3, 0]], "faktisk": [0, 1, 2],
                                          "fast": [0, 0, 0], "omega": [0.75, 0.25], "bw": 2.0}),
    ("A11 randpunkt omega_m = 0", {"mu": [1, 2, 1], "est": [[0, 1, 2], [0, 2, 5]], "faktisk": [2, 1, 0],
                                    "fast": [0, 0, 0], "omega": [1.0, 0.0], "bw": 1.0}),
]


# --- Eksakt del: e^(-beta w) = 1/2 og heiltalseksponentar gjev rasjonale sannsyn.
def gibbs_eksakt(mu, eksp):
    w = []
    for m, p in zip(mu, eksp):
        p = Fraction(p)
        assert p.denominator == 1, "eksponenten må vere heiltal"
        w.append(Fraction(m) * Fraction(1, 2) ** int(p))
    z = sum(w)
    return [x / z for x in w]


def blanding(a, f, b, g):
    return [a * x + b * y for x, y in zip(f, g)]


def strengt_stigande(v):
    return all(a < b for a, b in zip(v, v[1:]))


def strengt_fallande(v):
    return all(a > b for a, b in zip(v, v[1:]))


def eksakt_del():
    kvart = [Fraction(i, 4) for i in range(5)]
    # E1: to tilstandar. Estimat i toleranseeiningar: L_k = (0, 4), L_m = (0, 8).
    Lk, Lm = [0, 4], [0, 8]
    norm = [E(gibbs_eksakt([1, 1], blanding(o, Lk, 1 - o, Lm)), Lk) for o in kvart]
    fasit = [Fraction(4, 257), Fraction(4, 129), Fraction(4, 65), Fraction(4, 33), Fraction(4, 17)]
    meld("PROV-KONTROLL", "E1 normalisert", norm == fasit and strengt_stigande(norm),
         "omega_k = 0, 1/4, 1/2, 3/4, 1 (sum 1): E[L_k] = " + ", ".join(map(str, norm)) + " — stig strengt")
    fri = [E(gibbs_eksakt([1, 1], blanding(a, Lk, Fraction(3, 4), Lm)), Lk) for a in kvart[1:]]
    fasit = [Fraction(4, 129), Fraction(4, 257), Fraction(4, 513), Fraction(4, 1025)]
    meld("PROV-KONTROLL", "E1 fri", fri == fasit and strengt_fallande(fri),
         "same start (1/4, 3/4), vekta på m halden fast, vekta på k = 1/4, 1/2, 3/4, 1: E[L_k] = "
         + ", ".join(map(str, fri)) + " — fell strengt")
    P = gibbs_eksakt([1, 1], blanding(Fraction(1, 4), Lk, Fraction(3, 4), Lm))
    var = E(P, [x * x for x in Lk]) - E(P, Lk) ** 2
    kov = E(P, [x * y for x, y in zip(Lk, Lm)]) - E(P, Lk) * E(P, Lm)
    meld("PROV-KONTROLL", "E1 forteikn", var > 0 and var - kov < 0,
         f"i (1/4, 3/4): Var(L_k) = {var}, Cov(L_k, L_m) = {kov}; -(Var - Cov) = {kov - var} > 0, "
         f"medan -Var = {-var} < 0")
    dif = [E(gibbs_eksakt([1, 1], blanding(o, Lk, 1 - o, Lm)), blanding(1, Lk, -1, Lm)) for o in kvart]
    meld("PROV-KONTROLL", "E1 differanse (N2)", strengt_fallande(dif),
         "E[L_k - L_m] = " + ", ".join(map(str, dif)) + " — fell strengt")

    # E2: tre tilstandar, omsorg etter 6.701. Biletet er feilfritt: bilete = e_B.
    eigne, bilete = [0, 10, 20], [0, 2, 4]
    gammaer = [Fraction(0), Fraction(1, 2), Fraction(1)]
    skade = [E(gibbs_eksakt([1, 1, 1], blanding(1 - g, eigne, g, bilete)), bilete) for g in gammaer]
    fasit = [Fraction(2052, 1049601), Fraction(132, 4161), Fraction(12, 21)]
    meld("PROV-KONTROLL", "E2 omsorgsdel", skade == fasit and strengt_stigande(skade),
         "gamma = 0, 1/2, 1, svarkurva h(u) = u uendra og stigande: E[e_B] = "
         + ", ".join(map(str, skade)) + " — stig strengt")
    fri = [E(gibbs_eksakt([1, 1, 1], blanding(1, eigne, a, bilete)), bilete) for a in range(4)]
    meld("PROV-KONTROLL", "E2 fri vekt", strengt_fallande(fri),
         "eigne omsyn haldne faste, vekta til biletet = 0, 1, 2, 3: E[e_B] = "
         + ", ".join(map(str, fri)) + " — fell strengt")

    # E3: tre tilstandar der forteiknet snur langs vegen.
    Lk, Lm = [0, 4, 8], [0, 12, 0]
    v = [E(gibbs_eksakt([1, 1, 1], blanding(o, Lk, 1 - o, Lm)), Lk) for o in kvart]
    meld("PROV-KONTROLL", "E3 ikkje monoton", strengt_fallande(v[:4]) and v[4] > v[3],
         "omega_k = 0 ... 1: E[L_k] = " + ", ".join(map(str, v)) + " — fell til 3/4, stig så")
    dif = [E(gibbs_eksakt([1, 1, 1], blanding(o, Lk, 1 - o, Lm)), blanding(1, Lk, -1, Lm)) for o in kvart]
    meld("PROV-KONTROLL", "E3 differanse (N2)", strengt_fallande(dif),
         "E[L_k - L_m] = " + ", ".join(map(str, dif)) + " — fell strengt")


# --- N3: E[e^_k] kan ikkje stige ved flytting m -> k for nokon grunnfordeling
#     viss og berre viss e^_k og e^_k - e^_m ordnar alle par likt (svakt).
def komonoton(f, g, slakk):
    return all((f[x] - f[y]) * (g[x] - g[y]) >= -slakk for x in range(len(f)) for y in range(x))


def komonoton_familie(T):
    rng = random.Random(FRO_KOMONOTON)
    for i in range(N_KOMONOTON):
        n, slag = (3, 5, 8)[i % 3], ("konflikt", "skalert", "fri")[(i // 3) % 3]
        f = [rng.uniform(0, 3) for _ in range(n)]
        if slag == "konflikt":      # motsett rekkjefølgje
            f.sort()
            m = sorted((rng.uniform(0, 3) for _ in range(n)), reverse=True)
        elif slag == "skalert":     # e^_m = c e^_k med c <= 1
            c = rng.uniform(-1, 1)
            m = [c * x for x in f]
        else:
            m = [rng.uniform(0, 3) for _ in range(n)]
        mu = [rng.uniform(0.2, 2) for _ in range(n)]
        fast = [rng.uniform(0, 2) for _ in range(n)]
        bw = rng.uniform(0.5, 4)
        g = [a - b for a, b in zip(f, m)]
        veg = [E(gibbs(mu, [fast[x] + bw * (o / 10 * f[x] + (1 - o / 10) * m[x]) for x in range(n)]), f)
               for o in range(11)]
        stig = any(b - a > ENDELEG_MARGIN for a, b in zip(veg, veg[1:]))
        if slag != "fri":
            T["N3_konstruert_n"] += 1
            T["N3_konstruert_ikkje_komonoton"] += not komonoton(f, g, 1e-12)
            T["N3_tilstrekkeleg_brot"] += stig
            continue
        T["N3_fri_n"] += 1
        T["N3_fri_komonoton"] += komonoton(f, g, 0.0)
        T["N3_fri_stig_med_eiga_mu"] += stig
        # Naudsyn: for kvart brotpar finst ei grunnfordeling som gjev stiging.
        base = [fast[x] + bw * 0.5 * (f[x] + m[x]) for x in range(n)]
        d = [bw * v for v in g]
        for x in range(n):
            for y in range(x):
                if (f[x] - f[y]) * (g[x] - g[y]) < -PAR_MARGIN:
                    mu2 = [math.exp(base[z]) * (1.0 if z in (x, y) else 1e-9) for z in range(n)]
                    num, _, tol = samanlikn(mu2, base, d, f)
                    T["N3_naudsyn_n"] += 1
                    T["N3_naudsyn_brot"] += not num > tol


# --- 6.711: svarkurva h(u) = E[e | bilete = u].
def svarkurve(P, e, niv):
    return [sum(p * a for p, a, u in zip(P, e, niv) if u == v) / sum(p for p, u in zip(P, niv) if u == v)
            for v in (0, 1, 2)]


def svarkurve_familie(T):
    rng = random.Random(FRO_SVARKURVE)
    niv = [0, 0, 1, 1, 2, 2]
    for _ in range(N_SVARKURVE):
        mu = [rng.uniform(0.2, 2) for _ in range(6)]
        eigne = [rng.uniform(0, 2) for _ in range(6)]
        e = [rng.uniform(0, 3) for _ in range(6)]
        bw = rng.uniform(0.5, 4)
        fri = lambda th: gibbs(mu, [a + th * u for a, u in zip(eigne, niv)])
        h1, h2 = svarkurve(fri(0.5), e, niv), svarkurve(fri(3.0), e, niv)
        T["S1_n"] += 1
        T["S1_avvik"] += max(abs(a - b) for a, b in zip(h1, h2)) > 1e-12
        veg = [E(fri(th), e) for th in (0, 0.5, 1, 2, 3, 5)]
        if h1[0] <= h1[1] <= h1[2]:
            T["S3_stigande_kurve_n"] += 1
            T["S3_brot"] += any(b - a > ENDELEG_MARGIN for a, b in zip(veg, veg[1:]))
        if h1[0] >= h1[1] >= h1[2]:
            T["S3_fallande_kurve_n"] += 1
            T["S3_brot"] += any(a - b > ENDELEG_MARGIN for a, b in zip(veg, veg[1:]))
        # Omsorgsdelen gamma etter 6.701: eigne omsyn vert skalerte med (1 - gamma).
        bunden = lambda g: gibbs(mu, [bw * ((1 - g) * a + g * u) for a, u in zip(eigne, niv)])
        g1, g2 = svarkurve(bunden(0.2), e, niv), svarkurve(bunden(0.8), e, niv)
        T["S2_flytta"] += max(abs(a - b) for a, b in zip(g1, g2)) > 1e-6
        if g1[0] <= g1[1] <= g1[2] and g2[0] <= g2[1] <= g2[2]:
            T["S4_stigande_begge_n"] += 1
            T["S4_skade_stig"] += E(bunden(0.8), e) - E(bunden(0.2), e) > ENDELEG_MARGIN


def main():
    global UVENTA
    UVENTA = []
    print(f"Python {sys.version.split()[0]} | frø {FRO_TILFELDIG}, {FRO_KOMONOTON}, {FRO_SVARKURVE} | "
          f"h = {H_STEG:g}, toleranse = {TOL:g}, margin = {ENDELEG_MARGIN:g}\n")
    eksakt_del()

    print()
    T = Counter()
    rng = random.Random(FRO_TILFELDIG)
    for i in range(N_TILFELDIG):
        granske(tilfeldig_modell(rng, i), T)
    A = Counter()
    for namn, M in ADVERSARIELLE:
        ein = Counter()
        granske(M, ein)
        A.update(ein)
        print(f"TELJING | {namn} | avvik fri {ein['K1_fri_avvik']}/{ein['K1_fri_n']}, "
              f"avvik normalisert {ein['K1_norm_avvik']}/{ein['K1_norm_n']}, "
              f"E[e^_k] stig ved parflytting {ein['K3_par_stig']}/{ein['K3_par_n']}, "
              f"fri monotoni broten {ein['K2_brot'] + ein['K2_endeleg_brot']}")
    print()
    for namn, C in (("tilfeldige", T), ("adversarielle", A)):
        meld("NUMERISK", f"K1 fri ({namn})", C["K1_fri_avvik"] == 0,
             f"dE[f]/dtheta_k mot -Cov(f, e^_k): {C['K1_fri_avvik']} avvik av {C['K1_fri_n']}")
        meld("NUMERISK", f"K1 normalisert ({namn})", C["K1_norm_avvik"] == 0,
             f"d/dt E[f] mot -beta w Cov(f, e^_k - e^_rest): {C['K1_norm_avvik']} avvik av {C['K1_norm_n']}")
        meld("NUMERISK", f"K2 fri monotoni ({namn})", C["K2_brot"] == 0 and C["K2_endeleg_brot"] == 0,
             f"E[e^_k] stig ved fri auke av theta_k: {C['K2_brot']} av {C['K2_n']} (derivert), "
             f"{C['K2_endeleg_brot']} av {C['K2_endeleg_n']} (endelege steg)")
        meld("NUMERISK", f"K4 forteiknsregel ({namn})", C["K4_mistilpassing"] == 0,
             f"forteikn mot -beta w (Var - Cov): {C['K4_mistilpassing']} mistilpassingar av {C['K4_n']}")
        meld("NUMERISK", f"N2 differansen ({namn})", C["N2_brot"] == 0 and C["N2_endeleg_brot"] == 0,
             f"E[e^_k - e^_rest] stig ved flytting til k: {C['N2_brot']} av {C['N2_n']} (derivert), "
             f"{C['N2_endeleg_brot']} av {C['N2_endeleg_n']} (endelege steg)")
        print(f"TELJING | K3 naiv rival ({namn}) | E[e^_k] stig når omega_k aukar under sum 1: "
              f"parflytting {C['K3_par_stig']}/{C['K3_par_n']} (derivert), "
              f"{C['K3_par_endeleg_stig']}/{C['K3_par_endeleg_n']} (endeleg); "
              f"proporsjonal {C['K3_prop_stig']}/{C['K3_prop_n']} (derivert), "
              f"{C['K3_prop_endeleg_stig']}/{C['K3_prop_endeleg_n']} (endeleg)")
        print(f"TELJING | negativ kontroll ({namn}) | fri formel -beta w Cov(f, e^_k) brukt på normalisert vekt: "
              f"{C['naivformel_avvik']} avvik av {C['naivformel_n']}")
    meld("NUMERISK", "K3 naiv rival", T["K3_par_stig"] > 0 and T["K3_par_endeleg_stig"] > 0,
         "den naive rivalen føreseier 0 stigingar; funne i den tilfeldige familien: "
         f"{T['K3_par_stig']} (derivert) og {T['K3_par_endeleg_stig']} (endeleg)")
    meld("NUMERISK", "negativ kontroll", T["naivformel_avvik"] > 0,
         "evalueringa skil den frie formelen frå den normaliserte (avvik > 0)")

    print()
    N = Counter()
    komonoton_familie(N)
    meld("NUMERISK", "N3 tilstrekkeleg", N["N3_tilstrekkeleg_brot"] == 0 and N["N3_konstruert_ikkje_komonoton"] == 0,
         f"komonotone par (e^_k, e^_k - e^_m): E[e^_k] stig langs omega_k = 0..1 i "
         f"{N['N3_tilstrekkeleg_brot']} av {N['N3_konstruert_n']} modellar")
    meld("NUMERISK", "N3 naudsynt", N["N3_naudsyn_brot"] == 0 and N["N3_naudsyn_n"] > 0,
         f"brotpar med konstruert grunnfordeling: stiging uteblir i {N['N3_naudsyn_brot']} av {N['N3_naudsyn_n']}")
    print(f"TELJING | N3 frie modellar | komonotone av seg sjølv: {N['N3_fri_komonoton']}/{N['N3_fri_n']}; "
          f"stig langs vegen med si eiga grunnfordeling: {N['N3_fri_stig_med_eiga_mu']}/{N['N3_fri_n']}")

    print()
    S = Counter()
    svarkurve_familie(S)
    meld("NUMERISK", "S1 svarkurve, fri vekt", S["S1_avvik"] == 0,
         f"h(u) endra når berre vekta til biletet veks: {S['S1_avvik']} av {S['S1_n']}")
    meld("NUMERISK", "S3 monoton svarkurve, fri vekt", S["S3_brot"] == 0,
         f"brot på 6.711 for fri vekt: {S['S3_brot']} av "
         f"{S['S3_stigande_kurve_n'] + S['S3_fallande_kurve_n']} modellar med monoton kurve "
         f"({S['S3_stigande_kurve_n']} stigande, {S['S3_fallande_kurve_n']} fallande)")
    meld("NUMERISK", "S2 svarkurve, omsorgsdel", S["S2_flytta"] > 0,
         f"h(u) flyttar seg når gamma går 0,2 -> 0,8: {S['S2_flytta']} av {S['S1_n']}")
    print(f"TELJING | S4 omsorgsdel | kurva stigande ved både gamma 0,2 og 0,8: {S['S4_stigande_begge_n']} modellar; "
          f"E[e] stig likevel i {S['S4_skade_stig']}")

    print("\nUventa utfall:", UVENTA if UVENTA else "ingen")
    return 1 if UVENTA else 0


def test_autoresearch_003():
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
