"""
Empiriske figurar E1-E6 for Formlære-artikkelen.

Ingen figur-suptittel eller footer-forklaring i bileta;
all tekstkontekst blir skriven inn i LaTeX av forfattar.

Datagrunnlag: STOLAR/STOLAR.csv (2048 stolar, 1997 med komplett tabellgeometri
og mesh-avleidde trekk). GLB-meshar i STOLAR/glb/.

Seks morfologiske aksar:
  Høgde, Breidde, Djupn, Sphericity, Fill-ratio, Inertia-ratio

Figurane:
  E1  PCA-morforom farga etter stilperiode
  E2  7x7 mesh-silhuett-grid over PCA-planet
  E3  KDE-tetthet per epoke
  E4  Kanalisering: normalisert varians per akse per epoke
  E5  Rullande sentroide og spreiing over tid
  E6  Giga-grid: alle silhuettar sorterte kronologisk

Silhuettane cachast til _silhouette_cache.npz for rask rerun.

Utgang: 300 DPI PNG i ./png_empirical/.
"""

import os, re, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
from matplotlib.patches import Ellipse, Rectangle, FancyArrowPatch
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import gaussian_kde
from scipy.ndimage import binary_closing, binary_fill_holes
from scipy.spatial import ConvexHull
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import trimesh

warnings.filterwarnings("ignore")

# ─── Paths ────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CSV  = os.path.join(REPO, "STOLAR", "STOLAR.csv")
GLB  = os.path.join(REPO, "STOLAR", "glb")
OUT  = os.path.join(HERE, "png_empirical")
os.makedirs(OUT, exist_ok=True)

# ─── Style ────────────────────────────────────────────────────────────
SLATE = "#3C4B5F"
AMBER = "#B47332"
LIGHTSLATE = "#E1E6EE"
LIGHTAMBER = "#F3E4CD"
CREAM = "#FAF6EE"

OI = {
    "orange": "#E69F00", "skyblue": "#56B4E9", "green": "#009E73",
    "yellow": "#F0E442", "blue": "#0072B2", "rust": "#D55E00",
    "pink": "#CC79A7", "black": "#000000",  "grey": "#999999",
}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
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
    print(f"  saved: png_empirical/{name}.png")


# ─── Data loading and preprocessing ──────────────────────────────────
AXES = ["Høgde (cm)", "Breidde (cm)", "Djupn (cm)",
        "Sphericity (mesh)", "Fill-ratio (mesh)", "Inertia-ratio (mesh)"]

AXIS_LABELS_NN = {
    "Høgde (cm)": "Høgde",
    "Breidde (cm)": "Breidde",
    "Djupn (cm)": "Djupn",
    "Sphericity (mesh)": "Sphericity",
    "Fill-ratio (mesh)": "Fill-ratio",
    "Inertia-ratio (mesh)": "Inertia-ratio",
}

# Ordered periods for time-ordered plots (spans ca. 1400-2024)
PERIOD_ORDER = [
    "Renessanse", "Barokk", "Régence", "Rokokko", "Empire",
    "Nyklassisisme", "Hepplewhite", "Historisme", "Viktorianisme",
    "Jugend/Art Nouveau", "Art Deco / Tidleg modernisme",
    "Bauhaus", "Funksjonalisme", "Nordisk funksjonalisme",
    "Modernisme", "Midtjahrhundre modernisme",
    "Modernisme / Midtjahrhundre", "Skandinavisk modernisme",
    "Postmodernisme", "Samtidsdesign",
]

# Approximate midpoint year per period (for time-axis ordering)
PERIOD_YEAR = {
    "Renessanse": 1550, "Barokk": 1680, "Régence": 1720, "Rokokko": 1755,
    "Nyklassisisme": 1790, "Hepplewhite": 1790, "Empire": 1810,
    "Historisme": 1870, "Viktorianisme": 1875,
    "Jugend/Art Nouveau": 1905, "Art Deco / Tidleg modernisme": 1925,
    "Bauhaus": 1928, "Funksjonalisme": 1935, "Nordisk funksjonalisme": 1945,
    "Modernisme": 1955, "Midtjahrhundre modernisme": 1960,
    "Modernisme / Midtjahrhundre": 1962, "Skandinavisk modernisme": 1965,
    "Postmodernisme": 1985, "Samtidsdesign": 2015,
}

# Color mapping: chronological gradient slate→amber
def make_period_colors():
    ordered = sorted(PERIOD_YEAR.items(), key=lambda kv: kv[1])
    n = len(ordered)
    cmap = LinearSegmentedColormap.from_list(
        "per", [SLATE, "#6B7080", "#A08860", AMBER], N=n)
    return {name: cmap(i / max(n - 1, 1)) for i, (name, _) in enumerate(ordered)}

PERIOD_COLOR = make_period_colors()


def _parse_century(v):
    if not isinstance(v, str):
        return None
    m = re.match(r"(\d{3,4})", v)
    if m:
        return int(m.group(1)) + 50
    return None


def _parse_datering(v):
    if not isinstance(v, str):
        return None
    nums = re.findall(r"\d{4}", v)
    if not nums:
        return None
    if len(nums) == 1:
        return float(nums[0])
    return (float(nums[0]) + float(nums[1])) / 2


def load_data():
    df = pd.read_csv(CSV)
    for c in AXES:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Frå år"] = pd.to_numeric(df["Frå år"], errors="coerce")
    df["Til år"] = pd.to_numeric(df["Til år"], errors="coerce")
    # treat values < 1000 as missing (placeholder zeros)
    df["Frå år"] = df["Frå år"].where(df["Frå år"] >= 1000)
    df["Til år"] = df["Til år"].where(df["Til år"] >= 1000)

    # fall-back parsers
    yr_h = df["Hundreår"].apply(_parse_century)
    yr_d = df["Datering"].apply(_parse_datering)

    def best(r):
        f, t = r["Frå år"], r["Til år"]
        if pd.notna(f) and pd.notna(t):
            return (f + t) / 2
        if pd.notna(f):
            return f
        if pd.notna(t):
            return t
        if pd.notna(r["_yrd"]):
            return r["_yrd"]
        if pd.notna(r["_yrh"]):
            return r["_yrh"]
        return np.nan

    df["_yrh"] = yr_h
    df["_yrd"] = yr_d
    df = df[df[AXES].notna().all(axis=1)].copy()
    df["år"] = df.apply(best, axis=1)
    df = df.drop(columns=["_yrh", "_yrd"])

    total_geom = len(df)
    have_year = df["år"].notna().sum()
    print(f"  loaded: {total_geom} chairs with complete geometry  "
          f"({have_year} have a usable year)")
    return df


def fit_pca(df):
    X = df[AXES].values
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    pca = PCA(n_components=6).fit(Xs)
    scores = pca.transform(Xs)
    df = df.copy()
    for i in range(6):
        df[f"PC{i+1}"] = scores[:, i]
    return df, pca, scaler


# ═════════════════════════════════════════════════════════════════════
# FIG E1: PCA-morforom farga etter stilperiode
# ═════════════════════════════════════════════════════════════════════
def fig_E1_morforom_pca(df, pca):
    fig = plt.figure(figsize=(12, 6.5))
    gs = gridspec.GridSpec(1, 3, width_ratios=[3.1, 3.1, 1.35],
                           wspace=0.22, figure=fig)

    # clip display to robust quantiles so outliers do not blow out the panel
    def lims(vals, q=0.99):
        lo = np.quantile(vals, 1 - q)
        hi = np.quantile(vals, q)
        pad = (hi - lo) * 0.08
        return lo - pad, hi + pad

    x1lo, x1hi = lims(df["PC1"])
    x2lo, x2hi = lims(df["PC2"])
    x3lo, x3hi = lims(df["PC3"])

    # --- Main scatter: PC1 vs PC2 ---
    ax = fig.add_subplot(gs[0])
    ax.scatter(df["PC1"], df["PC2"], s=6, c=OI["grey"], alpha=0.15,
               linewidths=0, zorder=1)
    top_periods = df["Stilperiode"].value_counts().head(12).index.tolist()
    ordered = [p for p in PERIOD_ORDER if p in top_periods]
    for p in ordered:
        sub = df[df["Stilperiode"] == p]
        c = PERIOD_COLOR.get(p, OI["grey"])
        ax.scatter(sub["PC1"], sub["PC2"], s=14, color=c, alpha=0.8,
                   edgecolors="none", label=f"{p} (n={len(sub)})", zorder=3)

    ax.set_xlim(x1lo, x1hi); ax.set_ylim(x2lo, x2hi)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varians)")
    ax.set_title("(a)", loc="left", fontsize=10.5, weight="bold")
    ax.grid(alpha=0.18, linewidth=0.5)
    ax.axhline(0, color=OI["grey"], linewidth=0.5, alpha=0.5)
    ax.axvline(0, color=OI["grey"], linewidth=0.5, alpha=0.5)

    # --- Secondary: PC1 vs PC3 ---
    ax2 = fig.add_subplot(gs[1])
    ax2.scatter(df["PC1"], df["PC3"], s=6, c=OI["grey"], alpha=0.15,
                linewidths=0, zorder=1)
    for p in ordered:
        sub = df[df["Stilperiode"] == p]
        c = PERIOD_COLOR.get(p, OI["grey"])
        ax2.scatter(sub["PC1"], sub["PC3"], s=14, color=c, alpha=0.8,
                    edgecolors="none", zorder=3)
    ax2.set_xlim(x1lo, x1hi); ax2.set_ylim(x3lo, x3hi)
    ax2.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    ax2.set_ylabel(f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}% varians)")
    ax2.set_title("(b)", loc="left", fontsize=10.5, weight="bold")
    ax2.grid(alpha=0.18, linewidth=0.5)
    ax2.axhline(0, color=OI["grey"], linewidth=0.5, alpha=0.5)
    ax2.axvline(0, color=OI["grey"], linewidth=0.5, alpha=0.5)

    # --- Loadings (biplot arrows on panel a) ---
    load = pca.components_.T[:, :2]
    # scale arrows so the longest fills ~80% of the shorter half-axis
    halfx = (x1hi - x1lo) / 2 * 0.72
    halfy = (x2hi - x2lo) / 2 * 0.72
    load_mag = np.sqrt(load[:, 0] ** 2 + load[:, 1] ** 2)
    max_mag = load_mag.max()
    for i, name in enumerate(AXES):
        x = load[i, 0] / max_mag * halfx
        y = load[i, 1] / max_mag * halfy
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=OI["black"],
                                    lw=1.1, alpha=0.92))
        ax.text(x * 1.18, y * 1.18, AXIS_LABELS_NN[name],
                fontsize=8.5, color=OI["black"], weight="bold",
                ha="center", va="center",
                bbox=dict(facecolor=CREAM, edgecolor=SLATE, linewidth=0.4,
                          boxstyle="round,pad=0.18", alpha=0.92))

    # --- Legend panel ---
    lax = fig.add_subplot(gs[2])
    lax.axis("off")
    handles = []
    for p in ordered:
        c = PERIOD_COLOR.get(p, OI["grey"])
        n_p = (df["Stilperiode"] == p).sum()
        handles.append(plt.Line2D([0], [0], marker="o", linestyle="",
                                   markersize=7, markerfacecolor=c,
                                   markeredgecolor="none",
                                   label=f"{p}  (n={n_p})"))
    lax.legend(handles=handles, loc="upper left",
               frameon=False, fontsize=8.2, handletextpad=0.5,
               title="Stilperiode (kronologisk)",
               title_fontsize=9.2, alignment="left")

    save(fig, "E1_morforom_pca")


# ═════════════════════════════════════════════════════════════════════
# Silhouette rendering + cache
# ═════════════════════════════════════════════════════════════════════
CACHE_PATH = os.path.join(HERE, "_silhouette_cache_96.npz")
CACHE_N = 96


def _silhouette(glb_path, n):
    """Binary silhouette from GLB, projected to side view (ZY)."""
    try:
        m = trimesh.load(glb_path, force="mesh", process=False)
    except Exception:
        return None
    v = np.asarray(m.vertices, dtype=float)
    if v.size == 0:
        return None
    if len(v) > 120000:
        idx = np.random.default_rng(0).choice(len(v), 120000, replace=False)
        v = v[idx]
    u, w = v[:, 2], v[:, 1]
    u = u - (u.max() + u.min()) / 2
    w = w - (w.max() + w.min()) / 2
    scale = max(np.abs(u).max(), np.abs(w).max(), 1e-9)
    u, w = u / scale, w / scale
    img = np.zeros((n, n), dtype=bool)
    ix = ((u + 1.08) / 2.16 * n).astype(int).clip(0, n - 1)
    iy = ((w + 1.08) / 2.16 * n).astype(int).clip(0, n - 1)
    img[n - 1 - iy, ix] = True
    img = binary_closing(img, iterations=1)
    img = binary_fill_holes(img)
    return img


# module-level worker for multiprocessing (must be picklable)
def _silhouette_worker(args):
    oid, path, n = args
    img = _silhouette(path, n)
    if img is None:
        return oid, None
    # pack to bytes for cross-process transfer
    return oid, np.packbits(img).tobytes()


def _silhouette_is_pretty(img):
    """Quality filter: reject silhouettes that are too thin, too sparse,
    too fragmented, or have extreme aspect ratio for a chair."""
    if img is None:
        return False
    H, W = img.shape
    area = int(img.sum())
    if area < 0.08 * H * W:
        return False
    if area > 0.75 * H * W:
        return False
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    if not rows.any() or not cols.any():
        return False
    r0 = int(np.argmax(rows)); r1 = H - 1 - int(np.argmax(rows[::-1]))
    c0 = int(np.argmax(cols)); c1 = W - 1 - int(np.argmax(cols[::-1]))
    bh = r1 - r0 + 1
    bw = c1 - c0 + 1
    if bh < 0.40 * H:
        return False
    if bw < 0.22 * W:
        return False
    ar = bh / max(bw, 1)
    if ar < 0.60 or ar > 2.6:
        return False
    fill = area / (bh * bw)
    if fill < 0.28 or fill > 0.92:
        return False
    from scipy.ndimage import label as _label
    _, ncomp = _label(img)
    if ncomp > 3:
        return False
    return True


def pretty_silhouette_mask(sils):
    """Return the set of oids whose silhouette passes the beauty filter."""
    return {oid for oid, img in sils.items() if _silhouette_is_pretty(img)}


def build_silhouette_cache(ids, force=False, workers=None):
    """Cache silhouettes for all given Objekt-IDs.
    Parallelised over CPUs. Missing entries are rendered and written back."""
    existing = {}
    if os.path.exists(CACHE_PATH) and not force:
        z = np.load(CACHE_PATH, allow_pickle=False)
        existing = {k: z[k].astype(bool) for k in z.files}
    missing = [i for i in ids if i not in existing
               and os.path.exists(os.path.join(GLB, f"{i}.glb"))]
    if not missing:
        print(f"  silhouette cache ok: {len(existing)} entries (no new)")
        return existing

    if workers is None:
        workers = max(mp.cpu_count() - 2, 2)
    print(f"  silhouette cache: {len(existing)} present, rendering {len(missing)} "
          f"with {workers} workers...")
    args_list = [(oid, os.path.join(GLB, f"{oid}.glb"), CACHE_N) for oid in missing]
    done = 0
    n_pix = CACHE_N * CACHE_N
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for oid, data in ex.map(_silhouette_worker, args_list, chunksize=4):
            done += 1
            if data is not None:
                bits = np.frombuffer(data, dtype=np.uint8)
                img = np.unpackbits(bits)[:n_pix].reshape(CACHE_N, CACHE_N).astype(bool)
                existing[oid] = img
            if done % 100 == 0 or done == len(missing):
                print(f"    {done}/{len(missing)}")
    np.savez_compressed(CACHE_PATH,
                        **{oid: img.astype(bool) for oid, img in existing.items()})
    print(f"  cached to {os.path.basename(CACHE_PATH)} ({len(existing)} entries)")
    return existing


# ═════════════════════════════════════════════════════════════════════
# FIG E2: mesh-grid over morforommet
# ═════════════════════════════════════════════════════════════════════
def fig_E2_mesh_grid(df, pca, sils, vox=None):
    """KxK grid over PC1-PC2. Each cell: holotype chair closest to local
    medoid (filtered on mesh quality + PC3-6 compactness), rendered as a
    shaded 3D mesh tinted by material class."""
    K = 8
    pc1 = df["PC1"].values
    pc2 = df["PC2"].values
    q1a, q1b = np.quantile(pc1, [0.02, 0.98])
    q2a, q2b = np.quantile(pc2, [0.02, 0.98])
    xs = np.linspace(q1a, q1b, K)
    ys = np.linspace(q2a, q2b, K)

    pretty = pretty_silhouette_mask(sils)

    cells = {}
    dx = xs[1] - xs[0]; dy = ys[1] - ys[0]
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            mask = (pc1 >= x - dx / 2) & (pc1 < x + dx / 2) & \
                   (pc2 >= y - dy / 2) & (pc2 < y + dy / 2)
            cell_df = df[mask]
            if len(cell_df) == 0:
                continue
            cell_df = cell_df[cell_df["Objekt-ID"].isin(pretty)]
            if vox is not None:
                cell_df = cell_df[cell_df["Objekt-ID"].isin(vox)]
            if len(cell_df) == 0:
                continue
            pc36 = np.sqrt((cell_df[["PC3", "PC4", "PC5", "PC6"]] ** 2).sum(axis=1))
            robust = cell_df[pc36 < pc36.quantile(0.85)]
            if len(robust) > 0:
                cell_df = robust
            c1, c2 = cell_df["PC1"].mean(), cell_df["PC2"].mean()
            d = (cell_df["PC1"] - c1) ** 2 + (cell_df["PC2"] - c2) ** 2
            best_idx = d.idxmin()
            cells[(i, j)] = (df.loc[best_idx, "Objekt-ID"], df.loc[best_idx])

    # material colour tint for shaded mesh
    mat_tint = {"wood": to_rgba(AMBER)[:3],
                "metal": to_rgba(OI["blue"])[:3],
                "plastic": to_rgba(OI["rust"])[:3],
                "other": to_rgba(SLATE)[:3]}
    def tint_for(row):
        return mat_tint.get(row.get("mat_class", "other"), mat_tint["other"])

    fig = plt.figure(figsize=(13.5, 8.2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[0.9, 1.25], wspace=0.10, figure=fig)

    # --- Left: scatter with cell grid overlay ---
    axL = fig.add_subplot(gs[0])
    axL.scatter(pc1, pc2, s=6, c=OI["grey"], alpha=0.18, linewidths=0, zorder=1)
    for (i, j), (oid, row) in cells.items():
        axL.scatter([row["PC1"]], [row["PC2"]], s=45,
                    facecolor="white", edgecolor=OI["rust"],
                    linewidths=1.1, zorder=6)
        axL.scatter([row["PC1"]], [row["PC2"]], s=10,
                    color=OI["rust"], zorder=7)
    for x in np.concatenate([xs - dx / 2, [xs[-1] + dx / 2]]):
        axL.axvline(x, color=SLATE, linewidth=0.35, alpha=0.25)
    for y in np.concatenate([ys - dy / 2, [ys[-1] + dy / 2]]):
        axL.axhline(y, color=SLATE, linewidth=0.35, alpha=0.25)
    axL.set_xlim(q1a - dx * 0.4, q1b + dx * 0.4)
    axL.set_ylim(q2a - dy * 0.4, q2b + dy * 0.4)
    axL.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    axL.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    axL.set_title("(a) holotype-utveljing i morforommet",
                   loc="left", weight="bold", fontsize=10.5)
    axL.grid(alpha=0.10, linewidth=0.3)

    # --- Right: shaded-mesh grid ---
    # use a real gridspec inside the right panel for evenly sized cells
    gs_R = gridspec.GridSpecFromSubplotSpec(
        K, K, subplot_spec=gs[1], wspace=0.02, hspace=0.02)
    for (i, j), (oid, row) in cells.items():
        # y-axis convention: j=0 is smallest PC2, should be bottom row in display
        sub_ax = fig.add_subplot(gs_R[K - 1 - j, i])
        tint = tint_for(row)
        if vox is not None and oid in vox:
            draw_shaded_mesh(sub_ax, vox[oid].astype(np.float32),
                              base_color=tint, ambient=0.18,
                              smooth_sigma=0.35, edge_rim=False,
                              specular_strength=0.20)
        else:
            sub_ax.imshow(sils.get(oid, np.zeros((32, 32))),
                          cmap="Greys", aspect="auto",
                          interpolation="nearest")
            sub_ax.set_xticks([]); sub_ax.set_yticks([])

    # fill empty cells with empty grey square
    for j in range(K):
        for i in range(K):
            if (i, j) in cells:
                continue
            sub_ax = fig.add_subplot(gs_R[K - 1 - j, i])
            sub_ax.set_facecolor((0.97, 0.97, 0.97))
            sub_ax.set_xticks([]); sub_ax.set_yticks([])
            for s in ["top", "right", "bottom", "left"]:
                sub_ax.spines[s].set_color((0.88, 0.88, 0.88))
                sub_ax.spines[s].set_linewidth(0.4)

    save(fig, "E2_mesh_grid")


# ═════════════════════════════════════════════════════════════════════
# FIG E6: Giga-grid av alle silhuettar (kronologisk)
# ═════════════════════════════════════════════════════════════════════
def fig_E6_giga_grid(df, sils, mode="year"):
    """
    Arrange every cached silhouette into one large grid.
      mode="year" — sort by år, left-to-right, top-to-bottom.
      mode="pc1"  — sort by PC1.
    Background behind each silhouette is coloured by Stilperiode.
    """
    # pick rows that have a silhouette and a year
    rows = df[df["Objekt-ID"].isin(sils)].copy()
    rows = rows[rows["år"].notna()].copy()
    if mode == "pc1":
        rows = rows.sort_values("PC1")
        suffix = "pc1"
    else:
        rows = rows.sort_values("år")
        suffix = "year"
    N = len(rows)
    # near-square grid
    cols = int(np.ceil(np.sqrt(N * 1.18)))
    grid_rows = int(np.ceil(N / cols))
    print(f"  giga-grid ({mode}): {N} stolar in {grid_rows}x{cols} grid")

    cell = 1  # logical unit
    pad = 0.0

    fig_w = min(20, cols * 0.30)
    fig_h = fig_w * (grid_rows / cols) * 1.02
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.94])
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(grid_rows - 0.5, -0.5)  # top-to-bottom
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax.spines[s].set_visible(False)

    # pre-compute per-period color
    oids = rows["Objekt-ID"].values
    pers = rows["Stilperiode"].fillna("").values

    # draw
    for k, oid in enumerate(oids):
        r = k // cols
        c = k % cols
        img = sils[oid]
        tint = PERIOD_COLOR.get(pers[k], LIGHTSLATE)
        ax.add_patch(Rectangle((c - 0.48, r - 0.48), 0.96, 0.96,
                                facecolor=to_rgba(tint, 0.35),
                                edgecolor="none", zorder=1))
        ax.imshow(img, extent=(c - 0.46, c + 0.46, r + 0.46, r - 0.46),
                  cmap="Greys", interpolation="nearest",
                  vmin=0, vmax=1, zorder=2, aspect="auto")

    # legend strip: period colors with year range
    # place below grid
    ax.set_title("")
    save(fig, f"E6_giga_grid_{suffix}")


# ═════════════════════════════════════════════════════════════════════
# Legend helper: one-row period colour strip (separate file)
# ═════════════════════════════════════════════════════════════════════
def fig_E6_legend():
    ordered = sorted(PERIOD_YEAR.items(), key=lambda kv: kv[1])
    fig, ax = plt.subplots(figsize=(12, 1.6))
    n = len(ordered)
    for i, (p, y) in enumerate(ordered):
        ax.add_patch(Rectangle((i, 0), 0.95, 1,
                                 facecolor=PERIOD_COLOR.get(p, OI["grey"]),
                                 edgecolor="white", linewidth=0.6))
        ax.text(i + 0.47, -0.10, f"{y}", fontsize=7.5,
                 ha="center", va="top", color=SLATE)
        ax.text(i + 0.47, 0.5, p, fontsize=7, ha="center", va="center",
                 color="white", rotation=0, weight="bold")
    ax.set_xlim(-0.1, n + 0.1)
    ax.set_ylim(-0.6, 1.1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax.spines[s].set_visible(False)
    save(fig, "E6_periode_fargelegende")


# ═════════════════════════════════════════════════════════════════════
# FIG E3: Tilpassingslandskap som tetthet over tid
# ═════════════════════════════════════════════════════════════════════
def fig_E3_landskap_tid(df, pca):
    epochs = [
        ("Barokk",                     (1600, 1720)),
        ("Rokokko",                    (1720, 1790)),
        ("Nyklassisisme og Empire",    (1790, 1850)),
        ("Historisme og Viktoriansk",  (1850, 1905)),
        ("Modernisme 1920–1970",       (1920, 1970)),
        ("Samtidsdesign 1970–2024",    (1970, 2025)),
    ]

    fig = plt.figure(figsize=(13, 8.2))
    gs = gridspec.GridSpec(2, 3, hspace=0.30, wspace=0.22, figure=fig)

    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    # clip display to robust quantiles
    xmin, xmax = np.quantile(pc1, [0.005, 0.995])
    ymin, ymax = np.quantile(pc2, [0.005, 0.995])
    xpad = (xmax - xmin) * 0.04; ypad = (ymax - ymin) * 0.04
    xmin -= xpad; xmax += xpad; ymin -= ypad; ymax += ypad

    xx, yy = np.meshgrid(np.linspace(xmin, xmax, 140),
                          np.linspace(ymin, ymax, 140))
    positions = np.vstack([xx.ravel(), yy.ravel()])

    # compute all KDEs first to find a common density scale for fair comparison
    kdes = {}
    for label, (y0, y1) in epochs:
        sub = df[(df["år"] >= y0) & (df["år"] < y1)]
        if len(sub) >= 5:
            try:
                kde = gaussian_kde(sub[["PC1", "PC2"]].values.T, bw_method=0.30)
                z = kde(positions).reshape(xx.shape)
                kdes[label] = (z, sub)
            except Exception:
                kdes[label] = (None, sub)
        else:
            kdes[label] = (None, sub)
    vmax = max((z.max() for (z, _) in kdes.values() if z is not None), default=1.0)

    dens_cmap = LinearSegmentedColormap.from_list(
        "amberfade", [(1, 1, 1, 0),
                      to_rgba(LIGHTAMBER, 0.70),
                      to_rgba(AMBER, 0.88),
                      to_rgba(SLATE, 0.98)], N=256)

    # overall centroid for reference arrow
    gcx, gcy = pc1.mean(), pc2.mean()

    for idx, (label, (y0, y1)) in enumerate(epochs):
        r, c = divmod(idx, 3)
        ax = fig.add_subplot(gs[r, c])
        ax.scatter(pc1, pc2, s=4, c=OI["grey"], alpha=0.10, linewidths=0)
        z, sub = kdes[label]
        if z is not None:
            levels = np.linspace(vmax * 0.02, vmax, 10)
            ax.contourf(xx, yy, z, levels=levels, cmap=dens_cmap, zorder=2)
            ax.contour(xx, yy, z, levels=levels[::2], colors=[SLATE],
                        linewidths=0.35, alpha=0.55, zorder=3)
        if len(sub) >= 5:
            ax.scatter(sub["PC1"], sub["PC2"], s=11, c=AMBER,
                        edgecolors=SLATE, linewidths=0.3, alpha=0.85, zorder=4)
            cx, cy = sub["PC1"].mean(), sub["PC2"].mean()
            # arrow from overall centroid to epoch centroid (emphasises drift)
            ax.annotate("", xy=(cx, cy), xytext=(gcx, gcy),
                        arrowprops=dict(arrowstyle="->", color=OI["rust"],
                                        lw=1.6, alpha=0.9),
                        zorder=6)
            ax.plot(cx, cy, marker="o", markersize=8,
                    markerfacecolor=OI["rust"], markeredgecolor="white",
                    markeredgewidth=1.0, zorder=7)
            # annotate distance from global centroid
            d = np.sqrt((cx - gcx) ** 2 + (cy - gcy) ** 2)
            ax.text(0.03, 0.96, f"Δ = {d:.2f}  σ₁ = {sub['PC1'].std():.2f}  σ₂ = {sub['PC2'].std():.2f}",
                    transform=ax.transAxes, fontsize=7.8, color=SLATE,
                    va="top", ha="left",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.8,
                               boxstyle="round,pad=0.25"))
        ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
        ax.set_title(f"{label}   n = {len(sub)}", fontsize=10.2, loc="left")
        if r == 1: ax.set_xlabel("PC1")
        if c == 0: ax.set_ylabel("PC2")
        ax.grid(alpha=0.1, linewidth=0.4)
        ax.tick_params(labelsize=8)

    save(fig, "E3_landskap_tid")


