"""
Fig 11 -- Mesh quality validation.
Panel A: Distribution of complexity (proxy for vertex density).
Panel B: Hull volume vs catalog volume (H x W x D) accuracy check.
Panel C: Mesh feature outlier summary.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

apply_style()

df = load_stolar()
geo = df.dropna(subset=["sphericity", "fill_ratio", "inertia_ratio",
                         "complexity", "hull_volume"]).copy()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(FULL_W, FULL_W * 0.35))

# Panel A: complexity distribution
ax1.hist(geo["complexity"], bins=50, color=ACCENT_TEAL, edgecolor="none",
         alpha=0.7)
med = geo["complexity"].median()
ax1.axvline(med, color=ACCENT_RUST, lw=1, ls="--",
            label=f"Median = {med:.2f}")
ax1.set_xlabel("Kompleksitet (log10 v/a)")
ax1.set_ylabel("Antal stolar")
ax1.legend(frameon=False, fontsize=6)
annotate_panel(ax1, "A")

# Panel B: hull volume vs catalog bounding box volume
dims = df.dropna(subset=["height_cm", "width_cm", "depth_cm",
                          "hull_volume"]).copy()
dims = dims[(dims["hull_volume"] > 0) & (dims["height_cm"] > 0)]
# catalog volume in m^3
dims["catalog_vol"] = (dims["height_cm"] * dims["width_cm"] * dims["depth_cm"]) / 1e6

ax2.scatter(dims["catalog_vol"], dims["hull_volume"],
            s=6, color=ACCENT_TEAL, alpha=0.3, edgecolors="none",
            rasterized=True)

# perfect fit line
lim = max(dims["catalog_vol"].quantile(0.99), dims["hull_volume"].quantile(0.99))
ax2.plot([0, lim], [0, lim], color=RULE, lw=0.8, ls=":", label="1:1 linje")

# correlation
from scipy.stats import pearsonr
r, p = pearsonr(dims["catalog_vol"], dims["hull_volume"])
ax2.text(0.05, 0.95, f"r = {r:.3f}\nn = {len(dims)}",
         transform=ax2.transAxes, fontsize=6, va="top", color=INK_SOFT)

ax2.set_xlabel("Katalogvolum H\u00d7B\u00d7D (m\u00b3)")
ax2.set_ylabel("Konvekst hylster-volum (m\u00b3)")
ax2.set_xlim(0, lim * 1.05)
ax2.set_ylim(0, lim * 1.05)
ax2.legend(frameon=False, fontsize=6)
annotate_panel(ax2, "B")

# Panel C: feature distributions summary (box plots of all 5 features, z-scored)
from sklearn.preprocessing import StandardScaler
features = ["sphericity", "fill_ratio", "inertia_ratio", "complexity", "hull_volume"]
labels = ["Sph.", "Fyll.", "Tregl.", "Kompl.", "Vol."]
X = geo[features].values
X_z = StandardScaler().fit_transform(X)

bp = ax3.boxplot(X_z, vert=True, patch_artist=True, widths=0.5,
                 showfliers=True,
                 flierprops=dict(marker=".", markersize=2, color=ACCENT_RUST, alpha=0.4),
                 medianprops=dict(color=INK, linewidth=1),
                 whiskerprops=dict(color=INK_SOFT, linewidth=0.5),
                 capprops=dict(color=INK_SOFT, linewidth=0.5))

colors_bp = [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RUST, INK_SOFT, "#6B5B4F"]
for patch, c in zip(bp["boxes"], colors_bp):
    patch.set_facecolor(c)
    patch.set_alpha(0.5)
    patch.set_edgecolor(INK_SOFT)

ax3.set_xticklabels(labels, fontsize=6)
ax3.set_ylabel("z-skore")
ax3.axhline(0, color=RULE, lw=0.4, ls=":")
ax3.axhline(3, color=ACCENT_RUST, lw=0.5, ls="--", alpha=0.5)
ax3.axhline(-3, color=ACCENT_RUST, lw=0.5, ls="--", alpha=0.5)

# count outliers
n_out = np.sum(np.abs(X_z) > 3)
ax3.text(0.95, 0.95, f"{n_out} uteliggjarar\n(|z| > 3)",
         transform=ax3.transAxes, fontsize=6, va="top", ha="right",
         color=ACCENT_RUST)
annotate_panel(ax3, "C")

fig.tight_layout()
save_fig(fig, "fig-11-mesh-quality")
print("fig-11-mesh-quality saved")
