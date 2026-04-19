"""
Fig 15 -- Style fingerprints: radar/polar charts for major style periods.
Each style gets a normalized feature profile showing its geometric signature.
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
FEATURES = ["sphericity", "fill_ratio", "inertia_ratio", "complexity", "hull_volume",
            "height_cm", "width_cm", "depth_cm"]
LABELS = ["Sph.", "Fyll.", "Tregl.", "Kompl.", "Vol.", "H", "B", "D"]

geo = df.dropna(subset=FEATURES).copy()

# z-score all features for comparability
from sklearn.preprocessing import StandardScaler
X = geo[FEATURES].values
X_z = StandardScaler().fit_transform(X)
for i, f in enumerate(FEATURES):
    geo[f"z_{f}"] = X_z[:, i]

styles = style_order(geo, min_n=40)
n_styles = len(styles)

# radar chart setup
angles = np.linspace(0, 2 * np.pi, len(FEATURES), endpoint=False).tolist()
angles += angles[:1]  # close the polygon

ncols = 4
nrows = (n_styles + ncols - 1) // ncols
fig, axes = plt.subplots(nrows, ncols, figsize=(FULL_W, FULL_W * 0.45 * nrows / 2),
                          subplot_kw=dict(polar=True))
axes = axes.flatten()

for idx, style in enumerate(styles):
    ax = axes[idx]
    mask = geo["style"] == style
    medians = [geo.loc[mask, f"z_{f}"].median() for f in FEATURES]
    medians += medians[:1]

    color = STYLE_COLOR.get(style, INK_SOFT)
    ax.fill(angles, medians, color=color, alpha=0.2)
    ax.plot(angles, medians, color=color, lw=1.5, marker="o", markersize=3)

    # reference circle at z=0
    ax.plot(angles, [0] * len(angles), color=RULE, lw=0.4, ls=":")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(LABELS, fontsize=4.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["-1", "0", "+1"], fontsize=3.5, color=INK_SOFT)

    short = style.split("/")[0].strip()
    if len(short) > 12:
        short = short[:11] + "."
    n = mask.sum()
    ax.set_title(f"{short}\n(n={n})", fontsize=6, pad=8, color=color, fontweight="bold")

# hide unused axes
for idx in range(len(styles), len(axes)):
    axes[idx].set_visible(False)

fig.tight_layout()
save_fig(fig, "fig-15-style-fingerprints")
print("done")
