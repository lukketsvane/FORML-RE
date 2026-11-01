# FORMLÆRE

LaTeX-manuskriptet er kjelda for både nettstaden og PDF-en. Begge vert bygde frå den same validerte dokumentmodellen, lesen frå `tekst/formlaere.tex`. Føreord, lesekode, proposisjonar, ordliste, notat, referansar og figurar høyrer til same utgåve.

## Kva me redigerer

| Fil | Innhald |
| --- | --- |
| `tekst/formlaere.tex` | Autoritativt LaTeX-manuskript: føreord, lesekode og alle proposisjonar, med matematikk, formatering og kjeldemarkørar. |
| `kjelder.json` | Bibliografipostar og notat med stabile ID-ar og mål i teksten. |
| `figurar.json` | Plassering, filnamn og alternativ tekst for figurar. |
| `edition.json` | Tittel, forfattar og reglar for utgåva, mellom anna utelatne kjelde-ID-ar. |
| `ordliste.json` | Omgrep med stabile ID-ar, korte forklaringar og tilvisingar til proposisjonane dei byggjer på. |

Sjølve biletfilene ligg i `nettstad/illustrations/`. Ei endring i figurplasseringa skal gjerast i `figurar.json`, slik at begge formata får same figur på same stad. Nye diagram vert redigerte som SVG. Nettstaden nyttar SVG-fila direkte; utskriftsbyggjet lagar ein vektor-PDF av henne til LaTeX og den portable pakka. Pakka inneheld berre figurane den aktive utgåva nyttar.

Dette er dei fem felles innhaldsfilene. Me vedlikeheld ingen eigen kopi av manuskriptet i tekstfiler eller HTML. LaTeX-kjelda er handredigert; PDF-oppsettet og nettutgåva er genererte. Ordlista har éi felles JSON-kjelde. Utforming og funksjon ligg i `layout/`, `nettstad/` og `scripts/`.

Den særskilde matematiske kortversjonen under «tl;dr» er redigert i `nettstad/kortversjon.tex` og kompilert til `nettstad/kortversjon.html` med Pandoc og native MathML. Ho ligg på `/kortversjon/` og får to spalter ved utskrift. `make all` byggjer kortversjonen automatisk frå LaTeX. `make web` og `make check-generated` kontrollerer både kjeldefingeravtrykket og heile den genererte HTML-fila, utan å krevje Pandoc. Endra eller avkorta HTML vert avvist sjølv om kjeldemarkøren står att. Ei kjeldeendring under konvertering stoppar byggjet og bevarer førre HTML-utgåve. Den fulltekstbaserte proposisjonsoversikta ligg i tillegg på `/kort/`. Kortversjonen følgjer dei vanlege utgåvekontrollane.

## Tekst og kjelder

Ein proposisjon har ei logisk adresse og ein statusbokstav:

```latex
\begin{formproposition}{1.01}{d}
Å skilje noko ut er å halde noko anna utanfor.
\end{formproposition}
```

Statusane er `d`, `a`, `t`, `o` og `i`. Tom line skil avsnitt innanfor same proposisjon. Bruk `\emph{kursiv}`, `\textbf{feit}`, `\section{Føreord}` og `\section{Lesekode}`. Skriv matematikk som vanleg LaTeX, til dømes `\(\frac{a}{b}\)` i ei line eller `\[ ... \]` som ei eiga likning. PDF-en nyttar uttrykket direkte; Pandoc omset det same uttrykket til native MathML for nettlesaren. Begge utgåvene får den same kjeldehashen.

Parseren støttar eit avgrensa LaTeX-språk og avviser ukjende kommandoar, uavslutta grupper og ugyldig matematikk. Dette hindrar at innhald forsvinn eller vert ulikt i dei to formata. Escape spesialteikn i brødtekst (`\%`, `\&`, `\_`); makrodefinisjonar og vilkårleg `\input` høyrer ikkje til manuskriptet.

Kjeldetilvisingar er uttrykkelege kommandoar:

```latex
Ei utsegn.\kjelder{3,8,58}
```

Vanlege tal, proposisjonsnummer og matematiske eksponentar vert ikkje tolka som kjelder. Ei ukjend eller feilforma tilvising stoppar byggjet. Me treng difor ikkje lenger å halde ved like teiknplasseringar eller kopiar av heile avsnitt for å lenkje ei kjelde.

Eit proposisjonsnotat vert knytt til den stabile adressa i `kjelder.json`. Notat som høyrer til føreordet, får ei uttrykkeleg plassering i manuskriptet, til dømes `\notat{intro-1}`. Notat-ID-en vert verande den same sjølv om visningsnummeret endrar seg. Kjelde-ID-ar er òg stabile og skal ikkje flyttast for å fylle hòl. Byggjet gjev dei aktive kjeldene samanhengande visningsnummer frå 1 i bibliografirekkjefølgje. Tilvisingar i tekst, ordliste og notat nyttar desse same nummera i PDF og nettutgåva; lenkjer og PDF-anker nyttar framleis kjelde-ID-en.

