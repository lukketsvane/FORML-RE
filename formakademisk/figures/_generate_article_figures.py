"""
Publikasjonskvalitets figurar for Formlære-artikkelen.

Kvar figur blir lagra som 300 DPI PNG i ./png/.
Fargeblind-venleg Okabe-Ito palett. Sans-serif. Nynorsk etikettar.

Kjør: python _generate_article_figures.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm, colors
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch, Ellipse
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
from matplotlib.colors import LinearSegmentedColormap

# ─── Setup ──────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "png")
os.makedirs(OUT, exist_ok=True)

# Okabe-Ito palette (colorblind-safe)
OI = {
    "orange": "#E69F00",
    "skyblue": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "rust": "#D55E00",
    "pink": "#CC79A7",
    "black": "#000000",
    "grey": "#999999",
    "lightgrey": "#DDDDDD",
}

# Domain-specific accents for the article
SLATE = "#3C4B5F"
AMBER = "#B47332"
LIGHTSLATE = "#E1E6EE"
LIGHTAMBER = "#F3E4CD"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
})

def save(fig, name):
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved: png/{name}.png")


# ═════════════════════════════════════════════════════════════════════
# FIG 01: Formrom som Raup-skjellrom (3D)
# ═════════════════════════════════════════════════════════════════════
def fig_morphospace_raup():
    np.random.seed(42)
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(111, projection="3d")

    # Realised shells (settled)
    n_real = 80
    W = np.random.uniform(1.5, 3.5, n_real)
    T = np.random.uniform(0.0, 2.5, n_real)
    D = np.random.uniform(0.1, 0.9, n_real)
    # Cluster them to look biological
    mask = (W - 2.5) ** 2 + (T - 1.2) ** 2 + (D - 0.5) ** 2 < 1.2
    ax.scatter(W[mask], T[mask], D[mask], s=40, c=SLATE, alpha=0.8, label="realisert (busett)")

    # Open but accessible (empty circles)
    n_open = 50
    Wo = np.random.uniform(1.2, 4, n_open)
    To = np.random.uniform(0, 3, n_open)
    Do = np.random.uniform(0, 1, n_open)
    mask_o = ((Wo - 2.5) ** 2 + (To - 1.2) ** 2 + (Do - 0.5) ** 2 > 1.2) & \
             ((Wo - 2.5) ** 2 + (To - 1.2) ** 2 + (Do - 0.5) ** 2 < 3.5)
    ax.scatter(Wo[mask_o], To[mask_o], Do[mask_o], s=30, facecolors="none",
               edgecolors=OI["grey"], linewidths=1, label="ope (tilgjengeleg)")

    # Forbidden region (grey translucent box)
    ax.scatter([3.8], [2.8], [0.95], s=200, c=OI["lightgrey"], alpha=0.3, marker="s")

    ax.set_xlabel("Spiralutviding $W$", labelpad=8)
    ax.set_ylabel("Spiraltranslasjon $T$", labelpad=8)
    ax.set_zlabel("Rulleakse $D$", labelpad=8)
    ax.set_title("Formrom $M$ for skjell (Raup, 1966)", pad=15, fontsize=11)

    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), frameon=False, fontsize=9)

    # Clean 3D appearance
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("w")
    ax.yaxis.pane.set_edgecolor("w")
    ax.zaxis.pane.set_edgecolor("w")
    ax.grid(True, linewidth=0.3, alpha=0.5)

    save(fig, "01_formrom_raup")


# ═════════════════════════════════════════════════════════════════════
# FIG 02: Tilpassingslandskap 3D (Wright-stil)
# ═════════════════════════════════════════════════════════════════════
def fig_adaptation_landscape_3d():
    fig = plt.figure(figsize=(7.5, 5.5))
    ax = fig.add_subplot(111, projection="3d")

    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    # Multi-peak landscape
    Z = (1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2) / 1.2) +
         1.2 * np.exp(-((X + 1.2) ** 2 + (Y - 0.3) ** 2) / 1.5) +
         0.9 * np.exp(-((X + 0.5) ** 2 + (Y + 1.8) ** 2) / 1.0) +
         0.6 * np.exp(-((X - 2) ** 2 + (Y + 1.5) ** 2) / 0.8))

    surf = ax.plot_surface(X, Y, Z, cmap="cividis", linewidth=0, antialiased=True, alpha=0.92)

    # Contour projection at bottom
    ax.contour(X, Y, Z, zdir="z", offset=-0.2, levels=10, cmap="cividis", alpha=0.5, linewidths=0.5)

    ax.set_xlabel("formdimensjon $x_1$", labelpad=8)
    ax.set_ylabel("formdimensjon $x_2$", labelpad=8)
    ax.set_zlabel("$\\hat{\\mathcal{L}}(x)$", labelpad=8)
    ax.set_title("Tilpassingslandskap $\\hat{\\mathcal{L}}$ med fleire haugar", pad=15)
    ax.set_zlim(-0.2, 1.8)

    ax.view_init(elev=28, azim=-55)

    cb = fig.colorbar(surf, ax=ax, shrink=0.55, pad=0.08, aspect=15)
    cb.set_label("$\\hat{\\mathcal{L}}$", fontsize=10)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, linewidth=0.3, alpha=0.5)

    save(fig, "02_tilpassingslandskap_3d")


# ═════════════════════════════════════════════════════════════════════
# FIG 03: Waddington epigenetisk landskap (branching valleys)
# ═════════════════════════════════════════════════════════════════════
def fig_waddington():
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.linspace(-5, 5, 400)
    # Start as single valley, branching into three
    def valley_1(x, t):
        # t in [0, 1] - early: single, late: branched
        if t < 0.3:
            return 0.5 * x**2 + 3
        else:
            # Branching
            depth = (t - 0.3) * 2
            centers = [-2.5, 0, 2.5]
            vals = [0.8 * (x - c)**2 for c in centers]
            merged = np.minimum.reduce(vals)
            return merged + 3 - depth

    # Draw terrain as stacked contour lines representing cross-sections at different t
    n_slices = 8
    for i, t in enumerate(np.linspace(0.0, 1.0, n_slices)):
        y_offset = (1 - t) * 4
        z = valley_1(x, t)
        color_val = 0.3 + 0.5 * t
        ax.fill_between(x, y_offset + z * 0.5, y_offset + 6, color=cm.cividis(color_val), alpha=0.85, zorder=i)
        ax.plot(x, y_offset + z * 0.5, color="white", linewidth=0.8, zorder=i+0.5)

    # Ball rolling down
    ball_x = np.array([0, 0, 0, 0.3, 0.8, 1.5, 2.3, 2.5])
    ball_t = np.linspace(0.02, 0.98, len(ball_x))
    for i, (bx, bt) in enumerate(zip(ball_x, ball_t)):
        by = (1 - bt) * 4 + valley_1(np.array([bx]), bt)[0] * 0.5 + 0.2
        ax.add_patch(Circle((bx, by), 0.18, color=AMBER, ec=SLATE, linewidth=1, zorder=100-i, alpha=0.4 + 0.6 * bt))

    # Final big ball
    bx_f = ball_x[-1]
    by_f = (1 - ball_t[-1]) * 4 + valley_1(np.array([bx_f]), ball_t[-1])[0] * 0.5 + 0.2
    ax.add_patch(Circle((bx_f, by_f), 0.3, color=AMBER, ec=SLATE, linewidth=1.5, zorder=200))

    # Annotations
    ax.annotate("tilstand i tidleg utvikling",
                xy=(-4.5, 5.2), fontsize=9, color=SLATE, style="italic")
    ax.annotate("kanaliserte endetilstandar",
                xy=(-4.5, 0.3), fontsize=9, color=SLATE, style="italic")
    ax.annotate("kanalisering = bratte dalveggar",
                xy=(3, 2.5), fontsize=8.5, color=SLATE, ha="right", style="italic")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_xlabel("formdimensjon", labelpad=6)
    ax.set_ylabel("tid →", labelpad=6)
    ax.set_title("Waddingtons epigenetiske landskap: forgrenande kanalar", pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    save(fig, "03_waddington_landskap")


# ═════════════════════════════════════════════════════════════════════
# FIG 04: Multiskala-landskap (stack)
# ═════════════════════════════════════════════════════════════════════
def fig_multiscale_landscapes():
    fig, ax = plt.subplots(figsize=(9, 6))

    scales = [
        ("Biosfære", "hundreår", 0),
        ("Økosystem", "tiår", 1),
        ("Samfunn", "år", 2),
        ("Organisme", "dag", 3),
        ("Celle", "sekund", 4),
        ("Molekyl", "mikrosek.", 5),
    ]

    np.random.seed(7)

    for i, (name, time, idx) in enumerate(scales):
        y_off = (len(scales) - idx - 1) * 1.8
        x_off = idx * 0.7

        # Generate a landscape "slice" as a contoured rectangle
        xx = np.linspace(0, 5, 80)
        yy = np.linspace(0, 3, 50)
        XX, YY = np.meshgrid(xx, yy)
        # Random bumps
        ZZ = np.zeros_like(XX)
        n_peaks = 3 + idx
        for _ in range(n_peaks):
            cx = np.random.uniform(0.5, 4.5)
            cy = np.random.uniform(0.3, 2.7)
            amp = np.random.uniform(0.4, 1.0)
            width = np.random.uniform(0.4, 1.0)
            ZZ += amp * np.exp(-((XX - cx) ** 2 + (YY - cy) ** 2) / width)

        # Draw as filled + contour
        cmap = colors.LinearSegmentedColormap.from_list(
            "scale", [LIGHTSLATE, SLATE]
        ) if idx % 2 == 0 else colors.LinearSegmentedColormap.from_list(
            "scale", [LIGHTAMBER, AMBER]
        )

        extent = (x_off, x_off + 5, y_off, y_off + 3)
        ax.imshow(ZZ, extent=extent, origin="lower", cmap=cmap, aspect="auto",
                  alpha=0.85, interpolation="bilinear", zorder=10 - idx)
        ax.contour(xx + x_off, yy + y_off, ZZ, levels=6, colors="white",
                   linewidths=0.5, alpha=0.7, zorder=10 - idx + 0.1)

        # Frame
        ax.add_patch(Rectangle((x_off, y_off), 5, 3, fill=False, edgecolor=SLATE,
                               linewidth=0.8, zorder=10 - idx + 0.2))

        # Label
        ax.text(x_off + 5.15, y_off + 2.4, name, fontsize=10, fontweight="bold",
                color=SLATE, va="center")
        ax.text(x_off + 5.15, y_off + 1.9, time, fontsize=8, color=SLATE,
                va="center", style="italic")

    # Vertical arrow showing scale axis
    ax.annotate("", xy=(-0.4, 10.3), xytext=(-0.4, -0.3),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))
    ax.text(-0.7, 5, "abstraksjonsskala", fontsize=10, color=SLATE,
            rotation=90, va="center", style="italic")

    ax.set_xlim(-1.2, 10)
    ax.set_ylim(-0.8, 11.2)
    ax.set_aspect("equal")
    ax.set_title("Tilpassingslandskap på ulike abstraksjonsskalaer", pad=12)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    save(fig, "04_multiskala_landskap")


# ═════════════════════════════════════════════════════════════════════
# FIG 05: Gradient-navigasjon (2D landscape with trajectory)
# ═════════════════════════════════════════════════════════════════════
def fig_gradient_trajectory():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), gridspec_kw={"width_ratios": [1.1, 1]})

    # ── Left: 2D heatmap landscape with contours + trajectory ──
    ax = axes[0]
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    Z = -(1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2) / 1.2) +
          1.2 * np.exp(-((X + 1.2) ** 2 + (Y - 0.3) ** 2) / 1.5) +
          0.9 * np.exp(-((X + 0.5) ** 2 + (Y + 1.8) ** 2) / 1.0))

    im = ax.imshow(Z, extent=[-3, 3, -3, 3], origin="lower", cmap="cividis_r", aspect="auto")
    cs = ax.contour(X, Y, Z, levels=12, colors="white", linewidths=0.4, alpha=0.6)

    # Trajectory — gradient descent
    # Start point
    pos = np.array([-2.5, 2.5])
    traj = [pos.copy()]
    def grad_Z(p):
        eps = 1e-4
        dx = (-(1.5 * np.exp(-((p[0] + eps - 1) ** 2 + (p[1] - 1) ** 2) / 1.2) -
                1.5 * np.exp(-((p[0] - eps - 1) ** 2 + (p[1] - 1) ** 2) / 1.2)) / (2 * eps) -
              (1.2 * np.exp(-((p[0] + eps + 1.2) ** 2 + (p[1] - 0.3) ** 2) / 1.5) -
               1.2 * np.exp(-((p[0] - eps + 1.2) ** 2 + (p[1] - 0.3) ** 2) / 1.5)) / (2 * eps) -
              (0.9 * np.exp(-((p[0] + eps + 0.5) ** 2 + (p[1] + 1.8) ** 2) / 1.0) -
               0.9 * np.exp(-((p[0] - eps + 0.5) ** 2 + (p[1] + 1.8) ** 2) / 1.0)) / (2 * eps))
        dy = (-(1.5 * np.exp(-((p[0] - 1) ** 2 + (p[1] + eps - 1) ** 2) / 1.2) -
                1.5 * np.exp(-((p[0] - 1) ** 2 + (p[1] - eps - 1) ** 2) / 1.2)) / (2 * eps) -
              (1.2 * np.exp(-((p[0] + 1.2) ** 2 + (p[1] + eps - 0.3) ** 2) / 1.5) -
               1.2 * np.exp(-((p[0] + 1.2) ** 2 + (p[1] - eps - 0.3) ** 2) / 1.5)) / (2 * eps) -
              (0.9 * np.exp(-((p[0] + 0.5) ** 2 + (p[1] + eps + 1.8) ** 2) / 1.0) -
               0.9 * np.exp(-((p[0] + 0.5) ** 2 + (p[1] - eps + 1.8) ** 2) / 1.0)) / (2 * eps))
        return np.array([dx, dy])
    for _ in range(60):
        g = grad_Z(pos)
        pos = pos - 0.2 * g
        traj.append(pos.copy())
    traj = np.array(traj)
    ax.plot(traj[:, 0], traj[:, 1], "-", color=AMBER, linewidth=2, alpha=0.85, zorder=10)
    ax.plot(traj[0, 0], traj[0, 1], "o", color=OI["rust"], markersize=8, zorder=11, label="start")
    ax.plot(traj[-1, 0], traj[-1, 1], "*", color=OI["rust"], markersize=14, zorder=11, label="lokalt optimum")

    ax.set_xlabel("formdimensjon $x_1$")
    ax.set_ylabel("formdimensjon $x_2$")
    ax.set_title("Agent-trajektorie: $\\nabla_{C(A)} \\hat{\\mathcal{L}}$")
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, edgecolor="none")

    cb = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02, aspect=20)
    cb.set_label("$\\hat{\\mathcal{L}}$ (lågare = betre)")

    # ── Right: gradient vector field alone ──
    ax2 = axes[1]
    xs = np.linspace(-3, 3, 18)
    ys = np.linspace(-3, 3, 18)
    Xs, Ys = np.meshgrid(xs, ys)
    U = np.zeros_like(Xs)
    V = np.zeros_like(Xs)
    for i in range(Xs.shape[0]):
        for j in range(Xs.shape[1]):
            g = grad_Z(np.array([Xs[i, j], Ys[i, j]]))
            U[i, j] = -g[0]
            V[i, j] = -g[1]

    # Background contour for context
    ax2.contour(X, Y, Z, levels=10, colors=OI["lightgrey"], linewidths=0.4)
    ax2.quiver(Xs, Ys, U, V, np.sqrt(U**2 + V**2), cmap="viridis",
               scale=18, width=0.004, headwidth=4)
    ax2.set_xlabel("formdimensjon $x_1$")
    ax2.set_ylabel("formdimensjon $x_2$")
    ax2.set_title("Gradientfelt: $-\\nabla \\hat{\\mathcal{L}}$")
    ax2.set_aspect("equal")

    fig.tight_layout()
    save(fig, "05_gradient_navigasjon")


# ═════════════════════════════════════════════════════════════════════
# FIG 06: Multi-agent felt (three gradient fields)
# ═════════════════════════════════════════════════════════════════════
def fig_multi_agent_field():
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.8))

    x = np.linspace(-3, 3, 150)
    y = np.linspace(-3, 3, 150)
    X, Y = np.meshgrid(x, y)

    # Agent A landscape
    L_A = -np.exp(-((X + 1) ** 2 + (Y + 0.5) ** 2) / 1.2)
    # Agent B landscape
    L_B = -np.exp(-((X - 1) ** 2 + (Y - 1) ** 2) / 1.2)
    # Agent C landscape (antagonist — opposite gradient)
    L_C = 0.7 * np.exp(-((X - 0.3) ** 2 + (Y + 0.5) ** 2) / 2)

    # Combined
    L_total = L_A + L_B + L_C

    colors_list = ["cividis_r", "cividis_r", "cividis_r", "cividis_r"]
    titles = ["Agent A: $\\hat{\\mathcal{L}}_A$",
              "Agent B: $\\hat{\\mathcal{L}}_B$",
              "Agent C: $\\hat{\\mathcal{L}}_C$ (antagonist)",
              "Sum: $\\sum_k w_k \\hat{\\mathcal{L}}_k$"]
    data_list = [L_A, L_B, L_C, L_total]

    for ax, data, title, cmap in zip(axes, data_list, titles, colors_list):
        im = ax.imshow(data, extent=[-3, 3, -3, 3], origin="lower", cmap=cmap)
        ax.contour(X, Y, data, levels=8, colors="white", linewidths=0.4, alpha=0.7)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([-2, 0, 2])
        ax.set_xlabel("$x_1$")
        if ax is axes[0]:
            ax.set_ylabel("$x_2$")

    fig.suptitle("Multi-agent landskap: $\\mathcal{L}_k = \\mathcal{L}_\\mathrm{ext} + \\sum_{j \\neq k} \\phi_{jk}(A_j, x)$",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "06_multi_agent_felt")


# ═════════════════════════════════════════════════════════════════════
# FIG 07: Nøsta representasjonsrom (light cones / nested domains)
# ═════════════════════════════════════════════════════════════════════
def fig_nested_representation():
    fig, ax = plt.subplots(figsize=(8, 6))

    # Outer: full morphospace
    ax.add_patch(Rectangle((-5, -3.5), 10, 7, fill=True, facecolor=LIGHTSLATE,
                           edgecolor=SLATE, linewidth=1.2, label="Formrom $M$"))
    ax.text(-4.7, 3.1, "Formrom $M$", fontsize=10, fontweight="bold", color=SLATE)

    # L(SG) — language generated by SG
    sg_poly = plt.Polygon([(-3.5, -2.5), (2, -3), (4, -1), (3, 2), (-2, 2.5), (-4, 0)],
                          closed=True, facecolor=OI["skyblue"], alpha=0.25,
                          edgecolor=OI["blue"], linewidth=1.5, linestyle="--")
    ax.add_patch(sg_poly)
    ax.text(-3.5, 2.3, "$L(\\mathrm{SG})$\n\\small mogelege former", fontsize=10, color=OI["blue"], fontweight="bold")

    # C(A_1) — smallest agent
    c1 = Ellipse((0, 0), 3.0, 2.0, angle=-15, facecolor=AMBER, alpha=0.35,
                 edgecolor=AMBER, linewidth=1.8)
    ax.add_patch(c1)
    ax.text(-0.3, -0.1, "$C(A_1)$", fontsize=11, fontweight="bold", color=AMBER, ha="center")

    # C(A_2) — larger
    c2 = Ellipse((0.3, 0.2), 5.0, 3.2, angle=-10, facecolor="none",
                 edgecolor=OI["rust"], linewidth=1.8, linestyle="-.")
    ax.add_patch(c2)
    ax.text(2.4, 1.4, "$C(A_2)$", fontsize=11, fontweight="bold", color=OI["rust"])

    # C(A_3) — largest
    c3 = Ellipse((0.2, 0.3), 7.0, 5.0, angle=-5, facecolor="none",
                 edgecolor=OI["green"], linewidth=1.8, linestyle=":")
    ax.add_patch(c3)
    ax.text(3.2, 2.4, "$C(A_3)$", fontsize=11, fontweight="bold", color=OI["green"])

    # Realised form F at the intersection
    ax.plot(0.1, 0.1, "o", color=SLATE, markersize=10, zorder=10)
    ax.annotate("$F$ realisert",
                xy=(0.1, 0.1), xytext=(1.3, -1.4), fontsize=10,
                color=SLATE,
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1))

    ax.set_xlim(-5, 5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Nøsta representasjonsrom: $F \\in L(\\mathrm{SG}) \\cap \\bigcap_k C(A_k)$", pad=10)
    for sp in ax.spines.values():
        sp.set_visible(False)

    save(fig, "07_nosta_representasjonsrom")


# ═════════════════════════════════════════════════════════════════════
# FIG 08: Stiavhengigheit — landskap deformerer seg over tid
# ═════════════════════════════════════════════════════════════════════
def fig_path_dependence():
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))

    x = np.linspace(-3, 3, 150)
    y = np.linspace(-3, 3, 150)
    X, Y = np.meshgrid(x, y)

    # Initial landscape
    L0 = -1.2 * np.exp(-((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 1.5)

    realised_points = []
    titles = ["$t = 0$: start", "$t = 1$: fyrste realisering", "$t = 2$: deformert landskap", "$t = 3$: ny optimum"]

    # At each step, add a "dent" at realisation
    realised = [(-0.5, -0.5), (0.8, -0.3), (-1.0, 1.2)]

    for i, ax in enumerate(axes):
        L = L0.copy()
        for j, (rx, ry) in enumerate(realised[:i]):
            # Each realised position deforms landscape locally (positive bump = less attractive after)
            L = L + 0.4 * np.exp(-((X - rx) ** 2 + (Y - ry) ** 2) / 0.5)
        im = ax.imshow(L, extent=[-3, 3, -3, 3], origin="lower", cmap="cividis_r", vmin=-1.2, vmax=0.3)
        ax.contour(X, Y, L, levels=8, colors="white", linewidths=0.4, alpha=0.7)

        # Show realised points
        for j, (rx, ry) in enumerate(realised[:i]):
            ax.plot(rx, ry, "o", color=AMBER, markersize=10, markeredgecolor="white",
                    markeredgewidth=1.2, zorder=10)
            ax.annotate(f"$F_{j+1}$", (rx, ry), xytext=(rx + 0.25, ry + 0.25),
                        fontsize=9, color=SLATE, fontweight="bold")

        ax.set_title(titles[i], fontsize=10)
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([-2, 0, 2])
        if ax is axes[0]:
            ax.set_ylabel("$x_2$")
        ax.set_xlabel("$x_1$")

    fig.suptitle("Stiavhengigheit: kvar realisert form deformerer landskapet for den neste", fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "08_stiavhengigheit")


# ═════════════════════════════════════════════════════════════════════
# FIG 09: Boltzmann-fordeling over formrommet
# ═════════════════════════════════════════════════════════════════════
def fig_boltzmann_distribution():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), gridspec_kw={"width_ratios": [1, 1, 1]})

    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)

    L = (1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2) / 1.2) +
         1.2 * np.exp(-((X + 1.2) ** 2 + (Y - 0.3) ** 2) / 1.5) +
         0.9 * np.exp(-((X + 0.5) ** 2 + (Y + 1.8) ** 2) / 1.0))

    # Three increasing beta values (colder = sharper peaks)
    betas = [0.5, 2.0, 8.0]
    titles = ["$\\beta = 0.5$ (varmt)", "$\\beta = 2.0$ (moderat)", "$\\beta = 8.0$ (kaldt)"]

    for ax, beta, title in zip(axes, betas, titles):
        P = np.exp(beta * L)
        P = P / P.sum()
        # Log scale for visibility
        Plog = np.log(P + 1e-10)
        im = ax.imshow(Plog, extent=[-3, 3, -3, 3], origin="lower", cmap="viridis")
        ax.contour(X, Y, L, levels=6, colors="white", linewidths=0.3, alpha=0.5)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("$x_1$")
        if ax is axes[0]:
            ax.set_ylabel("$x_2$")

    fig.suptitle("Boltzmann-fordeling $P(F) \\propto \\exp(\\beta \\hat{\\mathcal{L}}(F))$: stasjonær konsekvens",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "09_boltzmann_fordeling")


# ═════════════════════════════════════════════════════════════════════
# FIG 10: Shape grammar rewrite (visual rule application)
# ═════════════════════════════════════════════════════════════════════
def fig_shape_grammar_rewrite():
    fig, axes = plt.subplots(1, 5, figsize=(14, 3.2))

    def draw_shape(ax, shapes, title):
        ax.set_aspect("equal")
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor(SLATE)
        for s in shapes:
            kind, params, color = s
            if kind == "rect":
                x, y, w, h = params
                ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=SLATE,
                                       linewidth=1.2))
            elif kind == "tri":
                pts = params
                ax.add_patch(plt.Polygon(pts, facecolor=color, edgecolor=SLATE, linewidth=1.2))
            elif kind == "circ":
                cx, cy, r = params
                ax.add_patch(Circle((cx, cy), r, facecolor=color, edgecolor=SLATE, linewidth=1.2))
        ax.set_title(title, fontsize=10, pad=6)

    # Step 0 — start ω
    draw_shape(axes[0], [
        ("rect", (1, 1, 2, 2), LIGHTSLATE),
    ], "$\\omega$ (start)")

    # Rule arrow
    axes[1].set_xlim(0, 1); axes[1].set_ylim(0, 1)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    for sp in axes[1].spines.values():
        sp.set_visible(False)
    axes[1].annotate("", xy=(0.8, 0.5), xytext=(0.2, 0.5),
                     arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.5))
    axes[1].text(0.5, 0.62, "rule $r_1$", ha="center", fontsize=9.5, color=SLATE, fontstyle="italic")
    axes[1].text(0.5, 0.35, "$a \\to b$", ha="center", fontsize=9.5, color=SLATE)

    # Step 1
    draw_shape(axes[2], [
        ("rect", (1, 1, 2, 2), LIGHTSLATE),
        ("tri", [(3, 1), (3, 3), (4, 2)], LIGHTAMBER),
    ], "$s_1$")

    # Rule arrow 2
    axes[3].set_xlim(0, 1); axes[3].set_ylim(0, 1)
    axes[3].set_xticks([]); axes[3].set_yticks([])
    for sp in axes[3].spines.values():
        sp.set_visible(False)
    axes[3].annotate("", xy=(0.8, 0.5), xytext=(0.2, 0.5),
                     arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.5))
    axes[3].text(0.5, 0.62, "rule $r_2$", ha="center", fontsize=9.5, color=SLATE, fontstyle="italic")

    # Step 2 (final)
    draw_shape(axes[4], [
        ("rect", (1, 1, 2, 2), LIGHTSLATE),
        ("tri", [(3, 1), (3, 3), (4, 2)], LIGHTAMBER),
        ("circ", (2, 3.5, 0.4), LIGHTAMBER),
    ], "$s_2 \\in L(\\mathrm{SG})$")

    fig.suptitle("Formgrammatikk-reskriving: reglar fyrer på innleiring",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "10_formgrammatikk_reskriving")


# ═════════════════════════════════════════════════════════════════════
# FIG 11: Reduksjons-diagram (limiting cases matrix)
# ═════════════════════════════════════════════════════════════════════
def fig_reduction_matrix():
    fig, ax = plt.subplots(figsize=(9, 6.5))

    # 2x2 grid
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # Axes
    ax.annotate("", xy=(10, 0.3), xytext=(0.5, 0.3),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))
    ax.annotate("", xy=(0.3, 8), xytext=(0.3, 0.5),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))

    # Axis labels
    ax.text(5, 0.05, "landskap-struktur $\\hat{\\mathcal{L}}$", ha="center", fontsize=10, color=SLATE)
    ax.text(0.9, 0.6, "flat", fontsize=8.5, color=SLATE)
    ax.text(8.7, 0.6, "strukturert", fontsize=8.5, color=SLATE)

    ax.text(0.05, 4, "grammatikk $\\mathrm{SG}$", rotation=90, va="center", fontsize=10, color=SLATE)
    ax.text(0.5, 1.3, "triviell", rotation=90, fontsize=8.5, color=SLATE)
    ax.text(0.5, 6.5, "rik", rotation=90, fontsize=8.5, color=SLATE)

    # Dashed quadrant dividers
    ax.plot([0.5, 10], [4.2, 4.2], "--", color=OI["grey"], linewidth=0.7)
    ax.plot([5.2, 5.2], [0.5, 8], "--", color=OI["grey"], linewidth=0.7)

    # Four quadrants
    # Top-left: Formgrammatikk (rik SG, flatt L)
    box1 = FancyBboxPatch((1, 4.7), 3.7, 2.5, boxstyle="round,pad=0.05",
                          facecolor=LIGHTSLATE, edgecolor=SLATE, linewidth=1.5)
    ax.add_patch(box1)
    ax.text(2.85, 6.5, "Formgrammatikk", ha="center", fontsize=11, fontweight="bold", color=SLATE)
    ax.text(2.85, 6.1, "Stiny \\& Gips (1972)", ha="center", fontsize=8.5, color=SLATE, style="italic")
    ax.text(2.85, 5.6, "$\\hat{\\mathcal{L}} \\equiv 0$", ha="center", fontsize=10, color=SLATE)
    ax.text(2.85, 5.15, "$P = 1/|L(\\mathrm{SG})|$", ha="center", fontsize=9, color=SLATE)

    # Top-right: Formlære
    box2 = FancyBboxPatch((5.7, 4.7), 3.7, 2.5, boxstyle="round,pad=0.05",
                          facecolor=LIGHTAMBER, edgecolor=AMBER, linewidth=2.2)
    ax.add_patch(box2)
    ax.text(7.55, 6.5, "Formlære", ha="center", fontsize=11.5, fontweight="bold", color=AMBER)
    ax.text(7.55, 6.1, "full kjerne-likning", ha="center", fontsize=8.5, color=AMBER, style="italic")
    ax.text(7.55, 5.55, "$\\mathrm{Form} = \\mathrm{SG}\\!\\left(\\sum_k \\nabla_{C(A_k)} \\mathcal{L}_k\\right)$",
            ha="center", fontsize=9, color=AMBER)

    # Bottom-right: CK
    box3 = FancyBboxPatch((5.7, 1.2), 3.7, 2.5, boxstyle="round,pad=0.05",
                          facecolor=LIGHTSLATE, edgecolor=SLATE, linewidth=1.5)
    ax.add_patch(box3)
    ax.text(7.55, 3.0, "C-K-teori", ha="center", fontsize=11, fontweight="bold", color=SLATE)
    ax.text(7.55, 2.6, "Hatchuel \\& Weil (2003)", ha="center", fontsize=8.5, color=SLATE, style="italic")
    ax.text(7.55, 2.1, "$\\mathrm{SG} = \\mathrm{id}_M$", ha="center", fontsize=10, color=SLATE)
    ax.text(7.55, 1.65, "$K / C$-partisjon", ha="center", fontsize=9, color=SLATE)

    # Bottom-left: null
    ax.text(2.85, 2.2, "uniform prior\n(null-hypotese)", ha="center", fontsize=9,
            color=OI["grey"], style="italic")

    ax.set_title("Dei to grensetilfella som degenererte hjørne av kjerne-likninga", fontsize=11, pad=10)

    save(fig, "11_grensetilfelle_matrix")


# ═════════════════════════════════════════════════════════════════════
# FIG 12: Precursor timeline
# ═════════════════════════════════════════════════════════════════════
def fig_precursor_timeline():
    fig, ax = plt.subplots(figsize=(12, 4.5))

    events = [
        (1860, "Semper", "materialteknikk + kulturell meining", SLATE, 1),
        (1917, "Thompson", "biologisk form = fysiske krefter", SLATE, -1),
        (1932, "Wright", "tilpassingslandskap", AMBER, 1),
        (1957, "Waddington", "epigenetisk landskap, kanalisering", AMBER, -1),
        (1964, "Alexander", "misfit-vektorar", OI["blue"], 1),
        (1966, "Raup", "morfologisk parameterrom", AMBER, -1),
        (1968, "Pye", "risikohandverk vs vissheitshandverk", OI["blue"], 1),
        (1969, "Simon", "vitskap om det artificielle", OI["blue"], -1),
        (1972, "Stiny \\& Gips", "formgrammatikk (generativ algebra)", OI["green"], 1),
        (1979, "Steadman", "biologisk analogi i design", OI["blue"], -1),
        (1988, "Basalla", "darwinistisk teknologi-evolusjon", OI["blue"], 1),
        (1992, "Petroski", "svikt som seleksjon", OI["blue"], -1),
        (1993, "Kauffman", "NK-landskap på kultur", OI["blue"], 1),
        (2003, "Hatchuel \\& Weil", "C-K-teori (epistemisk)", OI["green"], -1),
        (2009, "W.\\,B.\\,Arthur", "teknologi = kombinatorisk evolusjon", OI["blue"], 1),
        (2022, "Levin + Fields", "substrat-uavhengig agens", OI["rust"], -1),
        (2026, "Formlære", "grammatikk + landskap + representasjon", AMBER, 1),
    ]

    # Timeline spine
    x0, x1 = 1855, 2032
    ax.plot([x0, x1], [0, 0], color=SLATE, linewidth=1.8, zorder=1)
    for year in range(1860, 2030, 20):
        ax.plot([year, year], [-0.06, 0.06], color=SLATE, linewidth=1.2, zorder=2)
        ax.text(year, -0.35, str(year), ha="center", fontsize=8.5, color=SLATE)

    # Events alternating above/below
    for year, name, desc, color, direction in events:
        ypos = 0.7 * direction
        ax.plot([year, year], [0, ypos], color=color, linewidth=0.8, alpha=0.5, zorder=3)
        ax.plot(year, 0, "o", color=color, markersize=8, markeredgecolor="white",
                markeredgewidth=1, zorder=10)
        va = "bottom" if direction > 0 else "top"
        ax.text(year, ypos + 0.05 * direction, name,
                ha="center", va=va, fontsize=9, fontweight="bold", color=color)
        ax.text(year, ypos + 0.23 * direction, desc,
                ha="center", va=va, fontsize=7.5, color=SLATE, style="italic",
                wrap=True)

    # Legend by color
    legend_items = [
        ("biologi-formvitskap", AMBER),
        ("partiell designteori-føregangar", OI["blue"]),
        ("formell designteori", OI["green"]),
        ("substrat-uavhengig agens", OI["rust"]),
        ("Formlære (denne artikkelen)", AMBER),
    ]
    for i, (label, color) in enumerate(legend_items):
        y = -1.3 - i * 0.15
        ax.plot([1863], [y], "o", color=color, markersize=7)
        ax.text(1867, y, label, fontsize=8.5, color=SLATE, va="center")

    ax.set_xlim(x0, x1)
    ax.set_ylim(-2.3, 1.6)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Partielle føregangarar: hundreåret med formtenking før Formlære", pad=10)

    save(fig, "12_foregangarar_tidslinje")


# ═════════════════════════════════════════════════════════════════════
# FIG 13: Falsifiseringsnivå (three-level hierarchy)
# ═════════════════════════════════════════════════════════════════════
def fig_falsification_levels():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # Three levels, each a row
    levels = [
        {
            "y": 4.5, "title": "Modellnivå",
            "cond": "$\\Delta \\mathrm{AIC} > 10$ i favør av full modell",
            "test": "estimer 3 komponentar separat, samanlikn prediktiv kraft",
            "outcome": "komponent er overflødig for klassen",
            "color": OI["blue"]
        },
        {
            "y": 2.8, "title": "Grensetilfelle-nivå",
            "cond": "ikkje-degenerert klasse der éin tradisjon predikerer like godt som full",
            "test": "finn klasse med $\\hat{\\mathcal{L}}$ ikkje flat, der SG åleine er nok",
            "outcome": "full modell har inga meirverdi for klassen",
            "color": OI["green"]
        },
        {
            "y": 1.1, "title": "Substrat-nivå",
            "cond": "domene med persistente former utan identifiserbart agenthierarki",
            "test": "forsøk å tilpasse alle sett av $\\{A_k\\}$ + $\\mathcal{L}_k$",
            "outcome": "substrat-uavhengigheita tilbakeviss for domenet",
            "color": OI["rust"]
        },
    ]

    for lvl in levels:
        y = lvl["y"]
        # Title box
        ax.add_patch(FancyBboxPatch((0.2, y - 0.4), 2.2, 0.8, boxstyle="round,pad=0.05",
                                    facecolor=lvl["color"], alpha=0.85, edgecolor=lvl["color"]))
        ax.text(1.3, y, lvl["title"], ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white")

        # Condition
        ax.text(2.7, y + 0.3, "Vilkår:", fontsize=9, fontweight="bold", color=SLATE)
        ax.text(3.5, y + 0.3, lvl["cond"], fontsize=9, color=SLATE)

        # Test
        ax.text(2.7, y, "Test:", fontsize=9, fontweight="bold", color=SLATE)
        ax.text(3.5, y, lvl["test"], fontsize=9, color=SLATE)

        # Outcome
        ax.text(2.7, y - 0.3, "Utfall:", fontsize=9, fontweight="bold", color=SLATE)
        ax.text(3.5, y - 0.3, lvl["outcome"], fontsize=9, color=SLATE, style="italic")

    ax.text(5, 5.7, "Tre nivå av falsifiseringsvilkår", fontsize=12, fontweight="bold",
            ha="center", color=SLATE)

    # Depth arrow
    ax.annotate("", xy=(9.7, 0.8), xytext=(9.7, 5.0),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.5))
    ax.text(9.85, 2.9, "aukande alvor", rotation=-90, va="center", fontsize=9,
            color=SLATE, style="italic")

    save(fig, "13_falsifiseringsniva")


# ═════════════════════════════════════════════════════════════════════
# FIG 14: Agenthierarki med representasjonsrom (inspired by graph-07)
# ═════════════════════════════════════════════════════════════════════
def fig_agent_hierarchy():
    fig, ax = plt.subplots(figsize=(10, 6))

    agents = [
        ("$A_0$", "Substrat", 0.4, OI["skyblue"]),
        ("$A_1$", "Verktøy", 0.8, OI["green"]),
        ("$A_2$", "Handverkar", 1.4, OI["yellow"]),
        ("$A_3$", "Organisasjon", 2.2, OI["orange"]),
        ("$A_4$", "Marknad", 3.2, OI["rust"]),
        ("$A_5$", "Regulering", 4.5, OI["pink"]),
    ]

    n = len(agents)

    # Left column: agent boxes
    for i, (sym, name, width, color) in enumerate(agents):
        y = n - i - 0.5
        ax.add_patch(FancyBboxPatch((0.3, y - 0.35), 2.5, 0.7, boxstyle="round,pad=0.03",
                                    facecolor=LIGHTSLATE, edgecolor=SLATE, linewidth=1.2))
        ax.text(0.55, y, sym, fontsize=11, fontweight="bold", color=SLATE, va="center")
        ax.text(1.0, y, name, fontsize=10, color=SLATE, va="center")

    # Arrow showing hierarchy (upward through agents)
    ax.annotate("", xy=(3.0, n - 0.2), xytext=(3.0, -0.5 + 0.5),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))
    ax.text(3.08, n / 2, "hierarki $\\mathcal{A}$", rotation=-90, fontsize=9, color=SLATE,
            va="center", style="italic")

    # Right column: light cones (representasjonsrom) as horizontal bars
    for i, (sym, name, width, color) in enumerate(agents):
        y = n - i - 0.5
        # Bar
        bar_width = width
        ax.add_patch(Rectangle((4.0, y - 0.25), bar_width, 0.5,
                               facecolor=color, alpha=0.7, edgecolor="white", linewidth=1))
        ax.text(4.0 + bar_width + 0.1, y, f"$C(A_{i})$", fontsize=10, color=SLATE, va="center")

        # Deformation arrow to next level
        if i > 0:
            y_prev = n - (i - 1) - 0.5
            ax.annotate("", xy=(4.2, y_prev - 0.3), xytext=(4.2, y + 0.3),
                        arrowprops=dict(arrowstyle="->", color=OI["rust"], lw=0.8, alpha=0.6,
                                        connectionstyle="arc3,rad=0.3"))

    ax.text(4.3, n + 0.15, "aukande representasjonsrom $C(A_k)$ →", fontsize=9.5,
            color=SLATE, style="italic")
    ax.text(5.0, -0.7, "pilene viser korleis høgare nivå deformerer lågare (og motsatt)",
            fontsize=8.5, color=OI["rust"], style="italic")

    ax.set_xlim(-0.2, 9.5)
    ax.set_ylim(-1, n + 0.6)
    ax.set_aspect("auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Agenthierarki $\\mathcal{A} = \\{A_0, \\ldots, A_n\\}$ med agent-spesifikke representasjonsrom", fontsize=11, pad=10)

    save(fig, "14_agenthierarki")


# ═════════════════════════════════════════════════════════════════════
# FIG 15: Formvitskapen si grunn-Venn (M ∩ L(SG) ∩ C(A))
# ═════════════════════════════════════════════════════════════════════
def fig_venn_components():
    fig, ax = plt.subplots(figsize=(8, 7))

    # Outer M
    ax.add_patch(Rectangle((-6, -5), 12, 10, fill=True, facecolor=LIGHTSLATE,
                           edgecolor=SLATE, linewidth=1.2))
    ax.text(-5.7, 4.3, "Formrom $M$", fontsize=11, fontweight="bold", color=SLATE)

    # Three overlapping circles
    r = 3.0
    offsets = [(-1.8, 1.0), (1.8, 1.0), (0, -2.0)]
    labels = ["$L(\\mathrm{SG})$", "$\\{F : \\hat{\\mathcal{L}}(F) \\ \\mathrm{låg}\\}$", "$C(A)$"]
    color_fills = [OI["skyblue"], AMBER, OI["green"]]
    outer_labels = [("formspråk\n det mogelege", (-3.8, 3.3), OI["blue"]),
                    ("tilpassingslandskap\n det sannsynlege", (3.8, 3.3), AMBER),
                    ("representasjonsrom\n det tilgjengelege", (0, -4.2), OI["green"])]

    # Draw with alpha so intersections show colour mixing
    for (dx, dy), color in zip(offsets, color_fills):
        c = Circle((dx, dy), r, facecolor=color, alpha=0.32, edgecolor=color, linewidth=2)
        ax.add_patch(c)

    # Inner labels (inside circle, outside intersection)
    for (dx, dy), lbl, color_pair in zip(offsets, labels, outer_labels):
        # Math label at circle center-top
        ax.text(dx, dy + 1.1, lbl, ha="center", fontsize=13, fontweight="bold", color=SLATE)

    for text, (x, y), color in outer_labels:
        ax.text(x, y, text, ha="center", fontsize=9.5, color=color, fontweight="bold")

    # F at triple intersection
    ax.plot(0, 0, "o", color=SLATE, markersize=12, zorder=10)
    ax.annotate("$F$ realisert form",
                xy=(0, 0), xytext=(3.8, -1.0), fontsize=10.5,
                color=SLATE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))

    ax.set_xlim(-6, 6)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Kjerne-domene: $F \\in L(\\mathrm{SG}) \\cap \\{\\hat{\\mathcal{L}} \\ \\mathrm{låg}\\} \\cap C(A)$",
                 fontsize=11.5, pad=12)

    save(fig, "15_kjernedomene_venn")


# ═════════════════════════════════════════════════════════════════════
# FIG 16: Boltzmann vs. Pareto vs. multiplicative (alternatives)
# ═════════════════════════════════════════════════════════════════════
def fig_distribution_alternatives():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    x = np.linspace(0, 5, 500)
    L = x  # energy increasing with x

    # Boltzmann
    P_boltz = np.exp(-1.5 * L)
    P_boltz = P_boltz / np.trapezoid(P_boltz, x)

    # Pareto
    alpha = 2.5
    P_pareto = np.where(x > 0.1, alpha * (0.1 ** alpha) / (x ** (alpha + 1)), 0)
    P_pareto = P_pareto / np.trapezoid(P_pareto, x)

    # Multiplicative / lognormal
    mu, sigma = 0.2, 0.6
    P_logn = np.where(x > 0, 1 / (x * sigma * np.sqrt(2 * np.pi)) * np.exp(-(np.log(x) - mu) ** 2 / (2 * sigma ** 2)), 0)
    P_logn = P_logn / np.trapezoid(P_logn, x)

    data = [(P_boltz, "Boltzmann", "$e^{-\\beta \\mathcal{L}}$", OI["blue"], "stramme halar, ein modus"),
            (P_pareto, "Pareto", "$\\mathcal{L}^{-\\alpha}$", OI["rust"], "tunge halar, fordelar seg vidt"),
            (P_logn, "Lognormal (multiplikativ)", "multiplikative prosessar", OI["green"], "høgreskeivt, moderate halar")]

    for ax, (p, title, formula, color, note) in zip(axes, data):
        ax.fill_between(x, p, alpha=0.35, color=color)
        ax.plot(x, p, color=color, linewidth=2)
        ax.set_xlabel("$\\mathcal{L}$ (eller $x$)")
        ax.set_ylabel("$P(x)$")
        ax.set_title(f"{title}\n\\small {formula}", fontsize=10)
        ax.text(0.98, 0.95, note, transform=ax.transAxes, ha="right", va="top",
                fontsize=9, style="italic", color=SLATE)

    fig.suptitle("Tre kandidatar til stasjonær fordeling: Formlære vel Boltzmann av MaxEnt-konsistens",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "16_fordeling_alternativ")


# ═════════════════════════════════════════════════════════════════════
# FIG 17: Konvergens-figur (som Figur 1 i artikkelen, som PNG)
# ═════════════════════════════════════════════════════════════════════
def fig_three_traditions_converge():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # Three source boxes at top
    sources = [
        (1.5, 6.5, "Syntaks", "Stiny \\& Gips (1972)", "formgrammatikk", LIGHTSLATE, SLATE),
        (5.0, 6.5, "Logikk", "Hatchuel \\& Weil (2003)", "C-K-teori", LIGHTSLATE, SLATE),
        (8.5, 6.5, "Dynamikk", "Levin (2022)", "substrat-agens", LIGHTAMBER, AMBER),
    ]

    for x, y, title, sub, role, bg, ec in sources:
        ax.add_patch(FancyBboxPatch((x - 1.3, y - 0.6), 2.6, 1.2, boxstyle="round,pad=0.05",
                                    facecolor=bg, edgecolor=ec, linewidth=1.5))
        ax.text(x, y + 0.3, title, ha="center", fontsize=11, fontweight="bold", color=ec)
        ax.text(x, y - 0.0, sub, ha="center", fontsize=8.5, color=SLATE, style="italic")
        ax.text(x, y - 0.3, role, ha="center", fontsize=8.5, color=SLATE)

    # Central equation
    ax.add_patch(FancyBboxPatch((1.5, 3.2), 7.0, 1.6, boxstyle="round,pad=0.08",
                                facecolor=LIGHTAMBER, edgecolor=AMBER, linewidth=2.5))
    ax.text(5.0, 4.4, "Formlære", ha="center", fontsize=13, fontweight="bold", color=AMBER)
    ax.text(5.0, 3.7, r"Form $= \mathrm{SG}\!\left(\sum_{k=0}^{n} \nabla_{C(A_k)} \mathcal{L}_k(c,t)\right)$",
            ha="center", fontsize=12, color=AMBER)

    # Arrows top to central
    for x, y, *_ in sources:
        ax.annotate("", xy=(x + (5 - x) * 0.1, 4.8), xytext=(x, y - 0.65),
                    arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))

    # Three components at bottom
    components = [
        (2.0, 1.3, "$\\mathrm{SG}$", "grammatikk", LIGHTSLATE, SLATE),
        (5.0, 1.3, "$\\mathcal{L}_k$", "landskap", LIGHTAMBER, AMBER),
        (8.0, 1.3, "$C(A_k)$", "representasjonsrom", LIGHTSLATE, SLATE),
    ]
    for x, y, sym, role, bg, ec in components:
        ax.add_patch(FancyBboxPatch((x - 1.0, y - 0.45), 2.0, 0.9, boxstyle="round,pad=0.05",
                                    facecolor=bg, edgecolor=ec, linewidth=1.3))
        ax.text(x, y + 0.1, sym, ha="center", fontsize=12, fontweight="bold", color=ec)
        ax.text(x, y - 0.22, role, ha="center", fontsize=8.5, color=SLATE, style="italic")

    # Arrows central to bottom
    for x, y, *_ in components:
        ax.annotate("", xy=(x, y + 0.5), xytext=(5, 3.1),
                    arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))

    ax.text(5, 7.7, "Tre tradisjonar konvergerer i kjerne-likninga",
            ha="center", fontsize=12, fontweight="bold", color=SLATE)

    save(fig, "17_tre_tradisjonar_konvergens")


# ═════════════════════════════════════════════════════════════════════
# FIG 18: Komponentdiagram (D-tuppel, som Figur 2 i artikkelen som PNG)
# ═════════════════════════════════════════════════════════════════════
def fig_component_diagram():
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    # M at top
    ax.add_patch(FancyBboxPatch((3.5, 6.5), 3.0, 1.2, boxstyle="round,pad=0.05",
                                facecolor=LIGHTSLATE, edgecolor=SLATE, linewidth=1.5))
    ax.text(5, 7.3, r"Formrom $M$", ha="center", fontsize=11.5, fontweight="bold", color=SLATE)
    ax.text(5, 6.9, "moglege konfigurasjonar", ha="center", fontsize=8.5, color=SLATE, style="italic")

    # Middle row: Π (left), SG (center), L (right)
    middle_boxes = [
        (1.5, 4.0, r"Partisjon $\Pi$", r"$(K, C, F)$", LIGHTSLATE, SLATE),
        (5.0, 4.0, r"Grammatikk $\mathrm{SG}$", r"$(S, R, \omega)$", LIGHTSLATE, SLATE),
        (8.5, 4.0, r"Landskap $\mathcal{L}_k$", "seleksjonstrykk", LIGHTAMBER, AMBER),
    ]
    for x, y, title, sub, bg, ec in middle_boxes:
        ax.add_patch(FancyBboxPatch((x - 1.2, y - 0.55), 2.4, 1.1, boxstyle="round,pad=0.05",
                                    facecolor=bg, edgecolor=ec, linewidth=1.5))
        ax.text(x, y + 0.2, title, ha="center", fontsize=10.5, fontweight="bold", color=ec)
        ax.text(x, y - 0.2, sub, ha="center", fontsize=8.5, color=SLATE, style="italic")

    # Bottom: A
    ax.add_patch(FancyBboxPatch((2.5, 1.0), 5.0, 1.0, boxstyle="round,pad=0.05",
                                facecolor=LIGHTSLATE, edgecolor=SLATE, linewidth=1.5))
    ax.text(5, 1.5, r"Agenthierarki $\mathcal{A} = \{A_0, \dots, A_n\}$",
            ha="center", fontsize=11.5, fontweight="bold", color=SLATE)

    # Arrows: middle → M
    def arrow(x1, y1, x2, y2, label):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))
        # Label midpoint with white bg
        midx, midy = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(midx, midy, label, fontsize=8, color=SLATE, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))

    arrow(1.5, 4.55, 3.7, 6.5, "partisjonerer")
    arrow(5.0, 4.55, 5.0, 6.5, r"genererer $L(\mathrm{SG})$")
    arrow(8.5, 4.55, 6.3, 6.5, "vektar sannsyn")

    arrow(3.0, 2.0, 1.8, 3.45, "strukturerer")
    arrow(5.0, 2.0, 5.0, 3.45, "realiserer")
    arrow(7.0, 2.0, 8.2, 3.45, r"$\nabla_{C(A_k)}$-navigerer")

    ax.text(5, 7.9, r"Formlære-tuppel: $\mathcal{D} = (M, \Pi, \mathrm{SG}, \mathcal{L}, \mathcal{A})$",
            ha="center", fontsize=12, fontweight="bold", color=SLATE)

    save(fig, "18_komponent_diagram")


# ═════════════════════════════════════════════════════════════════════
# FIG 19: Stase + brot dynamikk (punctuated equilibrium)
# ═════════════════════════════════════════════════════════════════════
def fig_punctuated_dynamics():
    fig, ax = plt.subplots(figsize=(10, 5))

    t = np.linspace(0, 100, 1000)
    # Form trajectory with long stasis + bifurcations
    f = np.zeros_like(t)
    f[0] = 0.5
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        # Mostly stable, with abrupt transitions
        if 25 < t[i] < 26:
            f[i] = f[i-1] + 1.5 * dt * 10
        elif 58 < t[i] < 59:
            f[i] = f[i-1] - 1.2 * dt * 10
        elif 82 < t[i] < 83:
            f[i] = f[i-1] + 0.8 * dt * 10
        else:
            f[i] = f[i-1] + 0.015 * np.random.randn() * dt

    ax.plot(t, f, "-", color=AMBER, linewidth=1.8)
    ax.fill_between(t, f - 0.08, f + 0.08, color=AMBER, alpha=0.2)

    # Highlight stase periods
    for start, end in [(0, 25), (26, 58), (59, 82), (83, 100)]:
        ax.axvspan(start, end, alpha=0.08, color=SLATE)

    # Annotate bifurcations
    for t_bif in [25.5, 58.5, 82.5]:
        ax.axvline(t_bif, color=OI["rust"], linestyle="--", alpha=0.6, linewidth=1)

    ax.annotate("stase", xy=(12, 0.3), fontsize=10, color=SLATE, style="italic")
    ax.annotate("brot", xy=(25.5, 1.9), fontsize=10, color=OI["rust"], fontweight="bold",
                xytext=(20, 2.2), arrowprops=dict(arrowstyle="->", color=OI["rust"]))
    ax.annotate("stase", xy=(42, 1.8), fontsize=10, color=SLATE, style="italic")
    ax.annotate("brot", xy=(58.5, 0.5), fontsize=10, color=OI["rust"], fontweight="bold",
                xytext=(65, 0.2), arrowprops=dict(arrowstyle="->", color=OI["rust"]))

    ax.set_xlabel("tid")
    ax.set_ylabel("formtrekk")
    ax.set_title("Dynamikk: lange stase-periodar bryter i brå skifte", pad=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.2, 2.5)

    save(fig, "19_stase_brot")


# ═════════════════════════════════════════════════════════════════════
# FIG 20: Kanalisering: bratte vs grunne dalar
# ═════════════════════════════════════════════════════════════════════
def fig_canalization():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(-3, 3, 400)

    # Steep (canalised)
    y_steep = x**4 - 2 * x**2 + 1
    # Shallow (not canalised)
    y_shallow = 0.1 * x**4 - 0.2 * x**2 + 0.5

    data = [
        (y_steep, "Bratt kanalisering", "liten variasjon trass forstyrring", OI["blue"]),
        (y_shallow, "Grunn kanalisering", "stor variasjon, drift", OI["rust"]),
    ]

    for ax, (y, title, sub, color) in zip(axes, data):
        ax.plot(x, y, color=color, linewidth=2.5)
        ax.fill_between(x, y, -0.5, color=color, alpha=0.15)

        # Balls with perturbation
        np.random.seed(11)
        n_balls = 12
        ball_x = np.random.uniform(-2.5, 2.5, n_balls)
        # Roll each to nearest minimum
        if title.startswith("Bratt"):
            # Steep: all converge to x = ±1
            ball_end_x = np.where(ball_x > 0, 1, -1)
        else:
            # Shallow: drift near where they started
            ball_end_x = ball_x * 0.3
        # Interpolate y
        ball_end_y = np.interp(ball_end_x, x, y)

        for bx, by in zip(ball_end_x, ball_end_y):
            ax.plot(bx, by + 0.15, "o", color=AMBER, markersize=9,
                    markeredgecolor=SLATE, markeredgewidth=0.7)

        ax.set_title(title, fontsize=11, color=color)
        ax.text(0, -0.3, sub, ha="center", fontsize=9.5, color=SLATE, style="italic",
                transform=ax.get_xaxis_transform())

        ax.set_xlabel("formdimensjon")
        ax.set_ylabel("$\\hat{\\mathcal{L}}$")
        ax.set_ylim(-0.5, 4.5)

    fig.suptitle("Kanalisering (Waddington, 1957): brattleik på dalveggar = robustheit",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "20_kanalisering")


# ═════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Generating figures to: {OUT}")
    print()

    figures = [
        fig_morphospace_raup,
        fig_adaptation_landscape_3d,
        fig_waddington,
        fig_multiscale_landscapes,
        fig_gradient_trajectory,
        fig_multi_agent_field,
        fig_nested_representation,
        fig_path_dependence,
        fig_boltzmann_distribution,
        fig_shape_grammar_rewrite,
        fig_reduction_matrix,
        fig_precursor_timeline,
        fig_falsification_levels,
        fig_agent_hierarchy,
        fig_venn_components,
        fig_distribution_alternatives,
        fig_three_traditions_converge,
        fig_component_diagram,
        fig_punctuated_dynamics,
        fig_canalization,
    ]

    for fn in figures:
        try:
            fn()
        except Exception as e:
            print(f"  FAIL: {fn.__name__}: {e}")

    print()
    print(f"Done. {len(figures)} figures attempted.")
