"""
Fig 13 -- Gemini Vision enrichment: structural annotation summary.
4 panels: component count, structure type, ornament level, back type.
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, save_fig, DATA,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W,
                   annotate_panel)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

apply_style()

with open(DATA / "enriched_chairs.json") as f:
    raw = json.load(f)

records = list(raw.values())
n = len(records)
print(f"Enriched chairs: {n}")

fig, axes = plt.subplots(2, 2, figsize=(FULL_W, FULL_W * 0.55))
(ax1, ax2), (ax3, ax4) = axes

# A: Component count
comps = [r.get("tal_komponentar", 0) for r in records]
ax1.hist(comps, bins=range(0, max(comps)+2), color=ACCENT_TEAL,
         edgecolor=RULE, linewidth=0.3, alpha=0.8, align="left")
ax1.set_xlabel("Tal komponentar")
ax1.set_ylabel("Antal stolar")
med = np.median(comps)
ax1.axvline(med, color=ACCENT_RUST, lw=1, ls="--")
ax1.text(med + 0.3, ax1.get_ylim()[1] * 0.9, f"median = {med:.0f}",
         fontsize=6, color=ACCENT_RUST)
annotate_panel(ax1, "A")

# B: Structure type
structs = Counter(r.get("struktur_type", "ukjend") for r in records)
labels, counts = zip(*structs.most_common())
# translate for display
display = {"fire-bein": "Fire-bein", "anna": "Anna", "pidestall": "Pidestall",
           "frittberande": "Frittberande", "gyngande": "Gyngande",
           "stablbar": "Stablbar", "samanleggbar": "Samanleggbar",
           "bukk": "Bukk"}
labels_d = [display.get(l, l) for l in labels]
colors_b = [ACCENT_TEAL] + [ACCENT_GOLD] * (len(labels) - 1)
ax2.barh(range(len(labels)), counts, color=colors_b, edgecolor="none", height=0.6)
ax2.set_yticks(range(len(labels)))
ax2.set_yticklabels(labels_d, fontsize=6)
ax2.set_xlabel("Antal")
ax2.invert_yaxis()
annotate_panel(ax2, "B")

# C: Ornament level
orn = Counter(r.get("ornament_nivaa", 0) for r in records)
orn_labels = ["0: Ingen", "1: Enkel", "2: Moderat", "3: Rikt"]
orn_vals = [orn.get(i, 0) for i in range(4)]
orn_colors = [RULE, ACCENT_GOLD, ACCENT_RUST, "#5A2A12"]
ax3.bar(range(4), orn_vals, color=orn_colors, edgecolor="none", width=0.6)
ax3.set_xticks(range(4))
ax3.set_xticklabels(orn_labels, fontsize=6)
ax3.set_ylabel("Antal stolar")
annotate_panel(ax3, "C")

# D: Back type
backs = Counter(r.get("rygg_type", "ukjend") for r in records)
back_display = {"polstra": "Polstra", "heiltre": "Heiltre", "ingen": "Ingen",
                "open": "Open", "spiler": "Spiler"}
b_labels, b_counts = zip(*backs.most_common())
b_labels_d = [back_display.get(l, l) for l in b_labels]
b_colors = [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RUST, INK_SOFT, RULE][:len(b_labels)]
ax4.barh(range(len(b_labels)), b_counts, color=b_colors, edgecolor="none", height=0.6)
ax4.set_yticks(range(len(b_labels)))
ax4.set_yticklabels(b_labels_d, fontsize=6)
ax4.set_xlabel("Antal")
ax4.invert_yaxis()
annotate_panel(ax4, "D")

fig.suptitle(f"Visjonsbasert strukturell annotering (n = {n})", fontsize=9, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.96])
save_fig(fig, "fig-13-enrichment")
print("fig-13-enrichment saved")
