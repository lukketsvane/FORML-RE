#!/usr/bin/env python3
"""Kontrollrekning til kritisk-gransking-2026-11.md.

Køyr: python3 revisjon/kontrollrekning-2026-11.py
Berre standardbiblioteket. Kvar line seier kva proposisjon prøva gjeld.
«STADFESTA» = identiteten held numerisk under dei oppgjevne vilkåra.
«MOTDØME»  = den verbale påstanden held ikkje når eit skjult vilkår fell bort.
"""
import math
import random

random.seed(2026)
FEIL = []


def gibbs(mu, phi, beta=1.0):
    w = [m * math.exp(-beta * p) for m, p in zip(mu, phi)]
    z = sum(w)
    return [x / z for x in w]


def E(P, f):
    return sum(p * x for p, x in zip(P, f))


def cov(P, f, g):
    return E(P, [a * b for a, b in zip(f, g)]) - E(P, f) * E(P, g)


def lin(theta, est):
    return [sum(t * e[i] for t, e in zip(theta, est)) for i in range(len(est[0]))]


def meld(kind, prop, ok, tekst):
    if not ok:
        FEIL.append(prop)
    print(f"{kind if ok else 'UVENTA'} | {prop} | {tekst}")


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def stasjonaer(T, n=20000):
    p = [1.0 / len(T)] * len(T)
    for _ in range(n):
        p = [sum(p[i] * T[i][j] for i in range(len(T))) for j in range(len(T))]
    return p


