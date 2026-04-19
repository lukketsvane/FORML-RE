"""
Fig 16 -- Morphospace evolution kymograph.
Shows how the distribution of sphericity (or PC1) shifts over time.
Ridge/joy plot with one KDE per half-century, stacked vertically.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, century_cmap,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize

apply_style()

df = load_stolar()
geo = df.dropna(subset=["sphericity", "year_mid"]).copy()
geo = geo[(geo["year_mid"] > 1450) & (geo["sphericity"] > 0)]

# 50-year bins
bins = np.arange(1450, 2050, 50)
bin_labels = [f"{int(b)}s" for b in bins[:-1]]

fig, ax = plt.subplots(figsize=(FULL_W * 0.75, FULL_W * 0.9))

cmap = century_cmap()
norm = Normalize(1450, 2000)
x_grid = np.linspace(0.05, 1.0, 200)

scale = 4.0  # vertical scale for KDE
for i, (lo, hi) in enumerate(zip(bins[:-1], bins[1:])):
    mask = (geo["year_mid"] >= lo) & (geo["year_mid"] < hi)
    vals = geo.loc[mask, "sphericity"].values
    if len(vals) < 5:
        continue

    kde = gaussian_kde(vals, bw_method=0.15)
    density = kde(x_grid)
    density = density / density.max() * scale  # normalize to max height

    baseline = i
    color = cmap(norm(lo))

    ax.fill_between(x_grid, baseline, baseline + density,
                    color=color, alpha=0.6, edgecolor="none")
    ax.plot(x_grid, baseline + density, color=color, lw=0.8)
    ax.plot([vals.mean()], [baseline + 0.15], "|",
            color=INK, markersize=6, markeredgewidth=0.8)

    # period label
    n = len(vals)
    ax.text(-0.02, baseline + 0.3, f"{int(lo)}",
            fontsize=6, color=INK_SOFT, ha="right", va="bottom")
    ax.text(1.03, baseline + 0.3, f"n={n}",
            fontsize=5, color=INK_SOFT, ha="left", va="bottom")

ax.set_xlabel("Sphaerisitet")
ax.set_ylabel("")
ax.set_xlim(-0.05, 1.08)
ax.set_yticks([])
ax.spines["left"].set_visible(False)

# arrow indicating time direction
ax.annotate("", xy=(-0.08, len(bins) - 2), xytext=(-0.08, 0),
            arrowprops=dict(arrowstyle="->", color=INK_SOFT, lw=1),
            annotation_clip=False)
ax.text(-0.12, (len(bins) - 2) / 2, "Tid", rotation=90,
        fontsize=7, color=INK_SOFT, ha="center", va="center")

fig.tight_layout()
save_fig(fig, "fig-16-morphospace-evolution")
print("done")