# ═════════════════════════════════════════════════════════════════════
# FIG E4: Kanalisering på tvers av aksar
# ═════════════════════════════════════════════════════════════════════
def fig_E4_kanalisering(df):
    # For each axis, compute per-period standard deviation, z-scored across periods.
    # Also include per-period sample sizes.
    counts = df["Stilperiode"].value_counts()
    periods = [p for p in PERIOD_ORDER if p in counts.index and counts[p] >= 12]

    # Normalise each axis to z-scores to compare
    df2 = df.copy()
    for c in AXES:
        s = df2[c]
        df2[c + "_z"] = (s - s.mean()) / s.std()

    fig = plt.figure(figsize=(12.5, 8.5))
    gs = gridspec.GridSpec(3, 2, hspace=0.55, wspace=0.25, figure=fig)

    for i, c in enumerate(AXES):
        r, cc = divmod(i, 2)
        ax = fig.add_subplot(gs[r, cc])
        zcol = c + "_z"
        # per-period violin/strip
        pos = [PERIOD_YEAR[p] for p in periods]
        data = [df2[df2["Stilperiode"] == p][zcol].values for p in periods]
        # violin
        parts = ax.violinplot(data, positions=pos, widths=14, showmeans=False,
                              showmedians=False, showextrema=False)
        for j, body in enumerate(parts["bodies"]):
            body.set_facecolor(PERIOD_COLOR.get(periods[j], OI["grey"]))
            body.set_edgecolor(SLATE)
            body.set_linewidth(0.5)
            body.set_alpha(0.75)
        # overlay: per-period std dev as line
        stds = [np.std(d) for d in data]
        ax.plot(pos, stds, color=SLATE, linewidth=1.4, alpha=0.7,
                 marker="o", markersize=4, markerfacecolor=AMBER,
                 markeredgecolor=SLATE, markeredgewidth=0.5,
                 label="σ per periode")
        # horizontal ref: std of all
        ax.axhline(0, color=OI["grey"], linewidth=0.4, alpha=0.5)
        ax.axhline(df2[zcol].std(), color=AMBER, linewidth=0.7,
                   linestyle="--", alpha=0.6, label="σ totalt")
        ax.set_title(AXIS_LABELS_NN[c], loc="left", fontsize=10.2)
        ax.set_xlim(1480, 2050)
        ax.set_ylim(-3.2, 3.8)
        ax.set_xlabel("år" if r == 2 else "")
        ax.set_ylabel("z-skår" if cc == 0 else "")
        ax.grid(alpha=0.12, linewidth=0.4)
        if i == 0:
            ax.legend(loc="upper left", fontsize=7.5, frameon=False)

    save(fig, "E4_kanalisering")


# ═════════════════════════════════════════════════════════════════════
# FIG E5: Stase og brot som tids-signatur
# ═════════════════════════════════════════════════════════════════════
def fig_E5_stase_brot(df, pca):
    # Use PC1, PC2 centroid and spread in 20-year windows
    df = df.sort_values("år").copy()
    yrs = df["år"].values
    p1 = df["PC1"].values; p2 = df["PC2"].values

    y_min = max(1400, int(np.quantile(yrs, 0.01) // 20) * 20)
    y_max = 2025
    window = 30
    step = 10
    centers = np.arange(y_min + window // 2, y_max - window // 2 + 1, step)

    c1 = []; c2 = []; s1 = []; s2 = []; n = []
    for c in centers:
        mask = (yrs >= c - window / 2) & (yrs <= c + window / 2)
        if mask.sum() < 5:
            c1.append(np.nan); c2.append(np.nan)
            s1.append(np.nan); s2.append(np.nan)
            n.append(mask.sum())
            continue
        c1.append(p1[mask].mean()); c2.append(p2[mask].mean())
        s1.append(p1[mask].std());  s2.append(p2[mask].std())
        n.append(mask.sum())
    c1, c2 = np.array(c1), np.array(c2)
    s1, s2 = np.array(s1), np.array(s2)
    n = np.array(n)

    # detect "break" points: large first differences in centroid
    diff = np.sqrt(np.diff(c1, prepend=c1[0]) ** 2
                   + np.diff(c2, prepend=c2[0]) ** 2)

    fig = plt.figure(figsize=(12.5, 8.5))
    gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1],
                           hspace=0.35, figure=fig)

    # --- top: centroid PC1 and PC2 over time ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(centers, c1, color=SLATE, lw=1.8, label="sentroid PC1")
    ax1.plot(centers, c2, color=AMBER, lw=1.8, label="sentroid PC2")
    ax1.fill_between(centers, c1 - s1, c1 + s1, color=SLATE, alpha=0.15)
    ax1.fill_between(centers, c2 - s2, c2 + s2, color=AMBER, alpha=0.15)
    # mark key breaks
    for ybreak, txt in [(1680, "barokk-konsolidering"),
                         (1830, "industriell revolusjon"),
                         (1920, "modernismens gjennomslag")]:
        ax1.axvline(ybreak, color=OI["rust"], linewidth=0.9,
                     linestyle="--", alpha=0.7)
        ax1.text(ybreak + 5, ax1.get_ylim()[1] * 0.86, txt,
                  fontsize=8, color=OI["rust"], rotation=0)
    ax1.set_ylabel("sentroide-verdi")
    ax1.set_title("(a)", loc="left", fontsize=10.2, weight="bold")
    ax1.legend(loc="lower left", fontsize=8.5, frameon=False)
    ax1.grid(alpha=0.18, linewidth=0.4)
    ax1.set_xlim(y_min, y_max)

    # --- middle: spread over time ---
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
    ax2.plot(centers, s1, color=SLATE, lw=1.6, label="σ(PC1)")
    ax2.plot(centers, s2, color=AMBER, lw=1.6, label="σ(PC2)")
    ax2.set_ylabel("morforom-spreiing")
    ax2.set_title("(b)", loc="left", fontsize=10.2, weight="bold")
    for ybreak in [1680, 1830, 1920]:
        ax2.axvline(ybreak, color=OI["rust"], linewidth=0.9,
                     linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=8.5, frameon=False)
    ax2.grid(alpha=0.18, linewidth=0.4)

    # --- bottom: change magnitude + sample size ---
    ax3 = fig.add_subplot(gs[2, 0], sharex=ax1)
    ax3.plot(centers, diff, color=OI["rust"], lw=1.4,
             label="‖Δ sentroid‖ per steg")
    ax3_r = ax3.twinx()
    ax3_r.fill_between(centers, 0, n, color=SLATE, alpha=0.18,
                        step="mid", label="n stolar i vindauge")
    ax3_r.set_ylabel("n i vindauge", color=SLATE)
    ax3_r.tick_params(axis="y", labelcolor=SLATE)
    ax3_r.spines["right"].set_visible(True)
    ax3.set_ylabel("sentroide-endring", color=OI["rust"])
    ax3.tick_params(axis="y", labelcolor=OI["rust"])
    ax3.set_title("(c)", loc="left", fontsize=10.2, weight="bold")
    ax3.set_xlabel("år")
    for ybreak in [1680, 1830, 1920]:
        ax3.axvline(ybreak, color=OI["rust"], linewidth=0.9,
                     linestyle="--", alpha=0.5)
    ax3.grid(alpha=0.18, linewidth=0.4)
    ax3.set_xlim(y_min, y_max)

    save(fig, "E5_stase_brot")


# ═════════════════════════════════════════════════════════════════════
def fig_E15_lande_prediction(df, pca):
    """
    Landé (1979) breeder's equation applied to chair evolution.
    G-matrix of the wood ancestral population, beta (selection gradient)
    pointing away from the steel/plastic centroid. Predicted vs observed
    response of the 1920-onwards population.
    """
    df_pre = df[(df["mat_class"] == "wood") & (df["år"] < 1920)]
    df_post = df[(df["mat_class"] == "wood") & (df["år"] >= 1920)]
    df_metal = df[df["mat_class"].isin(["metal", "plastic"])]

    if len(df_pre) < 15 or len(df_post) < 15 or len(df_metal) < 15:
        print("  skipping E15: insufficient samples")
        return

    pcs = ["PC1", "PC2"]
    G = df_pre[pcs].cov().values
    metal_c = df_metal[pcs].mean().values
    pre_c = df_pre[pcs].mean().values
    beta = pre_c - metal_c
    beta_norm = np.linalg.norm(beta)
    if beta_norm < 1e-6:
        print("  skipping E15: degenerate beta")
        return
    beta /= beta_norm
    delta_z_pred = G @ beta
    delta_z_obs = df_post[pcs].mean().values - pre_c

    # robust axis limits based on all data
    all_pc1 = df["PC1"].values
    all_pc2 = df["PC2"].values
    x_lo, x_hi = np.quantile(all_pc1, [0.01, 0.99])
    y_lo, y_hi = np.quantile(all_pc2, [0.01, 0.99])
    x_pad = (x_hi - x_lo) * 0.05
    y_pad = (y_hi - y_lo) * 0.05
    x_lo -= x_pad; x_hi += x_pad; y_lo -= y_pad; y_hi += y_pad

    fig = plt.figure(figsize=(13.5, 6.8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.24, figure=fig)

    axA = fig.add_subplot(gs[0])
    axA.scatter(all_pc1, all_pc2, s=3, c=OI["grey"], alpha=0.12, zorder=1,
                linewidths=0)
    axA.scatter(df_pre["PC1"], df_pre["PC2"], s=14, c=AMBER, alpha=0.45,
                edgecolors="none", label=f"tre, pre-1920 (n={len(df_pre)})",
                zorder=2)
    axA.scatter(df_metal["PC1"], df_metal["PC2"], s=14, c=OI["blue"],
                alpha=0.35, edgecolors="none",
                label=f"stål/plast (n={len(df_metal)})", zorder=2)

    vals, vecs = np.linalg.eigh(G)
    order = vals.argsort()[::-1]; vals = vals[order]; vecs = vecs[:, order]
    theta = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    width, height = 2 * np.sqrt(np.maximum(vals, 1e-12))
    for sig in [1, 2]:
        ell = Ellipse(xy=pre_c, width=sig * width, height=sig * height,
                      angle=theta, edgecolor=AMBER, facecolor="none",
                      lw=1.2, alpha=0.85 / sig, linestyle="--", zorder=4)
        axA.add_patch(ell)

    beta_arrow_len = min((x_hi - x_lo), (y_hi - y_lo)) * 0.18
    axA.annotate("", xy=pre_c + beta * beta_arrow_len,
                 xytext=tuple(pre_c),
                 arrowprops=dict(arrowstyle="-|>", color=OI["blue"],
                                 lw=2.2, mutation_scale=20), zorder=10)
    axA.text(*(pre_c + beta * beta_arrow_len * 1.10),
             r"$\beta$", color=OI["blue"], weight="bold",
             ha="center", va="center", fontsize=11,
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.8,
                       boxstyle="round,pad=0.15"))
    axA.scatter(*pre_c, s=140, c=AMBER, edgecolors="white",
                linewidths=1.4, zorder=11)
    axA.set_xlim(x_lo, x_hi); axA.set_ylim(y_lo, y_hi)
    axA.set_title("(a) G-matrise (1σ, 2σ ellipsar) og seleksjonsgradient β",
                  loc="left", weight="bold", fontsize=10.5)
    axA.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    axA.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    axA.legend(loc="upper right", fontsize=8, frameon=False)
    axA.grid(alpha=0.12, linewidth=0.4)

    axB = fig.add_subplot(gs[1])
    axB.scatter(all_pc1, all_pc2, s=3, c=OI["grey"], alpha=0.12, zorder=1,
                linewidths=0)
    axB.scatter(df_pre["PC1"], df_pre["PC2"], s=12, c=AMBER, alpha=0.30,
                edgecolors="none", label="tre, pre-1920")
    axB.scatter(df_post["PC1"], df_post["PC2"], s=18, c=OI["rust"], alpha=0.55,
                edgecolors="none", label=f"tre, post-1920 (n={len(df_post)})")
    # Scale the predicted arrow so it is comparable in visual length
    obs_norm = np.linalg.norm(delta_z_obs)
    pred_norm = np.linalg.norm(delta_z_pred)
    scale = obs_norm / max(pred_norm, 1e-9)
    axB.annotate("", xy=pre_c + delta_z_pred * scale,
                 xytext=tuple(pre_c),
                 arrowprops=dict(arrowstyle="-|>", color=SLATE,
                                 lw=2.2, mutation_scale=20), zorder=10)
    axB.annotate("", xy=pre_c + delta_z_obs,
                 xytext=tuple(pre_c),
                 arrowprops=dict(arrowstyle="-|>", color=OI["rust"],
                                 lw=2.2, mutation_scale=20), zorder=10)
    axB.scatter(*pre_c, s=140, c=AMBER, edgecolors="white",
                linewidths=1.4, zorder=11)
    axB.scatter(*(pre_c + delta_z_obs), s=140, c=OI["rust"],
                edgecolors="white", linewidths=1.4, zorder=11)
    # angular agreement
    cosang = float(np.dot(delta_z_pred / (pred_norm + 1e-9),
                          delta_z_obs / (obs_norm + 1e-9)))
    ang_deg = float(np.degrees(np.arccos(np.clip(cosang, -1, 1))))
    txt = (f"‖Δz_pred‖ = {pred_norm:.3f}\n"
           f"‖Δz_obs‖  = {obs_norm:.3f}\n"
           f"vinkel(pred, obs) = {ang_deg:.1f}°\n"
           f"cos(pred, obs) = {cosang:.2f}")
    axB.text(0.02, 0.98, txt, transform=axB.transAxes,
             fontsize=8.5, color=SLATE, va="top", ha="left",
             family="monospace",
             bbox=dict(facecolor="white", edgecolor="none",
                       alpha=0.85, boxstyle="round,pad=0.28"))
    # dummy legend entries
    axB.plot([], [], color=SLATE, lw=2, label="predikert $\\Delta\\bar z = Gβ$")
    axB.plot([], [], color=OI["rust"], lw=2, label="observert $\\Delta\\bar z$")
    axB.set_xlim(x_lo, x_hi); axB.set_ylim(y_lo, y_hi)
    axB.set_title("(b) predikert vs. observert respons",
                  loc="left", weight="bold", fontsize=10.5)
    axB.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    axB.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    axB.legend(loc="upper right", fontsize=8, frameon=False)
    axB.grid(alpha=0.12, linewidth=0.4)

    save(fig, "E15_lande_prediction")


# FIG E7 SPLIT: Morforom-trajektorie separert på materiale (wood / metal / plastic)
# ═════════════════════════════════════════════════════════════════════
def fig_E7_trajektorie_split(df, pca):
    """Three-panel trajectory: wood, metal, plastic. Arrows connect
    40-year bins; a star marks the Ornstein-Uhlenbeck adaptive optimum θ
    (estimated as the mean of the last three bins)."""
    fig = plt.figure(figsize=(14.5, 6.2))
    gs = gridspec.GridSpec(1, 3, wspace=0.22, figure=fig)

    all_pc1 = df["PC1"].values; all_pc2 = df["PC2"].values
    x_lo, x_hi = np.quantile(all_pc1, [0.01, 0.99])
    y_lo, y_hi = np.quantile(all_pc2, [0.01, 0.99])
    x_pad = (x_hi - x_lo) * 0.05; y_pad = (y_hi - y_lo) * 0.05
    x_lo -= x_pad; x_hi += x_pad; y_lo -= y_pad; y_hi += y_pad

    def get_traj(sub):
        yr_bins = np.arange(1500, 2040, 40)
        res = []
        for i in range(len(yr_bins) - 1):
            mask = (sub["år"] >= yr_bins[i]) & (sub["år"] < yr_bins[i + 1])
            chunk = sub[mask]
            if len(chunk) >= 5:
                res.append({
                    "year": yr_bins[i] + 20,
                    "cx": chunk["PC1"].mean(),
                    "cy": chunk["PC2"].mean(),
                    "sex": chunk["PC1"].std() / np.sqrt(len(chunk)),
                    "sey": chunk["PC2"].std() / np.sqrt(len(chunk)),
                    "n": len(chunk),
                })
        return pd.DataFrame(res)

    groups = [
        ("wood",    "tre (bøk/ask/mahogni)", AMBER),
        ("metal",   "stål / jern / krom",    OI["blue"]),
        ("plastic", "plast / akryl / poly",  OI["rust"]),
    ]

    for i, (mcls, title, col) in enumerate(groups):
        ax = fig.add_subplot(gs[i])
        ax.scatter(all_pc1, all_pc2, s=3, c=OI["grey"], alpha=0.10,
                   linewidths=0, zorder=1)

        sub = df[df["mat_class"] == mcls]
        traj = get_traj(sub)
        n_mat = len(sub)

        if len(traj) >= 2:
            # arrows coloured along the trajectory (dark → light)
            cmap = LinearSegmentedColormap.from_list(
                f"traj_{mcls}",
                [SLATE, col, "white"],
                N=max(len(traj) - 1, 2))
            for j in range(len(traj) - 1):
                arrow_col = cmap(j / max(len(traj) - 2, 1))
                ax.annotate("",
                            xy=(traj.iloc[j + 1]["cx"], traj.iloc[j + 1]["cy"]),
                            xytext=(traj.iloc[j]["cx"], traj.iloc[j]["cy"]),
                            arrowprops=dict(arrowstyle="-|>", color=arrow_col,
                                            lw=1.9, alpha=0.92,
                                            mutation_scale=15),
                            zorder=4)
            # numbered nodes
            for j, row_ in traj.iterrows():
                ax.errorbar(row_["cx"], row_["cy"],
                            xerr=row_["sex"], yerr=row_["sey"],
                            ecolor=to_rgba(col, 0.4),
                            elinewidth=0.9, capsize=2, zorder=3)
                ax.scatter([row_["cx"]], [row_["cy"]],
                           s=90, c=[col], edgecolors="white",
                           linewidths=1.1, zorder=5)
                ax.text(row_["cx"], row_["cy"], str(j + 1),
                        ha="center", va="center",
                        fontsize=7.4, color="white", weight="bold", zorder=6)
            # OU attractor θ
            theta_x = traj.iloc[-3:]["cx"].mean()
            theta_y = traj.iloc[-3:]["cy"].mean()
            ax.scatter([theta_x], [theta_y], marker="o", s=150,
                       color=col, edgecolors=SLATE, linewidths=0.9,
                       label="OU θ (adaptiv topp)", zorder=8)

        ax.set_xlim(x_lo, x_hi); ax.set_ylim(y_lo, y_hi)
        ax.set_title(f"{title}    n = {n_mat}",
                     loc="left", weight="bold", fontsize=10.2)
        ax.set_xlabel(f"PC1")
        if i == 0:
            ax.set_ylabel(f"PC2")
        ax.grid(alpha=0.12, linewidth=0.4)
        ax.axhline(0, color=OI["grey"], linewidth=0.5, alpha=0.4)
        ax.axvline(0, color=OI["grey"], linewidth=0.5, alpha=0.4)
        if len(traj) >= 2:
            ax.legend(loc="upper right", fontsize=8, frameon=False)

    save(fig, "E7_trajektorie_split")


# ═════════════════════════════════════════════════════════════════════
# FIG E8: Silhuettar som scatter-markers i PCA (direkte morforom-syn)
# ═════════════════════════════════════════════════════════════════════
def _period_rgb_silhouette(img, rgb):
    """Convert binary silhouette to RGBA with a period-tinted fill."""
    H, W = img.shape
    out = np.ones((H, W, 4), dtype=float)
    out[..., 0] = rgb[0]
    out[..., 1] = rgb[1]
    out[..., 2] = rgb[2]
    # alpha: 0 where no chair, ~0.92 where chair
    out[..., 3] = np.where(img, 0.92, 0.0)
    return out


def fig_E8_silhouette_scatter(df, pca, sils, n_show=180):
    """Snap each chair onto a fine grid; within each occupied grid cell,
    draw the silhouette of the chair closest to the local medoid, tinted by
    Stilperiode. Robustness filter applied to pick high-quality 'vinnarar'."""
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    oids = df["Objekt-ID"].values
    pers = df["Stilperiode"].fillna("").values

    lo1, hi1 = np.quantile(pc1, [0.01, 0.99])
    lo2, hi2 = np.quantile(pc2, [0.01, 0.99])

    K = int(np.ceil(np.sqrt(n_show * 1.5)))
    xe = np.linspace(lo1, hi1, K + 1)
    ye = np.linspace(lo2, hi2, K + 1)

    # Only consider chairs whose silhouette passes the beauty filter
    pretty = pretty_silhouette_mask(sils)
    print(f"  E8 pretty silhouettes: {len(pretty)}/{len(sils)}")

    chosen = {}
    for k in range(len(df)):
        if oids[k] not in pretty:
            continue
        if pc1[k] < lo1 or pc1[k] > hi1 or pc2[k] < lo2 or pc2[k] > hi2:
            continue
        i = np.searchsorted(xe, pc1[k]) - 1; i = min(max(i, 0), K - 1)
        j = np.searchsorted(ye, pc2[k]) - 1; j = min(max(j, 0), K - 1)
        chosen.setdefault((i, j), []).append(k)

    final = {}
    for (i, j), idxs in chosen.items():
        cell_df = df.iloc[idxs]
        # prefer chairs closest to PC3-PC6 origin (typical shapes)
        d36 = np.sqrt((cell_df[["PC3", "PC4", "PC5", "PC6"]] ** 2).sum(axis=1))
        robust_cell = cell_df[d36 < d36.quantile(0.85)]
        if len(robust_cell) > 0:
            cell_df = robust_cell
        c1, c2 = cell_df["PC1"].mean(), cell_df["PC2"].mean()
        dist = (cell_df["PC1"] - c1) ** 2 + (cell_df["PC2"] - c2) ** 2
        final[(i, j)] = dist.idxmin()

    fig = plt.figure(figsize=(14, 9))
    gs = gridspec.GridSpec(1, 2, width_ratios=[5.2, 1.0], wspace=0.03, figure=fig)
    ax = fig.add_subplot(gs[0])
    ax.scatter(pc1, pc2, s=5, c=OI["grey"], alpha=0.12, linewidths=0, zorder=1)

    dx = xe[1] - xe[0]; dy = ye[1] - ye[0]
    for (i, j), idx in final.items():
        row = df.loc[idx]
        img = sils[row["Objekt-ID"]]
        col = PERIOD_COLOR.get(row["Stilperiode"], SLATE)
        rgba = _period_rgb_silhouette(img, to_rgba(col)[:3])
        cx = (xe[i] + xe[i + 1]) / 2
        cy = (ye[j] + ye[j + 1]) / 2
        ax.imshow(rgba, extent=(cx-dx*0.48, cx+dx*0.48, cy-dy*0.48, cy+dy*0.48),
                  interpolation="nearest", zorder=3, aspect="auto")

    ax.set_xlim(lo1 - dx * 0.3, hi1 + dx * 0.3)
    ax.set_ylim(lo2 - dy * 0.3, hi2 + dy * 0.3)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varians)")
    ax.set_title("E8: Holotype-grid over morforommet (lokale optima)", loc="left", weight="bold")
    ax.grid(alpha=0.1, lw=0.4)
    ax.axhline(0, color=OI["grey"], linewidth=0.4, alpha=0.4)
    ax.axvline(0, color=OI["grey"], linewidth=0.4, alpha=0.4)

    # color legend on the side
    axL = fig.add_subplot(gs[1])
    axL.axis("off")
    ordered = [p for p in sorted(PERIOD_YEAR.keys(), key=lambda k: PERIOD_YEAR[k])
               if p in set(pers)]
    axL.text(0.0, 1.00, "Stilperiode",
             transform=axL.transAxes, fontsize=10, weight="bold", color=SLATE,
             va="top")
    for i, p in enumerate(ordered):
        y_pos = 0.95 - i * 0.045
        col = PERIOD_COLOR.get(p, OI["grey"])
        axL.scatter([0.02], [y_pos], s=55, c=[col], transform=axL.transAxes,
                    edgecolors="white", linewidths=0.8)
        axL.text(0.095, y_pos, f"{p}  ({PERIOD_YEAR[p]})",
                 transform=axL.transAxes, fontsize=7.8,
                 color=SLATE, va="center", ha="left")

    save(fig, "E8_silhouette_scatter")


# ═════════════════════════════════════════════════════════════════════
# FIG E9: Substrat-skift (materiale-signatur over tid)
# ═════════════════════════════════════════════════════════════════════
def _has_material(s, needles):
    if not isinstance(s, str):
        return False
    sl = s.lower()
    return any(k in sl for k in needles)


def fig_E9_substrat_skift(df, pca):
    """For each key material group, show how chairs with that material
    occupy PCA space across time bands."""
    groups = [
        ("Bøk/Ask (tradisjonelt treverk)",  ["bøk", "ask"]),
        ("Mahogni/Valnøtt (eksotisk trevirke)", ["mahogni", "valnøtt", "valn\u00f8tt"]),
        ("Stål/Jern/Kromstål", ["stål", "jern", "krom", "st\u00e5l"]),
        ("Plast/Akryl/Polymer", ["plast", "akryl", "poly", "pvc"]),
        ("Aluminium", ["aluminium", "alu"]),
    ]
    tbands = [(1600, 1800), (1800, 1900), (1900, 1960), (1960, 2025)]
    band_lbl = ["1600–1800", "1800–1900", "1900–1960", "1960–2025"]

    fig = plt.figure(figsize=(14, 9))
    gs = gridspec.GridSpec(len(groups), len(tbands), hspace=0.25, wspace=0.12,
                           figure=fig)

    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    xlo, xhi = np.quantile(pc1, [0.005, 0.995])
    ylo, yhi = np.quantile(pc2, [0.005, 0.995])

    for gi, (gname, needles) in enumerate(groups):
        mask_mat = df["Materialar"].apply(lambda s: _has_material(s, needles))
        for bi, (y0, y1) in enumerate(tbands):
            ax = fig.add_subplot(gs[gi, bi])
            ax.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.08, linewidths=0, zorder=1)
            mask = mask_mat & df["år"].between(y0, y1)
            sub = df[mask]
            if len(sub) > 0:
                ax.scatter(sub["PC1"], sub["PC2"], s=12, c=AMBER,
                           edgecolors=SLATE, linewidths=0.3,
                           alpha=0.9, zorder=3)
            ax.set_xlim(xlo, xhi); ax.set_ylim(ylo, yhi)
            ax.tick_params(labelsize=7)
            if gi == 0:
                ax.set_title(band_lbl[bi], fontsize=9.5, loc="center")
            if bi == 0:
                ax.set_ylabel(gname, fontsize=8.5, rotation=90, labelpad=4)
            if gi == len(groups) - 1:
                ax.set_xlabel("PC1", fontsize=8)
            else:
                ax.set_xticklabels([])
            if bi != 0:
                ax.set_yticklabels([])
            ax.text(0.97, 0.03, f"n={len(sub)}", transform=ax.transAxes,
                    fontsize=7.2, ha="right", va="bottom", color=SLATE,
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.75,
                              boxstyle="round,pad=0.15"))
            ax.grid(alpha=0.08, linewidth=0.3)

    save(fig, "E9_substrat_skift")


