#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make-art.py — genererer rasterelementa til GRUNNLAUS-smussomslaget:

  art/title-frost.png   den store, frosta display-tittelen GRUNN / LAUS / DESIGN
  art/ean13.png         ISBN-strekkoden (EAN-13)

Den frosta effekten er ekte gaussisk uskarpleik (Pillow), ikkje ein LaTeX-fake.
Alle mål er i mm; me rasteriserer ved RES dpi. xelatex (omslag.tex) plasserer
PNG-ane på rett panel med skarp tekst lagt oppå.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, barcode
from barcode.writer import ImageWriter

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
# 1) Frosta tittel
# --------------------------------------------------------------------------
def lag_tittel():
    ord_ = ["GRUNN", "LAUS", "DESIGN"]
    mal_breidd_mm = 132.0        # «GRUNN»/«DESIGN» skal spenne om lag så breitt
    blur_mm       = 1.15         # uskarpleik-radius (frost)
    leading       = 0.92         # linjeavstand som faktor av cap-storleik (tett)

    # finn punktstorleik slik at det breiaste ordet treffer mal-breidda
    breiast = max(ord_, key=len)
    pt = 10
    while True:
        f = ImageFont.truetype(FONT_BOLD, pt)
        w = f.getbbox(breiast)[2]
        if w >= mm(mal_breidd_mm):
            break
        pt += 4
    font = ImageFont.truetype(FONT_BOLD, pt)

    capb = font.getbbox("H")
    cap_h = capb[3] - capb[1]
    line_step = int(round(cap_h * (1 + leading)))

    pad = mm(blur_mm * 4)        # rom rundt for at bluren ikkje skal klippast
    breidd = max(font.getbbox(o)[2] for o in ord_) + pad * 2
    hogd   = line_step * (len(ord_) - 1) + cap_h + pad * 2

    img  = Image.new("RGBA", (breidd, hogd), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = pad
    for o in ord_:
        b = font.getbbox(o)
        draw.text((pad - b[0], y - b[1]), o, font=font, fill=INK + (255,))
        y += line_step

    img = img.filter(ImageFilter.GaussianBlur(radius=mm(blur_mm)))
    ut = os.path.join(ART, "title-frost.png")
    img.save(ut, dpi=(RES, RES))
    print(f"  art/title-frost.png  {img.width}x{img.height}px  (pt={pt})")

# --------------------------------------------------------------------------
# 2) EAN-13 strekkode
# --------------------------------------------------------------------------
def lag_strekkode():
    EAN = barcode.get_barcode_class("ean13")
    code = EAN("978822956184", writer=ImageWriter())   # check-siffer => ...847
    opts = dict(module_width=0.30, module_height=14.0, font_size=8,
                text_distance=3.0, quiet_zone=3.0, dpi=RES,
                background="white", foreground="black", write_text=True)
    sti = code.save(os.path.join(ART, "ean13"), options=opts)
    print(f"  art/{os.path.basename(sti)}  (EAN-13 {code.get_fullcode()})")

if __name__ == "__main__":
    print("genererer omslags-art:")
    lag_tittel()
    lag_strekkode()
    print("ferdig.")
