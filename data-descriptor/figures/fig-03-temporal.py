"""
Fig 03 -- Temporal distribution of chairs in the STOLAR database.
Stacked histogram by museum source; 50-year bins; clean period markers.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, fig_full,
                   INK, INK_SOFT, RULE, ACCENT_TEAL, ACCENT_RUST,
                   ACCENT_GOLD, HIGHLIGHT, FULL_W)
import numpy as np
import matplotlib.pyplot as plt

apply_style()

df = load_stolar()
df = df[df["year_from"] > 1200].copy()

bins = np.arange(1250, 2075, 50)

nm = df[df["museum"] == "Nasjonalmuseet"]["year_mid"].dropna()
va = df[df["museum"] == "V&A"]["year_mid"].dropna()

fig, ax = plt.subplots(figsize=(FULL_W, FULL_W * 0.38))

ax.hist([va, nm], bins=bins, stacked=True,
        color=[ACCENT_TEAL, ACCENT_RUST],
        edgecolor=RULE, linewidth=0.3,
        label=["Victoria and Albert Museum", "Nasjonalmuseet"],
        alpha=0.85, rwidth=0.92)

# period brackets at top (non-overlapping)
ymax = 220
periods = [
    (1400, 1600, "Renessanse"),
    (1600, 1730, "Barokk"),
    (1730, 1790, "Rokokko"),
    (1790, 1840, "Empire"),
    (1840, 1910, "Historisme"),
    (1920, 1970, "Modernisme"),
    (1970, 2025, "Samtid"),
]
for y_off, (start, end, label) in zip(
        [ymax+5]*len(periods), periods):
    mid = (start + end) / 2
    ax.annotate("", xy=(start, ymax), xytext=(end, ymax),
                arrowprops=dict(arrowstyle="|-|", color=RULE, lw=0.5,
                                mutation_scale=3))
    ax.text(mid, ymax + 8, label, ha="center", fontsize=5,
            color=INK_SOFT, fontstyle="italic")

ax.set_xlabel("Årstal")
ax.set_ylabel("Antal stolar")
ax.set_xlim(1250, 2050)
ax.set_ylim(0, ymax + 25)
ax.legend(loc="upper left", frameon=False, fontsize=6.5)

fig.tight_layout()
save_fig(fig, "fig-03-temporal")
print("fig-03-temporal saved")
