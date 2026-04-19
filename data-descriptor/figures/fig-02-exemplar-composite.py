"""
Fig 02 -- Exemplar composite: 4 chairs shown as bguw images across time.
Simple grid with metadata labels. No mesh rendering needed.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, DATA,
                   INK, INK_SOFT, RULE, PAPER, HIGHLIGHT,
                   ACCENT_TEAL, ACCENT_RUST, ACCENT_GOLD, FULL_W)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

apply_style()

df = load_stolar()

# pick 4 chairs spanning periods with good bguw images
exemplars = [
    "O113389",                  # Renessanse, 1525
    "O107557",                  # Rokokko, 1700
    "NMK.INVENTAR.2017.0213",   # Jugend/Art Nouveau, 1900
    "NMK.2005.0638",            # Postmodernisme, 1983 (Balans Gravity)
]

# fallback: find chairs with bguw images if IDs don't match
found = []
for eid in exemplars:
    row = df[df["id"] == eid]
    if len(row) > 0:
        found.append(row.iloc[0])

# if not enough, pick from dataset
if len(found) < 4:
    candidates = df.dropna(subset=["height_cm", "width_cm", "style"]).copy()
    candidates = candidates[candidates["bguw_url"].notna()]
    for style_target in ["Renessanse", "Barokk", "Postmodernisme", "Samtidsdesign"]:
        match = candidates[candidates["style"] == style_target]
        if len(match) > 0 and len(found) < 4:
            found.append(match.iloc[0])

fig, axes = plt.subplots(1, min(len(found), 4),
                          figsize=(FULL_W, FULL_W * 0.4))
if not hasattr(axes, '__len__'):
    axes = [axes]

for ax, row in zip(axes, found[:4]):
    # try to load bguw image
    bguw_path = DATA / "bguw" / f"{row['id']}_bguw.png"
    if bguw_path.exists():
        img = Image.open(bguw_path)
        img.thumbnail((400, 400))
        ax.imshow(img, aspect="equal")
    else:
        ax.text(0.5, 0.5, row["id"], transform=ax.transAxes,
                ha="center", va="center", fontsize=7, color=INK_SOFT)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # label
    name = str(row.get("name", ""))[:25]
    year = int(row["year_from"]) if not np.isnan(row.get("year_from", np.nan)) else "?"
    style = str(row.get("style", ""))[:20]
    dims = ""
    if not np.isnan(row.get("height_cm", np.nan)):
        h = int(row["height_cm"])
        w = int(row.get("width_cm", 0)) if not np.isnan(row.get("width_cm", np.nan)) else "?"
        d = int(row.get("depth_cm", 0)) if not np.isnan(row.get("depth_cm", np.nan)) else "?"
        dims = f"{h} x {w} x {d} cm"

    caption = f"{name}\n{year}  {style}\n{dims}"
    ax.set_xlabel(caption, fontsize=5.5, color=INK_SOFT, linespacing=1.4)

fig.suptitle("")
fig.tight_layout()
save_fig(fig, "fig-02-exemplar-composite")
print("fig-02-exemplar-composite saved")