Alle aktive kjelder skal vere brukte i teksten, notata eller ordlista. `requireReferencedSources` i `edition.json` gjer dette til ein byggjekontroll. Dublettar kan få eit direkte alias i `kjelder.json`, til dømes `"aliases": {"63": "19"}`. Gamle lenkjer og PDF-anker vert då bevarte utan ei ekstra bibliografioppføring. Kjelder som vert tekne ut, vert arkiverte med opphavleg metadata og grunn for uttaket.

Det historiske migreringsgrunnlaget i arkivet har 375 proposisjonar, 41 notat, 108 referansar og seks figurar. Desse tala høyrer til arkivprøva, ikkje den gjeldande utgåva eller ei fast grense i lesaren. LaTeX-migreringa bevarer alle dei 377 proposisjonsadressene i den gjeldande teksten. Nye, gyldige proposisjonar krev inga endring av ein teljekonstant.

Det publiserte føreordet er bevart ordrett. Kjelde-ID `108` er utelaten med vilje og skal ikkje brukast på nytt. Utelatne ID-ar gjev ikkje hòl i den synlege referanselista.

## Ordliste

Ordlista forklarer innlånte fagomgrep teksten føreset at lesaren kjenner, og viser korleis omgrep frå ulike fagfelt møtest i teksten. Ho skal ikkje gjenta definisjonane i proposisjonane. Ho står før notat og referansar i begge framstillingane og vert redigert berre i `ordliste.json`:

```json
{
  "schemaVersion": 1,
  "entries": [
    {
      "id": "fri-energi-prinsippet",
      "term": "Fri energi-prinsippet",
      "definition": "Teoretisk ramme for persepsjon og handling i sjølvorganiserte system.",
      "propositions": ["5.11"],
      "sources": ["19"]
    }
  ]
}
```

`symbol` er eit valfritt felt med vanleg Unicode-notasjon. ID-en skal vere ein stabil slug med små ASCII-bokstavar, tal og bindestrek. `propositions` peikar til kvar omgrepet vert brukt; `sources` peikar til grunnlaget i den felles bibliografien. `fields` er ei valfri liste over fagfelt. `connection` vert vist under «I teksten:» og forklarer koplinga til teksten, med skilje mellom analogi, overlapp og fagleg identitet. Forklaringane skal vere korte og på nynorsk; krysskoplingar skal ikkje omdefinere modellen eller framstille ulike fagomgrep som synonym. Parseren avviser duplikat, tomme forklaringar og ukjende tilvisingar. Ei endring i ordlista krev eit nytt komplett bygg på same måte som ei tekstendring.

## Éin kommando etter ei endring

Frå `traktat/`:

```sh
make all
```

Kommandoen kontrollerer kjeldene, byggjer LaTeX, kompilerer PDF-en og lagar nettutgåva. Utskriftsfilene vert klargjorde som éi komplett mappe med PDF, LaTeX-pakke og manifest før dei erstattar førre utgåve. Nettbyggjet vert òg klargjort før utskifting. Ved feil under pakking eller utskifting vert førre komplette utgåve bevart. Byggjet stoppar dersom kjelder, figurar eller byggjeinngangar endrar seg undervegs; køyr kommandoen på nytt etter redigeringa. Først når heile byggjet har lukkast, er utgåva klar til å publiserast. Dette er eit lokalt byggjesteg som må køyrast etter redigering; det skjer ingen automatisk publisering berre ved å lagre LaTeX-kjelda.

Etterpå skal dei endra kjeldefilene og heile `pdf/` leggjast i same commit. Dersom me har endra utforming eller byggjekode, må dei endringane òg vere med. Me redigerer aldri den genererte PDF-en eller LaTeX-byggjefila i `build/latex/` for hand. Den handredigerte kjelda er `tekst/formlaere.tex`.

| Resultat | Rolle |
| --- | --- |
| `pdf/formlaere.pdf` | Utskriftsversjonen, kompilert med XeLaTeX. |
| `pdf/formlaere-latex.zip` | Portabel LaTeX-utgåve med aktive figurar; `source/` inneheld det redigerbare manuskriptet og felles katalogar. |
| `pdf/release.json` | Kjeldehash, inngangsfiler, kontrolltal og hashar for utskriftsfilene. |
| `build/document.json` | Felles, validert dokumentmodell som begge framstillingane nyttar. |
| `build/latex/` | Mellombelse LaTeX-filer og kompileringsloggar. |
| `nettstad/dist/` | Ferdig nettutgåve med same PDF, LaTeX-pakke og kjeldehash. |

Berre utskriftsfilene i `pdf/` vert lagde i git. `build/` og `nettstad/dist/` er mellombelse byggjeresultat.

## Avhengnader

Heile byggjet krev Python 3.12, Node.js, GNU Make, Pandoc og XeLaTeX. Publiseringssteget `make web` krev berre Python: MathML-en vert henta frå den kontrollerte utskriftsutgåva, og kvar formel må svare til den gjeldande LaTeX-kjelda. Python-avhengnadene er festa i `requirements-build.txt`:

```sh
python3 -m pip install -r requirements-build.txt
```

