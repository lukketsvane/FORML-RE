# GRUNNLAUS DESIGN — omslag

Trykkjeklare omslagsfiler for boka:

- **`omslag.pdf`** — smussomslag (dust jacket, med flikar).
- **`omslag-perm.pdf`** — hardcase-perm (case wrap, utan flikar), med ombrett
  (turn-in), bordovergrep (square) og falsgap dimensjonert for innbindinga.

## Bygg

```sh
make            # python3 make-art.py  →  xelatex  →  omslag.pdf + omslag-perm.pdf
```

Krev `xelatex` og `python3` med `Pillow` (`pip install Pillow`).

## Filer

- `omslag.tex` — smussomslaget: bakflik · bakside · rygg · framside · framflik,
  3 mm utfall + skjere-/brettemerke.
- `omslag-perm.tex` — hardcase-permen: ombrett · bakbord · fals · rygg · fals ·
  frambord · ombrett, med fals-/score- og skjeremerke. Bokbinding-måla
  (bordtjukn, blokk-rygg, falsgap, ombrett) ligg i parameterblokka øvst.
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

- **ISBN/strekkode** er plasshaldar (EAN-13 `978-82-95123-45-1`, generert i
  `make-art.py`); set inn det endelege ISBN-et før trykk.
- **Ryggbreidd** avheng av endeleg papir og innbinding. Permen
  (`omslag-perm.tex`) reknar rygg = blokk-rygg + 2 × bordtjukn; juster
  `\BLOCK`, `\BOARDTH`, `\HINGE` og `\TURNIN` mot bokbindaren sine mål.
- **Display-fonten** er Liberation Sans Bold (fri Helvetica-ekvivalent);
  byt til den lisensierte grotesken før endeleg trykk om ynskjeleg.
