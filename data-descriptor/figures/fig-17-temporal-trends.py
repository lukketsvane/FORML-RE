"""
Fig 17 -- Temporal trends in all four mesh features.
Four-panel scatter with LOESS-like rolling median + Spearman rho annotation.
THE science figure: shows chairs getting rounder and more compact over 500 years.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, century_cmap,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.stats import spearmanr

apply_style()

df = load_stolar()
geo = df.dropna(subset=["sphericity","fill_ratio","inertia_ratio","complexity","year_mid"]).copy()
geo = geo[(geo["year_mid"] > 1450) & (geo["year_mid"] < 2025)]

features = [
    ("sphericity",    "Sphaerisitet",   ACCENT_TEAL),
    ("inertia_ratio", "Tregleiksratio", ACCENT_GOLD),
    ("complexity",    "Kompleksitet",   ACCENT_RUST),
    ("fill_ratio",    "Fyllgrad",       INK_SOFT),
]

fig, axes = plt.subplots(2, 2, figsize=(FULL_W, FULL_W * 0.55), sharex=True)
axes = axes.flatten()

cmap = century_cmap()
norm = Normalize(1450, 2025)

for idx, (feat, label, color) in enumerate(features):
    ax = axes[idx]

    # scatter colored by year
    ax.scatter(geo["year_mid"], geo[feat],
               c=geo["year_mid"], cmap=cmap, norm=norm,
               s=3, alpha=0.25, edgecolors="none", rasterized=True)

    # rolling median (50-year window)
    bins = np.arange(1450, 2050, 25)
    meds, q25s, q75s, centers = [], [], [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        vals = geo.loc[(geo["year_mid"] >= lo) & (geo["year_mid"] < hi), feat]
        if len(vals) > 5:
            meds.append(vals.median())
            q25s.append(vals.quantile(0.25))
            q75s.append(vals.quantile(0.75))
            centers.append((lo + hi) / 2)

    ax.fill_between(centers, q25s, q75s, color=color, alpha=0.15)
    ax.plot(centers, meds, color=color, lw=2, zorder=3)

    # Spearman correlation
    rho, p = spearmanr(geo["year_mid"], geo[feat])
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    ax.text(0.03, 0.95, f"$\\rho$ = {rho:.3f}{sig}",
            transform=ax.transAxes, fontsize=7, va="top", color=color,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=PAPER,
                      edgecolor=color, linewidth=0.5, alpha=0.9))

    ax.set_ylabel(label, fontsize=7)
    annotate_panel(ax, chr(65 + idx))

axes[2].set_xlabel("Årstal")
axes[3].set_xlabel("Årstal")

fig.tight_layout()
save_fig(fig, "fig-17-temporal-trends")
print("done")
