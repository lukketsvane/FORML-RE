# Figurar — GRUNNLAUS DESIGN

Strek- og diagram-illustrasjonar til boka, med transparent bakgrunn og
trimma til motivet (ingen tom monn).

## Heilside-teikningar med OpenAI (`teikne-sider.py`)

Genererer heilside-illustrasjonar i penn-og-blekk-stilen til Andreas Töpfer
(Avanessian-bøkene) via `gpt-image-2` (`client.images.edit`), med teksten frå
boka som brief. Lite tekst per side — teikninga tek over storparten av sida.

```sh
pip install -r requirements.txt           # openai + Pillow + numpy
export OPENAI_API_KEY=sk-...

# 1) legg 3–6 stilreferansar i  stil-referansar/  (sjå mappa sin README)
# 2) sjå planen utan å kalle APIet (gratis):
python3 teikne-sider.py --proev
# 3) lag teikningane for dei kuraterte utsnitta i  utsnitt.txt :
python3 teikne-sider.py                   # eitt utsnitt = éi teikning
python3 teikne-sider.py --grense 1        # berre den fyrste (test)
```

- **Kuraterte utsnitt** (føretrekt): `utsnitt.txt` — korte, sterke parti, eitt
  per teikning. Format: blokker skilde med `===`, valfri `@ etikett`-linje.
- **Autokutt** (heile boka): `--auto` deler `src/*.tex` i korte oppslag
  (`--ord N`, std 200) i `\input`-rekkjefølgja frå `grunnlaust.tex`.
- Idempotent (hoppar over ferdige sider; `--paa-nytt` tvingar). Flagg:
  `--modell --storleik --kvalitet --input-fidelity --berre --fraa --ut`.
- Utdata: `sider/*.png` + `sider/manifest.json` (PNG-ane er git-ignorerte).

NB: `images.edit` (eintal) er rett metode; `moderation` finst berre på
`generate`. Boktrimmet er 165×240 mm, så storleiken er ståande (portrett),
ikkje 16:9.

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

| `designmetode-syklus.png` | analyse → syntese → evaluering (metoderørsla) |
| `tamt-vs-vrangt.png` | tamt mot vrangt problem (tabell) |
| `refleksjon-i-handling.png` | handling ↔ refleksjon-i-handling, taus kunnskap (Schön) |
| `forsking-design-venn.png` | research into / through / for design (Frayling) |
| `semiotisk-triangel.png` | objekt – teikn – tyding |
| `form-abstraksjonslag.png` | fysisk produkt → GUI → tenestelag |
| `design-thinking-migrasjon.png` | design thinking → management / offentleg / konsulent |
| `agentar-manglande-nei.png` | form → agentar, kvar utan eit nei |
| `fagsprak-grensa.png` | ICD kryssar grensa, «god balanse» stoggar |
| `ti-namna-falsifisering.png` | dei ti namna: lét det seg falsifisere? |
| `formgrammatikk-syklus-rund.png` | sirkulær variant av formgrammatikk-sløyfa (alternativ) |

`formgrammatikk-syklus.png` vart oppdatert til den boksa, forfina sløyfa.
Dei tre opplastingane som forfinar tidlegare figurar er dei som ligg i boka:
`ruskin-morris-greiner` (for `ruskin-morris`), `bauhaus-hjul-rein` (for
`bauhaus-hjul`) og `modernist-objekt` (for `bauhaus-objekt`). Dei eldre filene
er haldne for referanse.
