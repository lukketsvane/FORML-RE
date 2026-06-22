#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fjern-bakgrunn.py — gjer kremfargen bakgrunn transparent på strek-
illustrasjonane, og autocrop til dei synlege pikslane.

Metode:
  * estimer bakgrunnsfargen frå kant-pikslane (median).
  * alpha = kor mykje mørkare pikselen er enn bakgrunnen (per kanal,
    maks), normalisert mellom T0 (støygolv) og T1 (full dekkevne). Dette
    bevarer kantutjamning og tynne strekar, og held grå skuggar dekkjande.
  * behald original-RGB (grå tonar blir verande grå).
  * trim til alfa-boundingboks (ingen tom monn att).
"""
import sys, os
import numpy as np
from PIL import Image

T0 = 14     # støygolv: skilnad <= T0 frå bakgrunn => heilt transparent
T1 = 42     # skilnad >= T1 => heilt dekkjande
PAD = 0     # piksels monn rundt motivet etter trim

def fjern(inn, ut):
    im = Image.open(inn).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape

    # bakgrunn = median av ein 8 px kantramme
    rand = np.concatenate([
        a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3),
        a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    bg = np.median(rand, axis=0)

    # kor mykje mørkare enn bakgrunnen (positiv = mørkare), maks over kanal
    diff = np.clip(bg[None, None, :] - a, 0, None).max(axis=2)
    alpha = np.clip((diff - T0) / (T1 - T0), 0, 1) * 255.0
    alpha = alpha.astype(np.uint8)

    rgba = np.dstack([np.asarray(im), alpha])
    out = Image.fromarray(rgba, "RGBA")

    # autocrop til synlege pikslar
    bbox = out.getbbox()           # bruker alfa
    if bbox:
        if PAD:
            l, t, r, b = bbox
            bbox = (max(0, l-PAD), max(0, t-PAD), min(w, r+PAD), min(h, b+PAD))
        out = out.crop(bbox)
    out.save(ut)
    print(f"  {os.path.basename(ut):28s} {out.size[0]}x{out.size[1]}  (bg≈{tuple(int(x) for x in bg)})")
    return out.size

if __name__ == "__main__":
    pairs = sys.argv[1:]
    for i in range(0, len(pairs), 2):
        fjern(pairs[i], pairs[i+1])
