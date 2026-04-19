"""
Fig 04 -- Data coverage heatmap: field x century.
Shows completeness of each metadata field across centuries.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, fig_full,
                   INK, INK_SOFT, RULE, PAPER, ACCENT_TEAL, HIGHLIGHT)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

apply_style()

df = load_stolar()

# fields to check (display name, column name)
fields = [
    ("Hogde (cm)",          "height_cm"),
    ("Breidde (cm)",        "width_cm"),
    ("Djupn (cm)",          "depth_cm"),
    ("Materialar",          "material"),
    ("Stilperiode",         "style"),
    ("Produksjonsstad",     "origin"),
    ("Nasjonalitet",        "nationality"),
    ("Designar",            "designer"),
    ("Sphaerisitet (mesh)", "sphericity"),
    ("Fyllgrad (mesh)",     "fill_ratio"),
    ("Tregleiksratio (mesh)","inertia_ratio"),
    ("Kompleksitet (mesh)", "complexity"),
    ("Konvekst volum (mesh)","hull_volume"),
    ("Teknikk",             "technique"),
    ("Setehogde (cm)",      "seat_height_cm"),
    ("Vekt (kg)",           "weight_kg"),
]

centuries = sorted([c for c in df["century"].dropna().unique()
                    if c not in ("Ikkje registrert",)],
                   key=lambda x: int(x.split("-")[0]))

# compute coverage matrix
matrix = np.zeros((len(fields), len(centuries)))
counts = np.zeros(len(centuries))

for j, cent in enumerate(centuries):
    mask = df["century"] == cent
    n = mask.sum()
    counts[j] = n
    for i, (_, col) in enumerate(fields):
        if col in df.columns:
            filled = df.loc[mask, col].notna().sum()
            matrix[i, j] = (filled / n * 100) if n > 0 else 0

# colormap: paper (0%) -> highlight (50%) -> teal (100%)
cmap = LinearSegmentedColormap.from_list("coverage",
    [PAPER, HIGHLIGHT, ACCENT_TEAL])

fig, ax = plt.subplots(figsize=(6.69, 4.5))

im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=100)

# labels
ax.set_xticks(range(len(centuries)))
ax.set_xticklabels([f"{c}\n(n={int(counts[i])})" for i, c in enumerate(centuries)],
                   fontsize=5.5, rotation=0)
ax.set_yticks(range(len(fields)))
ax.set_yticklabels([f[0] for f in fields], fontsize=6.5)

# annotate cells with percentage
for i in range(len(fields)):
    for j in range(len(centuries)):
        v = matrix[i, j]
        color = INK if v < 70 else PAPER
        ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                fontsize=5, color=color, fontweight="bold" if v == 100 else "normal")

# overall column
overall = np.zeros(len(fields))
for i, (_, col) in enumerate(fields):
    if col in df.columns:
        overall[i] = df[col].notna().mean() * 100

# add a thin column at the right for overall
ax2 = fig.add_axes([0.88, ax.get_position().y0,
                     0.04, ax.get_position().height])
ax2.imshow(overall.reshape(-1, 1), cmap=cmap, aspect="auto", vmin=0, vmax=100)
ax2.set_xticks([0])
ax2.set_xticklabels(["Totalt"], fontsize=5.5)
ax2.set_yticks([])
for i, v in enumerate(overall):
    color = INK if v < 70 else PAPER
    ax2.text(0, i, f"{v:.0f}", ha="center", va="center",
             fontsize=5, color=color, fontweight="bold" if v >= 99 else "normal")

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01, shrink=0.6)
cbar.set_label("Dekning (%)", fontsize=7)
cbar.ax.tick_params(labelsize=6)

fig.tight_layout()
save_fig(fig, "fig-04-coverage-heatmap")
print("fig-04-coverage-heatmap saved")
