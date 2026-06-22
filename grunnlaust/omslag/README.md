# GRUNNLAUS DESIGN — smussomslag

Trykkjeklar smussomslag-spreidning (dust jacket) for boka.

## Bygg

```sh
make            # python3 make-art.py  →  xelatex omslag.tex  →  omslag.pdf
```

Krev `xelatex` og `python3` med `Pillow` + `python-barcode`
(`pip install Pillow python-barcode`).

## Filer

- `omslag.tex` — spreidninga: bakflik · bakside · rygg · framside · framflik,
  med 3 mm utfall og skjere-/brettemerke. Alle mål i parameterblokka øvst.
- `make-art.py` — genererer rasterelementa: den frosta display-tittelen
  (ekte gaussisk uskarpleik, Pillow) og EAN-13-strekkoden.
- `art/` — generert (title-frost.png, ean13.png).

## Mål og parametrar (i `omslag.tex`)

| Parameter | Verdi  | Merknad |
|-----------|--------|---------|
| TRIMW × TRIMH | 165 × 240 mm | bokformat (som brødteksten) |
| SPINE     | 16 mm  | rygg — rekn om ved anna sidetal/papir (295 s. ≈ 15,5 mm) |
| FLAP      | 90 mm  | flikbreidd |
| BLEED     | 3 mm   | utfall |
| AARSTAL   | 2028   | NB: kolofonen i boka er datert 2026 |

## Ting å stadfeste før trykk

- **ISBN** (`978-82-9561-84-7`) er eit plasshaldar; byt ut i `make-art.py`.
- **Ryggbreidd** avheng av endeleg papir og innbinding.
- **Display-fonten** er Liberation Sans Bold (fri Helvetica-ekvivalent);
  byt til den lisensierte grotesken før endeleg trykk om ynskjeleg.
