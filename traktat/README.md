# FORMLÆRE

Gjeldande utgåve har 375 proposisjonar. Nettlesaren og LaTeX-utgåva vert genererte frå same tekst og kjeldekatalog.

- `tekst/formlaere.txt`: føreord, lesekode og proposisjonar. `[[kjelde:11,18]]` er ei kjeldetilvising; vanlege tal og matematiske eksponentar er ikkje kjeldetilvisingar.
- `kjelder.json`: 108 bibliografipostar, 47 forankra kjeldenotar og fem føreordnotar. Nummera 1–107 følgjer den eksisterande bibliografien. Wittgenstein er lagt til som 108 for namngjevne tekstlege parallellar.
- `src/traktat.tex`: hovudfil for den gjeldande bokutgåva. `forord.tex`, `proposisjonar.tex`, `referansar.tex` og `kjeldenotar.tex` er genererte filer.
- `nettstad/`: lesar, kjeldetips og seks illustrasjonar. Kjeldelista ved slutten er samanleggbar.
- `pdf/traktat.pdf`: kompilert gjeldande utgåve.

Kjeldeapparatet skil fagleg bakgrunn, vidareføringar i FORMLÆRE og tekstlege parallellar. Eit kjeldenummer er ikkje i seg sjølv eit prov for ei utsegn. Opphavlege bibliografiske metadata er overførte, ikkje systematisk nyverifiserte.

## Bygg og kontroll

Frå denne mappa:

```sh
make check
make web
make pdf
```

Nettbyggjet krev Node.js og ingen tilleggspakkar. Resultatet ligg i `nettstad/dist/`. Bokbyggjet krev Python 3 og XeLaTeX med `fontspec`, `polyglossia` og `unicode-math`.

Vercel byggjer med `traktat` som rotmappe, `node nettstad/build.mjs` som byggjekommando og `nettstad/dist` som resultatmappe. `vercel.json` inneheld desse innstillingane. Dei eldre nettadressene `/traktat/index.html` og `/traktat/scroll.html` er bevarte.

Rediger felles tekst og katalog, køyr kontrollane, og generer begge formata før commit. Eldre utgåver og vedlegg finst i git-historia og dei opphavlege kjeldefilene.
