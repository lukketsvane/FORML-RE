"""
Generate Figure 2 for the Formakademisk article: grensetilfelle.png

Conceptual 2D placement diagram showing how Formgrammatikk (Stiny & Gips, 1972)
and C-K-teori (Hatchuel & Weil, 2003) are degenerate limiting cases of Formlære.

Axes:
  - vertical: grammatikk-rikdom (triviell bottom -> rik top)
  - horizontal: landskaps-struktur (flatt left -> strukturert right)

Quadrant placements follow the axis semantics (theoretical coherence):
  - top-left  (rik + flatt)        : Formgrammatikk (Stiny & Gips)
  - bottom-right (triviell + strukturert): C-K-teori (Hatchuel & Weil)
  - top-right (rik + strukturert)  : Formlære - full likning  [accent]
  - bottom-left (triviell + flatt) : Utelukka

Output: writings/formakademisk/figures/grensetilfelle.png (1200x800 @ 150 dpi)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
from matplotlib.lines import Line2D

# ----- style -----
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.linewidth": 0.8,
    "savefig.dpi": 150,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})

ACCENT = "#C9A24B"          # muted warm ochre
ACCENT_FILL = "#F3E8C8"     # pale ochre tint
NEUTRAL_DARK = "#2B2B2B"
NEUTRAL_MID = "#6B6B6B"
NEUTRAL_LIGHT = "#AAAAAA"
DIM_FILL = "#F5F5F5"
DIM_TEXT = "#9A9A9A"

# ----- canvas -----
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect("equal")
ax.axis("off")

# plot area (inner region of axes)
PLOT_L, PLOT_R = 1.6, 11.2
PLOT_B, PLOT_T = 1.2, 7.2
MID_X = (PLOT_L + PLOT_R) / 2
MID_Y = (PLOT_B + PLOT_T) / 2

# ----- desaturated bottom-left quadrant fill -----
ax.add_patch(Rectangle(
    (PLOT_L, PLOT_B), MID_X - PLOT_L, MID_Y - PLOT_B,
    facecolor=DIM_FILL, edgecolor="none", zorder=0,
))

# ----- accent fill for top-right Formlære quadrant -----
ax.add_patch(Rectangle(
    (MID_X, MID_Y), PLOT_R - MID_X, PLOT_T - MID_Y,
    facecolor=ACCENT_FILL, edgecolor="none", alpha=0.45, zorder=0,
))
# slightly thicker accent border around Formlære quadrant
ax.add_patch(Rectangle(
    (MID_X, MID_Y), PLOT_R - MID_X, PLOT_T - MID_Y,
    facecolor="none", edgecolor=ACCENT, linewidth=1.4, zorder=1,
))

# ----- dashed quadrant dividers -----
ax.plot([PLOT_L, PLOT_R], [MID_Y, MID_Y],
        linestyle=(0, (4, 4)), color=NEUTRAL_LIGHT, linewidth=0.8, zorder=2)
ax.plot([MID_X, MID_X], [PLOT_B, PLOT_T],
        linestyle=(0, (4, 4)), color=NEUTRAL_LIGHT, linewidth=0.8, zorder=2)

# ----- axes with arrow tips (both ends) -----
ARROW_KW = dict(
    arrowstyle="-|>,head_width=4,head_length=6",
    color=NEUTRAL_DARK, linewidth=1.1, mutation_scale=1.0, zorder=3,
)
# horizontal axis (slightly below bottom of plot area)
ax.add_patch(FancyArrowPatch(
    (PLOT_L - 0.3, PLOT_B - 0.45), (PLOT_R + 0.3, PLOT_B - 0.45), **ARROW_KW
))
# vertical axis (slightly left of plot area)
ax.add_patch(FancyArrowPatch(
    (PLOT_L - 0.45, PLOT_B - 0.3), (PLOT_L - 0.45, PLOT_T + 0.3), **ARROW_KW
))

# ----- axis end labels -----
# horizontal: flatt (left) / strukturert (right)
ax.text(PLOT_L - 0.3, PLOT_B - 0.85, "flatt",
        ha="left", va="top", fontsize=10, color=NEUTRAL_DARK, style="italic")
ax.text(PLOT_R + 0.3, PLOT_B - 0.85, "strukturert",
        ha="right", va="top", fontsize=10, color=NEUTRAL_DARK, style="italic")
# horizontal axis title (centered, below)
ax.text(MID_X, PLOT_B - 1.15, "landskaps-struktur",
        ha="center", va="top", fontsize=11.5, color=NEUTRAL_DARK, weight="semibold")

# vertical: triviell (bottom) / rik (top)
ax.text(PLOT_L - 0.85, PLOT_B - 0.3, "triviell",
        ha="right", va="bottom", fontsize=10, color=NEUTRAL_DARK, style="italic", rotation=90)
ax.text(PLOT_L - 0.85, PLOT_T + 0.3, "rik",
        ha="right", va="top", fontsize=10, color=NEUTRAL_DARK, style="italic", rotation=90)
# vertical axis title (rotated, left)
ax.text(PLOT_L - 1.15, MID_Y, "grammatikk-rikdom",
        ha="right", va="center", fontsize=11.5, color=NEUTRAL_DARK, weight="semibold", rotation=90)

# =======================================================================
# QUADRANT CONTENTS
# =======================================================================

# --- helper for quadrant label blocks ---
def place_label(cx, cy_top, title, subtitle=None, color=NEUTRAL_DARK, bold=True):
    ax.text(cx, cy_top, title,
            ha="center", va="top", fontsize=13,
            weight=("bold" if bold else "normal"), color=color)
    if subtitle:
        ax.text(cx, cy_top - 0.42, subtitle,
                ha="center", va="top", fontsize=10,
                style="italic", color=color)

# ===== TOP-LEFT: Formgrammatikk (Stiny & Gips, 1972) =====
# (rik + flatt)  -- theoretically: rich rewrite rules, no concept landscape
q1_cx = (PLOT_L + MID_X) / 2
q1_top = PLOT_T - 0.35
place_label(q1_cx, q1_top, "Formgrammatikk", "(Stiny & Gips, 1972)", color=NEUTRAL_DARK)

# icon: small square -> triangle rewrite rule
icon_y = q1_top - 1.6
# square
sq_x = q1_cx - 1.15
ax.add_patch(Rectangle((sq_x - 0.22, icon_y - 0.22), 0.44, 0.44,
                       facecolor="none", edgecolor=NEUTRAL_DARK, linewidth=1.2))
# arrow
ax.add_patch(FancyArrowPatch((sq_x + 0.35, icon_y), (sq_x + 1.35, icon_y),
                             arrowstyle="-|>,head_width=3,head_length=4",
                             color=NEUTRAL_DARK, linewidth=1.1))
# triangle
tri_cx = sq_x + 1.7
tri = plt.Polygon([(tri_cx - 0.26, icon_y - 0.22),
                   (tri_cx + 0.26, icon_y - 0.22),
                   (tri_cx, icon_y + 0.28)],
                  closed=True, facecolor="none", edgecolor=NEUTRAL_DARK, linewidth=1.2)
ax.add_patch(tri)
# caption below icon
ax.text(q1_cx, icon_y - 0.65, "a  \u2192  b",
        ha="center", va="top", fontsize=10, style="italic", color=NEUTRAL_MID)

# ===== BOTTOM-RIGHT: C-K-teori (Hatchuel & Weil, 2003) =====
# (triviell + strukturert) -- concept landscape with minimal grammar
q2_cx = (MID_X + PLOT_R) / 2
q2_top = MID_Y - 0.35
place_label(q2_cx, q2_top, "C-K-teori", "(Hatchuel & Weil, 2003)", color=NEUTRAL_DARK)

icon_y = q2_top - 1.55
# circle K (left)
k_x = q2_cx - 0.75
ax.add_patch(Circle((k_x, icon_y), 0.32,
                    facecolor="none", edgecolor=NEUTRAL_DARK, linewidth=1.2))
ax.text(k_x, icon_y, "K", ha="center", va="center",
        fontsize=11, weight="bold", color=NEUTRAL_DARK)
# circle C (right)
c_x = q2_cx + 0.75
ax.add_patch(Circle((c_x, icon_y), 0.32,
                    facecolor="none", edgecolor=NEUTRAL_DARK, linewidth=1.2))
ax.text(c_x, icon_y, "C", ha="center", va="center",
        fontsize=11, weight="bold", color=NEUTRAL_DARK)
# bidirectional arrow between
ax.add_patch(FancyArrowPatch((k_x + 0.35, icon_y), (c_x - 0.35, icon_y),
                             arrowstyle="<|-|>,head_width=3,head_length=4",
                             color=NEUTRAL_DARK, linewidth=1.1))
ax.text(q2_cx, icon_y - 0.62, "K  \u2194  C",
        ha="center", va="top", fontsize=10, style="italic", color=NEUTRAL_MID)

# ===== TOP-RIGHT: Formlære -- full likning  (ACCENT) =====
# (rik + strukturert) -- the target region
q3_cx = (MID_X + PLOT_R) / 2
q3_top = PLOT_T - 0.35
# title + subtitle in accent color
ax.text(q3_cx, q3_top, "Formlære",
        ha="center", va="top", fontsize=14.5, weight="bold", color=ACCENT)
ax.text(q3_cx, q3_top - 0.48, "full likning",
        ha="center", va="top", fontsize=12, weight="semibold", color=ACCENT)
ax.text(q3_cx, q3_top - 0.95, "(den nye ramma)",
        ha="center", va="top", fontsize=9.5, style="italic", color=NEUTRAL_MID)

# icon: Boltzmann-style formula in a thin-bordered box
formula = r"$P \;\propto\; \exp\!\left(-\sum_{i} w_i \, \hat{L}_i\right)$"
form_y = q3_top - 1.95
ax.text(q3_cx, form_y, formula,
        ha="center", va="center", fontsize=12.5, color=NEUTRAL_DARK,
        bbox=dict(boxstyle="round,pad=0.45",
                  facecolor="white", edgecolor=ACCENT, linewidth=0.9))

# ===== BOTTOM-LEFT: Utelukka =====
# (triviell + flatt) -- empty, desaturated
q4_cx = (PLOT_L + MID_X) / 2
q4_top = MID_Y - 0.35
ax.text(q4_cx, q4_top, "Utelukka",
        ha="center", va="top", fontsize=12.5, weight="normal", color=DIM_TEXT)
ax.text(q4_cx, q4_top - 0.48, "verken grammatikk eller landskap",
        ha="center", va="top", fontsize=9.5, style="italic", color=DIM_TEXT)

# ----- save -----
out = Path("C:/Users/Shadow/Documents/GitHub/stolar-db/writings/formakademisk/figures/grensetilfelle.png")
out.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out, dpi=150, bbox_inches="tight", pad_inches=0.3, facecolor="white")
print(f"Saved: {out}")
