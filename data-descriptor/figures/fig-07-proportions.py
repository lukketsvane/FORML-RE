"""
Fig 07 -- Proportion ratios over time.
H:W, H:D, W:D as flowing ribbons with IQR bands, 25-year bins.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

apply_style()

df = load_stolar()
dims = df.dropna(subset=["height_cm", "width_cm", "depth_cm", "year_mid"]).copy()
dims = dims[(dims["year_mid"] > 1400) & (dims["height_cm"] > 0) &
            (dims["width_cm"] > 0) & (dims["depth_cm"] > 0)]

dims["H_W"] = dims["height_cm"] / dims["width_cm"]
dims["H_D"] = dims["height_cm"] / dims["depth_cm"]
dims["W_D"] = dims["width_cm"]  / dims["depth_cm"]

# bin by 25 years
dims["bin"] = (dims["year_mid"] // 25) * 25

ratios = [("H_W", "Hogde : Breidde", ACCENT_TEAL),
          ("H_D", "Hogde : Djupn",   ACCENT_RUST),
          ("W_D", "Breidde : Djupn", ACCENT_GOLD)]

fig, ax = plt.subplots(figsize=(FULL_W, FULL_W * 0.45))

for col, label, color in ratios:
    stats = dims.groupby("bin")[col].agg(["median", lambda x: x.quantile(0.25),
                                          lambda x: x.quantile(0.75)])
    stats.columns = ["median", "q25", "q75"]
    stats = stats.dropna()
    x = stats.index.values
    ax.fill_between(x, stats["q25"], stats["q75"], color=color, alpha=0.15)
    ax.plot(x, stats["median"], color=color, lw=1.5, label=label)

# reference: ratio = 1
ax.axhline(1.0, color=RULE, lw=0.8, ls=":", zorder=0)
ax.text(2030, 1.02, "1:1", fontsize=6, color=RULE, va="bottom")

# period markers
for yr, label in [(1750, "Rokokko"), (1850, "Industri"),
                  (1925, "Modernisme"), (1970, "Postmod.")]:
    ax.axvline(yr, color=RULE, lw=0.4, ls=":", zorder=0, alpha=0.5)
    ax.text(yr + 3, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 3.5,
            label, fontsize=5, color=INK_SOFT, va="top", fontstyle="italic")

ax.set_xlabel("Årstal")
ax.set_ylabel("Proporsjonsratio")
ax.set_xlim(1400, 2030)
ax.legend(frameon=False, fontsize=7, loc="upper right")

fig.tight_layout()
save_fig(fig, "fig-07-proportions")
print("fig-07-proportions saved")
