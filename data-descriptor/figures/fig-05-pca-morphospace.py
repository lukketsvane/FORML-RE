"""
Fig 05 -- PCA of mesh-derived geometric features.  STAR FIGURE.
Panel A: PC1 vs PC2, warm KDE contour + scatter colored by century.
Panel B: Loading biplot.
Panel C: Scree.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, style_order,
                   STYLE_COLOR, century_cmap,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import gaussian_kde
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

apply_style()

df = load_stolar()
FEATURES = ["sphericity", "fill_ratio", "inertia_ratio", "complexity", "hull_volume"]
LABELS   = ["Sph.", "Fyll.", "Tregl.", "Kompl.", "Vol."]

geo = df.dropna(subset=FEATURES).copy()
X_std = StandardScaler().fit_transform(geo[FEATURES].values)

pca = PCA(n_components=5)
Z = pca.fit_transform(X_std)
geo["PC1"], geo["PC2"] = Z[:, 0], Z[:, 1]
loadings = pca.components_[:2]
vr = pca.explained_variance_ratio_

# soft clip: set axis limits but keep all data for KDE
pc1_lo, pc1_hi = geo["PC1"].quantile(0.01), geo["PC1"].quantile(0.99)
pc2_lo, pc2_hi = geo["PC2"].quantile(0.01), geo["PC2"].quantile(0.99)

print(f"PCA: n={len(geo)}, PC1+PC2={sum(vr[:2]):.1%}")

# ── layout ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(FULL_W, FULL_W * 0.48))
gs = fig.add_gridspec(1, 3, width_ratios=[3, 1, 1], wspace=0.4)
ax = fig.add_subplot(gs[0, 0])
ax_ld = fig.add_subplot(gs[0, 1])
ax_sc = fig.add_subplot(gs[0, 2])

# ── A: KDE contour + scatter ─────────────────────────────────────────────────
cmap_warm = LinearSegmentedColormap.from_list(
    "kraft", [PAPER, "#F5EDD8", HIGHLIGHT, "#D4A84B", ACCENT_RUST, "#5A2A12"])

x, y = geo["PC1"].values, geo["PC2"].values
kde = gaussian_kde(np.vstack([x, y]), bw_method=0.2)
xi = np.linspace(x.min() - 0.3, x.max() + 0.3, 180)
yi = np.linspace(y.min() - 0.3, y.max() + 0.3, 180)
Xi, Yi = np.meshgrid(xi, yi)
Zi = kde(np.vstack([Xi.ravel(), Yi.ravel()])).reshape(Xi.shape)
ax.contourf(Xi, Yi, Zi, levels=10, cmap=cmap_warm, alpha=0.8)
ax.contour(Xi, Yi, Zi, levels=6, colors=INK_SOFT, linewidths=0.25, alpha=0.35)

cmap_c = century_cmap()
norm = Normalize(1400, 2025)
ax.scatter(x, y, c=geo["year_mid"], cmap=cmap_c, norm=norm,
           s=4, alpha=0.4, edgecolors="none", rasterized=True, zorder=2)

# style trajectory
styles = style_order(geo, min_n=40)
cx = [geo.loc[geo["style"] == s, "PC1"].median() for s in styles]
cy = [geo.loc[geo["style"] == s, "PC2"].median() for s in styles]
ax.plot(cx, cy, "o-", color=ACCENT_TEAL, markersize=4, lw=1,
        markeredgecolor=INK, markeredgewidth=0.3, zorder=4, alpha=0.85)

ax.set_xlim(pc1_lo - 0.3, pc1_hi + 0.3)
ax.set_ylim(pc2_lo - 0.3, pc2_hi + 0.3)
ax.set_xlabel(f"PC1 ({vr[0]:.1%})")
ax.set_ylabel(f"PC2 ({vr[1]:.1%})")
annotate_panel(ax, "A")

# ── B: loadings ──────────────────────────────────────────────────────────────
ax_ld.set_xlim(-1.15, 1.15); ax_ld.set_ylim(-1.15, 1.15)
ax_ld.set_aspect("equal")
ax_ld.axhline(0, color=RULE, lw=0.3); ax_ld.axvline(0, color=RULE, lw=0.3)
th = np.linspace(0, 2*np.pi, 80)
ax_ld.plot(np.cos(th), np.sin(th), color=RULE, lw=0.4, ls=":")

ac = [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RUST, INK_SOFT, "#6B5B4F"]
for i, lab in enumerate(LABELS):
    lx, ly = loadings[0, i], loadings[1, i]
    ax_ld.annotate("", xy=(lx, ly), xytext=(0, 0),
                   arrowprops=dict(arrowstyle="-|>", color=ac[i], lw=1.2,
                                   mutation_scale=8))
    ha = "left" if lx >= 0 else "right"
    ax_ld.text(lx + 0.08*np.sign(lx), ly + 0.08*np.sign(ly),
               lab, fontsize=5.5, color=ac[i], ha=ha, fontweight="bold")

ax_ld.set_xlabel("PC1", fontsize=7); ax_ld.set_ylabel("PC2", fontsize=7)
ax_ld.tick_params(labelsize=5)
annotate_panel(ax_ld, "B")

# ── C: scree ─────────────────────────────────────────────────────────────────
ax_sc.bar(range(1,6), vr*100, color=ac, edgecolor="none", width=0.55)
cum = np.cumsum(vr)*100
ax_sc.plot(range(1,6), cum, "o-", color=INK, ms=3, lw=0.8)
for i, v in enumerate(vr*100):
    ax_sc.text(i+1, v+2, f"{v:.0f}%", ha="center", fontsize=5, color=INK_SOFT)
ax_sc.set_xlabel("PC", fontsize=7); ax_sc.set_ylabel("Var. (%)", fontsize=7)
ax_sc.set_xticks(range(1,6)); ax_sc.set_ylim(0, 108)
ax_sc.tick_params(labelsize=5)
annotate_panel(ax_sc, "C")

fig.tight_layout()
save_fig(fig, "fig-05-pca-morphospace")
print("done")
