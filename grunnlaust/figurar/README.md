# Figurar — GRUNNLAUS DESIGN

Strek- og diagram-illustrasjonar til boka, med transparent bakgrunn og
trimma til motivet (ingen tom monn).

## Reprosessering

```sh
python3 fjern-bakgrunn.py  KJELDE.png  UT.png  [KJELDE2.png UT2.png ...]
```

`fjern-bakgrunn.py` gjer den kremfargen bakgrunnen transparent (alpha frå
kor mykje mørkare pikselen er enn bakgrunnen, så kantutjamning og tynne
strekar blir bevarte), behaldar original-RGB, og autocroppar til dei
synlege pikslane. Krev `Pillow` + `numpy`.

## Filer

| Fil | Motiv |
|-----|-------|
| `laug-manufaktur-industri.png` | laug → manufaktur → industri (som teiknar / som lagar) |
| `hand-vs-maskin.png` | handa vs. maskina; forma flytta ut |
| `crystal-palace.png` | Crystal Palace + verdas ting → fyrste reform-kritikk |
| `ruskin-morris.png` | Ruskin → Morris → gilda / verkstadene |
| `werkbund-akse.png` | Muthesius (standardisering) – Werkbund – Velde (fridom) |
| `bauhaus-hjul.png` | Bauhaus-læreplan: Vorkurs → verkstader → bygg |
| `bauhaus-objekt.png` | Bauhaus-objekt med årstal (1924–1930) |
| `produktlevetid.png` | produktlevetid 1920→2000 (planlagd forelding) |
| `skandinavisk-kart.png` | skandinavisk design / eksportmerke — «ikkje eit fundament» |
| `formgrammatikk-syklus.png` | formgrammatikk → form → agentar → plattform (lukka sløyfe) |
| `ruskin-morris-greiner.png` | Ruskin → Morris → gilda / verkstadene (tre greiner) |
| `modernist-objekt.png` | modernistisk objektkanon med årstal (1925–1952) |
| `bauhaus-hjul-rein.png` | Bauhaus-læreplan som ring (rein versjon) |
| `ulm-matrise.png` | Ulm: verkstad × metodefag (2×2-matrise) |

Dei tre siste opplastingane forfinar tidlegare figurar og er dei som ligg i
boka: `ruskin-morris-greiner` (i staden for `ruskin-morris`), `bauhaus-hjul-rein`
(i staden for `bauhaus-hjul`) og `modernist-objekt` (i staden for
`bauhaus-objekt`). Dei eldre filene er haldne for referanse.
