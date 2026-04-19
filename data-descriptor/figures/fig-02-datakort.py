"""
Fig 02 -- Datakort-kompositt: 6 stolar frå ulike periodar vist som
pre-genererte datakort (stolar-nn bilete med metadata + mesh-trekk).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, REPO,
                   INK, RULE, PAPER, FULL_W)
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

apply_style()

NN_DIR = REPO / "writings" / "figures" / "stolar-nn"

# pick 6 chairs spanning time and style
exemplars = [
    "NMK.2005.0640",   # Tripp Trapp (Stokke), 1972
    "NMK.2005.0638",   # Balans Gravity, 1983
    "NMK.2005.0644",   # Safari, 2002
    "NMK.2005.0639",   # another classic
    "NMK.2006.0076",   #
    "NMK.2005.0645",   #
]

# find which exist
cards = []
for eid in exemplars:
    path = NN_DIR / f"objekt_{eid}_nn.png"
    if path.exists():
        cards.append(path)

# if not enough, fill from directory
if len(cards) < 6:
    for f in sorted(NN_DIR.glob("*.png")):
        if f not in cards:
            cards.append(f)
        if len(cards) >= 6:
            break

ncols = 3
nrows = 2
fig, axes = plt.subplots(nrows, ncols, figsize=(FULL_W, FULL_W * 0.45))

for idx, (ax, card_path) in enumerate(zip(axes.flatten(), cards[:6])):
    img = Image.open(card_path)
    ax.imshow(img, aspect="equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(RULE)
        spine.set_linewidth(0.5)

fig.tight_layout(pad=0.3)
save_fig(fig, "fig-02-datakort")
print("done")
