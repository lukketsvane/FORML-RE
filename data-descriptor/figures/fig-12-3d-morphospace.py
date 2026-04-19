"""
Fig 12 -- 3D morphospace: single perspective view.
W x H x D scatter; color = century; warm palette.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, century_cmap,
                   INK, INK_SOFT, RULE, PAPER, FULL_W)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

apply_style()

df = load_stolar()
geo = df.dropna(subset=["height_cm", "width_cm", "depth_cm", "year_mid"]).copy()
geo = geo[(geo["height_cm"] > 0) & (geo["width_cm"] > 0) &
          (geo["depth_cm"] > 0) & (geo["year_mid"] > 1200)]

# clip outliers
for c in ["height_cm", "width_cm", "depth_cm"]:
    q99 = geo[c].quantile(0.99)
    geo = geo[geo[c] <= q99]

fig = plt.figure(figsize=(FULL_W * 0.7, FULL_W * 0.65))
ax = fig.add_subplot(111, projection="3d")

cmap = century_cmap()
norm = Normalize(vmin=1400, vmax=2025)

sc = ax.scatter(geo["width_cm"], geo["depth_cm"], geo["height_cm"],
                c=geo["year_mid"], cmap=cmap, norm=norm,
                s=6, alpha=0.5, edgecolors="none", rasterized=True)

ax.set_xlabel("Breidde (cm)", fontsize=7, labelpad=2)
ax.set_ylabel("Djupn (cm)", fontsize=7, labelpad=2)
ax.set_zlabel("Hogde (cm)", fontsize=7, labelpad=2)
ax.tick_params(labelsize=5)
ax.view_init(elev=22, azim=40)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor(RULE)
ax.yaxis.pane.set_edgecolor(RULE)
ax.zaxis.pane.set_edgecolor(RULE)
ax.grid(True, alpha=0.15, color=RULE)

cbar = fig.colorbar(sc, ax=ax, fraction=0.025, pad=0.08, shrink=0.65)
cbar.set_label("Årstal", fontsize=7)
cbar.ax.tick_params(labelsize=5)

fig.tight_layout()
save_fig(fig, "fig-12-3d-morphospace")
print("fig-12-3d-morphospace saved")
