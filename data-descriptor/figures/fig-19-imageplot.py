"""
Fig 19 -- Manovich-style ImagePlot.
Chair thumbnails plotted at their morphometric coordinates.
X = complexity, Y = sphericity. Each chair IS its own data point.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style import (apply_style, load_stolar, save_fig, DATA,
                   INK, INK_SOFT, RULE, PAPER, ACCENT_TEAL, ACCENT_RUST, FULL_W)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

apply_style()

df = load_stolar()
geo = df.dropna(subset=["complexity", "sphericity", "year_mid"]).copy()
geo = geo[(geo["year_mid"] > 1400) & (geo["sphericity"] > 0.1)]

# sample ~150 chairs for readability (stratified by style)
np.random.seed(42)
sampled = geo.groupby("style", group_keys=False).apply(
    lambda x: x.sample(min(12, len(x)), random_state=42)
)
print(f"Sampled {len(sampled)} chairs for ImagePlot")

fig, ax = plt.subplots(figsize=(FULL_W * 1.2, FULL_W * 0.9))
ax.set_facecolor(PAPER)

bguw_dir = DATA / "bguw"

plotted = 0
for _, row in sampled.iterrows():
    bguw_path = bguw_dir / f"{row['id']}_bguw.png"
    if not bguw_path.exists():
        continue

    try:
        img = Image.open(bguw_path)
        img.thumbnail((40, 40))
        img_arr = np.array(img)

        im = OffsetImage(img_arr, zoom=0.5)
        ab = AnnotationBbox(im, (row["complexity"], row["sphericity"]),
                            frameon=False, pad=0)
        ax.add_artist(ab)
        plotted += 1
    except Exception:
        continue

print(f"Plotted {plotted} chair thumbnails")

ax.set_xlabel("Kompleksitet (log10 verteksar / overflate)")
ax.set_ylabel("Sphaerisitet")
ax.set_xlim(geo["complexity"].quantile(0.01) - 0.3,
            geo["complexity"].quantile(0.99) + 0.3)
ax.set_ylim(geo["sphericity"].quantile(0.01) - 0.02,
            geo["sphericity"].quantile(0.99) + 0.02)

fig.tight_layout()
save_fig(fig, "fig-19-imageplot")
print("done")
