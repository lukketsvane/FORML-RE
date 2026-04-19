"""
Fig 18 -- Golden ratio test.
Distribution of H:W ratio with the golden ratio (1.618) marked.
One-sample t-test: is the mean H:W indistinguishable from phi?
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp

apply_style()

df = load_stolar()
geo = df.dropna(subset=["height_cm", "width_cm"]).copy()
geo = geo[(geo["height_cm"] > 10) & (geo["width_cm"] > 10)]
geo["hw"] = geo["height_cm"] / geo["width_cm"]
hw = geo["hw"]
hw = hw[(hw > 0.5) & (hw < 4)]  # remove extreme outliers

phi = (1 + np.sqrt(5)) / 2  # 1.618...

t_stat, p_val = ttest_1samp(hw, phi)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FULL_W, FULL_W * 0.35),
                                gridspec_kw={"width_ratios": [2, 1]})

# Panel A: histogram of H:W ratio
ax1.hist(hw, bins=60, color=ACCENT_TEAL, edgecolor="none", alpha=0.7,
         density=True)

# golden ratio line
ax1.axvline(phi, color=ACCENT_RUST, lw=2, ls="-",
            label=f"Gylne snitt ($\\phi$ = {phi:.3f})")
# mean line
ax1.axvline(hw.mean(), color=ACCENT_GOLD, lw=1.5, ls="--",
            label=f"Gjennomsnitt = {hw.mean():.3f}")

ax1.set_xlabel("Hogde : Breidde ratio")
ax1.set_ylabel("Tettleik")
ax1.legend(frameon=False, fontsize=6.5, loc="upper right")

# test result
ax1.text(0.03, 0.95,
         f"t = {t_stat:.2f}, p = {p_val:.3f}\nn = {len(hw)}",
         transform=ax1.transAxes, fontsize=7, va="top", color=INK_SOFT,
         bbox=dict(boxstyle="round,pad=0.3", facecolor=PAPER,
                   edgecolor=RULE, linewidth=0.5))
annotate_panel(ax1, "A")

# Panel B: H:W ratio over time
geo_t = geo[geo["year_mid"] > 1450].copy()
bins = np.arange(1450, 2050, 50)
means, stds, centers = [], [], []
for lo, hi in zip(bins[:-1], bins[1:]):
    vals = geo_t.loc[(geo_t["year_mid"] >= lo) & (geo_t["year_mid"] < hi), "hw"]
    vals = vals[(vals > 0.5) & (vals < 4)]
    if len(vals) > 5:
        means.append(vals.mean())
        stds.append(vals.std())
        centers.append((lo + hi) / 2)

ax2.errorbar(centers, means, yerr=stds, color=ACCENT_TEAL,
             fmt="o-", markersize=4, lw=1, capsize=2, capthick=0.5)
ax2.axhline(phi, color=ACCENT_RUST, lw=1.5, ls="-", alpha=0.7)
ax2.set_xlabel("Årstal")
ax2.set_ylabel("H:W ratio")
ax2.set_ylim(0.5, 3.0)
ax2.text(2030, phi + 0.05, "$\\phi$", fontsize=7, color=ACCENT_RUST, va="bottom")
annotate_panel(ax2, "B")

fig.tight_layout()
save_fig(fig, "fig-18-golden-ratio")
print(f"Golden ratio test: mean={hw.mean():.3f}, phi={phi:.3f}, t={t_stat:.2f}, p={p_val:.3f}")
