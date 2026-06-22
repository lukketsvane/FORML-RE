# GRUNNLAUS DESIGN — smussomslag

Trykkjeklar smussomslag-spreidning (dust jacket) for boka.

## Bygg

```sh
make            # python3 make-art.py  →  xelatex omslag.tex  →  omslag.pdf
```

Krev `xelatex` og `python3` med `Pillow` (`pip install Pillow`).

## Filer

- `omslag.tex` — spreidninga: bakflik · bakside · rygg · framside · framflik,
  med 3 mm utfall og skjere-/brettemerke. Alle mål i parameterblokka øvst.
- `make-art.py` — genererer den frosta display-tittelen GRUNN / LAUS / DESIGN
  (ekte gaussisk uskarpleik, Pillow; GRUNN/DESIGN venstrestilt, LAUS høgrestilt).
- `art/` — generert (title-frost.png).

## Mål og parametrar (i `omslag.tex`)

| Parameter | Verdi  | Merknad |
|-----------|--------|---------|
| TRIMW × TRIMH | 165 × 240 mm | bokformat (som brødteksten) |
| SPINE     | 16 mm  | rygg — rekn om ved anna sidetal/papir (295 s. ≈ 15,5 mm) |
| FLAP      | 90 mm  | flikbreidd |
| BLEED     | 3 mm   | utfall |
| AARSTAL   | 2028   | NB: kolofonen i boka er datert 2026 |

## Ting å stadfeste før trykk

- **ISBN** er plasshaldar (`978-82-00-00000-0`); set inn det endelege.
  Skal boka i detaljhandel, legg til EAN-13-strekkode på baksida.
- **Ryggbreidd** avheng av endeleg papir og innbinding.
- **Display-fonten** er Liberation Sans Bold (fri Helvetica-ekvivalent);
  byt til den lisensierte grotesken før endeleg trykk om ynskjeleg.
