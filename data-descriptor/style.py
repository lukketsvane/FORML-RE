"""
style.py -- Shared aesthetic and data-loading utilities for STOLAR Paper A.

All figure scripts import this module.  Call apply_style() once before plotting.
"""

from __future__ import annotations
import pathlib, warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# ── paths ────────────────────────────────────────────────────────────────────
REPO   = pathlib.Path(__file__).resolve().parents[2]       # stolar-db root
DATA   = REPO / "STOLAR"
FIG_DIR = pathlib.Path(__file__).resolve().parent / "figures"

# ── palette (from FORMLÆRE traktat aesthetic) ────────────────────────────────
INK          = "#1A1A1A"
INK_SOFT     = "#4A4A4A"
RULE         = "#B8B4AC"
PAPER        = "#FAFAF7"
ACCENT_RUST  = "#B8542A"
ACCENT_TEAL  = "#2B5F75"
ACCENT_GOLD  = "#B4892A"
HIGHLIGHT    = "#E8DDC4"

# extended palette for 15 style periods
STYLE_PALETTE = [
    "#2B5F75",  # Renessanse
    "#3A7C8F",  # Barokk
    "#4A9EA8",  # Rokokko
    "#B4892A",  # Nyklassisisme
    "#D4A84B",  # Empire
    "#C9944A",  # Historisme
    "#B8542A",  # Viktorianisme
    "#C96B3C",  # Jugend / Art Nouveau
    "#8B5E3C",  # Art Deco / Tidleg modernisme
    "#6B5B4F",  # Funksjonalisme
    "#5A5A5A",  # Bauhaus
    "#3D3D3D",  # Modernisme / Midtjahrhundre
    "#1A1A1A",  # Midtjahrhundre modernisme
    "#7A3B2E",  # Postmodernisme
    "#4A4A4A",  # Samtidsdesign
]

CENTURY_COLORS = {
    "1200-talet": "#2B5F75",
    "1300-talet": "#2E6A82",
    "1400-talet": "#337A93",
    "1500-talet": "#3A8BA3",
    "1600-talet": "#4A9EA8",
    "1700-talet": "#B4892A",
    "1800-talet": "#D4A84B",
    "1900-talet": "#B8542A",
    "2000-talet": "#1A1A1A",
}

# ── typography ───────────────────────────────────────────────────────────────
FONT_FAMILY = "EB Garamond"
FONT_MONO   = "IBM Plex Mono"

# ── figure sizing (Scientific Data: 170 mm max width) ────────────────────────
MM  = 1 / 25.4
FULL_W = 170 * MM   # ~6.69 in
HALF_W = 82 * MM    # ~3.23 in
GOLDEN = (1 + 5**0.5) / 2
DPI    = 300

# ── canonical style-period ordering (chronological) ──────────────────────────
STYLE_ORDER = [
    "Renessanse",
    "Barokk",
    "Rokokko",
    "Nyklassisisme",
    "Empire",
    "Historisme",
    "Viktorianisme",
    "Jugend/Art Nouveau",
    "Art Deco / Tidleg modernisme",
    "Funksjonalisme",
    "Bauhaus",
    "Modernisme / Midtjahrhundre",
    "Midtjahrhundre modernisme",
    "Postmodernisme",
    "Samtidsdesign",
]

STYLE_COLOR = dict(zip(STYLE_ORDER, STYLE_PALETTE))

# ── column mapping (Nynorsk -> English) ──────────────────────────────────────
_COL_MAP = {
    "Namn":                          "name",
    "Objekt-ID":                     "id",
    "Nemning":                       "type",
    "Materialar":                    "material",
    "Materialkommentar":             "material_desc",
    "Datering":                      "dating",
    "Frå år":                        "year_from",
    "Til år":                        "year_to",
    "Hundreår":                      "century",
    "Stilperiode":                   "style",
    "Produsent":                     "designer",
    "Produksjonsstad":               "origin",
    "Nasjonalitet":                  "nationality",
    "Høgde (cm)":                    "height_cm",
    "Breidde (cm)":                  "width_cm",
    "Djupn (cm)":                    "depth_cm",
    "Setehøgde (cm)":               "seat_height_cm",
    "Estimert vekt (kg)":            "weight_kg",
    "Teknikk":                       "technique",
    "Emneord":                       "keywords",
    "Erverving":                     "acquisition",
    "Nasjonalmuseet":                "museum_url",
    "Bilete-URL":                    "image_url",
    "Bilete-bguw":                   "bguw_url",
    "3D-modell":                     "glb_url",
    "Sphericity (mesh)":             "sphericity",
    "Fill-ratio (mesh)":             "fill_ratio",
    "Inertia-ratio (mesh)":          "inertia_ratio",
    "Kompleksitet (mesh, log10 v/a)":"complexity",
    "Konveks hylster-volum (m³)":    "hull_volume",
}

