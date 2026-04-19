"""
Fig 10 -- Shape space: complexity vs sphericity.
Single-column sized. Scatter colored by century, no KDE (clean).
Style centroids connected chronologically.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, style_order,
                   STYLE_COLOR, century_cmap,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, HALF_W)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

apply_style()

df = load_stolar()
geo = df.dropna(subset=["complexity", "sphericity", "year_mid"]).copy()
geo = geo[geo["year_mid"] > 1200]

fig, ax = plt.subplots(figsize=(HALF_W * 1.8, HALF_W * 1.5))

cmap = century_cmap()
norm = Normalize(1400, 2025)

ax.scatter(geo["complexity"], geo["sphericity"],
           c=geo["year_mid"], cmap=cmap, norm=norm,
           s=5, alpha=0.35, edgecolors="none", rasterized=True)

# style centroids
styles = style_order(geo, min_n=40)
cx = [geo.loc[geo["style"] == s, "complexity"].median() for s in styles]
cy = [geo.loc[geo["style"] == s, "sphericity"].median() for s in styles]
ax.plot(cx, cy, "o-", color=ACCENT_TEAL, markersize=5, lw=1.2,
        markeredgecolor=INK, markeredgewidth=0.4, zorder=4)

# label ends
for idx, offset in [(0, (-6, -8)), (-1, (5, 4))]:
    short = styles[idx].split("/")[0][:12]
    ax.annotate(short, (cx[idx], cy[idx]), fontsize=6, color=ACCENT_TEAL,
                fontweight="bold", xytext=offset, textcoords="offset points")

ax.set_xlabel("Kompleksitet (log10 v/a)")
ax.set_ylabel("Sphaerisitet")

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02, shrink=0.7)
cbar.set_label("Årstal", fontsize=7)
cbar.ax.tick_params(labelsize=5)

fig.tight_layout()
save_fig(fig, "fig-10-shape-space")
print("done")
