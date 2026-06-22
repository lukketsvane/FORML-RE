# Figurar — GRUNNLAUS DESIGN

Strek- og diagram-illustrasjonar til boka, med transparent bakgrunn og
trimma til motivet (ingen tom monn).

## Heilside-oppslag med OpenAI (`teikne-sider.py`)

Genererer **oppslag** (to sider side om side, liggjande) i penn-og-blekk-stilen
til Andreas Töpfer (Avanessian-bøkene) via `gpt-image-2`, ut frå det fungerande
prompt-eksempelet: kort nynorsk-instruks + eit oppslag av bokteksten (≈ to
boksider), med stilreferansar sende med på kvart kall. Lite/inga handskrift —
men brødtekst, header/footer og figurar som eit ekte boksoppslag.

```sh
pip install -r requirements.txt           # openai + Pillow + numpy
export OPENAI_API_KEY=sk-...

# 1) legg 1–6 stilreferansar i  stil-referansar/  (t.d. IMG_4017.jpeg)
# 2) sjå planen utan å kalle APIet (gratis):
python3 teikne-sider.py --proev
# 3) skriv ut ferdige kall til å lime inn sjølv (ingen API-kall):
python3 teikne-sider.py --kode --fraa 2 --grense 5
# 4) eller automatiser heile boka (eitt kall per oppslag, gjenoppstartbart):
python3 teikne-sider.py                   # alle oppslag
python3 teikne-sider.py --grense 1        # berre det fyrste (test)
```

- **Oppslag frå boka** (standard): `del_i_oppslag` deler `src/*.tex` i
  oppslag på ~`--ord` ord (std 850 ≈ to sider) i `\input`-rekkjefølgja frå
  `grunnlaust.tex`; for små halar blir slegne inn i førre oppslag.
- **`--kode`**: skriv ut `client.images.edits(...)`-kall (eitt per oppslag) i
  same form som det fungerande eksempelet — til å lime inn der du vil.
- **`--utsnitt FIL`**: valfri kurert liste med korte parti (`utsnitt.txt`).
- Idempotent (hoppar over ferdige sider; `--paa-nytt` tvingar). Flagg:
  `--modell --storleik --kvalitet --ref-fil --berre --fraa --grense --ut`.
- Utdata: `sider/*.png` + `sider/manifest.json` (PNG-ane er git-ignorerte).

NB: eit oppslag er liggjande, difor `size="3840x2160"`. Sjølve køyringa brukar
`client.images.edit` (eintal — `images.edits` finst ikkje i SDK-en).

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
