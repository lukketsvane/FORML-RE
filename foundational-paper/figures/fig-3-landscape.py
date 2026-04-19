"""
Figure 1, Panel B: Fitness landscape as KDE density + gradient vectors.
Generates fig-3-landscape.pdf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

# ── Load data ──
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
df = pd.read_csv(os.path.join(REPO, "STOLAR", "STOLAR.csv"))

# ── Map Nynorsk column names ──
df = df.rename(columns={
    "Breidde (cm)": "w_cm",
    "Høgde (cm)": "h_cm",
    "Frå år": "year_from",
    "Til år": "year_to",
})
df["w_cm"] = pd.to_numeric(df["w_cm"], errors="coerce")
df["h_cm"] = pd.to_numeric(df["h_cm"], errors="coerce")
df["year_mid"] = (pd.to_numeric(df["year_from"], errors="coerce") +
                  pd.to_numeric(df["year_to"], errors="coerce")) / 2

# ── Clean ──
df = df.dropna(subset=["w_cm", "h_cm", "year_mid"])
df = df[(df["w_cm"] > 0) & (df["h_cm"] > 0)]
df = df[(df["year_mid"] >= 1500) & (df["year_mid"] <= 2025)]

x = df["w_cm"].values
y = df["h_cm"].values

# ── KDE ──
xmin, xmax = 10, 110
ymin, ymax = 30, 170
xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([x, y])
kde = gaussian_kde(values, bw_method=0.15)
zz = np.reshape(kde(positions), xx.shape)

# ── Gradient field ──
grad_y, grad_x = np.gradient(zz, yy[0, 1] - yy[0, 0], xx[1, 0] - xx[0, 0])
step = 12
gx = grad_x[::step, ::step]
gy = grad_y[::step, ::step]
mag = np.sqrt(gx**2 + gy**2)
mag[mag == 0] = 1
gx_n = gx / mag
gy_n = gy / mag

# ── Centroid trajectory ──
periods = sorted(df["year_mid"].apply(lambda y: (y // 50) * 50).unique())
centroids_w = []
centroids_h = []
for p in periods:
    mask = (df["year_mid"] >= p) & (df["year_mid"] < p + 50)
    sub = df[mask]
    if len(sub) >= 5:
        centroids_w.append(sub["w_cm"].median())
        centroids_h.append(sub["h_cm"].median())
    else:
        centroids_w.append(np.nan)
        centroids_h.append(np.nan)

# ── Plot ──
fig, ax = plt.subplots(figsize=(5.5, 4.5))

# Density surface
cf = ax.contourf(xx, yy, zz, levels=20, cmap="Greys", alpha=0.7)
ax.contour(xx, yy, zz, levels=8, colors="black", linewidths=0.3, alpha=0.5)

# Gradient vectors
ax.quiver(
    xx[::step, ::step], yy[::step, ::step],
    gx_n, gy_n,
    mag[mag > 0].mean() * np.ones_like(gx_n),
    cmap="Oranges", scale=30, width=0.004, alpha=0.5, headwidth=3
)

# Centroid trajectory
cw = np.array(centroids_w, dtype=float)
ch = np.array(centroids_h, dtype=float)
valid = ~np.isnan(cw)
ax.plot(cw[valid], ch[valid], "o-", color="crimson", markersize=4,
        linewidth=1.5, alpha=0.8, label="Period centroids")

# Labels
ax.set_xlabel("Width (cm)", fontsize=10)
ax.set_ylabel("Height (cm)", fontsize=10)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.tick_params(labelsize=8)
ax.legend(fontsize=7, loc="upper right")

ax.set_title("B. Fitness Landscape", fontsize=11, fontweight="bold", loc="left")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig-3-landscape.pdf")
fig.savefig(out, dpi=300, bbox_inches="tight")
print(f"Saved: {out}")
