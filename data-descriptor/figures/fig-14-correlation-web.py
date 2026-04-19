"""
Fig 14 -- Feature correlation web.
Heatmap of all pairwise correlations between dimensions and mesh features.
Annotated with r-values; warm palette matching traktat style.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

apply_style()

df = load_stolar()
cols = ["height_cm", "width_cm", "depth_cm",
        "sphericity", "fill_ratio", "inertia_ratio", "complexity", "hull_volume"]
labels = ["Hogde", "Breidde", "Djupn",
          "Sph.", "Fyll.", "Tregl.", "Kompl.", "Vol."]

geo = df.dropna(subset=cols)
corr = geo[cols].corr()

# diverging colormap: teal (negative) -> paper (zero) -> rust (positive)
cmap = LinearSegmentedColormap.from_list(
    "corr", [ACCENT_TEAL, "#7AACB8", PAPER, "#D4956A", ACCENT_RUST])

fig, ax = plt.subplots(figsize=(FULL_W * 0.6, FULL_W * 0.55))

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
masked = np.ma.masked_where(mask, corr.values)

im = ax.imshow(masked, cmap=cmap, vmin=-1, vmax=1, aspect="equal")

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=7, rotation=45, ha="right")
ax.set_yticklabels(labels, fontsize=7)

# annotate lower triangle with r-values
for i in range(len(labels)):
    for j in range(len(labels)):
        if i > j:
            r = corr.values[i, j]
            color = PAPER if abs(r) > 0.4 else INK_SOFT
            weight = "bold" if abs(r) > 0.3 else "normal"
            ax.text(j, i, f"{r:.2f}", ha="center", va="center",
                    fontsize=6.5, color=color, fontweight=weight)

# diagonal labels
for i in range(len(labels)):
    ax.text(i, i, labels[i], ha="center", va="center",
            fontsize=7, color=INK, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=PAPER,
                      edgecolor=RULE, linewidth=0.5))

cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02, shrink=0.8)
cbar.set_label("Pearson r", fontsize=7)
cbar.ax.tick_params(labelsize=6)

ax.spines[:].set_visible(False)
ax.tick_params(length=0)

fig.tight_layout()
save_fig(fig, "fig-14-correlation-web")
print("done")