def mh_kjerne(mu, phi, q, beta, hastings=True, aksept=None):
    n = len(mu)
    T = [[0.0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x == y or q[x][y] == 0:
                continue
            r = (mu[y] * q[y][x]) / (mu[x] * q[x][y]) if hastings else 1.0
            a = aksept(x, y, r) if aksept else min(1.0, r * math.exp(-beta * (phi[y] - phi[x])))
            T[x][y] = q[x][y] * a
        T[x][x] = 1.0 - sum(T[x])
    return T


# 1. 6.673, 6.674, 7.1521: kovariansidentitetane for ei FRI vekt -------------
n = 7
mu = [random.uniform(0.2, 2) for _ in range(n)]
est = [[random.uniform(0, 3) for _ in range(n)] for _ in range(3)]
faktisk = [random.uniform(0, 3) for _ in range(n)]
ind = [1.0 if v > 1.5 else 0.0 for v in faktisk]
theta = [0.7, 1.3, 0.4]
h = 1e-6
P0 = gibbs(mu, lin(theta, est))
maxavvik = 0.0
for k in range(3):
    th = theta[:]
    th[k] += h
    P1 = gibbs(mu, lin(th, est))
    for f in est + [faktisk, ind]:
        maxavvik = max(maxavvik, abs((E(P1, f) - E(P0, f)) / h + cov(P0, f, est[k])))
meld("STADFESTA", "6.673/6.674/7.1521", maxavvik < 1e-4,
     f"dE[f]/dtheta_k = -Cov(f, e^_k) for fri vekt; største avvik {maxavvik:.1e}")

# 2. 6.6741: same rekkjefølgje => Cov >= 0 under kvar fordeling ---------------
verst = min(
    cov(gibbs([random.uniform(0.01, 5) for _ in range(n)], [0] * n),
        sorted(random.uniform(0, 3) for _ in range(n)),
        sorted(random.uniform(0, 9) for _ in range(n)))
    for _ in range(5000))
meld("STADFESTA", "6.6741", verst >= -1e-12, f"komonotone e og e^: minste kovarians i 5000 trekk {verst:.3f} >= 0")

# 3. 6.673 siste setning under normaliseringa i 6.61 ------------------------
ek, em, beta = [0.0, 1.0], [0.0, 2.0], 2.0
foer = E(gibbs([1, 1], lin([beta * 0.2, beta * 0.8], [ek, em])), ek)
etter = E(gibbs([1, 1], lin([beta * 0.8, beta * 0.2], [ek, em])), ek)
meld("MOTDØME", "6.673 (siste setning) + 6.61", etter > foer,
     f"omhug flytta frå m til k (0,2->0,8, sum 1): E[e^_k] stig {foer:.4f} -> {etter:.4f}")

# 4. 6.711: svarkurva står fast for fri vekt, men «meir omsorg» etter 6.701 ---
niv = [0, 0, 1, 1, 2, 2]
anna = [0.3, 1.1, 0.2, 0.9, 0.5, 1.4]
e_f = [0.1, 0.9, 1.0, 0.2, 0.4, 1.7]


def svarkurve(P):
    return [sum(P[i] * e_f[i] for i in range(6) if niv[i] == u) / sum(P[i] for i in range(6) if niv[i] == u)
            for u in (0, 1, 2)]


h1 = svarkurve(gibbs([1] * 6, [0.5 * a + b for a, b in zip(niv, anna)]))
h2 = svarkurve(gibbs([1] * 6, [3.0 * a + b for a, b in zip(niv, anna)]))
meld("STADFESTA", "6.711", max(abs(a - b) for a, b in zip(h1, h2)) < 1e-12,
     "h(u) er uendra når berre den frie vekta til biletet veks")
h3 = svarkurve(gibbs([1] * 6, [0.5 * a + 0.2 * b for a, b in zip(niv, anna)]))
meld("MOTDØME", "6.711 + 6.701", max(abs(a - b) for a, b in zip(h1, h3)) > 1e-3,
     "h(u) flyttar seg når vekta på eigne omsyn vert skalert med (1-gamma)")
phi0, bilete, e_B = [0.0, 5.0, 10.0], [0.0, 1.0, 2.0], [0.0, 1.0, 2.0]
skade = [E(gibbs([1, 1, 1], [(1 - g) * a + g * b for a, b in zip(phi0, bilete)]), e_B) for g in (0.2, 0.8)]
meld("MOTDØME", "6.711/6.71 + 6.701", skade[1] > skade[0],
     f"feilfritt bilete, stigande svarkurve, gamma 0,2->0,8: E[e_B] stig {skade[0]:.4f} -> {skade[1]:.4f}")

# 5. 6.614 mot 5.711: nytt alternativ endrar grunnvekta ----------------------
grad_foer = {"x": 1, "y": 1}            # x—y
grad_etter = {"x": 2, "y": 1, "z": 1}   # z—x—y
T = [[0, 1, 0], [.5, 0, .5], [0, 1, 0]]  # z, x, y: lik sjanse for kvart reversible steg
pi = [0.25, 0.5, 0.25]
stasj = all(abs(sum(pi[i] * T[i][j] for i in range(3)) - pi[j]) < 1e-12 for j in range(3))
meld("MOTDØME", "6.614 + 5.711", stasj and grad_etter["x"] / grad_etter["y"] == 2 * grad_foer["x"] / grad_foer["y"],
     "mu_SG ∝ N(x): eit nytt alternativ z ved x doblar P(x)/P(y) med uendra Phi")

# 6. 6.64: detaljert balanse, konvergens; r = 1 med skeive forslag ----------
n = 5
mu = [random.uniform(0.3, 2) for _ in range(n)]
phi = [random.uniform(0, 2) for _ in range(n)]
q = []
for x in range(n):
    rad = [0 if x == y else random.uniform(0.1, 1) for y in range(n)]
    s = sum(rad) * 1.25
    q.append([v / s for v in rad])
beta = 1.7
P = gibbs(mu, phi, beta)
T = mh_kjerne(mu, phi, q, beta)
db = max(abs(P[x] * T[x][y] - P[y] * T[y][x]) for x in range(n) for y in range(n))
konv = max(abs(a - b) for a, b in zip(stasjonaer(T), P))
meld("STADFESTA", "6.64", db < 1e-12 and konv < 1e-9, f"detaljert balanse (avvik {db:.1e}) og konvergens mot P (avvik {konv:.1e})")
avvik = max(abs(a - b) for a, b in zip(stasjonaer(mh_kjerne(mu, phi, q, beta, hastings=False)), P))
meld("STADFESTA", "5.702 (r_A = 1)", avvik > 1e-2,
     f"utan korreksjon og med skeive forslag er stasjonær fordeling ikkje Gibbs-forma (avvik {avvik:.3f})")

# 7. 6.633: samrøystes godkjenning ------------------------------------------
phi1 = [random.uniform(0, 2) for _ in range(n)]
phi2 = [random.uniform(0, 2) for _ in range(n)]
b1, b2 = 1.1, 0.6


def samroystes(x, y, r):
    return min(1, r) * min(1, math.exp(-b1 * (phi1[y] - phi1[x]))) * min(1, math.exp(-b2 * (phi2[y] - phi2[x])))


Pm = gibbs(mu, [b1 * a + b2 * b for a, b in zip(phi1, phi2)])
Tm = mh_kjerne(mu, None, q, None, aksept=samroystes)
db = max(abs(Pm[x] * Tm[x][y] - Pm[y] * Tm[y][x]) for x in range(n) for y in range(n))
meld("STADFESTA", "6.633", db < 1e-12, f"samrøystes kjerne har same stasjonære fordeling (avvik {db:.1e})")
meld("MOTDØME", "6.633 mot 5.7 / føreseiing (v)", math.exp(-1) * 1 < min(1, math.exp(-(1 - 1))),
     f"dPhi_1=+1, dPhi_2=-1, beta_i=1: samla dPhi=0, men aksepten er {math.exp(-1):.3f}, ikkje 1")

# 8. 6.642: opphaldstid ------------------------------------------------------
beta, hh = 3.0, 1.0
p_ut = sum((1 / 3) * min(1, math.exp(-beta * hh)) for _ in range(3))
meld("STADFESTA", "6.642", abs(1 / p_ut - math.exp(beta * hh)) < 1e-9, f"venta opphald {1 / p_ut:.2f} = e^(beta h)")

# 9. 6.6722: Laplace-variansen 2 eps^2/(beta W)^2 ---------------------------
def var_gitter(a_over_eps, steg, halvbreidd):
    xs = [i * steg for i in range(-int(halvbreidd / steg), int(halvbreidd / steg) + 1)]
    Pg = gibbs([1] * len(xs), [a_over_eps * abs(x) for x in xs])
    return E(Pg, [x * x for x in xs]) - E(Pg, xs) ** 2


fasit = 2.0  # a/eps = 1
v_fin, v_grov, v_kort = var_gitter(1, 0.01, 60), var_gitter(1, 2.0, 60), var_gitter(1, 0.01, 2)
meld("STADFESTA", "6.6722", abs(v_fin - fasit) < 1e-3, f"fint, vidt gitter: Var = {v_fin:.4f} (formel 2)")
meld("MOTDØME", "6.6722 + 6.62", abs(v_grov - fasit) > 0.2 and abs(v_kort - fasit) > 0.2,
     f"grove steg: {v_grov:.3f}; rom avkorta ved ±2: {v_kort:.3f} (formel 2) — likskapsteiknet held ikkje på endeleg D")

# 10. 6.672: kryssledd i krumminga ------------------------------------------
H = [[1.0, 0.8], [0.8, 1.0]]
xs = [i * 0.1 for i in range(-80, 81)]
vekt = [(x, math.exp(-0.5 * (H[0][0] * x * x + 2 * H[0][1] * x * y + H[1][1] * y * y))) for x in xs for y in xs]
Z = sum(w for _, w in vekt)
var1 = sum(w * x * x for x, w in vekt) / Z
meld("MOTDØME", "6.672 (skalarforma)", abs(var1 - 1 / (1 - 0.64)) < 0.02 and var1 > 2.5,
     f"H_12 = 0,8: Var(x_1) = {var1:.2f} = [(beta H)^-1]_11, ikkje 1/(beta H_11) = 1")

# 11. 6.72: sterk seleksjon, feilvendt estimat ------------------------------
Ps = gibbs([1, 1], [0.0, 1.0], beta=50)
meld("MOTDØME", "6.72", E(Ps, [1.0, 0.0]) > 0.999,
     f"målet har vekt, ingen vinn på skaden, likevel E[faktisk avvik] = {E(Ps, [1.0, 0.0]):.4f} ved beta = 50")


# 12. 6.76 / 6.731: chi = sum_n C^n (I - diag gamma) ------------------------
def chi(C, gamma, ledd=4000):
    m = len(C)
    S = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    Pn = [rad[:] for rad in S]
    for _ in range(ledd):
        Pn = matmul(Pn, C)
        S = [[S[i][j] + Pn[i][j] for j in range(m)] for i in range(m)]
    return [[S[i][j] * (1 - gamma[j]) for j in range(m)] for i in range(m)]


X = chi([[0, 0], [1, 0]], [0, 1])      # A held alt sjølv; B gjev alt til A
vekt_B = 0 * X[0][1] + 1 * X[1][1]     # w_A = 0, w_B = 1
meld("MOTDØME", "6.76", vekt_B == 0,
     "B har all innverknad (w_B = 1), men gamma_B = 1: vekta på B sine eigne mål er 0")
C = [[0, .3, .2], [.5, 0, .1], [.4, .4, 0]]
X = chi(C, [sum(r) for r in C])
meld("STADFESTA", "6.731", max(abs(sum(r) - 1) for r in X) < 1e-9 and min(min(r) for r in X) >= 0, "chi >= 0 med radsummar 1")
g = 0.999
X = chi([[0, g], [g, 0]], [g, g], ledd=40000)
meld("STADFESTA", "6.741", abs(X[0][0] - X[1][0]) < 1e-3, f"eigenandel 0,001: radene i chi fell saman ({X[0][0]:.4f} mot {X[1][0]:.4f})")

# 13. 6.754 ------------------------------------------------------------------
phi0 = [random.uniform(0, 3) for _ in range(6)]
psi = [random.uniform(0, 3) for _ in range(6)]
d = [a - b for a, b in zip(psi, phi0)]
bw, g0 = 1.4, 0.3
Pa = gibbs([1] * 6, [bw * (p + g0 * x) for p, x in zip(phi0, d)])
Pb = gibbs([1] * 6, [bw * (p + (g0 + h) * x) for p, x in zip(phi0, d)])
meld("STADFESTA", "6.754", abs((E(Pb, d) - E(Pa, d)) / h + bw * cov(Pa, d, d)) < 1e-4,
     "d/dgamma E[Psi - Phi0] = -beta w Var(Psi - Phi0)")

# 14. 5.704: drift per steg ---------------------------------------------------
beta, grad, sd = 1.0, (1.0, 0.5), (0.05, 0.10)
sx = sy = 0.0
N = 400000
for _ in range(N):
    dx, dy = random.gauss(0, sd[0]), random.gauss(0, sd[1])
    if random.random() < min(1.0, math.exp(-beta * (grad[0] * dx + grad[1] * dy))):
        sx += dx
        sy += dy
maal = (-beta / 2 * sd[0] ** 2 * grad[0], -beta / 2 * sd[1] ** 2 * grad[1])
meld("STADFESTA", "5.704", abs(sx / N - maal[0]) < 3e-4 and abs(sy / N - maal[1]) < 6e-4,
     f"drift ({sx / N:.5f}, {sy / N:.5f}) mot -(beta/2) Sigma grad = ({maal[0]:.5f}, {maal[1]:.5f})")

# 15. 6.63: grunnfordeling og vurdering kan ikkje skiljast frå utfalla åleine --
gg = [random.uniform(-1, 1) for _ in range(n)]
Pa = gibbs(mu, phi, 1.0)
Pb = gibbs([m * math.exp(x) for m, x in zip(mu, gg)], [p + x for p, x in zip(phi, gg)], 1.0)
meld("MOTDØME", "6.63", max(abs(a - b) for a, b in zip(Pa, Pb)) < 1e-12,
     "(mu, Phi) og (mu·e^g, Phi+g) gjev same P: utfalla åleine peikar ikkje ut kva ledd som er feil")

print("\nUventa utfall:", FEIL if FEIL else "ingen")
raise SystemExit(1 if FEIL else 0)