# ── public helpers ───────────────────────────────────────────────────────────

def apply_style() -> None:
    """Set matplotlib rcParams for the STOLAR paper aesthetic."""
    # detect font availability
    from matplotlib.font_manager import findSystemFonts, FontProperties
    available = {pathlib.Path(f).stem for f in findSystemFonts()}
    family = "serif"  # EB Garamond via LaTeX; matplotlib uses serif fallback

    mpl.rcParams.update({
        "font.family":       family,
        "font.size":         9,
        "axes.titlesize":    10,
        "axes.labelsize":    9,
        "xtick.labelsize":   7,
        "ytick.labelsize":   7,
        "legend.fontsize":   7.5,
        "figure.facecolor":  PAPER,
        "axes.facecolor":    PAPER,
        "savefig.facecolor": PAPER,
        "axes.edgecolor":    INK_SOFT,
        "axes.linewidth":    0.5,
        "axes.grid":         False,
        "grid.color":        RULE,
        "grid.alpha":        0.3,
        "grid.linewidth":    0.4,
        "xtick.color":       INK,
        "ytick.color":       INK,
        "text.color":        INK,
        "axes.labelcolor":   INK,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "figure.dpi":        DPI,
        "savefig.dpi":       DPI,
        "savefig.bbox":      "tight",
        "savefig.pad_inches": 0.05,
    })


def fig_full(aspect: float = GOLDEN, **kw) -> tuple:
    """Return (fig, ax) at full journal width."""
    fig, ax = plt.subplots(figsize=(FULL_W, FULL_W / aspect), **kw)
    return fig, ax


def fig_half(aspect: float = GOLDEN, **kw) -> tuple:
    """Return (fig, ax) at half journal width."""
    fig, ax = plt.subplots(figsize=(HALF_W, HALF_W / aspect), **kw)
    return fig, ax


def fig_panels(ncols: int, nrows: int = 1, aspect: float = GOLDEN,
               height_ratio: float = 1.0, **kw) -> tuple:
    """Return (fig, axes) sized for multi-panel layout."""
    h = (FULL_W / ncols / aspect) * nrows * height_ratio
    fig, axes = plt.subplots(nrows, ncols, figsize=(FULL_W, h), **kw)
    return fig, axes


def save_fig(fig, name: str, directory: pathlib.Path | None = None,
             formats: tuple = ("pdf", "png")) -> None:
    """Save figure to directory in specified formats."""
    d = directory or FIG_DIR
    d.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(d / f"{name}.{fmt}")
    plt.close(fig)


def load_stolar() -> pd.DataFrame:
    """Load STOLAR.csv, rename columns to English, compute year_mid."""
    df = pd.read_csv(DATA / "STOLAR.csv", encoding="utf-8")
    df = df.rename(columns=_COL_MAP)
    # numeric coercion
    for c in ("height_cm", "width_cm", "depth_cm", "seat_height_cm",
              "weight_kg", "year_from", "year_to",
              "sphericity", "fill_ratio", "inertia_ratio",
              "complexity", "hull_volume"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # year midpoint
    df["year_mid"] = df[["year_from", "year_to"]].mean(axis=1)
    df.loc[df["year_mid"].isna(), "year_mid"] = df.loc[df["year_mid"].isna(), "year_from"]
    # museum source
    df["museum"] = df["id"].apply(
        lambda x: "Nasjonalmuseet" if str(x).startswith(("NMK", "OK-", "NAMF"))
        else "V&A" if str(x).startswith("O") else "Ukjend"
    )
    return df


def load_mesh_features() -> pd.DataFrame:
    """Load mesh_features.csv with full geometric columns."""
    return pd.read_csv(DATA / "mesh_features.csv", encoding="utf-8")


def style_order(df: pd.DataFrame, min_n: int = 20) -> list[str]:
    """Return style periods present in df with n >= min_n, in chronological order."""
    counts = df["style"].value_counts()
    valid = {s for s, n in counts.items() if n >= min_n}
    return [s for s in STYLE_ORDER if s in valid]


def style_cmap() -> ListedColormap:
    """Categorical colormap for style periods."""
    return ListedColormap(STYLE_PALETTE[:len(STYLE_ORDER)])


def century_cmap() -> LinearSegmentedColormap:
    """Sequential colormap for centuries (teal -> gold -> rust -> ink)."""
    colors = ["#2B5F75", "#4A9EA8", "#B4892A", "#D4A84B", "#B8542A", "#1A1A1A"]
    return LinearSegmentedColormap.from_list("century", colors)


def annotate_panel(ax, label: str, x: float = -0.08, y: float = 1.05) -> None:
    """Add a panel label (A, B, C...) to an axes."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=12, fontweight="bold", va="top", ha="right", color=INK)
