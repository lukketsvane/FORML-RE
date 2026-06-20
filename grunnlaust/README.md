# GRUNNLAUST — Ein kritisk historie om designfaget og fundamentet det aldri fekk

Hovudlærebok i **kritisk designhistorie** for eit femårig masterløp, og den
historiske tvillingen til **FORMLÆRE**-traktaten. Boka fortel heile
designhistoria — frå laugshandverket til overvakingskapitalismen — men les
henne mot håra: som historia om eit fag som gong på gong lova seg sjølv eit
fundament og kvar gong leverte noko anna (ein stil, ein metode, ein
pedagogikk, ein prosess). Diagnosen blir ikkje hamra inn, men lesen ut av
**fråværa** (ingen internasjonale etiske råd, inga felles etikk, metode,
fagspråk eller stemme) og **skadane** (planlagd forelding, eingongskultur,
ekstraksjon, avhengigheit, algoritmisk styring).

## Omfang

- **27 kapittel** i sju delar + innleiing, etterord og full litteraturliste.
- **~46 000 ord** brødtekst i dette utkastet (veks mot målet på 400–550 sider).
- **Litteraturapparat:** biblatex (forfattar–år), `referansar.bib` med ~165
  reelle, verifiserte kjelder; ~140 aktivt siterte, resten som vidare lesing.
- **Vidare lesing** etter kvart kapittel.

## Delar og kapittel

**I. Føresetnadene** — 01 Form før faget · 02 Skiljet · 03 Den fyrste reforma
**II. Rørslene som lova eit grunnlag** — 04 Arts and Crafts · 05 Werkbund · 06 Bauhaus · 07 Funksjonalismen
**III. Institusjonaliseringa** — 08 Ulm · 09 Amerikansk styling · 10 Skandinavisk · 11 Gute Form / Rams
**IV. Den vitskaplege ambisjonen** — 12 Metoderørsla · 13 Simon · 14 Vrange problem · 15 Atelieret · 16 Forsking utan objekt
**V. Migrasjonen** — 17 Semantisk vending · 18 Brukaren og skjermen · 19 Design thinking (poda som flytta)
**VI. Skadane og fråværa** — 20 Ekstraksjonen · 21 Faget som ikkje kan seie nei · 22 Fråværet · 23 Sjølvbedraget
**VII. Avrekninga** — 24 Avleggaren · 25 Grunnen · 26 Etterord

## Bygg

```sh
make            # xelatex → biber → xelatex → xelatex  →  pd/grunnlaust.pdf
```

Krev `xelatex` og `biber`. Brødtekst i EB Garamond (fallback TeX Gyre Pagella).
Symbol-fallback via Cambria Math / Symbola.

## Status og vegen vidare

Dette er eit komplett **fyrsteutkast av heile strukturen**: alle 27 kapittel er
skrivne, alle sitatnøklar er verifiserte mot `referansar.bib`. Vegen mot full
lengd (400–550 sider) går gjennom (1) utviding av kvart kapittel med fleire
kasus, personar og institusjonar, (2) utviding av `referansar.bib` mot ~400
oppføringar, og (3) illustrasjonar. **Ikkje kompilert i sesjonen der utkastet
vart skrive** (miljøet mangla `xelatex`/`biber`); køyr `make` lokalt for PDF.

## Tilhøvet til resten av prosjektet

Les saman med `traktat/` (FORMLÆRE). Traktaten legg fram fundamentet i full
aksiomatisk form; `GRUNNLAUST` fortel historia som påviser fråvêret av eitt.
