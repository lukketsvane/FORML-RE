"""
Fig 09 -- Convex hull volume as visual mass.
Panel A: Box plots by primary material.
Panel B: Hull volume vs time with LOESS trend.
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
geo = df.dropna(subset=["hull_volume", "year_mid"]).copy()
geo = geo[geo["hull_volume"] > 0]
geo["log_hull"] = np.log10(geo["hull_volume"])

# extract primary material (first in comma-separated list)
geo["primary_material"] = geo["material"].fillna("Ukjend").str.split(",").str[0].str.strip()

# top 10 materials
top_mats = geo["primary_material"].value_counts().head(10).index.tolist()
mat_data = geo[geo["primary_material"].isin(top_mats)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FULL_W, FULL_W * 0.45),
                                gridspec_kw={"width_ratios": [1, 1.3]})

# Panel A: box plots by material
mat_order = (mat_data.groupby("primary_material")["log_hull"]
             .median().sort_values().index.tolist())
data_boxes = [mat_data.loc[mat_data["primary_material"] == m, "log_hull"].values
              for m in mat_order]

bp = ax1.boxplot(data_boxes, vert=False, patch_artist=True,
                 widths=0.6, showfliers=False,
                 medianprops=dict(color=INK, linewidth=1),
                 whiskerprops=dict(color=INK_SOFT, linewidth=0.5),
                 capprops=dict(color=INK_SOFT, linewidth=0.5))

# warm palette matching traktat style
from matplotlib.colors import LinearSegmentedColormap
_warm = LinearSegmentedColormap.from_list("warm", [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RUST])
colors_mat = _warm(np.linspace(0.1, 0.9, len(mat_order)))
for patch, c in zip(bp["boxes"], colors_mat):
    patch.set_facecolor(c)
    patch.set_alpha(0.6)
    patch.set_edgecolor(INK_SOFT)
    patch.set_linewidth(0.5)

ax1.set_yticklabels(mat_order, fontsize=6)
ax1.set_xlabel("log10 konvekst hylster-volum (m\u00b3)", fontsize=7)
annotate_panel(ax1, "A")

# Panel B: hull volume vs time
geo_time = geo[geo["year_mid"] > 1400]
ax2.scatter(geo_time["year_mid"], geo_time["log_hull"],
            s=5, color=ACCENT_TEAL, alpha=0.2, edgecolors="none",
            rasterized=True)

# rolling median trend
bins = np.arange(1400, 2050, 25)
bin_centers = (bins[:-1] + bins[1:]) / 2
medians = []
q25s, q75s = [], []
for lo, hi in zip(bins[:-1], bins[1:]):
    vals = geo_time.loc[(geo_time["year_mid"] >= lo) &
                        (geo_time["year_mid"] < hi), "log_hull"]
    medians.append(vals.median() if len(vals) > 5 else np.nan)
    q25s.append(vals.quantile(0.25) if len(vals) > 5 else np.nan)
    q75s.append(vals.quantile(0.75) if len(vals) > 5 else np.nan)

ax2.fill_between(bin_centers, q25s, q75s, color=ACCENT_RUST, alpha=0.15)
ax2.plot(bin_centers, medians, color=ACCENT_RUST, lw=1.5, label="Median (25-\u00e5rs vindauge)")

ax2.set_xlabel("Årstal")
ax2.set_ylabel("log10 konvekst hylster-volum (m\u00b3)", fontsize=7)
ax2.legend(frameon=False, fontsize=6)
annotate_panel(ax2, "B")

fig.tight_layout()
save_fig(fig, "fig-09-convex-hull-mass")
print("fig-09-convex-hull-mass saved")
