#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make-art.py — genererer rasterelementet til GRUNNLAUS-smussomslaget:

  art/title-frost.png   den store, frosta display-tittelen GRUNN / LAUS / DESIGN
                        (GRUNN og DESIGN venstrestilte, LAUS høgrestilt)

Den frosta effekten er ekte gaussisk uskarpleik (Pillow), ikkje ein LaTeX-fake.
Alle mål er i mm; me rasteriserer ved RES dpi. xelatex (omslag.tex) plasserer
PNG-en på framsida med skarp tekst lagt oppå.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

HER = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HER, "art")
os.makedirs(ART, exist_ok=True)

RES = 600                       # dpi — rikeleg for offset
MM  = RES / 25.4                # px per mm
def mm(x): return int(round(x * MM))

# Liberation Sans Bold == metrisk Helvetica/Arial; den frie grotesk-ekvivalenten.
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

INK = (43, 41, 38)              # varm mørk grå — tittelfargen

# --------------------------------------------------------------------------
# Frosta tittel — GRUNN/DESIGN venstrestilt, LAUS høgrestilt
# --------------------------------------------------------------------------
def lag_tittel():
    # (ord, justering): "L" = venstre, "R" = høgre
    linjer = [("GRUNN", "L"), ("LAUS", "R"), ("DESIGN", "L")]
    mal_breidd_mm = 132.0        # «GRUNN»/«DESIGN» skal spenne om lag så breitt
    blur_mm       = 1.15         # uskarpleik-radius (frost)
    leading       = 0.92         # linjeavstand som faktor av cap-storleik (tett)

    breiast = max((o for o, _ in linjer), key=len)
    pt = 10
    while True:
        f = ImageFont.truetype(FONT_BOLD, pt)
        if f.getbbox(breiast)[2] >= mm(mal_breidd_mm):
            break
        pt += 4
    font = ImageFont.truetype(FONT_BOLD, pt)

    capb = font.getbbox("H")
    cap_h = capb[3] - capb[1]
    line_step = int(round(cap_h * (1 + leading)))

    pad = mm(blur_mm * 4)        # rom rundt for at bluren ikkje skal klippast
    tekstbreidd = max(font.getbbox(o)[2] for o, _ in linjer)
    breidd = tekstbreidd + pad * 2
    hogd   = line_step * (len(linjer) - 1) + cap_h + pad * 2

    img  = Image.new("RGBA", (breidd, hogd), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = pad
    for o, just in linjer:
        b = font.getbbox(o)
        w = b[2] - b[0]
        x = pad - b[0] if just == "L" else pad + (tekstbreidd - w) - b[0]
        draw.text((x, y - b[1]), o, font=font, fill=INK + (255,))
        y += line_step

    img = img.filter(ImageFilter.GaussianBlur(radius=mm(blur_mm)))
    ut = os.path.join(ART, "title-frost.png")
    img.save(ut, dpi=(RES, RES))
    print(f"  art/title-frost.png  {img.width}x{img.height}px  (pt={pt})")

# --------------------------------------------------------------------------
# Frosta grunn — teksturert varmgrå bakgrunn + gjennomskinleg frosta panel
# (glassine-effekten). Full omslagsstorleik; tittel/tekst leggjast oppå i TeX.
# --------------------------------------------------------------------------
def lag_grunn():
    import numpy as np
    W_MM, H_MM = 165.0, 240.0          # trim (= framsidepanelet)
    DPI = 400                          # lågfrekvent motiv; held fila nede
    px = lambda mmv: int(round(mmv / 25.4 * DPI))
    W, H = px(W_MM), px(H_MM)
    rng = np.random.default_rng(7)

    base = np.array([201, 197, 188], float)     # varm grå grunn
    img = np.ones((H, W, 3)) * base

    # mjuk vertikal gradient (litt lysare mot midten)
    yy = np.linspace(-1, 1, H)[:, None, None]
    img += (1 - yy**2) * 7.0

    # vertikale «pensel»-strok: 1D-støy langs x, mjuka, strekt loddrett
    streak = rng.normal(0, 1, W)
    k = max(3, W // 90)
    ker = np.ones(k) / k
    streak = np.convolve(streak, ker, mode="same")
    img += (streak[None, :, None]) * 3.0
    # fin korn-støy
    img += rng.normal(0, 1.0, (H, W, 1))

    # frosta panel: lysare rektangel med svært mjuke (blura) kantar
    panel = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(panel)
    x0, x1 = int(0.115 * W), int(0.885 * W)
    y0, y1 = int(0.135 * H), int(0.795 * H)
    d.rectangle([x0, y0, x1, y1], fill=255)
    panel = panel.filter(ImageFilter.GaussianBlur(radius=px(8.0)))   # fjør kantane
    a = (np.asarray(panel, float) / 255.0)[:, :, None] * 0.62        # paneldekkevne
    panel_col = np.array([231, 227, 219], float)                     # frosta lysare
    img = img * (1 - a) + panel_col * a

    out = Image.fromarray(np.clip(img, 0, 255).astype("uint8"), "RGB")
    ut = os.path.join(ART, "cover-ground.png")
    out.save(ut, dpi=(DPI, DPI))
    print(f"  art/cover-ground.png  {out.width}x{out.height}px")

if __name__ == "__main__":
    print("genererer omslags-art:")
    lag_tittel()
    lag_grunn()
    print("ferdig.")