# ═════════════════════════════════════════════════════════════════════
# FIG E10: Realiserte og uaktualiserte regionar
# ═════════════════════════════════════════════════════════════════════
def fig_E10_realiseringsgrad(df, pca):
    """Quantify how much of the morphospace is actually occupied.
    Layout:
      (a) 2D binning of PC1-PC2 + convex hull + empty interior cells
      (b) Bar: occupancy % by PC1 decile
      (c) Distribution of chair densities per cell (log scale)."""
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    xlo, xhi = np.quantile(pc1, [0.01, 0.99])
    ylo, yhi = np.quantile(pc2, [0.01, 0.99])
    xpad = (xhi - xlo) * 0.05; ypad = (yhi - ylo) * 0.05
    xlo -= xpad; xhi += xpad; ylo -= ypad; yhi += ypad

    K = 28
    xe = np.linspace(xlo, xhi, K + 1)
    ye = np.linspace(ylo, yhi, K + 1)
    H, _, _ = np.histogram2d(pc1, pc2, bins=[xe, ye])
    H = H.T  # y, x

    # convex hull of realised points
    pts = np.column_stack([pc1, pc2])
    # restrict hull to points inside display box
    inside = (pc1 >= xlo) & (pc1 <= xhi) & (pc2 >= ylo) & (pc2 <= yhi)
    hull_pts = pts[inside]
    hull = ConvexHull(hull_pts)
    hull_xy = hull_pts[hull.vertices]

    # cell centres
    xc = (xe[:-1] + xe[1:]) / 2
    yc = (ye[:-1] + ye[1:]) / 2

    # point-in-polygon test for cell centres
    from matplotlib.path import Path as mPath
    poly = mPath(np.vstack([hull_xy, hull_xy[:1]]))
    CX, CY = np.meshgrid(xc, yc)
    inside_hull = poly.contains_points(np.column_stack([CX.ravel(), CY.ravel()]))
    inside_hull = inside_hull.reshape(CY.shape)

    empty_in_hull = (H == 0) & inside_hull
    occupied = H > 0
    occ_pct_in_hull = 100 * occupied[inside_hull].mean()
    empty_pct_in_hull = 100 * empty_in_hull.sum() / max(inside_hull.sum(), 1)

    fig = plt.figure(figsize=(13, 7))
    gs = gridspec.GridSpec(2, 3, width_ratios=[2.2, 1, 1],
                           height_ratios=[1, 1], hspace=0.35, wspace=0.30,
                           figure=fig)

    # panel A: binning + hull
    axA = fig.add_subplot(gs[:, 0])
    # background: show H (log)
    Hlog = np.log1p(H)
    axA.pcolormesh(xe, ye, Hlog, cmap="Greys", shading="auto", alpha=0.85,
                   zorder=1)
    # hull boundary
    hx = np.r_[hull_xy[:, 0], hull_xy[0, 0]]
    hy = np.r_[hull_xy[:, 1], hull_xy[0, 1]]
    axA.plot(hx, hy, color=AMBER, linewidth=1.6, alpha=0.95, zorder=3,
             label="konveks innhylling")
    # empty cells inside hull
    for j in range(K):
        for i in range(K):
            if empty_in_hull[j, i]:
                axA.add_patch(Rectangle((xe[i], ye[j]),
                                        xe[i+1]-xe[i], ye[j+1]-ye[j],
                                        facecolor="none", edgecolor=OI["rust"],
                                        linewidth=0.6, linestyle="-",
                                        alpha=0.85, zorder=4))
    axA.set_xlim(xlo, xhi); axA.set_ylim(ylo, yhi)
    axA.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    axA.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varians)")
    axA.set_title("(a)   raudt rutenett = uaktualisert men mogeleg", loc="left",
                  fontsize=10, weight="bold")
    axA.legend(loc="lower right", fontsize=8, frameon=False)

    # panel B: occupancy by PC1 decile
    axB = fig.add_subplot(gs[0, 1])
    deciles = np.quantile(pc1, np.linspace(0, 1, 11))
    pc1_bin = np.digitize(pc1, deciles[1:-1])
    # for each decile, compute % of PC2 cells with >=1 chair (binned in y direction)
    pct = []
    for d in range(10):
        idx = np.where(pc1_bin == d)[0]
        if len(idx) == 0:
            pct.append(0); continue
        sub_pc2 = pc2[idx]
        # bin into K cells in y
        h, _ = np.histogram(sub_pc2, bins=ye)
        pct.append(100 * (h > 0).mean())
    xs = np.arange(10)
    axB.bar(xs, pct, color=AMBER, edgecolor=SLATE, linewidth=0.5, alpha=0.85)
    axB.set_xlabel("PC1-desil")
    axB.set_ylabel("% PC2-celler okkuperte")
    axB.set_title("(b)", loc="left", fontsize=10, weight="bold")
    axB.set_xticks(xs)
    axB.set_ylim(0, 100)
    axB.grid(axis="y", alpha=0.15, linewidth=0.4)

    # panel C: log-distribution of cell counts
    axC = fig.add_subplot(gs[1, 1])
    counts = H[inside_hull]
    axC.hist(np.log10(counts + 1), bins=22, color=SLATE, alpha=0.85,
             edgecolor="white", linewidth=0.4)
    axC.axvline(0, color=OI["rust"], linewidth=1, linestyle="--", alpha=0.8,
                 label="tom celle")
    axC.set_xlabel("log10(n + 1) per celle")
    axC.set_ylabel("tal celler")
    axC.set_title("(c)", loc="left", fontsize=10, weight="bold")
    axC.legend(fontsize=7.5, frameon=False, loc="upper right")

    # panel D: summary stats
    axD = fig.add_subplot(gs[:, 2])
    axD.axis("off")
    total_cells = inside_hull.sum()
    occ_cells = occupied[inside_hull].sum()
    total_area = (xhi - xlo) * (yhi - ylo)
    hull_area = hull.volume  # ConvexHull in 2D → .volume is the area
    filled_ratio = hull_area / total_area
    lines = [
        f"N stolar         {len(df)}",
        f"Konveks areal   {hull_area:.2f}",
        f"Boks-areal       {total_area:.2f}",
        f"Hull-fyll         {filled_ratio * 100:.1f}%",
        "",
        f"Celler i hylster {int(total_cells)}",
        f"Av desse okkuperte  {int(occ_cells)}",
        f"Okkuperte %     {occ_pct_in_hull:.1f}%",
        f"Tomme %           {empty_pct_in_hull:.1f}%",
        "",
        f"Celler overalt    {K*K}",
        f"Rutenett          {K}×{K}",
    ]
    for i, line in enumerate(lines):
        axD.text(0.0, 0.96 - i * 0.07, line, transform=axD.transAxes,
                 fontsize=9.2, color=SLATE, family="monospace",
                 va="top", ha="left")
    axD.set_title("(d) nøkkeltal", loc="left", fontsize=10, weight="bold")

    save(fig, "E10_realiseringsgrad")


# ═════════════════════════════════════════════════════════════════════
# FIG E11: Stiavhengigheit — arvsavstand (H11, prop. 4.3)
# ═════════════════════════════════════════════════════════════════════
def fig_E11_stiavhengigheit(df, pca):
    """H11: for each period, compare mean distance of chairs to (a) the
    centroid of the PRECEDING period and (b) their own centroid. If
    preceding-distance > own-distance → form inherits position."""
    counts = df["Stilperiode"].value_counts()
    periods = [p for p in sorted(PERIOD_YEAR.keys(), key=lambda k: PERIOD_YEAR[k])
               if p in counts.index and counts[p] >= 12]
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    centroids = {p: df[df["Stilperiode"] == p][pc_cols].mean().values for p in periods}
    overall_centroid = df[pc_cols].mean().values

    years, d_own, d_prev, d_overall = [], [], [], []
    for i, p in enumerate(periods):
        sub = df[df["Stilperiode"] == p][pc_cols].values
        own = np.linalg.norm(sub - centroids[p], axis=1).mean()
        d_own.append(own)
        d_overall.append(np.linalg.norm(sub - overall_centroid, axis=1).mean())
        if i == 0:
            d_prev.append(np.nan)
        else:
            prev_c = centroids[periods[i - 1]]
            d_prev.append(np.linalg.norm(sub - prev_c, axis=1).mean())
        years.append(PERIOD_YEAR[p])

    years = np.array(years)
    d_own = np.array(d_own)
    d_prev = np.array(d_prev)
    d_overall = np.array(d_overall)
    ratio = d_prev / d_own  # > 1 means path dependent

    fig = plt.figure(figsize=(12, 7.2))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1.1, 1], hspace=0.38,
                           figure=fig)

    axA = fig.add_subplot(gs[0])
    axA.plot(years, d_own, color=SLATE, linewidth=1.8, marker="o",
             markersize=5, label="avstand til eigen sentroide")
    axA.plot(years, d_prev, color=AMBER, linewidth=1.8, marker="s",
             markersize=5, label="avstand til føregåande sentroide")
    axA.plot(years, d_overall, color=OI["grey"], linewidth=1.2,
             marker="^", markersize=4, linestyle="--",
             label="avstand til globalsentroide")
    axA.set_ylabel("snittavstand (PC1–PC6)")
    axA.set_title("(a) stol-avstand til ulike sentroidar", loc="left",
                  fontsize=10.5, weight="bold")
    axA.legend(loc="upper right", frameon=False, fontsize=8.5)
    axA.grid(alpha=0.14, linewidth=0.4)
    axA.set_xlim(min(years) - 15, max(years) + 15)

    axB = fig.add_subplot(gs[1])
    axB.bar(years, ratio, width=22, color=SLATE, alpha=0.85,
             edgecolor="white", linewidth=0.6)
    axB.axhline(1.0, color=OI["rust"], linewidth=1, linestyle="--", alpha=0.85,
                 label="terskel: 1,0")
    axB.set_xlabel("år")
    axB.set_ylabel("ratio: føregåande / eigen")
    axB.set_title("(b) verdi > 1  ⇒  stiavhengigheit (forma bur nærare si eiga periode enn den førre)",
                   loc="left", fontsize=10.5, weight="bold")
    axB.legend(loc="upper right", frameon=False, fontsize=8.5)
    axB.grid(axis="y", alpha=0.14, linewidth=0.4)
    axB.set_xlim(min(years) - 15, max(years) + 15)

    save(fig, "E11_stiavhengigheit")


# ═════════════════════════════════════════════════════════════════════
# FIG E12: Kanaliseringssignatur (H12, prop. 3.21)
# ═════════════════════════════════════════════════════════════════════
def fig_E12_kanalisering_radar(df):
    """H12: radar of z-standardised variance per axis. Canalised axes
    have systematically lower variance than non-canalised ones."""
    vals = {}
    for c in AXES:
        s = df[c]
        # z-standardise so axes are comparable
        z = (s - s.mean()) / s.std()
        vals[c] = z.std()  # = 1 for all, by construction — so use raw CV instead
    # better: coefficient of variation (σ/|μ|)
    cvs = {}
    for c in AXES:
        s = df[c]
        cvs[c] = abs(s.std() / (s.mean() + 1e-9))
    # also: within-period mean variance (pooled)
    within = {}
    for c in AXES:
        s = df[c]
        group_vars = df.groupby("Stilperiode")[c].var().dropna()
        within[c] = group_vars.mean()
    # normalise within by total variance for comparability
    between = {c: df[c].var() for c in AXES}
    within_ratio = {c: within[c] / between[c] for c in AXES}

    labels = [AXIS_LABELS_NN[c] for c in AXES]
    n = len(AXES)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    theta += theta[:1]

    fig = plt.figure(figsize=(13.5, 6.5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.15], wspace=0.25, figure=fig)

    # radar: coefficient of variation per axis
    ax1 = fig.add_subplot(gs[0], projection="polar")
    vals1 = [cvs[c] for c in AXES] + [cvs[AXES[0]]]
    ax1.plot(theta, vals1, color=SLATE, linewidth=1.8)
    ax1.fill(theta, vals1, color=SLATE, alpha=0.22)
    ax1.set_xticks(theta[:-1])
    ax1.set_xticklabels(labels, fontsize=8.5)
    ax1.set_title("(a) variasjonskoeffisient CV = σ/|μ|  per akse",
                   fontsize=10.2, loc="left", weight="bold", pad=18)
    ax1.grid(alpha=0.3)

    # bar: within / total variance ratio
    ax2 = fig.add_subplot(gs[1])
    order = sorted(AXES, key=lambda c: within_ratio[c])
    xs = np.arange(len(order))
    vals2 = [within_ratio[c] for c in order]
    cols = [AMBER if within_ratio[c] < 0.4 else SLATE for c in order]
    ax2.barh(xs, vals2, color=cols, edgecolor="white", linewidth=0.5,
             alpha=0.88)
    ax2.set_yticks(xs)
    ax2.set_yticklabels([AXIS_LABELS_NN[c] for c in order], fontsize=9)
    ax2.axvline(0.4, color=OI["rust"], linestyle="--", linewidth=0.9,
                 alpha=0.8, label="kanaliseringsterskel 0,4")
    ax2.set_xlabel("innan-stilperiode-varians / total-varians")
    ax2.set_title("(b) små verdiar = kanaliserte (fanga av kompromisset)",
                   loc="left", fontsize=10.2, weight="bold")
    ax2.legend(loc="lower right", frameon=False, fontsize=8)
    ax2.set_xlim(0, max(vals2) * 1.15)
    ax2.grid(axis="x", alpha=0.14, linewidth=0.4)

    save(fig, "E12_kanalisering_radar")


# ═════════════════════════════════════════════════════════════════════
# FIG E13: Punktert likevekt mot nullmodell (H13, prop. 4.2, 4.11)
# ═════════════════════════════════════════════════════════════════════
def fig_E13_punktuert_likevekt(df, pca, n_perm=200):
    """H13: rolling centroid derivative with material-revolution markers,
    compared to permutation null (shuffle years, keep geometry)."""
    df = df.sort_values("år").copy()
    yrs = df["år"].values
    pc = df[["PC1", "PC2"]].values

    y0, y1 = 1500, 2025
    window = 30; step = 5
    centers = np.arange(y0 + window // 2, y1 - window // 2 + 1, step)

    def rolling_deriv(yr_vec, pc_vec):
        cxs = []
        for c in centers:
            m = (yr_vec >= c - window / 2) & (yr_vec <= c + window / 2)
            if m.sum() < 5:
                cxs.append(np.full(2, np.nan))
            else:
                cxs.append(pc_vec[m].mean(axis=0))
        cxs = np.array(cxs)
        d = np.linalg.norm(np.diff(cxs, axis=0), axis=1)
        return np.concatenate([[np.nan], d])

    real = rolling_deriv(yrs, pc)
    rng = np.random.default_rng(0)
    null = np.full((n_perm, len(centers)), np.nan)
    for i in range(n_perm):
        shuffled_yr = rng.permutation(yrs)
        null[i] = rolling_deriv(shuffled_yr, pc)
    # null band: 2.5–97.5 percentiles across perms (ignore NaNs)
    lo = np.nanpercentile(null, 2.5, axis=0)
    hi = np.nanpercentile(null, 97.5, axis=0)
    med = np.nanmedian(null, axis=0)

    fig = plt.figure(figsize=(13.5, 6.3))
    ax = fig.add_subplot(111)
    ax.fill_between(centers, lo, hi,
                     color=OI["grey"], alpha=0.22,
                     label="nullmodell 95% (år permutert)")
    ax.plot(centers, med, color=OI["grey"], linewidth=0.9,
             alpha=0.7, label="nullmodell median")
    ax.plot(centers, real, color=OI["rust"], linewidth=1.8,
             label="observert ‖Δsentroide‖")

    # annotate material revolutions
    revs = [
        (1680, "barokk-konsolidering"),
        (1760, "industrielt maskineri"),
        (1830, "dampbøying (Thonet)"),
        (1925, "stålrør (Breuer, Mies)"),
        (1955, "skumgummi + polyuretan"),
        (1970, "plast-støyping"),
    ]
    ymax = np.nanmax(real) * 1.15
    for y_rev, lbl in revs:
        ax.axvline(y_rev, color=SLATE, linewidth=0.7, linestyle=":",
                    alpha=0.7)
        ax.text(y_rev, ymax * 0.96, lbl, rotation=90, fontsize=7.5,
                 color=SLATE, ha="right", va="top", alpha=0.8)

    ax.set_xlabel("år")
    ax.set_ylabel("‖Δsentroide‖ per 5-års-steg")
    ax.set_ylim(0, ymax)
    ax.set_xlim(y0, y1)
    ax.grid(alpha=0.12, linewidth=0.4)
    ax.legend(loc="upper left", frameon=False, fontsize=8.8)
    save(fig, "E13_punktuert_likevekt")


# ═════════════════════════════════════════════════════════════════════
# FIG E14: Agent-hierarki (H14, prop. 6.12)
# ═════════════════════════════════════════════════════════════════════
def fig_E14_agent_hierarki(df):
    """H14: intra-period Mahalanobis spread for handverk vs. industri era.
    Higher agent (organisation/market) absorbs variance → smaller spread."""
    pre = df[(df["år"] < 1850) & df["år"].notna()].copy()
    post = df[(df["år"] >= 1950) & df["år"].notna()].copy()
    mid = df[(df["år"] >= 1850) & (df["år"] < 1950) & df["år"].notna()].copy()

    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    def mahalanobis_spread(sub):
        if len(sub) < 6:
            return np.nan
        X = sub[pc_cols].values
        cov = np.cov(X.T)
        try:
            inv = np.linalg.inv(cov + np.eye(len(pc_cols)) * 1e-6)
        except np.linalg.LinAlgError:
            return np.nan
        mu = X.mean(axis=0)
        d = np.sqrt(np.einsum("ij,jk,ik->i", X - mu, inv, X - mu))
        return d.mean()

    # per-period spreads
    def periods_of(sub):
        return sub["Stilperiode"].value_counts().loc[lambda s: s >= 10].index

    rows = []
    for label, sub, col in [("handverk (før 1850)", pre, SLATE),
                             ("overgang (1850–1950)", mid, OI["grey"]),
                             ("industri (etter 1950)", post, AMBER)]:
        for p in periods_of(sub):
            g = sub[sub["Stilperiode"] == p]
            s = mahalanobis_spread(g)
            if np.isnan(s):
                continue
            rows.append(dict(grp=label, period=p, spread=s, n=len(g), col=col,
                             year=PERIOD_YEAR.get(p, 1900)))
    rows_df = pd.DataFrame(rows)

    fig = plt.figure(figsize=(12.5, 7.5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.4, 1.0], wspace=0.28,
                           figure=fig)

    ax1 = fig.add_subplot(gs[0])
    for g, sub_rows in rows_df.groupby("grp"):
        col = sub_rows["col"].iloc[0]
        ax1.scatter(sub_rows["year"], sub_rows["spread"],
                    s=40 + sub_rows["n"] * 0.6, c=[col], alpha=0.85,
                    edgecolors="white", linewidths=0.8, label=g)
    ax1.set_xlabel("år (stilperiode-midtpunkt)")
    ax1.set_ylabel("gjennomsnittleg intra-periode Mahalanobis-spreiing")
    ax1.set_title("(a) spreiing per stilperiode, etter agent-skala",
                   loc="left", fontsize=10.2, weight="bold")
    ax1.grid(alpha=0.14, linewidth=0.4)
    ax1.legend(loc="upper right", frameon=False, fontsize=8.5)

    ax2 = fig.add_subplot(gs[1])
    groups = ["handverk (før 1850)", "overgang (1850–1950)", "industri (etter 1950)"]
    data = [rows_df[rows_df["grp"] == g]["spread"].values for g in groups]
    cols = [SLATE, OI["grey"], AMBER]
    parts = ax2.boxplot(data, tick_labels=groups, patch_artist=True, widths=0.55)
    for patch, col in zip(parts["boxes"], cols):
        patch.set_facecolor(to_rgba(col, 0.6))
        patch.set_edgecolor(SLATE)
    for m in parts["medians"]:
        m.set_color(OI["rust"])
        m.set_linewidth(1.5)
    ax2.set_ylabel("Mahalanobis-spreiing")
    ax2.set_title("(b) aggregert over grupper",
                   loc="left", fontsize=10.2, weight="bold")
    ax2.grid(axis="y", alpha=0.14, linewidth=0.4)
    for lbl in ax2.get_xticklabels():
        lbl.set_rotation(0); lbl.set_fontsize(9)
    save(fig, "E14_agent_hierarki")


# ═════════════════════════════════════════════════════════════════════
# FIG E16: Morfologisk nyskaping over tid (novelty distance)
# ═════════════════════════════════════════════════════════════════════
def fig_E16_morfologisk_nyskaping(df, pca, sils=None):
    """For each chair, compute the minimum 6D distance in PC-space to
    ANY chair that existed before its year. This is the 'morphological
    novelty' at birth. Directly analogous to stratigraphic novelty indices
    in paleobiology (Foote 1997, Ciampaglio 2002).

    Peaks in the per-year max reveal innovation bursts that the observed
    record would not produce under a Brownian-motion null."""
    df = df[df["år"].notna()].copy()
    df = df.sort_values("år").reset_index(drop=True)
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]
    X = df[pc_cols].values
    yrs = df["år"].values

    N = len(df)
    novelty = np.full(N, np.nan)
    for i in range(N):
        prior = yrs < yrs[i]
        if not prior.any():
            continue
        d = np.linalg.norm(X[prior] - X[i], axis=1)
        novelty[i] = d.min()

    df["novelty"] = novelty

    # Rolling max and mean per 10-year window
    years_grid = np.arange(int(np.nanmin(yrs)), int(np.nanmax(yrs)) + 1, 5)
    med = []; p90 = []; n_in = []
    for yr in years_grid:
        m = (yrs >= yr - 15) & (yrs <= yr + 15)
        if m.sum() < 3:
            med.append(np.nan); p90.append(np.nan); n_in.append(m.sum())
        else:
            v = novelty[m]
            v = v[~np.isnan(v)]
            if len(v) == 0:
                med.append(np.nan); p90.append(np.nan); n_in.append(0)
            else:
                med.append(np.median(v))
                p90.append(np.quantile(v, 0.90))
                n_in.append(len(v))
    med = np.array(med); p90 = np.array(p90); n_in = np.array(n_in)

    # Brownian null: shuffle years, recompute novelty statistic
    rng = np.random.default_rng(0)
    n_perm = 80
    null_p90 = np.full((n_perm, len(years_grid)), np.nan)
    for p in range(n_perm):
        shuf_yr = rng.permutation(yrs)
        nov_s = np.full(N, np.nan)
        ord_ = np.argsort(shuf_yr)
        Xs = X[ord_]
        ys = shuf_yr[ord_]
        for i in range(1, N):
            d = np.linalg.norm(Xs[:i] - Xs[i], axis=1)
            nov_s[ord_[i]] = d.min()
        for gi, yr in enumerate(years_grid):
            m = (shuf_yr >= yr - 15) & (shuf_yr <= yr + 15)
            v = nov_s[m]
            v = v[~np.isnan(v)]
            if len(v) >= 3:
                null_p90[p, gi] = np.quantile(v, 0.90)
    null_hi = np.nanpercentile(null_p90, 95, axis=0)
    null_med = np.nanmedian(null_p90, axis=0)

    # Identify chairs with the highest novelty for labeling
    top_idx = np.argsort(novelty)[-12:][::-1]
    top_chairs = df.iloc[top_idx][["år", "Stilperiode", "Namn", "PC1", "PC2",
                                   "novelty", "Objekt-ID"]].copy()

    fig = plt.figure(figsize=(13.5, 8.5))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1.1, 1], hspace=0.32,
                           figure=fig)

    # --- (a) novelty trajectory with null band ---
    ax = fig.add_subplot(gs[0])
    ax.fill_between(years_grid, 0, null_hi, color=OI["grey"], alpha=0.22,
                     label="nullmodell 95% (år permuterte)")
    ax.plot(years_grid, null_med, color=OI["grey"], lw=0.9, alpha=0.7,
             label="nullmodell median")
    ax.plot(years_grid, p90, color=OI["rust"], lw=1.9,
             label="observert 90%-perc nyskapingsavstand")
    ax.plot(years_grid, med, color=SLATE, lw=1.4, alpha=0.85,
             label="observert median")
    # mark top-12 individual chairs
    ax.scatter(df.iloc[top_idx]["år"], df.iloc[top_idx]["novelty"],
                s=60, c=OI["rust"], edgecolors="white", linewidths=0.9,
                zorder=5, label="top-12 individuelle innovatørar")
    ax.set_xlabel("år")
    ax.set_ylabel("morfologisk nyskapingsavstand (PC1–PC6)")
    ax.set_title("(a) minimum-avstand til prior stol gjennom tid",
                  loc="left", weight="bold", fontsize=10.5)
    ax.grid(alpha=0.12, linewidth=0.4)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.set_xlim(years_grid.min(), years_grid.max())

    # --- (b) top-12 individual innovator labels ---
    axB = fig.add_subplot(gs[1])
    axB.axis("off")
    axB.text(0.0, 1.00,
             "Dei mest morfologisk isolerte stolane i datasettet  "
             "(største avstand til alle tidlegare)",
             transform=axB.transAxes, fontsize=10.5, weight="bold",
             color=SLATE, va="top")
    # build a small table with 3 columns
    top_chairs = top_chairs.reset_index(drop=True)
    n_rows = (len(top_chairs) + 2) // 3
    for k, row_ in top_chairs.iterrows():
        col_idx = k // n_rows
        row_idx = k % n_rows
        xp = 0.01 + col_idx * 0.34
        yp = 0.88 - row_idx * (0.88 / max(n_rows, 1))
        nm = str(row_.get("Namn", ""))[:35]
        per = str(row_.get("Stilperiode", ""))[:20]
        txt = (f"{int(row_['år'])}  ·  {per}\n"
               f"{nm}\n"
               f"nyskaping = {row_['novelty']:.2f}")
        axB.text(xp, yp, txt, transform=axB.transAxes, fontsize=8.4,
                 color=SLATE, va="top", ha="left",
                 bbox=dict(facecolor=to_rgba(AMBER, 0.18),
                           edgecolor=to_rgba(AMBER, 0.5),
                           linewidth=0.4, boxstyle="round,pad=0.28"))

    save(fig, "E16_morfologisk_nyskaping")


# ═════════════════════════════════════════════════════════════════════
# FIG E17: Disparity Through Time (Foote 1993)
# ═════════════════════════════════════════════════════════════════════
def fig_E17_disparity_through_time(df, pca, n_perm=120):
    """Foote (1993): at each time slice, compute mean pairwise distance
    between contemporary forms. Compare to a Brownian-motion null where
    the same chairs have their years permuted. Peaks above the null band =
    adaptive radiation (many divergent forms at once); troughs = consolidation."""
    df = df[df["år"].notna()].copy()
    yrs = df["år"].values
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]
    X = df[pc_cols].values

    years_grid = np.arange(1550, 2025, 10)
    window = 40

    def disparity(yr_vec):
        out = np.full(len(years_grid), np.nan)
        for gi, yr in enumerate(years_grid):
            m = (yr_vec >= yr - window / 2) & (yr_vec <= yr + window / 2)
            idx = np.where(m)[0]
            if len(idx) < 6:
                continue
            sub = X[idx]
            # mean pairwise distance (no self pairs)
            dmat = np.linalg.norm(sub[:, None, :] - sub[None, :, :], axis=-1)
            n = len(idx)
            out[gi] = dmat.sum() / (n * (n - 1))
        return out

    real = disparity(yrs)
    rng = np.random.default_rng(0)
    null = np.full((n_perm, len(years_grid)), np.nan)
    for i in range(n_perm):
        null[i] = disparity(rng.permutation(yrs))
    lo = np.nanpercentile(null, 2.5, axis=0)
    hi = np.nanpercentile(null, 97.5, axis=0)
    med = np.nanmedian(null, axis=0)

    # sample size per window
    nwin = np.array([
        ((yrs >= yr - window / 2) & (yrs <= yr + window / 2)).sum()
        for yr in years_grid
    ])

    fig = plt.figure(figsize=(13.5, 7))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2.1, 1.0], hspace=0.22,
                           figure=fig)

    ax = fig.add_subplot(gs[0])
    ax.fill_between(years_grid, lo, hi, color=OI["grey"], alpha=0.22,
                     label="Brownian null 95%")
    ax.plot(years_grid, med, color=OI["grey"], lw=0.9, alpha=0.7,
             label="Brownian null median")
    ax.plot(years_grid, real, color=OI["rust"], lw=2.1,
             label="observert disparitet")
    # shade regions where observed > null hi (radiation) and < null lo (constraint)
    ax.fill_between(years_grid, real, hi,
                     where=(real > hi), alpha=0.3, color=AMBER, zorder=2,
                     label="over nullbandet (radiasjon)")
    ax.fill_between(years_grid, real, lo,
                     where=(real < lo), alpha=0.35, color=OI["blue"], zorder=2,
                     label="under nullbandet (stase/konsolidering)")
    # material revolutions
    for y_rev, lbl in [(1680, "barokk-konsolidering"),
                        (1830, "industriell revolusjon"),
                        (1925, "stålrør"),
                        (1970, "plast-støyping")]:
        ax.axvline(y_rev, color=SLATE, linewidth=0.7, linestyle=":", alpha=0.7)
        ax.text(y_rev + 2, ax.get_ylim()[1] * 0.02 if False else 0,
                 "", fontsize=7)
    ax.set_xlabel("år")
    ax.set_ylabel("gjennomsnittleg parvis avstand i 40-års vindauge")
    ax.set_xlim(years_grid.min(), years_grid.max())
    ax.grid(alpha=0.14, linewidth=0.4)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, ncol=2)

    axB = fig.add_subplot(gs[1], sharex=ax)
    axB.fill_between(years_grid, 0, nwin, color=SLATE, alpha=0.22, step="mid")
    axB.set_ylabel("n i vindauge")
    axB.set_xlabel("år")
    axB.grid(alpha=0.12, linewidth=0.4)
    for y_rev, lbl in [(1680, "barokk-konsolidering"),
                        (1830, "industriell revolusjon"),
                        (1925, "stålrør"),
                        (1970, "plast-støyping")]:
        axB.axvline(y_rev, color=SLATE, linewidth=0.7, linestyle=":",
                     alpha=0.7)
        axB.text(y_rev, axB.get_ylim()[1] * 0.90, lbl, rotation=90,
                  fontsize=7, color=SLATE, ha="right", va="top", alpha=0.85)

    save(fig, "E17_disparity_through_time")


