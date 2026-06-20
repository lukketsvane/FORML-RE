# GRUNNFEST — Forsvaret for designfaget som disiplin

Spegel-tvillingen til **GRUNNLAUST**. Der GRUNNLAUST hevdar at designfaget aldri
nådde eit haldbart fundament, presenterer GRUNNFEST **det motsette synet i si
sterkaste form** (ein stålmann): at design har ei eiga, legitim kunnskapsform,
ein metode, ein etikk og ei stemme — og at kravet om eit naturvitskapleg
«fundament» er ein kategorifeil påført faget utanfrå. Boka les samtidas, og
særleg dei norske/nordiske, designforskarane med på laget.

Dei to bøkene er meinte å lesast mot kvarandre. Eit syn som ikkje toler sitt
eige sterkaste motsvar, fortener ikkje å bli ståande.

## Slik vart boka til

1. **Kartlegging.** Fem parallelle forskingsagentar las samtidslitteraturen
   (særleg norsk/nordisk) på fem frontar: norsk designforsking, designepistemologi,
   metode/vitskap, etikk/profesjon, og design thinking/filosofi. Alle kjelder er
   reelle og verifiserte med URL.
2. **Stålmann.** Funna er kondenserte i [`motargument-katalog.md`](motargument-katalog.md):
   alt som utfordrar GRUNNLAUST-tesen, ført i si sterkaste form, med ærleg
   rangering av kva som råkar hardast og kvar tesen overlever.
3. **Boka.** 17 kapittel i sju delar byggjer forsvaret og endar med eit direkte
   oppgjer mot GRUNNLAUST, påstand for påstand.

## Delar

**I. Det feilstilte spørsmålet** — 01 Kategorifeilen · 02 Kva eit fag er
**II. Design har ei kunnskapsform** — 03 Designerly · 04 Refleksjon-i-handling · 05 Abduksjon og framing
**III. Design har metode og kumulasjon** — 06 Metoden finst · 07 Forsking gjennom design · 08 Kumulasjonen
**IV. Det vrange som innsikt** — 09 Vrange problem rett forstått · 10 Det fjerde kunstfaget
**V. Meining, menneske og det gode** — 11 Den semantiske vendinga · 12 Menneskesentreringa · 13 Etikken og stemma
**VI. Norske og samtidige svar** — 14 Det norske bidraget · 15 Design som verdsskaping
**VII. Oppgjeret** — 16 Mot Grunnlaust · 17 Etterord

## Ærleg om grensene

Stålmannen er ikkje ein triumf. Boka innrømmer det katalogen flaggar som tesens
sterkaste overlevande punkt: design manglar **bindande handheving** (lisensiering /
rett til å utelukke frå yrket, slik arkitektane har) og **éin samla etikk** utleidd
av faget sjølv. Forsvaret hevdar at dette er manglar ved institusjonell modning,
ikkje ved intellektuelt fundament — men nektar dei ikkje.

## Bygg

```sh
make            # xelatex → biber → xelatex → xelatex  →  pdf/grunnfest.pdf
```

Krev `xelatex` og `biber`. `referansar.bib` har ~225 oppføringar (kopiert frå
GRUNNLAUST + tillegg frå kartlegginga). **Ikkje kompilert i sesjonen** der utkastet
vart skrive (miljøet mangla `xelatex`/`biber`); køyr `make` lokalt for PDF.

## Status

Komplett fyrsteutkast av heile strukturen (17 kapittel). Same veg vidare som
GRUNNLAUST: utvide kvart kapittel, utvide litteraturlista, og illustrere.