På Ubuntu 24.04 kan TeX og kontrollverktøya installerast slik:

```sh
sudo apt-get update
sudo apt-get install --no-install-recommends texlive-xetex texlive-latex-extra texlive-lang-european texlive-fonts-recommended fonts-dejavu-core poppler-utils libcairo2 pandoc
```

PDF-byggjet nyttar mellom anna `fontspec`, `polyglossia` og `unicode-math`. CairoSVG lagar vektor-PDF frå SVG-kjeldene. Byggjet stoppar ved manglande glyffar eller linjer som går ut over tekstfeltet. Dei ferdig konverterte figurane følgjer LaTeX-pakka; ho kan kompilerast etter utpakking med same TeX-avhengnader, utan CairoSVG:

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error formlaere.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error formlaere.tex
```

PDF-en har bokformatet 125 × 200 mm, med eiga tittelside, marginale proposisjonsnummer og seksjon/sidetal i toppteksten. Tittelsida hentar tittel, undertittel og forfattaropplysningar frå den same LaTeX-kjelda som nettstaden.

Den trykte boka nyttar dei faste EB Garamond-filene i `layout/fonts/`, med optiske variantar for brødtekst og liten skrift. Fontane er uendra frå pakkene `fonts-ebgaramond` og `fonts-ebgaramond-extra`, versjon `0.016+git20230418-2`; opphav og SIL Open Font License følgjer i same mappe. Byggjet kopierer fontane og lisensen til den portable LaTeX-pakka, så utforminga ikkje avheng av kva Garamond-versjon som er installert på maskina. Omslagsbiletet i `layout/cover-stolar.png` er den uendra stolmosaikken frå den tidlegare bokutgåva og følgjer òg pakka. Desse filene høyrer til utforminga og er med i den felles kjeldehashen.

## Kontroll og publisering

| Kommando | Kva han gjer |
| --- | --- |
| `make check` | Kontrollerer parser, kjelder, migrering og lesarkode. |
| `make pdf` | Byggjer PDF, portabel LaTeX-pakke og utskriftsmanifest. |
| `make web` | Byggjer nettutgåva dersom utskriftsfilene høyrer til noverande kjelde. |
| `make check-generated` | Avviser manglande, endra eller utdaterte utskriftsfiler. |
| `make clean` | Fjernar mellombelse byggjefiler og nettbyggjet, men bevarer `pdf/`. |

Kjeldehashen tek med innhald, figurar, utforming og byggjekode. Nettstad og PDF ber den same hashen. Den avleidde MathML-cachen ligg òg i den hashkontrollerte LaTeX-pakka; nettbyggjet krev at cachen der og i utskriftsmanifestet er identiske før formlane vert tekne i bruk. `make web` nektar å kopiere ein gammal PDF inn i ei ny nettutgåve; løysinga er å køyre `make all` og committe dei oppdaterte utskriftsfilene.

GitHub-kontrollen køyrer `make check-generated` før han byggjer på nytt. Ein commit med tekstendringar og gammal PDF vert difor avvist. Deretter byggjer kontrollen heile utgåva og prøver å kompilere den portable LaTeX-pakka for seg. Ferdig nettutgåve og utskriftsfiler vert lagra som byggjeartefaktar. Kontrollen endrar ikkje git og publiserer ikkje nettstaden.

Nettutgåva vert publisert frå `nettstad/dist/`. Ho er éi side med føreordet på `/#introduksjon`, heile teksten og notat og referansar til slutt. Eldre lesaradresser peikar vidare til denne sida. PWA-filene vert genererte saman med utgåva, og opne leseøkter vert ikkje tvinga til å laste på nytt ved ei oppdatering.

På Vercel skal prosjektrota vere `traktat`. `vercel.json` i denne mappa er det eine aktive oppsettet for byggjekommando, resultatmappe, omdirigeringar og mellomlagring.

## Kvar den tidlegare teksten ligg

Den tidlegare aktive `tekst/formlaere.txt` er fjerna; git-historia tek vare på henne. Ho er ikkje eit byggjeinngangspunkt. `layout/authoring.tex` kan nyttast til ein enkel, sjølvstendig førehandsvising av LaTeX-manuskriptet; `make all` byggjer den komplette utgåva med ordliste, notat, kjelder og figurar.

`archive/2026-11-01/` tek vare på migreringsgrunnlaget og det som ikkje var med i den publiserte utgåva. Testane nyttar dette som eit fast samanlikningsgrunnlag. Tidlegare LaTeX-oppsett og PDF-filer ligg i `archive/legacy-layout/` og `archive/legacy-pdf/`. Pensjonerte byggjarar og nettlesarfiler ligg i git-historia.

Kjeldeoppryddinga tek vare på bibliografien før gjennomgangen i `bibliography-before-audit-b2a208.json` og på uttaka med grunngjeving i `retired-references-b2a208.json`. Erstatta og uttekne illustrasjonar ligg uendra i `archive/2026-11-01/illustrations/`.

Vidare tekstarbeid skal gjerast i dei fem aktive innhaldsfilene over. Arkivet er dokumentasjon av tidlegare tilstand.