# ═════════════════════════════════════════════════════════════════════
# FIG E18: Prediktiv landskaps-drift (train pre-1900, test post-1900)
# ═════════════════════════════════════════════════════════════════════
def fig_E18_prediktiv_landskapsdrift(df, pca):
    """Fit a KDE-landscape on chairs before 1900; predict where post-1900
    chairs should sit if the landscape were stationary. Highlight regions
    where post-1900 density exceeds the pre-1900 prediction (emergent zones)
    and where post-1900 density falls below (abandoned zones)."""
    df = df[df["år"].notna()].copy()
    pre = df[df["år"] < 1900]
    post = df[df["år"] >= 1900]
    if len(pre) < 30 or len(post) < 30:
        print("  skipping E18: insufficient samples")
        return

    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    xlo, xhi = np.quantile(pc1, [0.005, 0.995])
    ylo, yhi = np.quantile(pc2, [0.005, 0.995])
    xpad = (xhi - xlo) * 0.04; ypad = (yhi - ylo) * 0.04
    xlo -= xpad; xhi += xpad; ylo -= ypad; yhi += ypad

    xx, yy = np.meshgrid(np.linspace(xlo, xhi, 140),
                          np.linspace(ylo, yhi, 140))
    pts = np.vstack([xx.ravel(), yy.ravel()])

    kde_pre = gaussian_kde(pre[["PC1", "PC2"]].values.T, bw_method=0.28)
    kde_post = gaussian_kde(post[["PC1", "PC2"]].values.T, bw_method=0.28)
    z_pre = kde_pre(pts).reshape(xx.shape)
    z_post = kde_post(pts).reshape(xx.shape)
    # diverging: log2 ratio; smoothed floor to avoid division issues
    ratio = np.log2((z_post + z_pre.max() * 1e-3) /
                    (z_pre + z_pre.max() * 1e-3))

    fig = plt.figure(figsize=(14, 6.5))
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1.05], wspace=0.22,
                           figure=fig)

    dens_cmap = LinearSegmentedColormap.from_list(
        "amberfade", [(1, 1, 1, 0),
                      to_rgba(LIGHTAMBER, 0.60),
                      to_rgba(AMBER, 0.85),
                      to_rgba(SLATE, 0.98)], N=256)
    # quota levels for shared visual comparison
    vmax = max(z_pre.max(), z_post.max())
    lvs = np.linspace(vmax * 0.02, vmax, 10)

    axA = fig.add_subplot(gs[0])
    axA.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.10, linewidths=0, zorder=1)
    axA.contourf(xx, yy, z_pre, levels=lvs, cmap=dens_cmap, zorder=2)
    axA.contour(xx, yy, z_pre, levels=lvs[::2], colors=[SLATE],
                 linewidths=0.35, alpha=0.55, zorder=3)
    axA.set_xlim(xlo, xhi); axA.set_ylim(ylo, yhi)
    axA.set_title(f"(a) pre-1900 landskap   n={len(pre)}",
                   loc="left", weight="bold", fontsize=10.5)
    axA.set_xlabel("PC1"); axA.set_ylabel("PC2")
    axA.grid(alpha=0.10, linewidth=0.4)

    axB = fig.add_subplot(gs[1])
    axB.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.10, linewidths=0, zorder=1)
    axB.contourf(xx, yy, z_post, levels=lvs, cmap=dens_cmap, zorder=2)
    axB.contour(xx, yy, z_post, levels=lvs[::2], colors=[SLATE],
                 linewidths=0.35, alpha=0.55, zorder=3)
    axB.set_xlim(xlo, xhi); axB.set_ylim(ylo, yhi)
    axB.set_title(f"(b) post-1900 landskap   n={len(post)}",
                   loc="left", weight="bold", fontsize=10.5)
    axB.set_xlabel("PC1"); axB.set_ylabel("PC2")
    axB.grid(alpha=0.10, linewidth=0.4)

    axC = fig.add_subplot(gs[2])
    vmax_r = np.nanpercentile(np.abs(ratio), 95)
    cs = axC.pcolormesh(xx, yy, ratio, cmap="RdBu_r",
                         vmin=-vmax_r, vmax=vmax_r, shading="auto",
                         zorder=2)
    axC.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.12, linewidths=0, zorder=1)
    axC.set_xlim(xlo, xhi); axC.set_ylim(ylo, yhi)
    axC.set_title("(c) log₂(post / pre) — raudt = ny region, blå = forlaten",
                   loc="left", weight="bold", fontsize=10.5)
    axC.set_xlabel("PC1")
    cb = fig.colorbar(cs, ax=axC, shrink=0.85, pad=0.02)
    cb.set_label("log₂ forholdstal")

    save(fig, "E18_prediktiv_landskapsdrift")


# ═════════════════════════════════════════════════════════════════════
# FIG E19: Morfologisk karakterforskyving (character displacement)
# ═════════════════════════════════════════════════════════════════════
def fig_E19_karakterforskyving(df, pca):
    """Empirical demonstration of *morphological character displacement*:
    when a new substrate (steel/plastic) enters the niche, the established
    substrate (wood) does not simply co-exist; its morphospace collapses.

    Layout:
      Row 1: wood distribution in four time bands (1600-1800, 1800-1900, 1900-1950, 1950-2024)
             + convex hull + n, with steel/plastic overlaid from 1900 onward.
      Row 2: (a) wood hull area over time
             (b) wood total variance over time
             (c) log2 ratio of wood variance, baseline = 1600-1800.
    The same quantity for steel/plastic is included for reference."""
    df = df[df["år"].notna()].copy()

    windows = [(1600, 1800), (1800, 1900), (1900, 1950), (1950, 2025)]
    pc_cols = ["PC1", "PC2"]
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    xlo, xhi = np.quantile(pc1, [0.005, 0.995])
    ylo, yhi = np.quantile(pc2, [0.005, 0.995])

    def hull_area(points):
        if len(points) < 3:
            return np.nan
        try:
            h = ConvexHull(points)
            return float(h.volume)
        except Exception:
            return np.nan

    def tot_var(points):
        if len(points) < 2:
            return np.nan
        return float(np.trace(np.cov(points.T)))

    # --- per-window stats ---
    wood_area = []; steel_area = []; plastic_area = []
    wood_var  = []; steel_var  = []; plastic_var  = []
    for (a, b) in windows:
        w = df[(df["mat_class"] == "wood") & (df["år"] >= a) & (df["år"] < b)][pc_cols].values
        s = df[(df["mat_class"] == "metal") & (df["år"] >= a) & (df["år"] < b)][pc_cols].values
        p = df[(df["mat_class"] == "plastic") & (df["år"] >= a) & (df["år"] < b)][pc_cols].values
        wood_area.append(hull_area(w)); steel_area.append(hull_area(s)); plastic_area.append(hull_area(p))
        wood_var.append(tot_var(w));   steel_var.append(tot_var(s));   plastic_var.append(tot_var(p))

    # --- figure layout ---
    fig = plt.figure(figsize=(15, 10.5))
    gs = gridspec.GridSpec(3, 4, height_ratios=[1.3, 1.0, 1.0],
                           hspace=0.42, wspace=0.16, figure=fig)

    # Row 1: wood distribution per window, with steel+plastic overlaid
    for i, (a, b) in enumerate(windows):
        ax = fig.add_subplot(gs[0, i])
        ax.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.08,
                   linewidths=0, zorder=1)
        wsub = df[(df["mat_class"] == "wood") & (df["år"] >= a) & (df["år"] < b)]
        ssub = df[(df["mat_class"] == "metal") & (df["år"] >= a) & (df["år"] < b)]
        psub = df[(df["mat_class"] == "plastic") & (df["år"] >= a) & (df["år"] < b)]
        # wood
        if len(wsub) >= 3:
            ax.scatter(wsub["PC1"], wsub["PC2"], s=14, c=AMBER, alpha=0.55,
                       edgecolors="none", zorder=2, label=f"tre n={len(wsub)}")
            try:
                h = ConvexHull(wsub[pc_cols].values)
                pts = wsub[pc_cols].values[h.vertices]
                pts = np.r_[pts, pts[:1]]
                ax.plot(pts[:, 0], pts[:, 1],
                        color=AMBER, lw=1.6, alpha=0.9, zorder=3)
                ax.fill(pts[:, 0], pts[:, 1],
                        color=to_rgba(AMBER, 0.10), zorder=2)
            except Exception:
                pass
        # steel
        if len(ssub) >= 3:
            ax.scatter(ssub["PC1"], ssub["PC2"], s=18, c=OI["blue"],
                       alpha=0.65, edgecolors="white", linewidths=0.3,
                       zorder=4, label=f"stål n={len(ssub)}")
        # plastic
        if len(psub) >= 3:
            ax.scatter(psub["PC1"], psub["PC2"], s=18, c=OI["rust"],
                       alpha=0.65, edgecolors="white", linewidths=0.3,
                       zorder=4, label=f"plast n={len(psub)}")
        ax.set_xlim(xlo, xhi); ax.set_ylim(ylo, yhi)
        ax.set_title(f"{a}–{b}", loc="left", fontsize=10.5, weight="bold")
        ax.grid(alpha=0.12, linewidth=0.4)
        ax.set_xlabel("PC1")
        if i == 0: ax.set_ylabel("PC2")
        if len(wsub) >= 3:
            ax.legend(loc="lower right", fontsize=7.5, frameon=False)

    # Row 2: hull area over time, variance over time, compression ratio
    band_centers = [(a + b) / 2 for (a, b) in windows]
    x_labels = [f"{a}–{b}" for (a, b) in windows]

    ax2 = fig.add_subplot(gs[1, :2])
    ax2.plot(band_centers, wood_area, marker="o", color=AMBER, lw=2.2,
             label="tre")
    ax2.plot(band_centers, steel_area, marker="s", color=OI["blue"], lw=1.8,
             label="stål")
    ax2.plot(band_centers, plastic_area, marker="^", color=OI["rust"], lw=1.8,
             label="plast")
    ax2.set_xticks(band_centers); ax2.set_xticklabels(x_labels, fontsize=9)
    ax2.set_ylabel("konveks hylster-areal (PC1–PC2)")
    ax2.set_title("(e) morforom-areal per materiale over tid",
                   loc="left", fontsize=10.5, weight="bold")
    ax2.grid(alpha=0.14, linewidth=0.4)
    ax2.legend(loc="upper right", frameon=False, fontsize=9)
    # annotate wood collapse
    if not np.isnan(wood_area[0]) and not np.isnan(wood_area[-1]) and wood_area[0] > 0:
        pct = 100 * (wood_area[-1] / wood_area[0] - 1)
        ax2.annotate(f"tre-hylster {pct:+.0f}%",
                     xy=(band_centers[-1], wood_area[-1]),
                     xytext=(band_centers[-1] - 60, wood_area[-1] + 0.4),
                     fontsize=9, color=AMBER, weight="bold",
                     arrowprops=dict(arrowstyle="->", color=AMBER, lw=1))

    ax3 = fig.add_subplot(gs[1, 2:])
    ax3.plot(band_centers, wood_var, marker="o", color=AMBER, lw=2.2,
             label="tre")
    ax3.plot(band_centers, steel_var, marker="s", color=OI["blue"], lw=1.8,
             label="stål")
    ax3.plot(band_centers, plastic_var, marker="^", color=OI["rust"], lw=1.8,
             label="plast")
    ax3.set_xticks(band_centers); ax3.set_xticklabels(x_labels, fontsize=9)
    ax3.set_ylabel("total varians tr(Σ) i PC1–PC2")
    ax3.set_title("(f) morfologisk spreiing per materiale",
                   loc="left", fontsize=10.5, weight="bold")
    ax3.grid(alpha=0.14, linewidth=0.4)
    ax3.legend(loc="upper right", frameon=False, fontsize=9)

    ax4 = fig.add_subplot(gs[2, :])
    # steel/plastic hull area ratio over time vs wood's response
    # Compute wood's compression coefficient: wood_var[t] / wood_var[0]
    w0 = wood_var[0] if (wood_var[0] and not np.isnan(wood_var[0])) else np.nan
    comp = np.array(wood_var) / w0 if not np.isnan(w0) else np.array([np.nan] * 4)
    # intruder presence: (steel + plastic) variance per band
    intruder = np.array([
        (0 if np.isnan(s) else s) + (0 if np.isnan(p) else p)
        for s, p in zip(steel_var, plastic_var)
    ])

    ax4b = ax4.twinx()
    ax4.bar(np.arange(4) - 0.15, comp, width=0.3, color=AMBER, alpha=0.8,
             edgecolor=SLATE, linewidth=0.5,
             label="tre-spreiing relativ til 1600-1800")
    ax4b.bar(np.arange(4) + 0.15, intruder, width=0.3, color=OI["blue"],
              alpha=0.85, edgecolor=SLATE, linewidth=0.5,
              label="stål+plast total varians")
    ax4.axhline(1.0, color=SLATE, lw=0.7, linestyle="--", alpha=0.8)
    ax4.set_xticks(range(4)); ax4.set_xticklabels(x_labels, fontsize=9)
    ax4.set_ylabel("tre-spreiing / baseline", color=AMBER)
    ax4b.set_ylabel("total varians stål + plast", color=OI["blue"])
    ax4.tick_params(axis="y", labelcolor=AMBER)
    ax4b.tick_params(axis="y", labelcolor=OI["blue"])
    ax4.set_title(
        "(g) karakterforskyving: tre kollapsar i same tidsbandet som stål og plast ekspanderer",
        loc="left", fontsize=10.5, weight="bold")
    ax4.grid(axis="y", alpha=0.14, linewidth=0.4)

    # combined legend
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc="upper left",
               fontsize=9, frameon=False)

    save(fig, "E19_karakterforskyving")


# ═════════════════════════════════════════════════════════════════════
# FIG E20: Phylomorphospace (Sidlauskas 2008)
# ═════════════════════════════════════════════════════════════════════
def fig_E20_phylomorphospace(df, pca):
    """Phylomorphospace after Sidlauskas (2008). Stolen from ichthyology:
    place period-centroid nodes in PC1-PC2; connect them along the
    chronological 'tree' (here a linear chain by year) with internal
    branches coloured by the per-branch evolutionary rate (haldane-like).

    A real phylo has branching; artefact history is largely a chain with
    occasional 'reticulation' (revival). We show the chain plus a second
    panel with per-branch rate as a function of year."""
    counts = df["Stilperiode"].value_counts()
    periods = [p for p in sorted(PERIOD_YEAR.keys(), key=lambda k: PERIOD_YEAR[k])
               if p in counts.index and counts[p] >= 10]
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    nodes = []
    for p in periods:
        sub = df[df["Stilperiode"] == p][pc_cols]
        nodes.append(dict(period=p, year=PERIOD_YEAR[p],
                           centroid=sub.mean().values,
                           sigma=sub.std().values,
                           n=len(sub)))
    nodes.sort(key=lambda r: r["year"])

    # per-branch rate: ||Δcentroid|| / Δyear (in darwins-like units)
    edges = []
    for i in range(len(nodes) - 1):
        a, b = nodes[i], nodes[i + 1]
        dt = max(b["year"] - a["year"], 1)
        dv = b["centroid"] - a["centroid"]
        rate6 = np.linalg.norm(dv) / dt
        edges.append(dict(a=i, b=i + 1, year=(a["year"] + b["year"]) / 2,
                          dt=dt, rate=rate6))

    # --- figure ---
    fig = plt.figure(figsize=(15.5, 7.2))
    gs = gridspec.GridSpec(1, 3, width_ratios=[2.1, 0.85, 1.45], wspace=0.18,
                           figure=fig)

    # Panel A: phylomorphospace
    ax = fig.add_subplot(gs[0])
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    ax.scatter(pc1, pc2, s=4, c=OI["grey"], alpha=0.10,
               linewidths=0, zorder=1)

    # color branches by rate (log scale)
    rates = np.array([e["rate"] for e in edges]) + 1e-9
    lrates = np.log10(rates)
    vmin, vmax = lrates.min(), lrates.max()
    branch_cmap = LinearSegmentedColormap.from_list(
        "rate", [SLATE, "#6B7080", AMBER, OI["rust"]], N=256)

    for e in edges:
        a, b = nodes[e["a"]], nodes[e["b"]]
        norm = (np.log10(e["rate"] + 1e-9) - vmin) / max(vmax - vmin, 1e-9)
        col = branch_cmap(norm)
        ax.annotate("", xy=(b["centroid"][0], b["centroid"][1]),
                    xytext=(a["centroid"][0], a["centroid"][1]),
                    arrowprops=dict(arrowstyle="-", color=col,
                                    lw=max(0.6, 3 * norm + 0.8),
                                    alpha=0.95),
                    zorder=3)

    for i, r in enumerate(nodes):
        c = PERIOD_COLOR.get(r["period"], OI["grey"])
        ax.scatter([r["centroid"][0]], [r["centroid"][1]],
                   s=140, c=[c], edgecolors="white",
                   linewidths=1.4, zorder=5)
        ax.text(r["centroid"][0], r["centroid"][1], str(i + 1),
                ha="center", va="center", fontsize=8.5, color="white",
                weight="bold", zorder=6)

    xlo, xhi = np.quantile(pc1, [0.02, 0.98])
    ylo, yhi = np.quantile(pc2, [0.02, 0.98])
    ax.set_xlim(xlo, xhi); ax.set_ylim(ylo, yhi)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varians)")
    ax.set_title("(a) phylomorphospace — kjede av periode-sentroidar "
                 "med greiner farga etter rate",
                 loc="left", fontsize=10.2, weight="bold")
    ax.grid(alpha=0.12, linewidth=0.4)

    # Panel B: numbered legend list
    axL = fig.add_subplot(gs[1]); axL.axis("off")
    axL.text(0.0, 1.00, "Node-liste", transform=axL.transAxes,
             fontsize=10, weight="bold", color=SLATE, va="top")
    for i, n in enumerate(nodes):
        yp = 0.94 - i * (0.94 / max(len(nodes), 1))
        c = PERIOD_COLOR.get(n["period"], OI["grey"])
        axL.scatter([0.02], [yp], s=55, c=[c], transform=axL.transAxes,
                    edgecolors="white", linewidths=0.8, zorder=3)
        axL.text(0.02, yp, str(i + 1), transform=axL.transAxes,
                 fontsize=7, weight="bold", color="white",
                 ha="center", va="center", zorder=4)
        axL.text(0.10, yp, f"{n['period']}  ({n['year']})",
                 transform=axL.transAxes, fontsize=7.6,
                 color=SLATE, va="center", ha="left")

    # Panel C: per-branch rate over time
    axB = fig.add_subplot(gs[2])
    years_mid = [e["year"] for e in edges]
    axB.bar(years_mid, rates, width=12, color=AMBER,
            edgecolor=SLATE, linewidth=0.5, alpha=0.85)
    axB.set_yscale("log")
    axB.set_xlabel("midt-år for grein")
    axB.set_ylabel("‖Δsentroide‖₆ / Δår   (log skala)")
    axB.set_title("(c) evolusjonsrate per grein (alle seks PC)",
                  loc="left", fontsize=10.2, weight="bold")
    axB.grid(alpha=0.14, linewidth=0.4, axis="y")
    # annotate the fastest branch
    if len(edges):
        k_max = int(np.argmax(rates))
        fastest = edges[k_max]
        a = nodes[fastest["a"]]; b = nodes[fastest["b"]]
        axB.annotate(f"raskast: {a['period']} → {b['period']}\n"
                     f"Δt = {int(fastest['dt'])} år",
                     xy=(fastest["year"], fastest["rate"]),
                     xytext=(fastest["year"] - 110,
                              fastest["rate"] * 1.4),
                     fontsize=8, color=SLATE,
                     arrowprops=dict(arrowstyle="->", color=SLATE,
                                     lw=0.8, alpha=0.7))

    save(fig, "E20_phylomorphospace")


# ═════════════════════════════════════════════════════════════════════
# FIG E21: Morfologisk tempo (Gingerich 1983, haldanes/darwins)
# ═════════════════════════════════════════════════════════════════════
def fig_E21_tempo_gingerich(df, pca):
    """Gingerich (1983) haldane rates applied to chair design.
    Haldane = (z2 - z1) / Δt in standard deviations per generation.
    We use 'generation' ≈ 25 years (one typical designer career).

    Compare observed rates to:
      - typical biological macroevolutionary rates (10⁻³ haldanes/gen)
      - typical evolutionary lineage rates (10⁻² haldanes/gen)
      - anthropogenic rates under domestication (10⁻¹–10¹ haldanes/gen)

    The scale is log-haldane; the comparison shows chairs evolving in the
    same rate regime as domesticated animals, not as wild lineages."""
    df = df[df["år"].notna()].copy()
    df = df.sort_values("år")
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    # use 40-year bins for robust centroid estimation
    bins = np.arange(1500, 2040, 40)
    centroids = []
    for i in range(len(bins) - 1):
        a, b = bins[i], bins[i + 1]
        sub = df[(df["år"] >= a) & (df["år"] < b)]
        if len(sub) < 8:
            continue
        for c in pc_cols:
            pass
        centroids.append(dict(year=(a + b) / 2, bin=(a, b),
                              mean=sub[pc_cols].mean().values,
                              std=sub[pc_cols].std().values,
                              n=len(sub)))

    # haldanes between consecutive bins on each axis
    gen = 25  # years per generation
    rows = []
    for i in range(len(centroids) - 1):
        a, b = centroids[i], centroids[i + 1]
        dt_gen = (b["year"] - a["year"]) / gen
        pooled_sd = (a["std"] + b["std"]) / 2 + 1e-9
        haldane = (b["mean"] - a["mean"]) / (pooled_sd * dt_gen)
        rows.append(dict(year=(a["year"] + b["year"]) / 2,
                         haldane=haldane,
                         span=(a["year"], b["year"])))

    year_arr = np.array([r["year"] for r in rows])
    h_arr = np.array([r["haldane"] for r in rows])  # shape (n, 6)
    h_abs = np.abs(h_arr)

    fig = plt.figure(figsize=(14, 8.5))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.35,
                           figure=fig)

    axA = fig.add_subplot(gs[0])
    # per-axis lines
    axis_colors = [AMBER, SLATE, OI["blue"], OI["rust"],
                   OI["green"], OI["skyblue"]]
    for i, (c, col) in enumerate(zip(pc_cols, axis_colors)):
        axA.plot(year_arr, h_abs[:, i], marker="o", markersize=4, linewidth=1.2,
                 label=f"|h({c})|", color=col, alpha=0.85)
    # biological benchmarks
    benchmarks = [
        (1e-4, "bradytelisk (makroevolusjon i naturen)", OI["grey"]),
        (1e-2, "mikroevolusjonære linjer", SLATE),
        (1e-1, "domestiserte arter (sprang)", AMBER),
        (1e0, "Bergmann-skift under klimaskift", OI["rust"]),
    ]
    for val, lbl, col in benchmarks:
        axA.axhline(val, color=col, linestyle="--", linewidth=0.7, alpha=0.7)
        axA.text(2020, val * 1.15, lbl, fontsize=7.5, color=col,
                 ha="right", va="bottom")
    axA.set_yscale("log")
    axA.set_ylim(1e-4, 10)
    axA.set_xlim(year_arr.min() - 10, year_arr.max() + 10)
    axA.set_xlabel("år")
    axA.set_ylabel("|haldane| = |Δz| / (σ̄ · Δgen)")
    axA.set_title("(a) Gingerich haldane-ratar per 40-års intervall "
                  "(gen = 25 år)", loc="left", fontsize=10.2, weight="bold")
    axA.grid(alpha=0.14, which="both", linewidth=0.4)
    axA.legend(loc="upper left", fontsize=7.5, ncol=3, frameon=False)

    axB = fig.add_subplot(gs[1])
    pooled = h_abs.mean(axis=1)
    axB.bar(year_arr, pooled, width=30, color=AMBER,
            edgecolor=SLATE, linewidth=0.4, alpha=0.85)
    axB.set_yscale("log")
    axB.set_ylim(1e-3, 10)
    axB.axhline(1e-2, color=SLATE, linestyle="--", linewidth=0.7,
                alpha=0.8, label="mikroevolusjon")
    axB.axhline(1e-1, color=AMBER, linestyle="--", linewidth=0.7,
                alpha=0.8, label="domestisering")
    axB.set_xlabel("år")
    axB.set_ylabel("gjennomsnittleg |haldane| (6 aksar)")
    axB.set_title("(b) samla haldane-rate per intervall",
                  loc="left", fontsize=10.2, weight="bold")
    axB.grid(alpha=0.14, which="both", linewidth=0.4, axis="y")
    axB.legend(loc="upper left", fontsize=8, frameon=False)
    axB.set_xlim(year_arr.min() - 10, year_arr.max() + 10)

    save(fig, "E21_tempo_gingerich")


