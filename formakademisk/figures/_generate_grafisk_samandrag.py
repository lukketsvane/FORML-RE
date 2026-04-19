"""
Generer grafisk samandrag for "Formlære: Grunnlaget for ein substrat-uavhengig
formvitskap". Tre overlappande Venn-regionar (L(SG), L̂, C(A)) over ein
Raup-aktig morfoplassbakgrunn med tilpassingspunkt.

Utgang: grafisk-samandrag.png (1200x600 @ 300 dpi).
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from matplotlib.patheffects import withStroke

# --- Stil ---------------------------------------------------------------
# Skriftval: Inter/Helvetica/Arial; fall tilbake til DejaVu Sans
plt.rcParams.update({
    "font.family": "sans-serif",
    # DejaVu Sans fyrst: har full nynorsk/norsk teiknsetjing (æ, ø, å)
    "font.sans-serif": ["DejaVu Sans", "Inter", "Arial", "Helvetica"],
    "font.size": 10,
    "axes.linewidth": 0.6,
    "axes.edgecolor": "#2c3e50",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Fargepalett: skifergrå/marine + rav-aksent
COL_BG      = "#fdfcf8"     # lun offwhite
COL_GRID    = "#dfe3e8"     # lett grå for akser
COL_AXIS    = "#4a5568"     # skiferblå for aksetekst
COL_SLATE   = "#2c3e50"     # djup marine for hovudtekst
COL_A       = "#5a6a7f"     # L(SG) - skiferblå
COL_B       = "#6b7c93"     # L̂    - anna skifernyanse
COL_C       = "#3f5065"     # C(A)  - djupare marine
COL_ACCENT  = "#c77c2f"     # rav/rust (F-markør og utheving)
COL_ACCENT_LIGHT = "#e8b878"
COL_FORBID  = "#f0ece4"     # forbode område - lyst beige
COL_SETTLED = "#2c3e50"     # fylte punkt
COL_UNREAL  = "#8a95a5"     # ope punkt

# --- Figur --------------------------------------------------------------
# 1200x600 px ved 150 dpi -> 8 x 4 tommar
FIG_W, FIG_H = 8.0, 4.0
DPI = 150

# Hjelpevariablar for margar og plassering
TOP_MARGIN = 0.62       # plass reservert til tittel/undertittel
BOTTOM_MARGIN = 0.42    # plass reservert til fotnote

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=COL_BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect("equal")
ax.axis("off")

# --- Bakgrunn: Raup-morfoplass -----------------------------------------
# Ein subtil 2D projeksjon av Raup sitt 3D morfoplass (W, T, D),
# med omriss rundt forbodne område, og spreidde tilpassingspunkt.

# Morfoplass-boks (lyst bakgrunnsareal) - avgrensa av margane
morpho_box = FancyBboxPatch(
    (0.35, BOTTOM_MARGIN - 0.05),
    FIG_W - 0.70,
    FIG_H - TOP_MARGIN - BOTTOM_MARGIN + 0.05,
    boxstyle="round,pad=0.02,rounding_size=0.08",
    linewidth=0.5, edgecolor=COL_GRID, facecolor="#ffffff", alpha=0.6,
    zorder=1,
)
ax.add_patch(morpho_box)

# Aksesystem (tenkt 3D projeksjon) - plassert innanfor margane
origin = np.array([1.25, 1.20])
axis_len = 0.95
# x-akse (W - whorl expansion)
ax.annotate("", xy=origin + np.array([axis_len, 0]), xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=COL_AXIS, lw=0.7,
                            mutation_scale=8),
            zorder=2)
# y-akse (T - whorl translation)
ax.annotate("", xy=origin + np.array([0, axis_len * 0.80]), xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=COL_AXIS, lw=0.7,
                            mutation_scale=8),
            zorder=2)
# z-akse (D - coiling axis / dist.) projisert diagonalt (innover i figuren)
ax.annotate("", xy=origin + np.array([-0.48, -0.34]), xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=COL_AXIS, lw=0.7,
                            mutation_scale=8),
            zorder=2)

# Akse-etikettar - diskre, i kant
ax.text(origin[0] + axis_len + 0.03, origin[1] - 0.02,
        "W  whorl expansion", fontsize=6.2, color=COL_AXIS,
        ha="left", va="center", style="italic", zorder=3)
ax.text(origin[0] - 0.02, origin[1] + axis_len * 0.80 + 0.06,
        "T  whorl translation", fontsize=6.2, color=COL_AXIS,
        ha="left", va="bottom", style="italic", zorder=3)
# D-etikett under axis-tip (tip ligg ved origin + (-0.48, -0.34))
ax.text(origin[0] - 0.46, origin[1] - 0.46,
        "D  coiling axis", fontsize=6.2, color=COL_AXIS,
        ha="center", va="top", style="italic", zorder=3)

# Rutenett i morfoplassen - lett prikk-grid (mellom tittel- og fotnote-margane)
gx = np.linspace(0.7, FIG_W - 0.55, 22)
gy = np.linspace(BOTTOM_MARGIN + 0.15, FIG_H - TOP_MARGIN - 0.05, 10)
GX, GY = np.meshgrid(gx, gy)
ax.scatter(GX.ravel(), GY.ravel(), s=0.6, c=COL_GRID, alpha=0.55,
           zorder=1.5, linewidths=0)

# Forbodne regionar (grå klattar - geometrisk/fysisk umogleg)
# Plassert innanfor morfoplass-boksen, unna Venn-sentrum og akser
rng = np.random.default_rng(7)
forbidden_patches = [
    # hjørne nede-til-høgre
    Polygon([(6.75, 0.52), (7.40, 0.52), (7.40, 1.15), (7.05, 1.25), (6.75, 1.00)],
            closed=True),
    # klatt oppe-til-venstre (innanfor morfoplass, under tittel)
    Polygon([(0.55, 2.95), (1.20, 3.08), (1.28, 3.30), (0.85, 3.28), (0.55, 3.15)],
            closed=True),
]
for p in forbidden_patches:
    p.set_facecolor(COL_FORBID)
    p.set_edgecolor("#d8d2c4")
    p.set_linewidth(0.4)
    p.set_alpha(0.75)
    p.set_zorder(1.2)
    ax.add_patch(p)

# Liten etikett for forbode område (inne i den nedre-høgre klatten)
ax.text(7.05, 0.85, "forbode\nregion", fontsize=5.3, color="#8a7f6a",
        ha="center", va="center", style="italic", zorder=2.5,
        linespacing=1.05)

# Tilpassingspunkt: fylte (realiserte), opne (tilgjengelege), diskret spreidde
# Vi held dei unna hjørna der Venn-regionane ligg for å unngå rot.
def in_forbidden(x, y):
    for p in forbidden_patches:
        if p.contains_point((x, y)):
            return True
    return False

def near_venn_center(x, y):
    # Unngå den tette overlappssona kring Venn-skjæringa
    return (x - 4.0) ** 2 + (y - 1.95) ** 2 < 0.50 ** 2

settled_pts = []
unreal_pts = []
n_target = 70
attempts = 0
while len(settled_pts) + len(unreal_pts) < n_target and attempts < 2000:
    attempts += 1
    x = rng.uniform(0.55, FIG_W - 0.55)
    y = rng.uniform(0.50, FIG_H - 0.55)
    if in_forbidden(x, y):
        continue
    if near_venn_center(x, y):
        continue
    # Halvparten fylte, halvparten opne
    if rng.random() < 0.55:
        settled_pts.append((x, y))
    else:
        unreal_pts.append((x, y))

sx, sy = zip(*settled_pts)
ux, uy = zip(*unreal_pts)
ax.scatter(sx, sy, s=7.5, c=COL_SETTLED, alpha=0.70, zorder=2,
           linewidths=0, label="realisert")
ax.scatter(ux, uy, s=9, facecolors="none", edgecolors=COL_UNREAL,
           linewidths=0.6, alpha=0.80, zorder=2, label="tilgjengeleg")

# --- Venn-regionar -----------------------------------------------------
# Tre sirklar i lysberg-skuming; lett halvgjennomsiktige slik at
# bakgrunnen skin gjennom.
venn_r = 1.35
venn_alpha_fill = 0.10

# Sentrum justert slik at skjæring ligg midt i tilgjengeleg område
cx_center = 4.00
cy_center = 1.95
offset = 0.78  # avstand frå sentrum til sirkel-sentrum

# Toppvenstre: L(SG)
c1 = (cx_center - offset, cy_center + offset * 0.55)
# Topphøgre: L-hat
c2 = (cx_center + offset, cy_center + offset * 0.55)
# Nede-sentrum: C(A)
c3 = (cx_center, cy_center - offset * 0.75)

for (cx, cy), col in [(c1, COL_A), (c2, COL_B), (c3, COL_C)]:
    ax.add_patch(Circle((cx, cy), venn_r, facecolor=col, alpha=venn_alpha_fill,
                        edgecolor=col, linewidth=1.3, zorder=3))

# Etikettar for dei tre regionane (utanfor overlappet)
label_effects = [withStroke(linewidth=2.6, foreground=COL_BG)]

# L(SG) - plassert over-til-venstre for sirkelen
ax.text(c1[0] - 0.90, c1[1] + 0.72, r"$L(SG)$", fontsize=12.5,
        fontweight="bold", color=COL_A, ha="center", va="center",
        zorder=6, path_effects=label_effects)
ax.text(c1[0] - 0.90, c1[1] + 0.48, "formspråk", fontsize=8.5,
        color=COL_A, ha="center", va="center", style="italic",
        zorder=6, path_effects=label_effects)
ax.text(c1[0] - 0.90, c1[1] + 0.31, "det mogelege", fontsize=6.8,
        color=COL_AXIS, ha="center", va="center",
        zorder=6, path_effects=label_effects)

# L-hat - plassert over-til-høgre
ax.text(c2[0] + 0.90, c2[1] + 0.72, r"$\widehat{L}$", fontsize=14,
        fontweight="bold", color=COL_B, ha="center", va="center",
        zorder=6, path_effects=label_effects)
ax.text(c2[0] + 0.90, c2[1] + 0.48, "tilpassingslandskap",
        fontsize=8.5, color=COL_B, ha="center", va="center",
        style="italic", zorder=6, path_effects=label_effects)
ax.text(c2[0] + 0.90, c2[1] + 0.31, "det sannsynlege", fontsize=6.8,
        color=COL_AXIS, ha="center", va="center",
        zorder=6, path_effects=label_effects)

# C(A) - plassert inne-under C-sirkelen, vel over fotnote
# c3[1] ~ 1.95 - 0.585 = ~1.365; sirkelsokkel ved c3[1] - venn_r = ~0.015
# Vi plasserer etiketten like innanfor nedre kant av sirkelen
ax.text(c3[0], c3[1] - 0.62, r"$C(A)$", fontsize=12.5,
        fontweight="bold", color=COL_C, ha="center", va="center",
        zorder=6, path_effects=label_effects)
ax.text(c3[0], c3[1] - 0.82, "representasjonsrom",
        fontsize=8.5, color=COL_C, ha="center", va="center",
        style="italic", zorder=6, path_effects=label_effects)
ax.text(c3[0], c3[1] - 0.98, "det tilgjengelege", fontsize=6.8,
        color=COL_AXIS, ha="center", va="center",
        zorder=6, path_effects=label_effects)

# --- F-markør i skjæringa ----------------------------------------------
# Liten rav-aksent i det trippel-overlappande sentrum
fx, fy = cx_center, cy_center
# Glød under markøren
for rr, aa in [(0.22, 0.18), (0.14, 0.28), (0.08, 0.55)]:
    ax.add_patch(Circle((fx, fy), rr, facecolor=COL_ACCENT_LIGHT,
                        alpha=aa, edgecolor="none", zorder=5))
ax.add_patch(Circle((fx, fy), 0.055, facecolor=COL_ACCENT,
                    edgecolor=COL_SLATE, linewidth=0.8, zorder=6))

# F-etikett med leielinje - kort, oppover-høgre, subtil bue
lx, ly = fx + 0.52, fy + 0.26
ax.annotate(
    "",
    xy=(fx + 0.07, fy + 0.05), xytext=(lx - 0.02, ly - 0.02),
    arrowprops=dict(arrowstyle="-", color=COL_SLATE, lw=0.55,
                    connectionstyle="arc3,rad=-0.12",
                    alpha=0.85),
    zorder=6,
)
ax.text(lx, ly, r"$F$", fontsize=11.5,
        fontweight="bold", color=COL_ACCENT,
        ha="left", va="center", zorder=7,
        path_effects=[withStroke(linewidth=2.6, foreground=COL_BG)])
ax.text(lx + 0.13, ly, "realisert form",
        fontsize=7.6, color=COL_SLATE, ha="left", va="center",
        style="italic", zorder=7,
        path_effects=[withStroke(linewidth=2.6, foreground=COL_BG)])

# --- Tittel / undertittel ----------------------------------------------
# To rader med god vertikal klaring
ax.text(FIG_W / 2, FIG_H - 0.22,
        "Formlære: den felles skjæringa",
        fontsize=11.5, fontweight="bold", color=COL_SLATE,
        ha="center", va="center", zorder=8)
ax.text(FIG_W / 2, FIG_H - 0.46,
        r"realisert form  $F \in L(SG) \,\cap\, \widehat{L} \,\cap\, C(A)$",
        fontsize=8.8, color=COL_AXIS,
        ha="center", va="center", zorder=8)

# --- Forklaring nede til høgre -----------------------------------------
# Horisontal stripe med tre oppføringar (fylt / opent / forbode)
legend_x = FIG_W - 2.25
legend_y = 0.22
# Fylt punkt
ax.scatter([legend_x + 0.03], [legend_y], s=12, c=COL_SETTLED,
           zorder=8, linewidths=0)
ax.text(legend_x + 0.11, legend_y, "realisert",
        fontsize=6.3, color=COL_SLATE, va="center", zorder=8)
# Ope punkt
ax.scatter([legend_x + 0.70], [legend_y], s=14,
           facecolors="none", edgecolors=COL_UNREAL, linewidths=0.7, zorder=8)
ax.text(legend_x + 0.78, legend_y, "tilgjengeleg",
        fontsize=6.3, color=COL_SLATE, va="center", zorder=8)
# Forbode sone-swatch
ax.add_patch(FancyBboxPatch((legend_x + 1.50, legend_y - 0.04), 0.10, 0.08,
                            boxstyle="round,pad=0.004,rounding_size=0.01",
                            facecolor=COL_FORBID, edgecolor="#d8d2c4",
                            linewidth=0.4, zorder=8))
ax.text(legend_x + 1.63, legend_y, "forbode",
        fontsize=6.3, color=COL_SLATE, va="center", zorder=8)

# --- Fotnote -----------------------------------------------------------
# To-linjers fotnote nede; kort nok til å ikkje kollidere med
# forklaringsstripe nede til høgre (som startar ved x ~ 5.75)
ax.text(0.18, 0.18,
        "Morfoplass etter Raup (1966): W, T, D spennar eit rom av mogelege skjelformer;",
        fontsize=5.7, color=COL_AXIS, ha="left", va="center", zorder=8,
        style="italic")
ax.text(0.18, 0.07,
        "fylte punkt er realiserte, opne punkt tilgjengelege men urealiserte.",
        fontsize=5.7, color=COL_AXIS, ha="left", va="center", zorder=8,
        style="italic")

# --- Lagre --------------------------------------------------------------
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "grafisk-samandrag.png")
fig.savefig(out_path, dpi=300, facecolor=COL_BG, bbox_inches=None,
            pad_inches=0)
plt.close(fig)
print(f"Saved: {out_path}")
