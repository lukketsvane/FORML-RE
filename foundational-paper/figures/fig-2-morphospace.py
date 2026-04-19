"""
Figure 1, Panel A: Morphospace scatter of 2,066 chairs in (Width x Height).
Color by half-century period. Generates fig-2-morphospace.pdf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os

# ── Load data ──
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
df = pd.read_csv(os.path.join(REPO, "STOLAR", "STOLAR.csv"))

# ── Map Nynorsk column names ──
df = df.rename(columns={
    "Breidde (cm)": "w_cm",
    "Høgde (cm)": "h_cm",
    "Djupn (cm)": "d_cm",
    "Frå år": "year_from",
    "Til år": "year_to",
    "Stilperiode": "style",
    "Materialar": "material",
    "Nasjonalitet": "nation",
})
df["year_mid"] = (pd.to_numeric(df["year_from"], errors="coerce") +
                  pd.to_numeric(df["year_to"], errors="coerce")) / 2

# ── Clean ──
df = df.dropna(subset=["w_cm", "h_cm", "year_mid"])
df["w_cm"] = pd.to_numeric(df["w_cm"], errors="coerce")
df["h_cm"] = pd.to_numeric(df["h_cm"], errors="coerce")
df = df.dropna(subset=["w_cm", "h_cm"])
df = df[(df["w_cm"] > 0) & (df["h_cm"] > 0)]
df["period"] = (df["year_mid"] // 50) * 50

# ── Plot ──
fig, ax = plt.subplots(figsize=(5.5, 4.5))

norm = Normalize(vmin=1500, vmax=2025)
cmap = plt.cm.viridis

scatter = ax.scatter(
    df["w_cm"], df["h_cm"],
    c=df["year_mid"], cmap=cmap, norm=norm,
    s=8, alpha=0.5, edgecolors="none", rasterized=True
)

# ── Convex hull outline (occupied region) ──
from scipy.spatial import ConvexHull
pts = df[["w_cm", "h_cm"]].values
try:
    hull = ConvexHull(pts)
    hull_pts = np.append(hull.vertices, hull.vertices[0])
    ax.plot(pts[hull_pts, 0], pts[hull_pts, 1],
            color="black", linewidth=0.8, linestyle="--", alpha=0.4, label="Occupied boundary")
except Exception:
    pass

# ── Labels ──
ax.set_xlabel("Width (cm)", fontsize=10)
ax.set_ylabel("Height (cm)", fontsize=10)
ax.set_xlim(0, 120)
ax.set_ylim(0, 180)
ax.tick_params(labelsize=8)

cbar = fig.colorbar(scatter, ax=ax, pad=0.02, shrink=0.85)
cbar.set_label("Year", fontsize=9)
cbar.ax.tick_params(labelsize=7)

ax.set_title("A. Morphospace", fontsize=11, fontweight="bold", loc="left")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig-2-morphospace.pdf")
fig.savefig(out, dpi=300, bbox_inches="tight")
print(f"Saved: {out} ({len(df)} chairs)")
