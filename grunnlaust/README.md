# GRUNNLAUST — Ei avrekning med designutdanninga

Den destruktive tvillingen til **FORMLÆRE**-traktaten. Der traktaten byggjer
grunnen designfaget kan stå på, river denne boka ned påstanden om at faget alt
har ein. Bok-manus, nynorsk, polemisk.

## Tese

Designfaget er det einaste profesjonsfaget som deler ut grader i ein kompetanse
det ikkje kan definere, måle eller forsvare. Det manglar ei grammatikk — ein
presis modell av kva ei form er, kva som verkar på henne, og kva som vert lagt
til side. Utan det har faget ingen intern måte å seie nei på, verken til det
dårlege arbeidet eller til det skadelege. Boka fører dette i bevis pilar for
pilar, og peikar til slutt mot det einaste fundamentet eg veit om som kan fylle
holet: rammeverket i traktaten.

## Struktur

| Fil | Kapittel |
|-----|----------|
| `src/00-forord.tex` | Føreord — klagemålet i kortform |
| `src/01-klagemaalet.tex` | I. Klagemålet |
| `src/02-tomme-formelen.tex` | II. Den tomme formelen (*form follows function*) |
| `src/03-atelieret.tex` | III. Atelieret (kritikk og smak forkledd som dom) |
| `src/04-pensum-av-laan.tex` | IV. Pensum av lån (design thinking, stilhistorie) |
| `src/05-forsking-utan-objekt.tex` | V. Forskinga utan objekt (forsking gjennom design, vrange problem) |
| `src/06-kan-ikkje-seie-nei.tex` | VI. Faget som ikkje kan seie nei (Palantir, etikken som tillegg) |
| `src/07-sjolvbedraget.tex` | VII. Sjølvbedraget (akkreditering, prisar, fagfelle) |
| `src/08-avleggaren.tex` | VIII. Avleggaren (frenologi, Kuhn, agentisk materiale) |
| `src/09-grunnen.tex` | IX. Grunnen (den konstruktive vendinga — éi setning, éi likning) |
| `src/10-etterord.tex` | Etterord: til dei som skal rive |
| `src/99-referansar.tex` | Notar og referansar |

## Bygg

```sh
make            # → pdf/grunnlaust.pdf
```

Krev `xelatex`. Brødtekst i EB Garamond (fallback TeX Gyre Pagella), same
font-familie som traktaten. Symbol-fallback via Cambria Math / Symbola.

## Tilhøvet til resten av prosjektet

`GRUNNLAUST` er meint å lesast saman med `traktat/` (FORMLÆRE). Diagnosen her
er grunngjeven der: påstandane i kapittel IX om at eit fundament finst, står i
full aksiomatisk form med falsifiseringsvilkår i traktaten.
