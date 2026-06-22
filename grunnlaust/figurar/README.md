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