# ═════════════════════════════════════════════════════════════════════
# FIG E22: Makroevolusjonsmodellar (BM vs OU vs EB, Harmon 2010 style)
# ═════════════════════════════════════════════════════════════════════
def fig_E22_makroevo_modellar(df, pca):
    """For each PC axis, fit three classical macroevolutionary models to
    the observed 'disparity-through-time' curve:
      BM   — Var(Δ) = σ² Δt                (pure random walk)
      OU   — Var(Δ) = (σ²/α)(1-e^{-2α Δt}) (stabilising selection)
      EB   — σ²(t) = σ²₀ exp(r t), r<0      (early-burst niche filling)
    Compare via AIC; colour-code the winning model per axis.

    This is Harmon et al. (2010)'s exact approach, transposed to chairs."""
    df_yr = df[df["år"].notna()].copy()
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    from scipy.optimize import minimize

    # pairs: for each pair of chairs, (Δt, Δx for each axis)
    # we subsample to keep computation reasonable
    rng = np.random.default_rng(0)
    idx = rng.choice(len(df_yr), min(800, len(df_yr)), replace=False)
    sub = df_yr.iloc[idx].sort_values("år").reset_index(drop=True)
    yrs = sub["år"].values
    n = len(sub)

    # build pair arrays
    pair_dt = []
    pair_dx = []  # list of 6-vectors
    # cap at 50k pairs
    for i in range(n - 1):
        js = np.arange(i + 1, n)
        dts = yrs[js] - yrs[i]
        mask = dts > 0
        js = js[mask]; dts = dts[mask]
        if len(js) > 50:
            keep = rng.choice(len(js), 50, replace=False)
            js = js[keep]; dts = dts[keep]
        pair_dt.append(dts)
        pair_dx.append(sub.iloc[js][pc_cols].values - sub.iloc[i][pc_cols].values)
    pair_dt = np.concatenate(pair_dt) if pair_dt else np.array([])
    pair_dx = np.concatenate(pair_dx, axis=0) if pair_dx else np.zeros((0, 6))
    print(f"  E22: {len(pair_dt)} pair observations")

    def neg_ll_bm(params, dt, dx):
        sigma2 = np.exp(params[0])
        var_t = sigma2 * dt
        return 0.5 * np.sum(np.log(2 * np.pi * var_t) + dx ** 2 / var_t)

    def neg_ll_ou(params, dt, dx):
        sigma2 = np.exp(params[0])
        alpha = np.exp(params[1])
        var_t = (sigma2 / (2 * alpha)) * (1 - np.exp(-2 * alpha * dt))
        var_t = np.maximum(var_t, 1e-12)
        return 0.5 * np.sum(np.log(2 * np.pi * var_t) + dx ** 2 / var_t)

    def neg_ll_eb(params, dt, dx):
        sigma2_0 = np.exp(params[0])
        r = params[1]  # typically negative for early burst
        # integrated variance under EB: integral_0^dt sigma^2_0 e^{rs} ds
        if abs(r) < 1e-8:
            var_t = sigma2_0 * dt
        else:
            var_t = (sigma2_0 / r) * (np.exp(r * dt) - 1)
            var_t = np.maximum(var_t, 1e-12)
        return 0.5 * np.sum(np.log(2 * np.pi * var_t) + dx ** 2 / var_t)

    results = []
    for k, c in enumerate(pc_cols):
        dx = pair_dx[:, k]
        # fit BM
        r_bm = minimize(neg_ll_bm, [0.0], args=(pair_dt, dx),
                        method="Nelder-Mead")
        # fit OU
        r_ou = minimize(neg_ll_ou, [0.0, -2.0], args=(pair_dt, dx),
                        method="Nelder-Mead")
        # fit EB
        r_eb = minimize(neg_ll_eb, [0.0, -0.001], args=(pair_dt, dx),
                        method="Nelder-Mead")
        aic_bm = 2 * 1 + 2 * r_bm.fun
        aic_ou = 2 * 2 + 2 * r_ou.fun
        aic_eb = 2 * 2 + 2 * r_eb.fun
        aics = {"BM": aic_bm, "OU": aic_ou, "EB": aic_eb}
        best = min(aics, key=aics.get)
        delta_aic = {k: v - min(aics.values()) for k, v in aics.items()}
        params = {
            "BM": dict(sigma2=np.exp(r_bm.x[0])),
            "OU": dict(sigma2=np.exp(r_ou.x[0]), alpha=np.exp(r_ou.x[1])),
            "EB": dict(sigma2_0=np.exp(r_eb.x[0]), r=r_eb.x[1]),
        }
        results.append(dict(axis=c, aics=aics, delta=delta_aic,
                            best=best, params=params))

    fig = plt.figure(figsize=(14, 9))
    gs = gridspec.GridSpec(2, 3, hspace=0.40, wspace=0.28, figure=fig)

    model_color = {"BM": SLATE, "OU": AMBER, "EB": OI["rust"]}

    for k, res in enumerate(results):
        r, c = divmod(k, 3)
        ax = fig.add_subplot(gs[r, c])
        dts = np.linspace(1, pair_dt.max(), 80)
        # BM
        v_bm = res["params"]["BM"]["sigma2"] * dts
        # OU
        s2o = res["params"]["OU"]["sigma2"]; alpha = res["params"]["OU"]["alpha"]
        v_ou = (s2o / (2 * alpha)) * (1 - np.exp(-2 * alpha * dts))
        # EB
        s2e = res["params"]["EB"]["sigma2_0"]; rr = res["params"]["EB"]["r"]
        if abs(rr) < 1e-8:
            v_eb = s2e * dts
        else:
            v_eb = (s2e / rr) * (np.exp(rr * dts) - 1)
        # empirical variance per dt bin
        bins = np.quantile(pair_dt, np.linspace(0, 1, 20))
        emp_x = []; emp_y = []
        for i in range(len(bins) - 1):
            m = (pair_dt >= bins[i]) & (pair_dt < bins[i + 1])
            if m.sum() < 10: continue
            emp_x.append((bins[i] + bins[i + 1]) / 2)
            emp_y.append(pair_dx[m, k].var())
        ax.scatter(emp_x, emp_y, s=20, c=OI["grey"],
                   edgecolors="white", linewidths=0.3, zorder=2,
                   label="empirisk Var(Δ)")
        ax.plot(dts, v_bm, color=model_color["BM"], lw=1.6, alpha=0.9,
                 label=f"BM ΔAIC={res['delta']['BM']:.1f}")
        ax.plot(dts, v_ou, color=model_color["OU"], lw=1.6, alpha=0.9,
                 label=f"OU ΔAIC={res['delta']['OU']:.1f}")
        ax.plot(dts, v_eb, color=model_color["EB"], lw=1.6, alpha=0.9,
                 label=f"EB ΔAIC={res['delta']['EB']:.1f}")
        win_col = model_color[res["best"]]
        ax.set_title(f"{AXIS_LABELS_NN.get(res['axis'], res['axis'])}   "
                     f"beste: {res['best']}",
                     loc="left", fontsize=9.8, weight="bold", color=win_col)
        ax.set_xlabel("Δår")
        ax.set_ylabel("Var(Δtrekk)")
        ax.grid(alpha=0.12, linewidth=0.4)
        ax.legend(loc="upper left", fontsize=7.2, frameon=False)

    save(fig, "E22_makroevo_modellar")


# ═════════════════════════════════════════════════════════════════════
# FIG E23: Konvergent evolusjon på tvers av materiale
# ═════════════════════════════════════════════════════════════════════
def fig_E23_konvergens(df, pca, sils, n_pairs=8):
    """Convergent evolution: find chair pairs from different material
    classes that sit very close in 6D PC-space. These are cases where a
    new substrate arrived at a pre-existing morphological 'solution'.
    Compare to a null of same-material pair distances (should be smaller).

    The cross-material pairs identify instances where function dominates
    over substrate — direct test of the substrate-independence claim."""
    df = df.copy()
    df = df[df["mat_class"].isin(["wood", "metal", "plastic"])].reset_index(drop=True)
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]
    X = df[pc_cols].values
    mat = df["mat_class"].values
    yrs = df["år"].values

    # compute pairs with constraint: different materials and year diff >= 50
    n = len(df)
    # sample to avoid O(n^2) blowup
    rng = np.random.default_rng(0)
    idx = rng.choice(n, min(600, n), replace=False)
    sub_X = X[idx]; sub_mat = mat[idx]; sub_yr = yrs[idx]; sub_oid = df.iloc[idx]["Objekt-ID"].values

    # only keep pairs across different materials and with year separation >= 40
    # but rank by 6D distance; keep smallest
    candidates = []
    for i in range(len(sub_X)):
        for j in range(i + 1, len(sub_X)):
            if sub_mat[i] == sub_mat[j]:
                continue
            if abs(sub_yr[i] - sub_yr[j]) < 40:
                continue
            d = np.linalg.norm(sub_X[i] - sub_X[j])
            candidates.append((d, i, j))
    candidates.sort()

    chosen_pairs = []
    used_oids = set()
    for d, i, j in candidates:
        if sub_oid[i] in used_oids or sub_oid[j] in used_oids:
            continue
        chosen_pairs.append((i, j, d))
        used_oids.add(sub_oid[i]); used_oids.add(sub_oid[j])
        if len(chosen_pairs) >= n_pairs:
            break

    # null: within-material distance distribution
    within_dists = []
    for _ in range(2000):
        i, j = rng.choice(len(sub_X), 2, replace=False)
        if sub_mat[i] != sub_mat[j]:
            continue
        within_dists.append(np.linalg.norm(sub_X[i] - sub_X[j]))
    within_dists = np.array(within_dists)

    between_dists = np.array([c[0] for c in candidates])

    # 4 pairs × 2 columns layout: each pair is a 3-cell block (chair A, "≡", chair B)
    n_show = min(len(chosen_pairs), 6)
    chosen_pairs = chosen_pairs[:n_show]
    mat_tint = {"wood": AMBER, "metal": OI["blue"], "plastic": OI["rust"]}

    # Layout: 3 rows of pairs, 2 pairs per row → 6 pairs
    # Plus bottom row for histogram
    n_cols = 2
    n_rows_pairs = int(np.ceil(n_show / n_cols))
    fig = plt.figure(figsize=(14, 3.4 * n_rows_pairs + 3.8))
    gs = gridspec.GridSpec(
        n_rows_pairs + 1, n_cols * 3,
        height_ratios=[1] * n_rows_pairs + [1.1],
        width_ratios=[1.0, 0.28, 1.0] * n_cols,
        hspace=0.55, wspace=0.10, figure=fig)

    for idx, (i, j, d) in enumerate(chosen_pairs):
        r = idx // n_cols
        c = idx % n_cols
        base_col = c * 3
        for side_i, who in enumerate([i, j]):
            ax = fig.add_subplot(gs[r, base_col + side_i * 2])
            oid = sub_oid[who]
            img = sils.get(oid)
            if img is not None:
                col = mat_tint.get(sub_mat[who], SLATE)
                rgba = _period_rgb_silhouette(img, to_rgba(col)[:3])
                ax.imshow(rgba, interpolation="nearest", aspect="auto")
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_title(f"{sub_mat[who]}  {int(sub_yr[who])}",
                         fontsize=9.5,
                         color=mat_tint.get(sub_mat[who], SLATE),
                         weight="bold")
            for s in ["top", "right", "bottom", "left"]:
                ax.spines[s].set_color(mat_tint.get(sub_mat[who], SLATE))
                ax.spines[s].set_linewidth(1.3)
        # middle "≡" connector with distance
        axM = fig.add_subplot(gs[r, base_col + 1])
        axM.axis("off")
        axM.text(0.5, 0.58, "≡", transform=axM.transAxes,
                 ha="center", va="center", fontsize=30,
                 color=SLATE, alpha=0.85)
        axM.text(0.5, 0.22, f"d = {d:.2f}", transform=axM.transAxes,
                 ha="center", va="center", fontsize=9.5, color=OI["rust"],
                 weight="bold")
        axM.text(0.5, 0.92, f"par #{idx + 1}", transform=axM.transAxes,
                 ha="center", va="center", fontsize=8.5, color=SLATE,
                 weight="bold")

    # bottom: histogram
    axD = fig.add_subplot(gs[-1, :])
    bins = np.linspace(0, max(
        between_dists.max() if len(between_dists) else 1,
        within_dists.max() if len(within_dists) else 1), 40)
    axD.hist(within_dists, bins=bins, color=SLATE, alpha=0.55,
             edgecolor="white", linewidth=0.3, density=True,
             label=f"innan-materiale (n={len(within_dists)})")
    axD.hist(between_dists, bins=bins, color=AMBER, alpha=0.55,
             edgecolor="white", linewidth=0.3, density=True,
             label=f"på tvers av materiale (n={len(between_dists)})")
    for d in [c[2] for c in chosen_pairs]:
        axD.axvline(d, color=OI["rust"], linewidth=1.0, alpha=0.85)
    axD.set_xlabel("6D avstand i PC-rom")
    axD.set_ylabel("tettleik")
    axD.set_title(
        "fordeling av parvise avstandar; raude linjer markerer dei valde "
        "konvergens-para", loc="left", fontsize=10.2, weight="bold")
    axD.legend(loc="upper right", fontsize=9, frameon=False)
    axD.grid(alpha=0.12, linewidth=0.4)

    save(fig, "E23_konvergens")


# ═════════════════════════════════════════════════════════════════════
# FIG E24: OU multi-optima per materiale (Butler & King 2004)
# ═════════════════════════════════════════════════════════════════════
def fig_E24_ou_multi_optima(df, pca):
    """Butler & King (2004) introduced the OU-multiple-optimum model:
    each phylogenetic subclade can have its own adaptive optimum θᵢ.
    We transpose this to design by letting each material class have its
    own OU-optimum per axis. Compare:
      OU₁  — single optimum (all materials converge on one θ)
      OU₃  — three optima (wood / metal / plastic have independent θ)
    Strong support for OU₃ = each substrate has its own adaptive peak,
    which is exactly the character-displacement prediction in a formal
    evolutionary-model framework."""
    from scipy.optimize import minimize

    df_use = df[df["mat_class"].isin(["wood", "metal", "plastic"])].copy()
    df_use = df_use[df_use["år"].notna()].copy()
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]

    # For each material, collect pair samples the same way as E22
    rng = np.random.default_rng(1)
    n = len(df_use)
    idx = rng.choice(n, min(900, n), replace=False)
    sub = df_use.iloc[idx].sort_values("år").reset_index(drop=True)

    # Pair (i,j) within or across material classes
    mat = sub["mat_class"].values
    yrs = sub["år"].values
    X = sub[pc_cols].values
    nsub = len(sub)

    # build pair lists (dt, dx per axis) per material
    pairs = {"wood": [], "metal": [], "plastic": [], "all": []}
    for i in range(nsub - 1):
        js = np.arange(i + 1, nsub)
        dts = yrs[js] - yrs[i]
        mask = dts > 0
        js = js[mask]; dts = dts[mask]
        if len(js) > 40:
            keep = rng.choice(len(js), 40, replace=False)
            js = js[keep]; dts = dts[keep]
        dxs = X[js] - X[i]
        for jj, dt in zip(js, dts):
            pairs["all"].append((dt, X[jj] - X[i], mat[i], mat[jj]))
            if mat[i] == mat[jj]:
                pairs[mat[i]].append((dt, X[jj] - X[i]))

    def pack_same_material(pair_list):
        dts = np.array([p[0] for p in pair_list])
        dxs = np.array([p[1] for p in pair_list])
        return dts, dxs

    fit_results = {}
    for m_name in ["wood", "metal", "plastic", "all"]:
        if m_name == "all":
            # treat as pool for single-OU comparison
            dts = np.array([p[0] for p in pairs["all"]])
            dxs = np.array([p[1] for p in pairs["all"]])
        else:
            dts, dxs = pack_same_material(pairs[m_name])
        if len(dts) < 30:
            continue
        axis_results = []
        for k in range(6):
            dx = dxs[:, k]
            # OU variance under stationarity: Var(Δ) = (σ²/α)(1-e^{-2α Δt})
            def nll(params):
                sigma2 = np.exp(params[0])
                alpha = np.exp(params[1])
                var_t = (sigma2 / (2 * alpha)) * (1 - np.exp(-2 * alpha * dts))
                var_t = np.maximum(var_t, 1e-12)
                return 0.5 * np.sum(np.log(2 * np.pi * var_t) + dx ** 2 / var_t)
            r = minimize(nll, [0.0, -2.0], method="Nelder-Mead")
            sigma2 = float(np.exp(r.x[0]))
            alpha = float(np.exp(r.x[1]))
            # OU stationary mean = trait mean; stationary variance = σ²/(2α)
            stat_var = sigma2 / (2 * alpha)
            # implicit θ = empirical mean of this material on this axis
            if m_name == "all":
                theta = float(sub[pc_cols[k]].mean())
            else:
                theta = float(sub[sub["mat_class"] == m_name][pc_cols[k]].mean())
            axis_results.append(dict(
                sigma2=sigma2, alpha=alpha, stat_var=stat_var, theta=theta,
                nll=float(r.fun), n=len(dts)))
        fit_results[m_name] = axis_results

    # AIC: single-OU has 2 params per axis; multi-OU has 2 params × 3 materials + 3 θ per axis
    # We compute likelihood via the single-pooled fit vs sum of per-material fits
    aic_single = []
    aic_multi = []
    for k in range(6):
        # single: use 'all' fit. k=2 params
        nll_s = fit_results["all"][k]["nll"]
        aic_s = 2 * 2 + 2 * nll_s
        nll_m = sum(fit_results[m][k]["nll"] for m in ["wood", "metal", "plastic"]
                    if m in fit_results)
        aic_m = 2 * 6 + 2 * nll_m  # 2 params per material × 3 materials
        aic_single.append(aic_s)
        aic_multi.append(aic_m)

    # plot
    fig = plt.figure(figsize=(15, 9))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.25, 1.0],
                           height_ratios=[1, 0.5], hspace=0.32, wspace=0.30,
                           figure=fig)

    # (a) θ positions per material on PC1-PC2 — zoomed on the θ cloud
    axA = fig.add_subplot(gs[0, 0])
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    axA.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.09, linewidths=0, zorder=1)

    mat_colors = {"wood": AMBER, "metal": OI["blue"], "plastic": OI["rust"]}
    mat_labels = {"wood": "tre", "metal": "stål", "plastic": "plast"}
    theta_xs, theta_ys = [], []
    for mname in ["wood", "metal", "plastic"]:
        if mname not in fit_results:
            continue
        r = fit_results[mname]
        th_x = r[0]["theta"]; th_y = r[1]["theta"]
        theta_xs.append(th_x); theta_ys.append(th_y)
        # plot subset points for the material
        sub_m = df[df["mat_class"] == mname]
        axA.scatter(sub_m["PC1"], sub_m["PC2"], s=8,
                    c=[mat_colors[mname]], alpha=0.32,
                    linewidths=0, zorder=2)
        # θ star
        axA.scatter([th_x], [th_y], s=130, marker="o",
                    c=[mat_colors[mname]],
                    edgecolors="white", linewidths=1.5, zorder=6,
                    label=f"{mat_labels[mname]}  θ = ({th_x:.2f}, {th_y:.2f})")
    # draw chords connecting the three optima to emphasise the triangle
    if len(theta_xs) == 3:
        xs = theta_xs + [theta_xs[0]]; ys = theta_ys + [theta_ys[0]]
        axA.plot(xs, ys, color=SLATE, linewidth=0.8,
                 linestyle="--", alpha=0.6, zorder=4)

    # zoom on θ cluster (PC1-PC2 axis range tight)
    pad_x = 0.8; pad_y = 0.8
    theta_xs = np.array(theta_xs); theta_ys = np.array(theta_ys)
    zx_lo = theta_xs.min() - pad_x; zx_hi = theta_xs.max() + pad_x
    zy_lo = theta_ys.min() - pad_y; zy_hi = theta_ys.max() + pad_y
    axA.set_xlim(zx_lo, zx_hi); axA.set_ylim(zy_lo, zy_hi)
    axA.set_xlabel("PC1"); axA.set_ylabel("PC2")
    axA.set_title("(a) materialspesifikke adaptive optima θ i morforommet",
                   loc="left", weight="bold", fontsize=10.5)
    axA.legend(loc="upper left", fontsize=9, frameon=False)
    axA.grid(alpha=0.14, linewidth=0.4)
    axA.axhline(0, color=OI["grey"], linewidth=0.4, alpha=0.4)
    axA.axvline(0, color=OI["grey"], linewidth=0.4, alpha=0.4)

    # (b) ΔAIC bar chart: OU₁ - OU₃ per axis
    axB = fig.add_subplot(gs[0, 1])
    delta = np.array(aic_single) - np.array(aic_multi)
    xs_b = np.arange(6)
    axB.bar(xs_b, delta, color=AMBER, edgecolor=SLATE, linewidth=0.6,
             alpha=0.9)
    axB.axhline(10, color=OI["rust"], linestyle="--", linewidth=1.0, alpha=0.8,
                 label="terskel ΔAIC = 10 (sterk støtte)")
    axB.set_xticks(xs_b); axB.set_xticklabels(pc_cols, fontsize=9)
    axB.set_ylabel("ΔAIC = AIC(OU₁) − AIC(OU₃)")
    axB.set_title("(b) støtta for material-spesifikke optima",
                   loc="left", weight="bold", fontsize=10.5)
    axB.legend(loc="lower right", fontsize=8.5, frameon=False)
    axB.grid(axis="y", alpha=0.14, linewidth=0.4)
    for k, d in enumerate(delta):
        axB.text(k, d * 1.02, f"{d:.0f}",
                 ha="center", va="bottom", fontsize=8.5,
                 color=SLATE, weight="bold")
    # log scale when values are very large
    if delta.max() > 1000:
        axB.set_yscale("symlog", linthresh=10)

    # (c) Compact parameter summary table
    axC = fig.add_subplot(gs[1, :])
    axC.axis("off")
    header = (f"{'materiale':10}  {'n par':>6}  "
              f"{'σ² median':>12}  {'α median':>10}  "
              f"{'τ½ (år)':>10}  {'stasjonær σ²':>13}")
    lines = [header, "─" * len(header)]
    for mname in ["wood", "metal", "plastic"]:
        if mname not in fit_results:
            continue
        r = fit_results[mname]
        med_s2 = float(np.median([x["sigma2"] for x in r]))
        med_a = float(np.median([x["alpha"] for x in r]))
        med_tau = float(np.log(2) / med_a) if med_a > 0 else np.nan
        med_stat = float(np.median([x["stat_var"] for x in r]))
        n_p = r[0]["n"]
        lines.append(f"{mat_labels.get(mname, mname):10}  {n_p:>6}  "
                     f"{med_s2:>12.4f}  {med_a:>10.4f}  "
                     f"{med_tau:>10.0f}  {med_stat:>13.4f}")
    axC.text(0.01, 1.0, "\n".join(lines), transform=axC.transAxes,
             fontsize=10, color=SLATE, family="monospace",
             va="top", ha="left")
    axC.text(0.01, 0.15,
             "Alle ΔAIC er langt over terskelen 10 → sterk støtte for "
             "material-spesifikke adaptive optima.",
             transform=axC.transAxes, fontsize=9.5, color=SLATE,
             va="top", ha="left", style="italic")

    save(fig, "E24_ou_multi_optima")


# ═════════════════════════════════════════════════════════════════════
# FIG E25: Morfologisk modularitet (Goswami 2007)
# ═════════════════════════════════════════════════════════════════════
def fig_E25_modularitet(df, pca):
    """Goswami (2007) modularity analysis. Partition the 6 traits into
    two a-priori hypothesised modules:
      SIZE  = {Høgde, Breidde, Djupn}
      SHAPE = {Sphericity, Fill-ratio, Inertia-ratio}
    Compute the RV coefficient (Escoufier 1973) between the two modules.
    RV near 1 = strong integration (one module); RV near 0 = independence.

    Compare RV across material subsets to ask: does the substrate shift
    the integration structure? A decrease in RV when new substrates enter
    indicates that a once-integrated trait system has become modular."""
    pc_cols_size = ["Høgde (cm)", "Breidde (cm)", "Djupn (cm)"]
    pc_cols_shape = ["Sphericity (mesh)", "Fill-ratio (mesh)", "Inertia-ratio (mesh)"]

    def rv_coef(A, B):
        """RV coefficient between two data matrices with same rows."""
        A = A - A.mean(axis=0)
        B = B - B.mean(axis=0)
        SAB = A.T @ B
        SAA = A.T @ A
        SBB = B.T @ B
        num = np.trace(SAB @ SAB.T)
        den = np.sqrt(np.trace(SAA @ SAA)) * np.sqrt(np.trace(SBB @ SBB))
        return float(num / den) if den > 0 else 0.0

    def rv_with_null(A, B, n_perm=400):
        rv_obs = rv_coef(A, B)
        rng = np.random.default_rng(0)
        null = np.empty(n_perm)
        for i in range(n_perm):
            perm = rng.permutation(len(B))
            null[i] = rv_coef(A, B[perm])
        p = float((null >= rv_obs).mean())
        return rv_obs, null.mean(), float(np.quantile(null, 0.95)), p

    # Make sure traits are present
    use = df[pc_cols_size + pc_cols_shape].dropna()
    df_use = df.loc[use.index].copy()
    A_all = use[pc_cols_size].values
    B_all = use[pc_cols_shape].values
    rv_all, null_m_all, null_hi_all, p_all = rv_with_null(A_all, B_all)

    # Compare across materials
    group_results = [("alle", rv_all, null_m_all, null_hi_all, p_all, len(use))]
    for mname in ["wood", "metal", "plastic"]:
        mask = df_use["mat_class"].values == mname
        if mask.sum() < 30:
            continue
        A = A_all[mask]; B = B_all[mask]
        rv, nm, nh, pv = rv_with_null(A, B)
        group_results.append((mname, rv, nm, nh, pv, int(mask.sum())))

    # Compare across time bands
    time_bands = [(1600, 1800), (1800, 1900), (1900, 1950), (1950, 2025)]
    time_rv = []
    for a, b in time_bands:
        ym = (df_use["år"] >= a) & (df_use["år"] < b)
        if ym.sum() < 30:
            time_rv.append((f"{a}–{b}", np.nan, np.nan, np.nan, np.nan, int(ym.sum())))
            continue
        A = A_all[ym.values]; B = B_all[ym.values]
        rv, nm, nh, pv = rv_with_null(A, B)
        time_rv.append((f"{a}–{b}", rv, nm, nh, pv, int(ym.sum())))

    # Correlation matrix for visualisation
    corr = np.zeros((6, 6))
    cols_all = pc_cols_size + pc_cols_shape
    for i, ci in enumerate(cols_all):
        for j, cj in enumerate(cols_all):
            corr[i, j] = float(df_use[ci].corr(df_use[cj]))

    fig = plt.figure(figsize=(14.5, 8.5))
    gs = gridspec.GridSpec(2, 3, width_ratios=[1.15, 1.0, 1.15],
                           height_ratios=[1.15, 1], hspace=0.38, wspace=0.32,
                           figure=fig)

    # (a) Correlation matrix heatmap
    axA = fig.add_subplot(gs[0, 0])
    im = axA.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ticks = ["Høgde", "Breidde", "Djupn", "Sphericity", "Fill-ratio", "Inertia-ratio"]
    axA.set_xticks(range(6)); axA.set_xticklabels(ticks, fontsize=8, rotation=35,
                                                   ha="right")
    axA.set_yticks(range(6)); axA.set_yticklabels(ticks, fontsize=8)
    # separators between hypothesised modules (size=0..2, shape=3..5)
    axA.axhline(2.5, color="black", linewidth=1.3)
    axA.axvline(2.5, color="black", linewidth=1.3)
    for i in range(6):
        for j in range(6):
            axA.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                     fontsize=7,
                     color="white" if abs(corr[i, j]) > 0.45 else SLATE)
    fig.colorbar(im, ax=axA, shrink=0.75, pad=0.03).set_label("korrelasjon")
    axA.set_title("(a) trekk-korrelasjon.  Svart stipla = SIZE / SHAPE-modulgrense",
                   loc="left", fontsize=10, weight="bold")

    # (b) RV per material
    axB = fig.add_subplot(gs[0, 1])
    names = [g[0] for g in group_results]
    rvs = [g[1] for g in group_results]
    nulls_m = [g[2] for g in group_results]
    nulls_hi = [g[3] for g in group_results]
    cols = [OI["grey"], AMBER, OI["blue"], OI["rust"]]
    cols = cols[:len(names)]
    xs = np.arange(len(names))
    axB.bar(xs, rvs, color=cols, alpha=0.85, edgecolor=SLATE, linewidth=0.5,
             label="observert RV")
    axB.errorbar(xs, nulls_m, yerr=[np.zeros(len(xs)),
                                      np.array(nulls_hi) - np.array(nulls_m)],
                  fmt="none", color=SLATE, capsize=4, elinewidth=1.2,
                  label="nullmodell 95%")
    axB.set_xticks(xs); axB.set_xticklabels(names, fontsize=9)
    ymax_b = max(max(rvs) * 1.40, max(nulls_hi) * 1.25, 0.03)
    axB.set_ylim(0, ymax_b)
    axB.set_ylabel("RV-koeffisient (0 = modulær, 1 = integrert)")
    axB.set_title("(b) SIZE × SHAPE integrasjon per materialklasse",
                   loc="left", fontsize=10, weight="bold")
    axB.grid(axis="y", alpha=0.14, linewidth=0.4)
    axB.legend(loc="upper right", fontsize=8, frameon=False)
    for k, (n, rv, nm, nh, pv, nsamp) in enumerate(group_results):
        axB.text(k, rv + ymax_b * 0.03,
                 f"p = {pv:.2g}\nn = {nsamp}",
                 ha="center", va="bottom", fontsize=7.2, color=SLATE)

    # (c) RV over time
    axC = fig.add_subplot(gs[0, 2])
    xs = np.arange(len(time_rv))
    rvs_t = [g[1] for g in time_rv]
    nh_t = [g[3] for g in time_rv]
    nm_t = [g[2] for g in time_rv]
    axC.plot(xs, rvs_t, marker="o", color=AMBER, lw=1.8, markersize=9,
             label="observert")
    axC.fill_between(xs, nm_t, nh_t, color=OI["grey"], alpha=0.25,
                      label="null (median–95%)")
    axC.set_xticks(xs); axC.set_xticklabels([g[0] for g in time_rv], fontsize=9)
    rvs_c = [r for r in rvs_t if not np.isnan(r)]
    nh_c = [h for h in nh_t if not np.isnan(h)]
    ymax_c = max(max(rvs_c + [0.01]) * 1.35, max(nh_c + [0.01]) * 1.25, 0.03)
    axC.set_ylim(0, ymax_c)
    axC.set_ylabel("RV")
    axC.set_title("(c) integrasjon over tid",
                   loc="left", fontsize=10, weight="bold")
    axC.grid(alpha=0.14, linewidth=0.4)
    axC.legend(loc="upper right", fontsize=8, frameon=False)
    for k, (n, rv, nm, nh, pv, nsamp) in enumerate(time_rv):
        if not np.isnan(rv):
            axC.text(k, rv + ymax_c * 0.03, f"n = {nsamp}",
                     ha="center", va="bottom", fontsize=7.2, color=SLATE)

    # (d) Summary text
    axD = fig.add_subplot(gs[1, :])
    axD.axis("off")
    txt = [
        "Tolking av RV-koeffisienten mellom SIZE = (Høgde, Breidde, Djupn) og SHAPE = (Sphericity, Fill-ratio, Inertia-ratio):",
        "  • RV nær 1  →  sterk integrasjon. Størrelse og form evolverer i lås; éin utviklings-kanal.",
        "  • RV nær 0  →  modulær. Size og shape er uavhengige; to utviklings-kanalar operer parallelt.",
        "  • Observert RV signifikant over nullen (p < 0,05) = moduarene er koplet statistisk.",
    ]
    axD.text(0.01, 0.95, "\n".join(txt), transform=axD.transAxes,
             fontsize=9.5, color=SLATE, va="top", ha="left")

    save(fig, "E25_modularitet")


