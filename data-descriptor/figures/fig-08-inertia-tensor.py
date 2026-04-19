"""
Fig 08 -- Inertia tensor: elongation vs compactness space.
Scatter of inertia_ratio vs sphericity with marginal densities.
Colored by century. Quadrant labels for interpretation.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, century_cmap,
                   CENTURY_COLORS, INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

apply_style()

df = load_stolar()
geo = df.dropna(subset=["inertia_ratio", "sphericity", "year_mid"]).copy()
geo = geo[geo["year_mid"] > 1200]

fig = plt.figure(figsize=(FULL_W, FULL_W * 0.75))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 4], width_ratios=[4, 1],
                      hspace=0.05, wspace=0.05)
ax_main = fig.add_subplot(gs[1, 0])
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)

# color by century
cmap = century_cmap()
norm = Normalize(vmin=1300, vmax=2025)
colors = cmap(norm(geo["year_mid"].values))

# main scatter
ax_main.scatter(geo["inertia_ratio"], geo["sphericity"],
                c=geo["year_mid"], cmap=cmap, norm=norm,
                s=8, alpha=0.45, edgecolors="none", rasterized=True)

# quadrant labels
kw = dict(fontsize=6.5, color=INK_SOFT, fontstyle="italic", alpha=0.7)
x_mid = geo["inertia_ratio"].median()
y_mid = geo["sphericity"].median()
ax_main.text(0.05, 0.97, "Langstrekt, rund", transform=ax_main.transAxes,
             va="top", ha="left", **kw)
ax_main.text(0.95, 0.97, "Kompakt, rund", transform=ax_main.transAxes,
             va="top", ha="right", **kw)
ax_main.text(0.05, 0.03, "Langstrekt, kantete", transform=ax_main.transAxes,
             va="bottom", ha="left", **kw)
ax_main.text(0.95, 0.03, "Kompakt, kantete", transform=ax_main.transAxes,
             va="bottom", ha="right", **kw)

ax_main.set_xlabel("Tregleiksratio (0 = langstrekt; 1 = isotrop)")
ax_main.set_ylabel("Sphaerisitet (0 = kantete; 1 = kuleforma)")

# marginal histograms
ax_histx.hist(geo["inertia_ratio"], bins=50, color=ACCENT_TEAL,
              edgecolor="none", alpha=0.6)
ax_histx.axis("off")

ax_histy.hist(geo["sphericity"], bins=50, color=ACCENT_TEAL,
              edgecolor="none", alpha=0.6, orientation="horizontal")
ax_histy.axis("off")

# colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(sm, ax=ax_histy, fraction=0.8, pad=0.1, shrink=0.7)
cbar.set_label("Årstal", fontsize=7)
cbar.ax.tick_params(labelsize=6)

annotate_panel(ax_main, "")

fig.tight_layout()
save_fig(fig, "fig-08-inertia-tensor")
print("fig-08-inertia-tensor saved")
