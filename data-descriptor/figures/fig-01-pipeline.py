"""
Fig 01 -- Data pipeline flow diagram.
Three stages: Data Acquisition -> Image Processing -> 3D Reconstruction.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, save_fig, FULL_W, GOLDEN, DPI,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_GOLD, ACCENT_RUST)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

apply_style()

fig, ax = plt.subplots(figsize=(FULL_W, FULL_W / 2.8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 40)
ax.axis("off")

# ── helper functions ─────────────────────────────────────────────────────────

def draw_box(ax, x, y, w, h, color, label, sublabel="", alpha=0.15):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.6",
                         facecolor=color, edgecolor=color,
                         alpha=alpha, linewidth=1.2)
    ax.add_patch(box)
    border = FancyBboxPatch((x, y), w, h,
                            boxstyle="round,pad=0.6",
                            facecolor="none", edgecolor=color,
                            linewidth=1.2)
    ax.add_patch(border)
    ax.text(x + w/2, y + h/2 + (1.2 if sublabel else 0), label,
            ha="center", va="center", fontsize=7.5, fontweight="bold",
            color=color)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 1.5, sublabel,
                ha="center", va="center", fontsize=6, color=INK_SOFT)


def draw_arrow(ax, x1, y, x2, label=""):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=INK_SOFT,
                                lw=1.0, mutation_scale=12))
    if label:
        ax.text((x1 + x2) / 2, y + 1.5, label,
                ha="center", va="bottom", fontsize=5.5, color=INK_SOFT,
                fontstyle="italic")


def draw_small_box(ax, x, y, w, h, color, label):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.3",
                         facecolor=PAPER, edgecolor=color,
                         linewidth=0.8)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label,
            ha="center", va="center", fontsize=5.5, color=INK_SOFT)


# ── stage headers ────────────────────────────────────────────────────────────
ax.text(15, 38, "1. Datainnhenting", ha="center", fontsize=8.5,
        fontweight="bold", color=ACCENT_TEAL)
ax.text(50, 38, "2. Bileteprosessering", ha="center", fontsize=8.5,
        fontweight="bold", color=ACCENT_GOLD)
ax.text(85, 38, "3. 3D-rekonstruksjon", ha="center", fontsize=8.5,
        fontweight="bold", color=ACCENT_RUST)

# ── stage 1: data acquisition ────────────────────────────────────────────────
draw_small_box(ax, 2, 27, 11, 5, ACCENT_TEAL, "Nasjonalmuseet\nAPI")
draw_small_box(ax, 17, 27, 11, 5, ACCENT_TEAL, "V&A\nAPI")
draw_arrow(ax, 13.5, 29.5, 16.5)

draw_box(ax, 4, 16, 22, 8, ACCENT_TEAL,
         "Konsolidering", "Kolonneharmonisering\nNN-omsetjing\nStilklassifisering")

ax.annotate("", xy=(15, 24), xytext=(8, 27),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.7))
ax.annotate("", xy=(15, 24), xytext=(22, 27),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.7))

draw_box(ax, 6, 4, 18, 7, ACCENT_TEAL,
         "2 048 stolar", "30 metadatafelt\n99% dimensjonsdekning")
ax.annotate("", xy=(15, 11), xytext=(15, 16),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.7))

# ── stage 2: image processing ────────────────────────────────────────────────
draw_box(ax, 36, 24, 14, 8, ACCENT_GOLD,
         "Museumsfoto", "Originalbilete\nfrå IIIF / API")

draw_arrow(ax, 50, 28, 54)

draw_box(ax, 54, 24, 14, 8, ACCENT_GOLD,
         "Gemini Vision", "Kvit bakgrunn (#fff)\nSkarp utklypping")

draw_box(ax, 40, 4, 20, 7, ACCENT_GOLD,
         "2 092 bguw", "Bakgrunnsfjerna PNG\nStandardisert visning")

ax.annotate("", xy=(50, 11), xytext=(61, 24),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.7))

# ── stage 3: 3D reconstruction ───────────────────────────────────────────────
draw_box(ax, 73, 24, 14, 8, ACCENT_RUST,
         "Hunyuan3D-2", "50 shape-gen steg\nLokal GPU")

draw_box(ax, 91, 24, 8, 8, ACCENT_RUST,
         "Skalering", "trimesh\nH x B x D")

draw_arrow(ax, 87, 28, 90.5, "")

draw_box(ax, 74, 4, 22, 7, ACCENT_RUST,
         "2 205 kalibrerte meshar", "GLB-format; 5 formtrekk\nSphericitet, fyllgrad,\ntregleik, kompleksitet, volum")

ax.annotate("", xy=(85, 11), xytext=(85, 24),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.7))

# ── connecting arrows between stages ─────────────────────────────────────────
draw_arrow(ax, 27, 7.5, 39, "CSV / JSON")
draw_arrow(ax, 61, 7.5, 73, "PNG inn")

fig.tight_layout()
save_fig(fig, "fig-01-pipeline")
print("fig-01-pipeline saved")