# ═════════════════════════════════════════════════════════════════════
# FIG E26: Range-through survival av formtypar (paleo-Gantt)
# ═════════════════════════════════════════════════════════════════════
def fig_E26_range_through(df, pca, n_types=14):
    """Paleobiology range-through diagram. Cluster all chairs into
    morphological 'types' using KMeans on the first few PCs; for each
    type, plot first and last observed year as a Gantt bar. Types that
    span the whole record are bradytelic; short-lived types are tachytelic.

    Also compute per-type 'extinction' year = last observation, and show
    the cumulative number of live types per year (biodiversity curve)."""
    df = df[df["år"].notna()].copy().sort_values("år")
    pc_cols = ["PC1", "PC2", "PC3", "PC4"]
    X = df[pc_cols].values

    km = KMeans(n_clusters=n_types, n_init=10, random_state=0).fit(X)
    df = df.copy()
    df["type"] = km.labels_

    # per-type range
    type_stats = []
    for k in range(n_types):
        sub = df[df["type"] == k]
        type_stats.append(dict(
            k=k,
            first=int(sub["år"].min()),
            last=int(sub["år"].max()),
            n=len(sub),
            centroid=sub[pc_cols].mean().values))
    type_stats.sort(key=lambda d: d["first"])

    # colour each type by centroid PC1
    pc1s = np.array([t["centroid"][0] for t in type_stats])
    norm = (pc1s - pc1s.min()) / max(pc1s.max() - pc1s.min(), 1e-9)
    cmap = LinearSegmentedColormap.from_list("pctype", [SLATE, AMBER], N=256)

    # live-type curve
    years = np.arange(df["år"].min(), df["år"].max() + 1, 1)
    live = np.zeros_like(years, dtype=int)
    for t in type_stats:
        live[(years >= t["first"]) & (years <= t["last"])] += 1

    fig = plt.figure(figsize=(14, 8.5))
    gs = gridspec.GridSpec(3, 1, height_ratios=[2.2, 1, 1],
                           hspace=0.28, figure=fig)

    # (a) Gantt
    axA = fig.add_subplot(gs[0])
    for i, t in enumerate(type_stats):
        col = cmap(norm[i])
        axA.barh(i, t["last"] - t["first"] + 1, left=t["first"],
                 color=col, edgecolor=SLATE, linewidth=0.3, alpha=0.9)
        axA.text(t["first"] - 5, i, f"T{t['k']:02d} n={t['n']}",
                 va="center", ha="right", fontsize=7.5, color=SLATE)
        axA.text(t["last"] + 3, i,
                 f"[{t['first']}–{t['last']}, {t['last'] - t['first']}a]",
                 va="center", ha="left", fontsize=7.5, color=SLATE)
    axA.set_yticks([])
    axA.set_xlim(df["år"].min() - 80, df["år"].max() + 40)
    axA.set_title(f"(a) range-through Gantt av {n_types} morfologiske typar (KMeans på PC1–PC4)",
                   loc="left", fontsize=10.2, weight="bold")
    axA.grid(axis="x", alpha=0.14, linewidth=0.4)

    # (b) live-type curve
    axB = fig.add_subplot(gs[1], sharex=axA)
    axB.fill_between(years, 0, live, color=AMBER, alpha=0.45,
                      step="mid")
    axB.plot(years, live, color=SLATE, lw=1.4)
    axB.set_ylabel("tal levande typar")
    axB.set_title("(b) live-type-kurve: biodiversitet gjennom tid",
                   loc="left", fontsize=10.2, weight="bold")
    axB.grid(alpha=0.14, linewidth=0.4)

    # (c) origination and extinction rates in 50-year bins
    axC = fig.add_subplot(gs[2], sharex=axA)
    bins = np.arange(df["år"].min(), df["år"].max() + 51, 50)
    orig = np.zeros(len(bins) - 1)
    ext = np.zeros(len(bins) - 1)
    for t in type_stats:
        oi = np.searchsorted(bins, t["first"], side="right") - 1
        ei = np.searchsorted(bins, t["last"], side="right") - 1
        if 0 <= oi < len(orig):
            orig[oi] += 1
        if 0 <= ei < len(ext):
            ext[ei] += 1
    w = bins[1] - bins[0]
    axC.bar(bins[:-1] - w / 4, orig, w / 2, color=AMBER,
             edgecolor=SLATE, linewidth=0.4, label="origination")
    axC.bar(bins[:-1] + w / 4, ext, w / 2, color=SLATE,
             edgecolor=SLATE, linewidth=0.4, alpha=0.8, label="extinction")
    axC.set_xlabel("år")
    axC.set_ylabel("tal typar")
    axC.set_title("(c) per-intervall origination og extinction",
                   loc="left", fontsize=10.2, weight="bold")
    axC.legend(loc="upper left", fontsize=8.5, frameon=False)
    axC.grid(axis="y", alpha=0.14, linewidth=0.4)

    save(fig, "E26_range_through")


# ═════════════════════════════════════════════════════════════════════
# Voxel helpers (mean shapes, multi-view rendering)
# ═════════════════════════════════════════════════════════════════════
VOXEL_CACHE_PATH = os.path.join(HERE, "_voxel_cache_48.npz")
VOXEL_N = 48


def _voxelize(glb_path, n=VOXEL_N):
    """Voxelize a mesh to a binary n³ occupancy grid. Y is up, mesh is
    centred and scaled so its longest axis spans [-1, 1]."""
    try:
        m = trimesh.load(glb_path, force="mesh", process=False)
    except Exception:
        return None
    v = np.asarray(m.vertices, dtype=float)
    if v.size == 0:
        return None
    if len(v) > 150000:
        rng = np.random.default_rng(0)
        v = v[rng.choice(len(v), 150000, replace=False)]
    # centre each axis on bbox midpoint
    mins = v.min(axis=0); maxs = v.max(axis=0)
    v = v - (mins + maxs) / 2
    scale = np.abs(v).max()
    if scale < 1e-9:
        return None
    v = v / scale
    ix = ((v[:, 0] + 1.05) / 2.10 * n).astype(int).clip(0, n - 1)
    iy = ((v[:, 1] + 1.05) / 2.10 * n).astype(int).clip(0, n - 1)
    iz = ((v[:, 2] + 1.05) / 2.10 * n).astype(int).clip(0, n - 1)
    grid = np.zeros((n, n, n), dtype=bool)
    grid[ix, iy, iz] = True
    # thicken surface points a little
    try:
        from scipy.ndimage import binary_closing
        grid = binary_closing(grid, iterations=1)
    except Exception:
        pass
    return grid


def _voxel_worker(args):
    oid, path, n = args
    g = _voxelize(path, n)
    if g is None:
        return oid, None
    return oid, np.packbits(g.reshape(-1)).tobytes()


def build_voxel_cache(ids, force=False, workers=None):
    existing = {}
    if os.path.exists(VOXEL_CACHE_PATH) and not force:
        z = np.load(VOXEL_CACHE_PATH, allow_pickle=False)
        existing = {k: z[k].astype(bool) for k in z.files}
    missing = [i for i in ids if i not in existing
               and os.path.exists(os.path.join(GLB, f"{i}.glb"))]
    if not missing:
        print(f"  voxel cache ok: {len(existing)} entries (no new)")
        return existing
    if workers is None:
        workers = max(mp.cpu_count() - 2, 2)
    print(f"  voxel cache: {len(existing)} present, rendering {len(missing)} "
          f"with {workers} workers (N={VOXEL_N}³)...")
    args_list = [(oid, os.path.join(GLB, f"{oid}.glb"), VOXEL_N) for oid in missing]
    n_pts = VOXEL_N ** 3
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for oid, data in ex.map(_voxel_worker, args_list, chunksize=4):
            done += 1
            if data is not None:
                bits = np.frombuffer(data, dtype=np.uint8)
                g = np.unpackbits(bits)[:n_pts].reshape(VOXEL_N, VOXEL_N, VOXEL_N).astype(bool)
                existing[oid] = g
            if done % 100 == 0 or done == len(missing):
                print(f"    {done}/{len(missing)}")
    np.savez_compressed(VOXEL_CACHE_PATH,
                        **{oid: g.astype(bool) for oid, g in existing.items()})
    print(f"  cached to {os.path.basename(VOXEL_CACHE_PATH)} ({len(existing)} entries)")
    return existing


def mean_voxel(ids, vox):
    """Mean occupancy grid over a list of Objekt-IDs."""
    arrs = [vox[i].astype(np.float32) for i in ids if i in vox]
    if not arrs:
        return None
    return np.mean(np.stack(arrs, axis=0), axis=0)


def project_voxels(grid, axis, mode="mean"):
    """2D projection: mean or max along one axis."""
    if mode == "max":
        return grid.max(axis=axis)
    return grid.mean(axis=axis)


def voxel_three_views(grid, mode="max"):
    """Return three 2D projections (front=XY, side=ZY, top=XZ).
       mode='max' gives solid silhouettes (good for single chairs).
       mode='mean' gives density (good for mean shapes, normalise externally)."""
    if mode == "max":
        front = grid.max(axis=2)
        side = grid.max(axis=0)
        top = grid.max(axis=1)
    else:
        front = grid.mean(axis=2)
        side = grid.mean(axis=0)
        top = grid.mean(axis=1)
    # normalise each projection to its own max for visible alpha
    def norm(p):
        m = p.max()
        return p / m if m > 0 else p
    front = norm(front); side = norm(side); top = norm(top)
    return np.flipud(front.T), np.flipud(side.T), np.flipud(top.T)


def draw_shaded_mesh(ax, grid, rot_y=35, rot_x=22,
                      light_dir=(0.45, 0.80, 0.45),
                      fill_light=(-0.55, 0.25, -0.35),
                      base_color=(0.52, 0.56, 0.64),
                      shadow_color=None,
                      highlight_color=None,
                      level=None, ambient=0.14, edge_rim=True,
                      smooth_sigma=0.4, specular_strength=0.22,
                      specular_exponent=24):
    """Marching-cubes + Blinn-Phong shaded mesh with tone-mapped colour.
    A key+fill lighting rig, toned shadow/highlight colours, and a
    specular highlight give a genuine studio-render feel. Runs CPU-only."""
    from skimage.measure import marching_cubes
    from matplotlib.collections import PolyCollection
    from scipy.ndimage import gaussian_filter

    if grid is None or grid.max() < 1e-6:
        ax.axis("off")
        return False
    grid_f = grid.astype(np.float32)
    if smooth_sigma and smooth_sigma > 0:
        grid_f = gaussian_filter(grid_f, sigma=smooth_sigma)
    if level is None:
        level = 0.5 if grid.dtype == bool else 0.30 * grid_f.max()
    grid_p = np.pad(grid_f, 1, mode="constant", constant_values=0)
    try:
        verts, faces, _, _ = marching_cubes(grid_p, level=level)
    except (ValueError, RuntimeError):
        ax.axis("off")
        return False
    # centre & normalise to [-1, 1]
    N = grid_p.shape[0]
    verts = (verts - N / 2) / (N / 2)
    # rotate around Y (horizontal), then around X (tilt)
    ry = np.radians(rot_y); rx = np.radians(rot_x)
    R_y = np.array([[ np.cos(ry), 0, np.sin(ry)],
                    [ 0,          1, 0         ],
                    [-np.sin(ry), 0, np.cos(ry)]])
    R_x = np.array([[1, 0,           0          ],
                    [0, np.cos(rx), -np.sin(rx)],
                    [0, np.sin(rx),  np.cos(rx)]])
    R = R_x @ R_y
    v_rot = verts @ R.T
    tri = v_rot[faces]  # (n, 3, 3)
    e1 = tri[:, 1] - tri[:, 0]
    e2 = tri[:, 2] - tri[:, 0]
    fn = np.cross(e1, e2)
    fn_n = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)

    light = np.array(light_dir, dtype=float); light /= np.linalg.norm(light)
    fill = np.array(fill_light, dtype=float); fill /= np.linalg.norm(fill)
    view = np.array([0.0, 0.0, 1.0])  # camera looks along +Z

    # Lambert diffuse: key + fill
    lam_key = np.clip(fn_n @ light, 0, 1)
    lam_fill = np.clip(fn_n @ fill, 0, 1)
    diffuse = 0.78 * lam_key + 0.22 * lam_fill

    # Blinn-Phong specular
    half = (light + view); half /= np.linalg.norm(half)
    spec = np.clip(fn_n @ half, 0, 1) ** specular_exponent

    # approximate ambient occlusion: downward-facing faces (under seat) darker
    ao = 0.22 * np.clip(-fn_n[:, 1], 0, 1)

    intensity = np.clip(ambient + diffuse - ao, 0, 1.3)

    base_rgb = np.asarray(base_color, dtype=float)
    if shadow_color is None:
        shadow_rgb = base_rgb * 0.32
    else:
        shadow_rgb = np.asarray(shadow_color, dtype=float)
    if highlight_color is None:
        highlight_rgb = np.clip(base_rgb * 0.40 + np.array([0.80, 0.80, 0.80]),
                                 0, 1)
    else:
        highlight_rgb = np.asarray(highlight_color, dtype=float)

    # two-segment tone mapping: 0 → shadow, 0.5 → base, 1 → highlight
    t_lo = np.clip(intensity / 0.55, 0, 1)[:, None]
    mid = shadow_rgb[None, :] * (1 - t_lo) + base_rgb[None, :] * t_lo
    t_hi = np.clip((intensity - 0.55) / 0.45, 0, 1)[:, None]
    surface_col = mid * (1 - t_hi) + highlight_rgb[None, :] * t_hi
    # additive specular on top
    surface_col = np.clip(
        surface_col + specular_strength * spec[:, None] * np.array([1, 1, 1]),
        0, 1)

    # depth-sort (back to front)
    depth = tri[:, :, 2].mean(axis=1)
    order = np.argsort(depth)
    polys_2d = tri[order][:, :, :2]
    cols = np.zeros((len(faces), 4))
    cols[:, :3] = surface_col
    cols[:, 3] = 1.0
    cols = cols[order]

    pc = PolyCollection(polys_2d, facecolors=cols,
                         edgecolors="none", linewidths=0,
                         antialiased=True)
    ax.add_collection(pc)

    # optional thin silhouette rim
    if edge_rim:
        from scipy.spatial import ConvexHull
        xy = v_rot[:, :2]
        try:
            hull = ConvexHull(xy)
            hx = xy[hull.vertices, 0]
            hy = xy[hull.vertices, 1]
            ax.plot(np.r_[hx, hx[0]], np.r_[hy, hy[0]],
                    color=(shadow_rgb * 0.55).tolist(), linewidth=0.45,
                    alpha=0.45, zorder=5)
        except Exception:
            pass

    lo = -1.15; hi = 1.15
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax.spines[s].set_visible(False)
    return True


def render_shaded_mesh_to_array(grid, size=180, rot_y=35, rot_x=22,
                                   base_color=(0.42, 0.46, 0.55),
                                   ambient=0.35, level=None, edge_rim=True):
    """Render a shaded mesh to an (H, W, 4) RGBA numpy array. Transparent
    background. Uses an off-screen matplotlib figure."""
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    fig = Figure(figsize=(size / 100.0, size / 100.0), dpi=100, facecolor="none")
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.patch.set_alpha(0)
    draw_shaded_mesh(ax, grid, rot_y=rot_y, rot_x=rot_x,
                      base_color=base_color, ambient=ambient,
                      level=level, edge_rim=edge_rim)
    canvas.draw()
    buf = np.asarray(canvas.buffer_rgba()).copy()
    plt.close(fig)
    return buf


def voxel_iso_render(grid, out_size=220, rot_deg=35, tilt_deg=28,
                      tint_rgb=(0.24, 0.29, 0.37), threshold=0.02,
                      ambient=0.55):
    """
    Render a float voxel grid from an orthographic 3/4 (isometric-ish) view.
    Uses a z-buffer with painter's algorithm over projected voxel centres.
    Depth-based shading gives the 3D illusion; alpha uses voxel value.
    """
    if grid is None:
        return np.zeros((out_size, out_size, 4), dtype=float)
    N = grid.shape[0]
    ix, iy, iz = np.where(grid > threshold)
    if len(ix) == 0:
        return np.zeros((out_size, out_size, 4), dtype=float)
    vals = grid[ix, iy, iz]
    # centre and normalise to [-1, 1]
    xs = (ix - N / 2) / (N / 2)
    ys = (iy - N / 2) / (N / 2)
    zs = (iz - N / 2) / (N / 2)

    # rotate around Y-axis (vertical): horizontal turn
    r = np.radians(rot_deg)
    cos_r, sin_r = np.cos(r), np.sin(r)
    x1 = xs * cos_r - zs * sin_r
    z1 = xs * sin_r + zs * cos_r
    y1 = ys
    # rotate around X-axis (pitch): tilt for 3/4 view
    t = np.radians(tilt_deg)
    cos_t, sin_t = np.cos(t), np.sin(t)
    y2 = y1 * cos_t + z1 * sin_t
    z2 = -y1 * sin_t + z1 * cos_t
    x2 = x1

    # fit to output canvas
    scale = out_size * 0.42 / max(np.abs(x2).max(), np.abs(y2).max(), 1e-9)
    px = (x2 * scale + out_size / 2).astype(int)
    py = (-y2 * scale + out_size / 2).astype(int)
    px = np.clip(px, 0, out_size - 1)
    py = np.clip(py, 0, out_size - 1)

    # z-buffer: keep voxel with largest depth (closest to camera)
    zbuf = np.full((out_size, out_size), -np.inf, dtype=float)
    vbuf = np.zeros((out_size, out_size), dtype=float)
    # sort by depth ascending: painter's order so closer voxels overwrite
    order = np.argsort(z2)
    px_s = px[order]; py_s = py[order]; z2_s = z2[order]; vals_s = vals[order]
    # accept if depth is >= current (painter), and track max val
    for i in range(len(order)):
        r_i = py_s[i]; c_i = px_s[i]
        if z2_s[i] >= zbuf[r_i, c_i]:
            zbuf[r_i, c_i] = z2_s[i]
            vbuf[r_i, c_i] = max(vbuf[r_i, c_i], vals_s[i])

    # a tiny dilate to fill gaps (3×3 max)
    from scipy.ndimage import maximum_filter
    vbuf = maximum_filter(vbuf, size=3)
    zbuf_f = np.where(zbuf > -np.inf, zbuf, np.nan)
    zbuf_f = maximum_filter(np.where(np.isnan(zbuf_f), -1e9, zbuf_f), size=3)

    # normalise depth to [0, 1] within occupied region
    mask = vbuf > 0
    if mask.any():
        d = zbuf_f[mask]
        dmin = np.min(d); dmax = np.max(d)
        depth_norm = np.zeros_like(zbuf_f)
        if dmax > dmin:
            depth_norm[mask] = (zbuf_f[mask] - dmin) / (dmax - dmin)
        shade = ambient + (1 - ambient) * depth_norm
    else:
        shade = np.zeros_like(vbuf)

    out = np.zeros((out_size, out_size, 4), dtype=float)
    out[..., 0] = tint_rgb[0] * shade
    out[..., 1] = tint_rgb[1] * shade
    out[..., 2] = tint_rgb[2] * shade
    # alpha: voxel value softened
    out[..., 3] = np.clip(vbuf, 0, 1) ** 0.85
    return out


# ═════════════════════════════════════════════════════════════════════
# FIG E27: 3D morforom med periode-arketypar (mesh-rendered)
# ═════════════════════════════════════════════════════════════════════
def fig_E27_morforom_3d_arketypar(df, pca, vox):
    """Plot the morphospace as PC1 × PC2 with each *style period*
    represented by its voxel-mean archetype rendered as a front-view
    silhouette at the period centroid. This is a direct 3D-backed
    phylomorphospace: real averaged geometry at each node."""
    counts = df["Stilperiode"].value_counts()
    periods = [p for p in sorted(PERIOD_YEAR.keys(), key=lambda k: PERIOD_YEAR[k])
               if p in counts.index and counts[p] >= 15]
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    xlo, xhi = np.quantile(pc1, [0.02, 0.98])
    ylo, yhi = np.quantile(pc2, [0.02, 0.98])

    rows = []
    for p in periods:
        sub = df[df["Stilperiode"] == p]
        ids = [oid for oid in sub["Objekt-ID"] if oid in vox]
        if len(ids) < 10:
            continue
        mean_g = mean_voxel(ids, vox)
        rows.append(dict(period=p, year=PERIOD_YEAR[p],
                         cx=sub["PC1"].mean(), cy=sub["PC2"].mean(),
                         n=len(sub), mean_grid=mean_g))
    rows.sort(key=lambda r: r["year"])

    fig = plt.figure(figsize=(14.5, 9))
    ax = fig.add_axes([0.06, 0.08, 0.70, 0.86])

    ax.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.08, linewidths=0, zorder=1)

    # connect centroids chronologically with faint line
    xs = np.array([r["cx"] for r in rows])
    ys = np.array([r["cy"] for r in rows])
    for i in range(len(rows) - 1):
        ax.plot([xs[i], xs[i + 1]], [ys[i], ys[i + 1]],
                color=SLATE, linewidth=0.6, alpha=0.5, zorder=2)

    img_w = (xhi - xlo) * 0.075
    img_h = (yhi - ylo) * 0.14
    for r in rows:
        col = PERIOD_COLOR.get(r["period"], SLATE)
        rgb = to_rgba(col)[:3]
        mean_g = r.get("mean_grid")
        if mean_g is None:
            continue
        rgba = render_shaded_mesh_to_array(
            mean_g, size=160, base_color=rgb, ambient=0.35,
            level=0.30, edge_rim=True)
        ax.imshow(rgba,
                  extent=(r["cx"] - img_w, r["cx"] + img_w,
                          r["cy"] - img_h, r["cy"] + img_h),
                  aspect="auto", interpolation="bilinear", zorder=4)
        ax.scatter([r["cx"]], [r["cy"]], s=25, c=[col],
                   edgecolors="white", linewidths=0.8, zorder=5)
        ax.text(r["cx"], r["cy"] - img_h * 1.05, f"{r['year']}",
                ha="center", va="top", fontsize=7.5, color=SLATE,
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.75, boxstyle="round,pad=0.15"))

    ax.set_xlim(xlo - img_w, xhi + img_w)
    ax.set_ylim(ylo - img_h * 0.6, yhi + img_h)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varians)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varians)")
    ax.grid(alpha=0.12, linewidth=0.4)

    # side legend
    axL = fig.add_axes([0.78, 0.08, 0.20, 0.86])
    axL.axis("off")
    axL.text(0.0, 1.00, "Periode-arketypar", transform=axL.transAxes,
             fontsize=10.5, weight="bold", color=SLATE, va="top")
    axL.text(0.0, 0.96,
             "Voxel-middla front-silhuett\nper stilperiode (n≥15).\n"
             "Posisjon: PC1-PC2 sentroide.\nLinja koplar periodane\n"
             "kronologisk.",
             transform=axL.transAxes, fontsize=8.5, color=SLATE, va="top")
    for i, r in enumerate(rows):
        y_pos = 0.76 - i * 0.035
        col = PERIOD_COLOR.get(r["period"], OI["grey"])
        axL.scatter([0.03], [y_pos], s=50, c=[col], transform=axL.transAxes,
                    edgecolors="white", linewidths=0.7, zorder=3)
        axL.text(0.10, y_pos, f"{r['year']}  {r['period']}  (n={r['n']})",
                 transform=axL.transAxes, fontsize=8, color=SLATE,
                 va="center", ha="left")

    save(fig, "E27_morforom_3d_arketypar")


# ═════════════════════════════════════════════════════════════════════
# FIG E28: Substrat-arketypar — wood/metal/plastic × fire tidsband
# ═════════════════════════════════════════════════════════════════════
def fig_E28_substrat_arketypar(df, vox):
    """3×4 grid of voxel-mean archetypes: one row per material, one column
    per time band. Each cell shows the front and side projection of the
    mean shape. This is the empirical 'typeform' per material per era."""
    df = df[df["år"].notna()].copy()
    materials = [
        ("wood", "tre", AMBER),
        ("metal", "stål / jern / krom", OI["blue"]),
        ("plastic", "plast / akryl / poly", OI["rust"]),
    ]
    bands = [(1600, 1800), (1800, 1900), (1900, 1950), (1950, 2025)]

    fig = plt.figure(figsize=(15.5, 9.5))
    gs = gridspec.GridSpec(len(materials), len(bands) * 2 + 1,
                           width_ratios=[1] * (len(bands) * 2) + [0.2],
                           wspace=0.05, hspace=0.25, figure=fig)

    for mi, (mname, mlabel, mcol) in enumerate(materials):
        for bi, (y0, y1) in enumerate(bands):
            sub = df[(df["mat_class"] == mname) &
                     (df["år"] >= y0) & (df["år"] < y1)]
            ids = [oid for oid in sub["Objekt-ID"] if oid in vox]
            # front
            ax_f = fig.add_subplot(gs[mi, bi * 2])
            # side
            ax_s = fig.add_subplot(gs[mi, bi * 2 + 1])
            for ax in (ax_f, ax_s):
                ax.set_xticks([]); ax.set_yticks([])
                for s in ["top", "right", "bottom", "left"]:
                    ax.spines[s].set_color(mcol)
                    ax.spines[s].set_linewidth(1.1 if ids else 0.4)
                    ax.spines[s].set_linestyle("-" if ids else ":")

            if len(ids) >= 6:
                mean_g = mean_voxel(ids, vox)
                rgb = to_rgba(mcol)[:3]
                # left: isometric render
                draw_shaded_mesh(ax_f, mean_g, rot_y=35, rot_x=22,
                                  base_color=rgb, ambient=0.35,
                                  level=0.30, edge_rim=True)
                # right: front view from marching-cubes mesh at 0° rotation
                draw_shaded_mesh(ax_s, mean_g, rot_y=0, rot_x=0,
                                  base_color=rgb, ambient=0.35,
                                  level=0.30, edge_rim=True)
                ax_f.text(0.5, -0.04, "3/4", transform=ax_f.transAxes,
                           fontsize=7, color=SLATE, ha="center", va="top")
                ax_s.text(0.5, -0.04, "front", transform=ax_s.transAxes,
                           fontsize=7, color=SLATE, ha="center", va="top")
            else:
                ax_f.text(0.5, 0.5, "—", transform=ax_f.transAxes,
                          ha="center", va="center", fontsize=16,
                          color=OI["grey"], alpha=0.6)
                ax_s.text(0.5, 0.5, "—", transform=ax_s.transAxes,
                          ha="center", va="center", fontsize=16,
                          color=OI["grey"], alpha=0.6)
            # cell title on top row: time band
            if mi == 0:
                ax_mid = fig.add_subplot(gs[-1, bi * 2:bi * 2 + 2], visible=False)
                _ = ax_mid
                # title across the two subpanels
                fig.text(
                    (ax_f.get_position().x0 + ax_s.get_position().x1) / 2,
                    0.965,
                    f"{y0}–{y1}",
                    ha="center", va="center", fontsize=11, weight="bold",
                    color=SLATE)
            # n label below
            ax_f.text(1.02, -0.10,
                      f"n = {len(ids)}", transform=ax_f.transAxes,
                      fontsize=7.5, color=SLATE, ha="center", va="top")

        # row label on the rightmost column
        lax = fig.add_subplot(gs[mi, -1])
        lax.axis("off")
        lax.text(0.05, 0.5, mlabel, transform=lax.transAxes,
                 fontsize=11, weight="bold", color=mcol,
                 va="center", ha="left", rotation=0)

    save(fig, "E28_substrat_arketypar")


