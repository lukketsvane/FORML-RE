"""
Fig 06 -- Shape descriptor distributions by style period (ridgeline/violin).
Five mesh features shown as violin plots for the 10 largest style periods.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, style_order,
                   STYLE_COLOR, INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W)
import numpy as np
import matplotlib.pyplot as plt

apply_style()

df = load_stolar()
FEATURES = ["sphericity", "fill_ratio", "inertia_ratio", "complexity", "hull_volume"]
FEAT_LABELS = ["Sphaerisitet", "Fyllgrad", "Tregleiksratio",
               "Kompleksitet\n(log10 v/a)", "Konvekst volum\n(m\u00b3)"]
geo = df.dropna(subset=FEATURES).copy()
styles = style_order(geo, min_n=30)

fig, axes = plt.subplots(1, 5, figsize=(FULL_W, FULL_W * 0.55), sharey=True)

for j, (feat, label) in enumerate(zip(FEATURES, FEAT_LABELS)):
    ax = axes[j]
    data = []
    colors = []
    positions = []
    for i, s in enumerate(styles):
        vals = geo.loc[geo["style"] == s, feat].dropna().values
        data.append(vals)
        colors.append(STYLE_COLOR.get(s, INK_SOFT))
        positions.append(i)

    parts = ax.violinplot(data, positions=positions, vert=False,
                          showmeans=False, showmedians=True,
                          showextrema=False)

    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor(colors[i])
        pc.set_alpha(0.5)
        pc.set_linewidth(0.5)

    parts["cmedians"].set_color(INK)
    parts["cmedians"].set_linewidth(0.8)

    # add individual points (jittered)
    for i, (vals, s) in enumerate(zip(data, styles)):
        if len(vals) > 200:
            idx = np.random.choice(len(vals), 200, replace=False)
            vals_sample = vals[idx]
        else:
            vals_sample = vals
        jitter = np.random.normal(0, 0.12, len(vals_sample))
        ax.scatter(vals_sample, i + jitter, s=1.5,
                   color=colors[i], alpha=0.3, edgecolors="none",
                   rasterized=True)

    ax.set_xlabel(label, fontsize=7)
    ax.axvline(geo[feat].median(), color=RULE, lw=0.5, ls=":", zorder=0)

    if j == 0:
        ax.set_yticks(range(len(styles)))
        ax.set_yticklabels(styles, fontsize=5.5)
    else:
        ax.set_yticklabels([])

    ax.tick_params(axis="x", labelsize=6)

fig.suptitle("")
fig.tight_layout()
save_fig(fig, "fig-06-shape-descriptors")
print("fig-06-shape-descriptors saved")