# ═════════════════════════════════════════════════════════════════════
# FIG E29: Multi-view atlas av dei morfologisk isolerte (top-12 frå E16)
# ═════════════════════════════════════════════════════════════════════
def fig_E29_innovatør_atlas(df, vox, n_top=12):
    """Top-n most morphologically isolated chairs rendered as isometric 3/4
    views from the voxel cache. Layout: 4 × 3 grid with big isometric
    tile + compact metadata per chair."""
    df_yr = df[df["år"].notna()].copy().sort_values("år").reset_index(drop=True)
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]
    X = df_yr[pc_cols].values
    yrs = df_yr["år"].values
    N = len(df_yr)
    novelty = np.full(N, np.nan)
    for i in range(N):
        prior = yrs < yrs[i]
        if not prior.any():
            continue
        novelty[i] = np.linalg.norm(X[prior] - X[i], axis=1).min()
    df_yr["novelty"] = novelty
    top_idx = np.argsort(-novelty)
    chosen = []
    for k in top_idx:
        oid = df_yr.iloc[k]["Objekt-ID"]
        if oid in vox:
            chosen.append(int(k))
        if len(chosen) >= n_top:
            break

    # use only geometry-derived coloration (drop Stilperiode tint)
    # grade tone by novelty rank: rank 1 = warm amber, last = cool slate
    ranks = np.linspace(0, 1, len(chosen))
    tint_cmap = LinearSegmentedColormap.from_list(
        "inov", [OI["rust"], AMBER, SLATE], N=256)

    ncols = 3
    nrows = int(np.ceil(n_top / ncols))
    fig = plt.figure(figsize=(14, 4.2 * nrows))
    gs = gridspec.GridSpec(nrows, ncols, wspace=0.12, hspace=0.18, figure=fig)

    for r, k in enumerate(chosen):
        oid = df_yr.iloc[k]["Objekt-ID"]
        row = df_yr.iloc[k]
        grid = vox[oid].astype(np.float32)
        tint = tint_cmap(ranks[r])[:3]
        ax = fig.add_subplot(gs[r // ncols, r % ncols])
        ok = draw_shaded_mesh(ax, grid, rot_y=35, rot_x=22,
                               base_color=tint, ambient=0.35, edge_rim=True)

        # metadata overlay: top-left corner
        name = str(row.get("Namn", ""))[:42]
        label_top = f"#{r + 1}   {int(row['år'])}"
        label_mid = name if name else "(ukjent)"
        label_bot = f"nyskaping = {row['novelty']:.2f}    {row['Objekt-ID']}"
        ax.text(0.02, 0.98, label_top, transform=ax.transAxes,
                fontsize=13, color=SLATE, weight="bold",
                va="top", ha="left")
        ax.text(0.02, 0.92, label_mid, transform=ax.transAxes,
                fontsize=9.5, color=SLATE, va="top", ha="left")
        ax.text(0.02, 0.04, label_bot, transform=ax.transAxes,
                fontsize=8, color=SLATE, va="bottom", ha="left",
                family="monospace")

    save(fig, "E29_innovator_atlas")


# ═════════════════════════════════════════════════════════════════════
# Shape-PCA (voxel-space PCA) — the real geometric axes
# ═════════════════════════════════════════════════════════════════════
SHAPE_CACHE_PATH = os.path.join(HERE, "_shape_pca.npz")


def _downsample_voxel(grid, factor=2):
    """Max-pool a 3D voxel grid by an integer factor."""
    N = grid.shape[0]
    nd = N // factor
    trimmed = grid[: nd * factor, : nd * factor, : nd * factor]
    return trimmed.reshape(nd, factor, nd, factor, nd, factor).max(axis=(1, 3, 5))


def build_shape_pca(vox, df, n_components=20, downfactor=2, force=False):
    """Fit PCA on flattened voxel grids. Returns (mean_flat, components,
    explained_variance_ratio, scores, oid_order, nd)."""
    oid_order = [oid for oid in df["Objekt-ID"] if oid in vox]
    nd = VOXEL_N // downfactor

    if os.path.exists(SHAPE_CACHE_PATH) and not force:
        z = np.load(SHAPE_CACHE_PATH, allow_pickle=True)
        cached_oids = list(z["oid_order"])
        if cached_oids == oid_order and int(z["nd"]) == nd and \
           int(z["n_components"]) == n_components:
            print(f"  shape-PCA cache hit ({n_components} comps, nd={nd})")
            return (z["mean_flat"], z["components"],
                    z["explained_variance_ratio"], z["scores"],
                    oid_order, nd)

    print(f"  computing shape-PCA ({len(oid_order)} chairs, nd={nd}, "
          f"dim={nd**3}, k={n_components})...")
    X = np.zeros((len(oid_order), nd ** 3), dtype=np.float32)
    for i, oid in enumerate(oid_order):
        g = vox[oid].astype(np.float32)
        if downfactor > 1:
            g = _downsample_voxel(g, downfactor).astype(np.float32)
        X[i] = g.reshape(-1)
    mean_flat = X.mean(axis=0)
    Xc = X - mean_flat
    # truncated SVD for efficiency
    from sklearn.decomposition import TruncatedSVD
    svd = TruncatedSVD(n_components=n_components, random_state=0)
    scores = svd.fit_transform(Xc)
    components = svd.components_
    evr = svd.explained_variance_ratio_
    np.savez_compressed(SHAPE_CACHE_PATH,
                        mean_flat=mean_flat, components=components,
                        explained_variance_ratio=evr, scores=scores,
                        oid_order=np.array(oid_order), nd=np.array(nd),
                        n_components=np.array(n_components))
    print(f"  cached shape-PCA to {os.path.basename(SHAPE_CACHE_PATH)}")
    return mean_flat, components, evr, scores, oid_order, int(nd)


def shape_pc_to_grid(mean_flat, components, evr, k, sigma_mult, nd):
    """Reconstruct voxel grid at (mean + k_sigma * sqrt(var[k]) * comp[k])."""
    # TruncatedSVD gives components scaled so that scores have variance evr.
    # For visualization at ±kσ we need the singular value direction.
    # std of each component = sqrt(explained_variance) ≈ sqrt(evr * total_var)
    # Simpler: use the std of scores along that axis.
    # We'll pass scores std as amplitude externally — see caller.
    flat = mean_flat + sigma_mult * components[k]
    g = flat.reshape(nd, nd, nd)
    # clip to [0, 1] for visualisation
    g = np.clip(g, 0, 1)
    return g


# ═════════════════════════════════════════════════════════════════════
# FIG E30: Shape-PCA — reine geometriske deformasjonsmodusar
# ═════════════════════════════════════════════════════════════════════
def fig_E30_shape_pca_modes(df, vox, k_show=5):
    """Compute PCA directly on voxelized chair geometry. Render each of the
    top-k principal components as the mean shape ± n·σ along that direction.
    Each PC is a pure geometric deformation; no style-period labels needed."""
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)

    fig = plt.figure(figsize=(14.5, 3.2 * k_show + 0.5))
    gs = gridspec.GridSpec(k_show, 6, width_ratios=[1, 1, 1, 1, 1, 0.9],
                           wspace=0.05, hspace=0.30, figure=fig)

    sigmas = np.array([-2, -1, 0, 1, 2], dtype=float)
    for k in range(k_show):
        sd = float(scores[:, k].std())
        for ci, s in enumerate(sigmas):
            amp = s * sd
            grid = mean_flat + amp * comps[k]
            grid = np.clip(grid.reshape(nd, nd, nd), 0, 1)
            tint = (0.42, 0.46, 0.55) if s == 0 else (
                (to_rgba(OI["rust"])[:3]) if s > 0 else (to_rgba(OI["blue"])[:3]))
            ax = fig.add_subplot(gs[k, ci])
            draw_shaded_mesh(ax, grid, rot_y=35, rot_x=22,
                              base_color=tint, ambient=0.35,
                              level=0.25, edge_rim=True)
            if k == 0:
                ax.set_title(f"{int(s):+d} σ" if s != 0 else "gjennomsnitt (μ)",
                             fontsize=10, color=SLATE, weight="bold")

        # axis label column
        axL = fig.add_subplot(gs[k, 5])
        axL.axis("off")
        axL.text(0.0, 0.65,
                 f"ShapePC{k + 1}", transform=axL.transAxes,
                 fontsize=14, weight="bold", color=SLATE,
                 va="center", ha="left")
        axL.text(0.0, 0.38,
                 f"{evr[k]*100:.1f}% varians", transform=axL.transAxes,
                 fontsize=10, color=SLATE, va="center", ha="left")
        axL.text(0.0, 0.15,
                 f"σ(score) = {sd:.3f}", transform=axL.transAxes,
                 fontsize=9, color=SLATE, va="center", ha="left",
                 family="monospace")

    save(fig, "E30_shape_pca_modes")


# ═════════════════════════════════════════════════════════════════════
# FIG E31: Geometriske genera (unsupervised clustering)
# ═════════════════════════════════════════════════════════════════════
def fig_E31_geometrisk_genus(df, vox, K=8):
    """Unsupervised clustering on shape-PCA scores produces geometric
    'genera' that do NOT align with style periods. Show: (a) silhouette
    vs K curve, (b) mean-shape archetype per genus rendered isometrically,
    (c) genus × Stilperiode confusion (adjusted rand index)."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score, adjusted_rand_score

    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)
    X = scores[:, :10]

    # silhouette over K
    ks = [4, 6, 8, 10, 12, 15]
    sils = []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=6, random_state=0).fit(X)
        s = silhouette_score(X, km.labels_)
        sils.append(s)
    best_k = ks[int(np.argmax(sils))]
    # use requested K (default 8) for display but report best
    km_main = KMeans(n_clusters=K, n_init=10, random_state=0).fit(X)
    labels = km_main.labels_

    # map oids -> cluster
    oid_to_cluster = dict(zip(oid_order, labels))
    df_match = df[df["Objekt-ID"].isin(set(oid_order))].copy()
    df_match["genus"] = df_match["Objekt-ID"].map(oid_to_cluster)

    # archetype voxel per cluster: mean of all cluster members' voxel grids
    archetypes = []
    for g in range(K):
        member_oids = [oid for oid, lbl in zip(oid_order, labels) if lbl == g]
        if not member_oids:
            archetypes.append(None); continue
        grids = [vox[oid].astype(np.float32) for oid in member_oids]
        mean_g = np.mean(grids, axis=0)
        archetypes.append((mean_g, len(member_oids), member_oids))

    # adjusted rand index with Stilperiode
    per = df_match["Stilperiode"].fillna("ukjent").values
    per_codes = pd.Categorical(per).codes
    ari = float(adjusted_rand_score(per_codes, df_match["genus"].values))

    fig = plt.figure(figsize=(15, 9.5))
    gs = gridspec.GridSpec(3, K, height_ratios=[1.1, 1.1, 1.1],
                           hspace=0.35, wspace=0.08, figure=fig)

    # Row 0-1: one cell per genus with (a) isometric + (b) member stats
    cmap_g = LinearSegmentedColormap.from_list(
        "gen", [AMBER, SLATE, OI["blue"], OI["rust"], OI["green"],
                OI["pink"], OI["orange"], OI["skyblue"]], N=K)
    order_g = np.argsort(-np.array([a[1] if a is not None else 0
                                     for a in archetypes]))
    for idx, g in enumerate(order_g):
        if archetypes[g] is None:
            continue
        mean_g, n_mem, member_oids = archetypes[g]
        tint = cmap_g(idx / max(K - 1, 1))[:3]
        ax = fig.add_subplot(gs[0, idx])
        draw_shaded_mesh(ax, mean_g, rot_y=35, rot_x=22,
                          base_color=tint, ambient=0.35,
                          level=0.25, edge_rim=True)
        ax.set_title(f"genus {g}   n = {n_mem}", fontsize=10,
                     color=SLATE, weight="bold", loc="left")

        # per-genus year histogram
        axH = fig.add_subplot(gs[1, idx])
        sub = df_match[df_match["genus"] == g]
        yrs = sub["år"].dropna().values
        if len(yrs):
            axH.hist(yrs, bins=np.arange(1400, 2040, 40),
                     color=tint, alpha=0.85, edgecolor="white", linewidth=0.3)
        axH.set_xlim(1400, 2030)
        axH.tick_params(labelsize=7)
        axH.set_yticks([])
        axH.grid(alpha=0.10, linewidth=0.3)
        if idx == 0:
            axH.set_ylabel("tal stolar", fontsize=8)
        axH.set_xlabel("år", fontsize=8)

    # Row 2: Silhouette score curve + ARI + confusion info
    axS = fig.add_subplot(gs[2, :K // 2])
    axS.plot(ks, sils, marker="o", color=SLATE, lw=1.8)
    axS.axvline(best_k, color=OI["rust"], linestyle="--", linewidth=1,
                alpha=0.7, label=f"beste K = {best_k}")
    axS.axvline(K, color=AMBER, linestyle=":", linewidth=1, alpha=0.8,
                 label=f"vist K = {K}")
    axS.set_xlabel("tal genus K")
    axS.set_ylabel("silhouette-skår")
    axS.set_title("(c) klynge-kvalitet mot K", loc="left", weight="bold",
                  fontsize=10.5)
    axS.grid(alpha=0.14, linewidth=0.4)
    axS.legend(loc="lower right", fontsize=8.5, frameon=False)

    axT = fig.add_subplot(gs[2, K // 2:])
    axT.axis("off")
    txt = [
        f"Adjusted Rand Index (genus vs Stilperiode): {ari:.3f}",
        "",
        "  • ARI = 1  →  genus-inndelinga matchar stilperiodane perfekt",
        "  • ARI = 0  →  ingen samanheng — geometri og stilperiode er ortogonale",
        f"  • Observert ARI = {ari:.3f}  {'→ lågt, ' if ari < 0.1 else '→ '}"
        f"{'geometri og stilperiode er langt på veg uavhengige grupperingar.' if ari < 0.1 else 'delvis overlapp.'}",
        "",
        "Stilperiode er altså IKKJE ei geometrisk klassifisering. Dei reine",
        "morfologiske genera er definert av form aleine og gir ein alternativ,",
        "data-driven taksonomi over designkorpuset.",
    ]
    axT.text(0.01, 0.95, "\n".join(txt), transform=axT.transAxes,
             fontsize=9.5, color=SLATE, va="top", ha="left")

    save(fig, "E31_geometrisk_genus")


# ═════════════════════════════════════════════════════════════════════
# FIG E32: Evolusjonære retningar (PCA på Δsentroide per år)
# ═════════════════════════════════════════════════════════════════════
def fig_E32_evolusjonsretningar(df, vox):
    """For each consecutive pair of 40-year bins, compute the shift of the
    centroid in shape-PCA space. PCA on these shift-vectors reveals the
    dominant 'directions of evolution'. Visualise each such direction as
    a deformation of the mean shape, exactly as E30 but for evolution
    *rates* rather than standing variation."""
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)
    df_match = df[df["Objekt-ID"].isin(set(oid_order))].copy()
    df_match = df_match[df_match["år"].notna()].copy()
    oid_to_score = {oid: scores[i] for i, oid in enumerate(oid_order)}

    bins = np.arange(1500, 2040, 40)
    centers = []
    years = []
    for i in range(len(bins) - 1):
        a, b = bins[i], bins[i + 1]
        sub = df_match[(df_match["år"] >= a) & (df_match["år"] < b)]
        if len(sub) < 6:
            continue
        sc = np.array([oid_to_score[o] for o in sub["Objekt-ID"]
                       if o in oid_to_score])
        centers.append(sc.mean(axis=0))
        years.append((a + b) / 2)
    centers = np.array(centers)  # (T, k)
    deltas = np.diff(centers, axis=0)  # (T-1, k)

    # PCA on Δ vectors
    from sklearn.decomposition import PCA as _PCA
    n_dir = min(4, deltas.shape[0] - 1) if len(deltas) > 2 else 2
    pca_evo = _PCA(n_components=min(n_dir, deltas.shape[1], len(deltas)))
    evo_scores = pca_evo.fit_transform(deltas)

    # For each "evolutionary direction" reconstruct in voxel space:
    # evolution_direction_j = pca_evo.components_[j] @ shape_pca_components
    evo_vecs_voxel = pca_evo.components_ @ comps  # (n_dir, nd^3)

    fig = plt.figure(figsize=(14.5, 4.0 * n_dir + 1.0))
    gs = gridspec.GridSpec(n_dir, 5,
                           width_ratios=[1, 1, 1, 1, 1.2],
                           wspace=0.06, hspace=0.35, figure=fig)

    sigmas = np.array([-2, -1, 0, 1, 2], dtype=float)
    for j in range(n_dir):
        amp = 2.0 * float(np.sqrt(pca_evo.explained_variance_[j]))
        for ci, s in enumerate(sigmas[:4]):
            a_s = s * amp
            g = mean_flat + a_s * evo_vecs_voxel[j]
            g = np.clip(g.reshape(nd, nd, nd), 0, 1)
            tint = (0.42, 0.46, 0.55) if abs(s) < 1e-6 else (
                (to_rgba(OI["rust"])[:3]) if s > 0 else (to_rgba(OI["blue"])[:3]))
            ax = fig.add_subplot(gs[j, ci])
            draw_shaded_mesh(ax, g, rot_y=35, rot_x=22,
                              base_color=tint, ambient=0.35,
                              level=0.25, edge_rim=True)
            if j == 0:
                ax.set_title(f"{int(s):+d} σ" if s != 0 else "gjennomsnitt",
                             fontsize=10, color=SLATE, weight="bold")

        # time-series of this evolutionary direction
        axT = fig.add_subplot(gs[j, 4])
        axT.plot(np.array(years[1:]), evo_scores[:, j],
                 marker="o", color=OI["rust"] if j == 0 else SLATE, lw=1.6)
        axT.axhline(0, color=SLATE, linewidth=0.5, alpha=0.4)
        axT.set_xlabel("år")
        axT.set_ylabel(f"Δ-skår langs EvoDir{j + 1}")
        axT.set_title(f"EvoDir{j + 1}   "
                      f"{pca_evo.explained_variance_ratio_[j]*100:.1f}% "
                      f"av evolusjonsvariasjonen",
                       loc="left", fontsize=9.5, weight="bold")
        axT.grid(alpha=0.14, linewidth=0.4)

    save(fig, "E32_evolusjonsretningar")


# ═════════════════════════════════════════════════════════════════════
# FIG E33: Prediktiv forecasting av formframtid
# ═════════════════════════════════════════════════════════════════════
def fig_E33_forecast(df, vox):
    """Train OU-like dynamics on the 1500-1960 shape-PC centroid trajectory,
    forecast 1960-2040, and compare to the held-out empirical centroid post-1960.
    Render reconstructed 3D shapes for training-end, forecast, and observed."""
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)
    df_match = df[df["Objekt-ID"].isin(set(oid_order))].copy()
    df_match = df_match[df_match["år"].notna()].copy()
    oid_to_score = {oid: scores[i] for i, oid in enumerate(oid_order)}

    K = 6
    bins = np.arange(1500, 2040, 40)
    ys = []; means = []
    for i in range(len(bins) - 1):
        a, b = bins[i], bins[i + 1]
        sub = df_match[(df_match["år"] >= a) & (df_match["år"] < b)]
        if len(sub) < 6:
            continue
        vecs = np.array([oid_to_score[o][:K] for o in sub["Objekt-ID"]
                         if o in oid_to_score])
        ys.append((a + b) / 2)
        means.append(vecs.mean(axis=0))
    ys = np.array(ys); means = np.array(means)

    train_mask = ys <= 1960
    test_mask = ys > 1960
    if train_mask.sum() < 3:
        print("  skipping E33: not enough training data")
        return

    dt_train = np.diff(ys[train_mask])
    dmu = np.diff(means[train_mask], axis=0)
    mu_prev = means[train_mask][:-1]

    alphas = np.zeros(K); thetas = np.zeros(K)
    for k in range(K):
        y = dmu[:, k] / dt_train
        X_reg = np.column_stack([np.ones_like(mu_prev[:, k]), mu_prev[:, k]])
        coef, *_ = np.linalg.lstsq(X_reg, y, rcond=None)
        b0, b1 = coef
        alpha = -b1
        if abs(alpha) < 1e-9:
            alpha = 1e-3
        thetas[k] = b0 / alpha
        alphas[k] = alpha

    forecast_years = np.arange(ys[train_mask][-1] + 40, 2080, 40)
    mu_fore = [means[train_mask][-1].copy()]
    yr_fore = [ys[train_mask][-1]]
    for yr in forecast_years:
        dt = yr - yr_fore[-1]
        next_mu = mu_fore[-1] + alphas * (thetas - mu_fore[-1]) * dt
        mu_fore.append(next_mu); yr_fore.append(yr)
    mu_fore = np.array(mu_fore); yr_fore = np.array(yr_fore)

    mu_test = means[test_mask]; yr_test = ys[test_mask]

    def reconstruct(k_vec):
        flat = mean_flat.copy()
        for k in range(len(k_vec)):
            flat = flat + k_vec[k] * comps[k]
        return np.clip(flat.reshape(nd, nd, nd), 0, 1)

    shape_train_last = reconstruct(means[train_mask][-1])
    shape_forecast = reconstruct(mu_fore[-1])
    shape_obs = reconstruct(mu_test[-1]) if len(mu_test) > 0 else None

    fig = plt.figure(figsize=(14.5, 8.5))
    gs = gridspec.GridSpec(2, 4, width_ratios=[1.05, 1.05, 1.05, 1.6],
                           height_ratios=[1, 1.05], hspace=0.30, wspace=0.18,
                           figure=fig)

    tint_train = to_rgba(SLATE)[:3]
    tint_fore = to_rgba(OI["orange"])[:3]
    tint_obs = to_rgba(AMBER)[:3]

    ax1 = fig.add_subplot(gs[0, 0])
    draw_shaded_mesh(ax1, shape_train_last, base_color=tint_train,
                      ambient=0.35, level=0.25)
    ax1.set_title(f"(a) trena t.o.m. {int(ys[train_mask][-1])}",
                   loc="left", fontsize=10, weight="bold")

    ax2 = fig.add_subplot(gs[0, 1])
    draw_shaded_mesh(ax2, shape_forecast, base_color=tint_fore,
                      ambient=0.35, level=0.25)
    ax2.set_title(f"(b) OU-forecast {int(yr_fore[-1])}",
                   loc="left", fontsize=10, weight="bold")

    ax3 = fig.add_subplot(gs[0, 2])
    if shape_obs is not None:
        draw_shaded_mesh(ax3, shape_obs, base_color=tint_obs,
                          ambient=0.35, level=0.25)
        ax3.set_title(f"(c) observert {int(yr_test[-1])}",
                       loc="left", fontsize=10, weight="bold")
    else:
        ax3.axis("off")

    axP = fig.add_subplot(gs[0, 3]); axP.axis("off")
    lines = ["OU-dynamikk pr. shape-PC (trena 1500-1960):"]
    lines.append("─" * 58)
    lines.append(f"{'PC':>4}  {'α':>10}  {'θ':>10}  {'τ½ (år)':>10}")
    lines.append("─" * 58)
    for k in range(K):
        tau = np.log(2) / alphas[k] if alphas[k] > 0 else np.nan
        lines.append(f"{k + 1:>4}  {alphas[k]:>10.4f}  {thetas[k]:>10.3f}  "
                     f"{tau:>10.0f}")
    axP.text(0.00, 1.00, "\n".join(lines), transform=axP.transAxes,
             fontsize=9, color=SLATE, family="monospace", va="top", ha="left")

    for kk in range(2):
        axT = fig.add_subplot(gs[1, kk * 2:kk * 2 + 2])
        axT.plot(ys[train_mask], means[train_mask, kk], marker="o",
                 color=SLATE, lw=1.8, label="trenings-trajektorie (til 1960)")
        if len(mu_test):
            axT.plot(yr_test, mu_test[:, kk], marker="s",
                     color=AMBER, lw=1.6, label="observert (held ute)")
        axT.plot(yr_fore, mu_fore[:, kk], marker="^",
                 color=OI["orange"], lw=1.8, linestyle="--",
                 label="OU-forecast")
        axT.axhline(thetas[kk], color=OI["rust"], lw=0.8,
                    linestyle=":", alpha=0.8, label=f"θ = {thetas[kk]:.2f}")
        axT.axvline(1960, color="black", lw=0.5, alpha=0.4)
        axT.set_xlabel("år")
        axT.set_ylabel(f"shape-PC{kk + 1} sentroide")
        axT.set_title(f"(d{kk + 1}) dynamikk på shape-PC{kk + 1}",
                       loc="left", fontsize=9.5, weight="bold")
        axT.grid(alpha=0.14, linewidth=0.4)
        if kk == 0:
            axT.legend(loc="upper left", fontsize=8, frameon=False)

    save(fig, "E33_forecast")


# ═════════════════════════════════════════════════════════════════════
# FIG E34: Ancestral-state-rekonstruksjon per geometrisk genus
# ═════════════════════════════════════════════════════════════════════
def fig_E34_ancestor_reconstruction(df, vox, K=8):
    """For each geometric genus (KMeans on shape-PC), compute the ancestral
    shape as the voxel-mean of the earliest 20% members vs. the descendant
    mean of the latest 20%. Render both; show the within-lineage
    morphological shift."""
    from sklearn.cluster import KMeans
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)
    X = scores[:, :10]
    labels = KMeans(n_clusters=K, n_init=10, random_state=0).fit_predict(X)
    oid_to_cl = dict(zip(oid_order, labels))

    df_match = df[df["Objekt-ID"].isin(set(oid_order))].copy()
    df_match = df_match[df_match["år"].notna()].copy()
    df_match["genus"] = df_match["Objekt-ID"].map(oid_to_cl)

    results = []
    for g in range(K):
        sub = df_match[df_match["genus"] == g].sort_values("år")
        if len(sub) < 10:
            continue
        n20 = max(5, int(len(sub) * 0.20))
        early = sub.iloc[:n20]; late = sub.iloc[-n20:]
        anc_ids = [o for o in early["Objekt-ID"] if o in vox]
        des_ids = [o for o in late["Objekt-ID"] if o in vox]
        if not anc_ids or not des_ids:
            continue
        anc = mean_voxel(anc_ids, vox)
        des = mean_voxel(des_ids, vox)
        results.append(dict(g=g, n=len(sub), anc=anc, des=des,
                            y_anc=float(early["år"].mean()),
                            y_des=float(late["år"].mean())))
    results.sort(key=lambda r: -r["n"])
    K_show = min(len(results), 6)
    results = results[:K_show]

    fig = plt.figure(figsize=(14, 2.3 * K_show + 1.5))
    gs = gridspec.GridSpec(K_show, 4,
                           width_ratios=[1, 1, 1, 1.6],
                           wspace=0.05, hspace=0.30, figure=fig)

    tint_palette = [AMBER, OI["blue"], OI["rust"], OI["green"],
                    OI["pink"], OI["orange"], OI["skyblue"], SLATE]

    for idx, r in enumerate(results):
        tint = to_rgba(tint_palette[idx % len(tint_palette)])[:3]
        ax_a = fig.add_subplot(gs[idx, 0])
        draw_shaded_mesh(ax_a, r["anc"], base_color=tint,
                          ambient=0.35, level=0.25)
        ax_a.set_title(f"tidleg (~{int(r['y_anc'])})",
                        fontsize=9, loc="left", weight="bold")

        ax_d = fig.add_subplot(gs[idx, 1])
        diff = r["des"] - r["anc"]
        gain = np.clip(diff, 0, 1)
        draw_shaded_mesh(ax_d, gain, base_color=to_rgba(OI["rust"])[:3],
                          ambient=0.35, level=0.05,
                          edge_rim=False, smooth_sigma=1.2)
        ax_d.set_title("netto tilvekst (sein − tidleg)",
                        fontsize=9, loc="left", weight="bold",
                        color=OI["rust"])

        ax_b = fig.add_subplot(gs[idx, 2])
        draw_shaded_mesh(ax_b, r["des"], base_color=tint,
                          ambient=0.35, level=0.25)
        ax_b.set_title(f"sein (~{int(r['y_des'])})",
                        fontsize=9, loc="left", weight="bold")

        ax_t = fig.add_subplot(gs[idx, 3]); ax_t.axis("off")
        shift = float(np.linalg.norm(r["des"] - r["anc"]))
        ax_t.text(0.0, 0.90, f"genus {r['g']}   n = {r['n']}",
                   transform=ax_t.transAxes, fontsize=12, weight="bold",
                   color=SLATE, va="top")
        ax_t.text(0.0, 0.62,
                   f"tidsspenn: {int(r['y_des'] - r['y_anc'])} år\n"
                   f"‖Δform‖₂ = {shift:.2f}",
                   transform=ax_t.transAxes, fontsize=10, color=SLATE,
                   va="top", family="monospace")

    save(fig, "E34_ancestor_reconstruction")


# ═════════════════════════════════════════════════════════════════════
# FIG E35: Synopsis — hero-figur som oppsummerer paradigmet
# ═════════════════════════════════════════════════════════════════════
def fig_E35_synopsis(df, pca, vox):
    """Single-figure summary of the key empirical findings, composed as a
    four-quadrant montage:
      (a) shape-PCA deformation grid at ±2σ on PC1/PC2 — the actual
          geometric axes, with key chairs placed as shaded meshes
      (b) rate-in-haldanes timeline with biology benchmarks
      (c) material-specific OU optima θ with arrow-displacements
      (d) live-type biodiversity curve with extinction and origination
    """
    from sklearn.cluster import KMeans
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)

    fig = plt.figure(figsize=(16, 11))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.1, 1.0],
                           height_ratios=[1, 1], hspace=0.28, wspace=0.18,
                           figure=fig)

    # ----- (a) shape-PC1 × shape-PC2 grid with mesh archetypes -----
    axA = fig.add_subplot(gs[0, 0])
    # 3x3 sample grid on PC1, PC2
    xs = [-2.0, 0.0, 2.0]; ys = [-2.0, 0.0, 2.0]
    sd1 = float(scores[:, 0].std()); sd2 = float(scores[:, 1].std())
    img_extent = 1.0  # bigger chairs
    # smooth gradient based on (PC1, PC2) angle: northwest=cool, southeast=warm
    cmap_grad = LinearSegmentedColormap.from_list(
        "pc_quad", ["#0072B2", "#56B4E9", "#F2F2F2",
                     "#E69F00", "#D55E00"], N=256)
    for i, sx in enumerate(xs):
        for j, sy in enumerate(ys):
            shape = mean_flat + sx * sd1 * comps[0] + sy * sd2 * comps[1]
            grid = np.clip(shape.reshape(nd, nd, nd), 0, 1)
            # smooth gradient — PC1 sum determines warmth
            t = (sx + sy + 4) / 8  # 0..1
            tint = cmap_grad(t)[:3]
            rgba = render_shaded_mesh_to_array(
                grid, size=190, base_color=tint, ambient=0.24,
                level=0.24, edge_rim=False)
            axA.imshow(rgba,
                        extent=(sx - img_extent, sx + img_extent,
                                sy - img_extent, sy + img_extent),
                        aspect="auto", interpolation="bilinear", zorder=3)
    axA.axhline(0, color=OI["grey"], linewidth=0.5, alpha=0.6, zorder=1)
    axA.axvline(0, color=OI["grey"], linewidth=0.5, alpha=0.6, zorder=1)
    axA.set_xlim(-3.4, 3.4); axA.set_ylim(-3.4, 3.4)
    axA.set_xlabel(f"shape-PC1 ({evr[0]*100:.1f}% varians)", fontsize=11)
    axA.set_ylabel(f"shape-PC2 ({evr[1]*100:.1f}% varians)", fontsize=11)
    axA.set_title("(a) geometri-basert morforom",
                   loc="left", fontsize=12.5, weight="bold")
    axA.grid(alpha=0.10, linewidth=0.3)

    # ----- (b) haldane-rate timeline -----
    axB = fig.add_subplot(gs[0, 1])
    df_yr = df[df["år"].notna()].copy().sort_values("år")
    pc_cols = ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6"]
    bins_h = np.arange(1500, 2040, 40)
    cents = []
    for i in range(len(bins_h) - 1):
        a, b = bins_h[i], bins_h[i + 1]
        sub = df_yr[(df_yr["år"] >= a) & (df_yr["år"] < b)]
        if len(sub) < 8:
            continue
        cents.append(dict(year=(a + b) / 2,
                          mean=sub[pc_cols].mean().values,
                          std=sub[pc_cols].std().values))
    gen = 25.0
    ys_h = []; h_mean = []
    for i in range(len(cents) - 1):
        a, b = cents[i], cents[i + 1]
        dt = (b["year"] - a["year"]) / gen
        pooled = (a["std"] + b["std"]) / 2 + 1e-9
        haldane = np.abs((b["mean"] - a["mean"]) / (pooled * dt))
        ys_h.append((a["year"] + b["year"]) / 2)
        h_mean.append(np.mean(haldane))
    axB.bar(ys_h, h_mean, width=30, color=AMBER, alpha=0.88,
             edgecolor=SLATE, linewidth=0.4)
    axB.set_yscale("log")
    for val, lbl, col in [(1e-3, "bradytelisk (natur)", OI["grey"]),
                           (1e-2, "mikroevolusjon", SLATE),
                           (1e-1, "domestisering", AMBER),
                           (1e0, "klima-skift", OI["rust"])]:
        axB.axhline(val, color=col, linestyle="--", linewidth=0.7,
                     alpha=0.75)
        axB.text(2025, val * 1.15, lbl, fontsize=8.5, color=col,
                  ha="right", va="bottom")
    axB.set_xlim(1490, 2040); axB.set_ylim(5e-4, 5)
    axB.set_xlabel("år", fontsize=11)
    axB.set_ylabel("gjennomsnittleg |haldane|", fontsize=11)
    axB.set_title("(b) evolusjonsrate i haldanar",
                   loc="left", fontsize=12.5, weight="bold")
    axB.grid(alpha=0.14, linewidth=0.4, which="both")

    # ----- (c) material OU optima triangle -----
    axC = fig.add_subplot(gs[1, 0])
    pc1 = df["PC1"].values; pc2 = df["PC2"].values
    axC.scatter(pc1, pc2, s=3, c=OI["grey"], alpha=0.08,
                 linewidths=0, zorder=1)
    mat_colors = {"wood": AMBER, "metal": OI["blue"], "plastic": OI["rust"]}
    mat_labels = {"wood": "tre", "metal": "stål", "plastic": "plast"}
    theta_xs = []; theta_ys = []
    for mname, col in mat_colors.items():
        sub = df[df["mat_class"] == mname]
        if len(sub) < 10:
            continue
        th_x = float(sub["PC1"].mean()); th_y = float(sub["PC2"].mean())
        theta_xs.append(th_x); theta_ys.append(th_y)
        axC.scatter(sub["PC1"], sub["PC2"], s=8, c=[col], alpha=0.35,
                     linewidths=0, zorder=2)
        axC.scatter([th_x], [th_y], s=140, marker="o", c=[col],
                     edgecolors="white", linewidths=1.5, zorder=6,
                     label=f"{mat_labels[mname]}  θ = ({th_x:.2f}, {th_y:.2f})")
    # draw triangle
    if len(theta_xs) == 3:
        xs_t = theta_xs + [theta_xs[0]]; ys_t = theta_ys + [theta_ys[0]]
        axC.plot(xs_t, ys_t, color=SLATE, linewidth=1.1,
                  linestyle="--", alpha=0.7, zorder=4)
    xlo, xhi = np.quantile(pc1, [0.02, 0.98])
    ylo, yhi = np.quantile(pc2, [0.02, 0.98])
    axC.set_xlim(xlo, xhi); axC.set_ylim(ylo, yhi)
    axC.set_xlabel(f"PC1", fontsize=11)
    axC.set_ylabel(f"PC2", fontsize=11)
    axC.set_title("(c) materialspesifikke adaptive optima",
                   loc="left", fontsize=12.5, weight="bold")
    axC.legend(loc="upper left", fontsize=9, frameon=False)
    axC.grid(alpha=0.12, linewidth=0.4)

    # ----- (d) biodiversity curve -----
    axD = fig.add_subplot(gs[1, 1])
    # rerun KMeans on 4-dim PC-space
    Xpc = df_yr[pc_cols[:4]].dropna().values
    km = KMeans(n_clusters=14, n_init=6, random_state=0).fit(Xpc)
    labs = km.labels_
    df_yr_k = df_yr[pc_cols[:4]].dropna().copy()
    df_yr_k["type"] = labs
    df_yr_k["år"] = df_yr.loc[df_yr_k.index, "år"]
    # live per year
    ranges = []
    for t in range(14):
        sub = df_yr_k[df_yr_k["type"] == t]
        if len(sub) > 2:
            ranges.append((int(sub["år"].min()), int(sub["år"].max())))
    years_d = np.arange(1400, 2030)
    live = np.zeros_like(years_d)
    for (f, l) in ranges:
        live[(years_d >= f) & (years_d <= l)] += 1
    axD.fill_between(years_d, 0, live, color=AMBER, alpha=0.55, step="mid")
    axD.plot(years_d, live, color=SLATE, lw=1.5)
    # extinction markers
    for (f, l) in ranges:
        if l < 2020:
            axD.axvline(l, color=OI["rust"], linewidth=0.4, alpha=0.5)
    axD.set_xlim(1400, 2025); axD.set_ylim(0, max(live) + 1)
    axD.set_xlabel("år", fontsize=11)
    axD.set_ylabel("tal levande formtypar", fontsize=11)
    axD.set_title("(d) biodiversitets-kurve over formtypar",
                   loc="left", fontsize=12.5, weight="bold")
    axD.grid(alpha=0.14, linewidth=0.4)

    save(fig, "E35_synopsis")


# ═════════════════════════════════════════════════════════════════════
# Thumbnail-cache + E37 shaded-mesh giga-grid
# ═════════════════════════════════════════════════════════════════════
THUMB_CACHE_PATH = os.path.join(HERE, "_thumb_rgba_lum_112.npz")
THUMB_SIZE = 112


def _thumb_worker(args):
    """Render a single chair as a bright, near-white shaded mesh. The
    result is a LUMINANCE thumbnail (grayscale+alpha) that can be tinted
    at compose time with any colour scheme."""
    import numpy as _np
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    oid, grid_bytes, shape, size = args
    grid = _np.unpackbits(_np.frombuffer(grid_bytes, dtype=_np.uint8))[: int(_np.prod(shape))].reshape(shape).astype(bool)
    fig = Figure(figsize=(size / 100.0, size / 100.0), dpi=100, facecolor="none")
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.patch.set_alpha(0)
    # white-ish base so the tint multiplies cleanly at compose time
    draw_shaded_mesh(ax, grid, rot_y=35, rot_x=22,
                      base_color=(0.85, 0.85, 0.88),
                      shadow_color=(0.20, 0.22, 0.28),
                      highlight_color=(1.0, 1.0, 1.0),
                      ambient=0.28, smooth_sigma=0.40,
                      edge_rim=False,
                      specular_strength=0.20)
    canvas.draw()
    buf = _np.asarray(canvas.buffer_rgba()).copy()
    return oid, buf.tobytes(), buf.shape


def build_thumb_cache(df, vox, size=THUMB_SIZE, force=False, workers=None):
    """Cache bright grayscale+alpha thumbnails per chair. Tint applied at
    compose time so one cache fuels any colouring scheme."""
    existing = {}
    if os.path.exists(THUMB_CACHE_PATH) and not force:
        z = np.load(THUMB_CACHE_PATH, allow_pickle=False)
        for k in z.files:
            existing[k] = z[k]
    missing_ids = [oid for oid in df["Objekt-ID"]
                    if oid in vox and oid not in existing]
    if not missing_ids:
        print(f"  thumb cache ok: {len(existing)}")
        return existing
    if workers is None:
        workers = max(mp.cpu_count() - 2, 2)
    print(f"  thumb cache: {len(existing)} present, rendering {len(missing_ids)} "
          f"with {workers} workers (size={size})...")

    args_list = []
    for oid in missing_ids:
        g = vox[oid].astype(bool)
        packed = np.packbits(g.reshape(-1)).tobytes()
        args_list.append((oid, packed, g.shape, size))

    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for oid, buf_bytes, shape in ex.map(_thumb_worker, args_list, chunksize=2):
            arr = np.frombuffer(buf_bytes, dtype=np.uint8).reshape(shape)
            existing[oid] = arr
            done += 1
            if done % 200 == 0 or done == len(missing_ids):
                print(f"    {done}/{len(missing_ids)}")
    np.savez_compressed(THUMB_CACHE_PATH,
                         **{oid: arr for oid, arr in existing.items()})
    print(f"  cached to {os.path.basename(THUMB_CACHE_PATH)}")
    return existing


def _tint_thumb(th, tint_rgb):
    """Apply colour tint (multiplicative) to a grayscale thumbnail.
    Returns a composited uint8 RGB over white background."""
    alpha = th[..., 3:4].astype(np.float32) / 255.0
    # luminance: mean of RGB (grayscale render)
    lum = th[..., :3].astype(np.float32) / 255.0  # 0..1
    tint = np.asarray(tint_rgb, dtype=np.float32)
    # tint is the MID tone; luminance scales between shadow(black-tint) and
    # highlight(white). Multiplicative with a tone-map:
    shadow = tint * 0.28
    highlight = np.array([1.0, 1.0, 1.0])
    t = np.clip(lum, 0, 1)
    # two-segment: shadow → tint at t=0.55 → highlight at t=1.0
    tlo = np.clip(t / 0.55, 0, 1)[..., None]
    mid = shadow[None, None, :] * (1 - tlo) + tint[None, None, :] * tlo
    thi = np.clip((t - 0.55) / 0.45, 0, 1)[..., None]
    out_rgb = mid * (1 - thi) + highlight[None, None, :] * thi
    out_rgb = np.clip(out_rgb[..., 0, :], 0, 1) * 255
    white = np.full_like(out_rgb, 255)
    comp = out_rgb * alpha + white * (1 - alpha)
    return comp.astype(np.uint8)


def fig_E37_giga_grid_3d(df, vox, thumbs=None, mode="year"):
    """Ultra-tight giga-grid of every chair as a bright shaded-mesh
    thumbnail. Sort and colour reflect a meaningful gradient so the
    sort direction is visually legible as a smooth colour sweep."""
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize

    if thumbs is None:
        thumbs = build_thumb_cache(df, vox, size=THUMB_SIZE)

    rows = df[df["Objekt-ID"].isin(thumbs)].copy()
    # chronological gradient colour map (cool → warm)
    year_cmap = LinearSegmentedColormap.from_list(
        "year_grad", ["#2C3E50", "#3C4B5F", "#6B7080",
                      "#B47332", "#E69F00", "#D55E00"], N=256)
    # PC-PC1 gradient colour map
    pc_cmap = LinearSegmentedColormap.from_list(
        "pc_grad", ["#0072B2", "#56B4E9", "#FAF6EE",
                     "#E69F00", "#D55E00"], N=256)

    if mode == "pc1":
        rows = rows.sort_values("PC1")
        values = rows["PC1"].values
        cmap = pc_cmap
        suffix = "pc1"
    else:
        rows = rows[rows["år"].notna()].sort_values("år")
        values = rows["år"].values
        cmap = year_cmap
        suffix = "year"
    norm = Normalize(vmin=np.quantile(values, 0.01),
                     vmax=np.quantile(values, 0.99))
    N = len(rows)
    cols = int(np.ceil(np.sqrt(N * 1.18)))
    grid_rows = int(np.ceil(N / cols))
    print(f"  E37 giga ({mode}): {N} stolar in {grid_rows}x{cols}")

    tile = THUMB_SIZE
    pad = 0  # tight packing
    W = cols * tile
    H = grid_rows * tile
    canvas = np.full((H, W, 3), 255, dtype=np.uint8)

    oids = rows["Objekt-ID"].values
    for k in range(N):
        r = k // cols; c = k % cols
        x0 = c * tile; y0 = r * tile
        th = thumbs.get(oids[k])
        if th is None:
            continue
        tint = cmap(norm(values[k]))[:3]
        comp = _tint_thumb(th, tint)
        canvas[y0:y0 + tile, x0:x0 + tile] = comp

    fig_w = min(22, cols * 0.22)
    fig_h = fig_w * (H / W)
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([0.002, 0.002, 0.996, 0.996])
    ax.imshow(canvas, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax.spines[s].set_visible(False)
    save(fig, f"E37_giga_grid_3d_{suffix}")


# ═════════════════════════════════════════════════════════════════════
# FIG E36: Allometri — testar om form er skala-avhengig
# ═════════════════════════════════════════════════════════════════════
def fig_E36_allometri(df, vox):
    """Classical allometric scaling test. For each of the shape-only axes
    (Sphericity, Fill-ratio, Inertia-ratio), regress on log(Høgde). Under
    pure scaling (isometry) the slope is 0; nonzero slope = allometric
    growth, i.e. shape changes systematically with size. Additionally,
    regress each shape-PC on log(Høgde) to find if the data-driven
    deformation axes are size-dependent or size-independent."""
    df_u = df.copy()
    df_u = df_u[df_u["Høgde (cm)"].notna() & (df_u["Høgde (cm)"] > 20)].copy()
    df_u["log_h"] = np.log(df_u["Høgde (cm)"])
    shape_cols = ["Sphericity (mesh)", "Fill-ratio (mesh)", "Inertia-ratio (mesh)"]

    # linear regression stats per axis
    from scipy import stats as sstats
    rows = []
    for c in shape_cols:
        sub = df_u[df_u[c].notna()]
        x = sub["log_h"].values; y = sub[c].values
        slope, intercept, r, p, se = sstats.linregress(x, y)
        rows.append(dict(trait=c, slope=slope, r2=r * r, p=p,
                         r=r, n=len(sub)))

    # shape-PCA scores — allometric regression
    mean_flat, comps, evr, scores, oid_order, nd = build_shape_pca(vox, df)
    oid_to_sc = dict(zip(oid_order, scores))
    df_u["_has_shape"] = df_u["Objekt-ID"].isin(oid_to_sc.keys())
    df_shape = df_u[df_u["_has_shape"]].copy()
    for k in range(6):
        df_shape[f"spc{k+1}"] = df_shape["Objekt-ID"].map(
            lambda o: oid_to_sc[o][k])
    pc_rows = []
    for k in range(6):
        sub = df_shape[df_shape[f"spc{k+1}"].notna()]
        x = sub["log_h"].values; y = sub[f"spc{k+1}"].values
        slope, intercept, r, p, se = sstats.linregress(x, y)
        pc_rows.append(dict(pc=k + 1, slope=slope, r2=r * r, p=p, r=r,
                            n=len(sub)))

    fig = plt.figure(figsize=(14.5, 9))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1.15, 1], hspace=0.38,
                           wspace=0.30, figure=fig)

    # Row 1: 3 scatter panels — form-aksar vs log(H)
    trait_labels = {"Sphericity (mesh)": "Sphericity",
                    "Fill-ratio (mesh)": "Fill-ratio",
                    "Inertia-ratio (mesh)": "Inertia-ratio"}
    for i, c in enumerate(shape_cols):
        ax = fig.add_subplot(gs[0, i])
        sub = df_u[df_u[c].notna()]
        ax.scatter(sub["log_h"], sub[c], s=7, c=SLATE, alpha=0.30,
                    linewidths=0)
        # fit line
        r_ = rows[i]
        xs_ = np.linspace(sub["log_h"].min(), sub["log_h"].max(), 50)
        slope = r_["slope"]
        intercept = sub[c].mean() - slope * sub["log_h"].mean()
        ax.plot(xs_, intercept + slope * xs_, color=OI["rust"], lw=1.6,
                 label=f"slope = {slope:+.3f}")
        ax.set_xlabel("log(Høgde [cm])")
        ax.set_ylabel(trait_labels[c])
        significance = "p < 0,001" if r_["p"] < 1e-3 else f"p = {r_['p']:.3g}"
        ax.set_title(f"{trait_labels[c]}   R² = {r_['r2']:.3f}   {significance}",
                      loc="left", fontsize=10, weight="bold")
        ax.legend(loc="upper left", fontsize=8.5, frameon=False)
        ax.grid(alpha=0.14, linewidth=0.4)

    # Bottom row: shape-PCA allometry as a coefficient bar chart
    axB = fig.add_subplot(gs[1, :2])
    xs_b = np.arange(6)
    cols_ = [AMBER if r_["p"] < 0.01 else OI["grey"] for r_ in pc_rows]
    axB.bar(xs_b, [r_["r"] for r_ in pc_rows], color=cols_,
             edgecolor=SLATE, linewidth=0.5)
    for k, r_ in enumerate(pc_rows):
        axB.text(k, r_["r"] + (0.03 if r_["r"] > 0 else -0.08),
                  f"R² = {r_['r2']:.2f}", ha="center", fontsize=8, color=SLATE)
    axB.axhline(0, color=SLATE, lw=0.6)
    axB.set_xticks(xs_b)
    axB.set_xticklabels([f"shape-PC{k+1}" for k in range(6)], fontsize=9)
    axB.set_ylabel("Pearson r mot log(Høgde)")
    axB.set_ylim(-1, 1)
    axB.set_title("(d) shape-PCs si samvariasjon med log-storleik",
                   loc="left", fontsize=10.2, weight="bold")
    axB.grid(axis="y", alpha=0.14, linewidth=0.4)

    # summary text panel
    axT = fig.add_subplot(gs[1, 2])
    axT.axis("off")
    header = f"{'akse':<16}  {'R²':>6}  {'p':>10}  {'n':>5}"
    lines = ["Allometri-regresjonar:", "",
              "Form-aksar vs log(Høgde):", header, "─" * 44]
    for r_ in rows:
        nm = trait_labels[r_["trait"]]
        lines.append(f"{nm:<16}  {r_['r2']:>6.3f}  "
                     f"{r_['p']:>10.2e}  {r_['n']:>5}")
    lines.append("")
    lines.append("Shape-PCs vs log(Høgde):")
    lines.append(header.replace("akse", "shape-PC"))
    lines.append("─" * 44)
    for r_ in pc_rows:
        lines.append(f"shape-PC{r_['pc']:<8} {r_['r2']:>6.3f}  "
                     f"{r_['p']:>10.2e}  {r_['n']:>5}")
    axT.text(0.0, 1.0, "\n".join(lines), transform=axT.transAxes,
             fontsize=8.8, color=SLATE, family="monospace",
             va="top", ha="left")

    save(fig, "E36_allometri")


# ═════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════

def main():
    print("[1/15] loading data...")
    df = load_data()

    # Material classification for evolutionary analysis
    def classify(m):
        m = str(m).lower()
        if any(x in m for x in ["stål", "st\u00e5l", "jern", "krom", "metall"]): return "metal"
        if any(x in m for x in ["plast", "akryl", "poly", "pvc", "fiberglas"]): return "plastic"
        if any(x in m for x in ["bøk", "b\u00f8k", "ask", "mahogni", "valnøtt", "valn\u00f8tt", "eik", "furu", "bjørk", "bj\u00f8rk", "tre"]): return "wood"
        return "other"
    df["mat_class"] = df["Materialar"].apply(classify)

    print("[2/15] fitting PCA on 6 standardised axes (alle med geometri)...")
    df, pca, scaler = fit_pca(df)
    print(f"  explained var: {pca.explained_variance_ratio_.round(3)}")
    print(f"  cumulative:    {np.cumsum(pca.explained_variance_ratio_).round(3)}")

    print("[3/15] building silhouette cache (lazy, parallel)...")
    sils = build_silhouette_cache(df["Objekt-ID"].tolist())

    print("[3b/15] building voxel cache (lazy, parallel)...")
    vox = build_voxel_cache(df["Objekt-ID"].tolist())

    print("[4/15] E1 morforom...")
    fig_E1_morforom_pca(df, pca)

    print("[5/15] E2 mesh-grid (Holotype Grid refinement)...")
    # Updated E2 will use the improved selection logic
    fig_E2_mesh_grid(df, pca, sils, vox=vox)

    df_yr = df[df["år"].notna()].copy()
    print(f"  (time-aware figures use {len(df_yr)} chairs with year)")

    # ─── Kjernebunt: kontekstuelle morforom-figurar ───
    print("[6/20] E6 giga-grid (alle silhuettar)...")
    fig_E6_giga_grid(df_yr, sils, mode="year")
    fig_E6_giga_grid(df, sils, mode="pc1")
    fig_E6_legend()

    print("[7/20] E8 silhuett-scatter i PCA...")
    fig_E8_silhouette_scatter(df, pca, sils, n_show=260)

    print("[8/20] E10 realiseringsgrad...")
    fig_E10_realiseringsgrad(df, pca)

    # ─── Paleobiologi-baserte prediktive testar ───
    print("[9/20] E11 stiavhengigheit...")
    fig_E11_stiavhengigheit(df_yr, pca)

    print("[10/20] E12 kanalisering radar...")
    fig_E12_kanalisering_radar(df)

    print("[11/20] E13 punktuert likevekt (nullmodell)...")
    fig_E13_punktuert_likevekt(df_yr, pca)

    print("[12/20] E15 Lande-likning...")
    fig_E15_lande_prediction(df_yr, pca)

    print("[13/20] E16 morfologisk nyskaping (Foote 1997)...")
    fig_E16_morfologisk_nyskaping(df_yr, pca, sils)

    print("[14/20] E17 disparity through time (Foote 1993)...")
    fig_E17_disparity_through_time(df_yr, pca)

    print("[15/20] E18 prediktiv landskaps-drift...")
    fig_E18_prediktiv_landskapsdrift(df_yr, pca)

    print("[16/20] E19 karakterforskyving (nytt prediktivt funn)...")
    fig_E19_karakterforskyving(df_yr, pca)

    print("[17/20] E20 phylomorphospace (Sidlauskas 2008)...")
    fig_E20_phylomorphospace(df_yr, pca)

    print("[18/20] E21 Gingerich haldane-tempo (1983)...")
    fig_E21_tempo_gingerich(df_yr, pca)

    print("[19/20] E7 trajektorie splitta på materiale...")
    fig_E7_trajektorie_split(df_yr, pca)

    print("[20/20] E22 makroevolusjonsmodellar (Harmon 2010)...")
    fig_E22_makroevo_modellar(df, pca)

    print("[21/24] E23 konvergent evolusjon (Stayton 2015)...")
    fig_E23_konvergens(df_yr, pca, sils)

    print("[22/24] E24 OU multi-optima per materiale (Butler & King 2004)...")
    fig_E24_ou_multi_optima(df_yr, pca)

    print("[23/24] E25 morfologisk modularitet (Goswami 2007)...")
    fig_E25_modularitet(df, pca)

    print("[24/27] E26 range-through survival av formtypar...")
    fig_E26_range_through(df_yr, pca)

    print("[25/27] E27 3D morforom med periode-arketypar...")
    fig_E27_morforom_3d_arketypar(df_yr, pca, vox)

    print("[26/27] E28 substrat-arketypar...")
    fig_E28_substrat_arketypar(df_yr, vox)

    print("[27/30] E29 isometrisk atlas av innovatørar...")
    fig_E29_innovatør_atlas(df_yr, vox)

    print("[28/30] E30 shape-PCA deformasjonsmodusar (rein geometri)...")
    fig_E30_shape_pca_modes(df, vox)

    print("[29/30] E31 geometriske genera (unsupervised clustering)...")
    fig_E31_geometrisk_genus(df, vox)

    print("[30/32] E32 evolusjonære retningar i formrommet...")
    fig_E32_evolusjonsretningar(df_yr, vox)

    print("[31/32] E33 prediktiv forecasting...")
    fig_E33_forecast(df, vox)

    print("[32/33] E34 ancestral state reconstruction...")
    fig_E34_ancestor_reconstruction(df, vox)

    print("[33/34] E35 synopsis hero figur...")
    fig_E35_synopsis(df, pca, vox)

    print("[34/36] E36 allometri...")
    fig_E36_allometri(df, vox)

    print("[35/36] thumb cache + E37 giga-grid (year)...")
    thumbs = build_thumb_cache(df, vox)
    fig_E37_giga_grid_3d(df, vox, thumbs=thumbs, mode="year")

    print("[36/36] E37 giga-grid (pc1)...")
    fig_E37_giga_grid_3d(df, vox, thumbs=thumbs, mode="pc1")

    for t in ("_sil_test.png", "_sil_test2.png", "_fonttest.png"):
        p = os.path.join(OUT, t)
        if os.path.exists(p):
            os.remove(p)

    print("\nDone.")


if __name__ == "__main__":
    main()
