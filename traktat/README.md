# FORMLÆRE

Teksten vert redigert éin stad og lesen av den same parseren før nettstad, LaTeX og PDF vert bygde. Føreord, lesekode, proposisjonar, notat, referansar og figurar høyrer til same utgåve.

## Kva me redigerer

| Fil | Innhald |
| --- | --- |
| `tekst/formlaere.txt` | Føreord, lesekode og alle proposisjonar, med formatering og kjeldemarkørar. |
| `kjelder.json` | Bibliografipostar og notat med stabile ID-ar og mål i teksten. |
| `figurar.json` | Plassering, filnamn og alternativ tekst for figurar. |
| `edition.json` | Tittel, forfattar og reglar for utgåva, mellom anna utelatne kjelde-ID-ar. |

Sjølve biletfilene ligg i `nettstad/illustrations/`. Ei endring i figurplasseringa skal gjerast i `figurar.json`, slik at begge formata får same figur på same stad.

Dette er dei fire felles innhaldsfilene. Me vedlikeheld ingen eigen kopi av teksten i HTML eller LaTeX. Utforming og funksjon ligg i `layout/`, `nettstad/` og `scripts/`.

## Tekst og kjelder

Ein proposisjon har ei logisk adresse og ein statusbokstav:

```text
**1.01d** Å skilje noko ut er å halde noko anna utanfor.
```

Statusane er `d`, `a`, `t`, `o` og `i`. Fleire avsnitt høyrer til same proposisjon fram til neste adresse eller overskrift. Bruk `*kursiv*` og `**feit**` i teksten.

Kjeldetilvisingar er uttrykkelege markørar:

```text
Ei utsegn.[[kjelde:3,8,58]]
```

Vanlege tal, proposisjonsnummer og matematiske eksponentar vert ikkje tolka som kjelder. Ei ukjend eller feilforma tilvising stoppar byggjet. Me treng difor ikkje lenger å halde ved like teiknplasseringar eller kopiar av heile avsnitt for å lenkje ei kjelde.

Eit proposisjonsnotat vert knytt til den stabile adressa i `kjelder.json`. Notat som høyrer til føreordet, får ei uttrykkeleg plassering i tekstfila, til dømes `[[notat:intro-1]]`. Notat-ID-en vert verande den same sjølv om visningsnummeret endrar seg. Kjelde-ID-ar er òg stabile: hòl i nummereringa skal ikkje fyllast ved å flytte seinare nummer.

Migreringa bevarer den publiserte utgåva med 375 proposisjonar, 41 notat, 108 referansar og seks figurar. Desse tala er ein kontroll av overføringa, ikkje ei fast grense i lesaren. Nye, gyldige proposisjonar krev inga endring av ein teljekonstant.

Det publiserte føreordet er bevart ordrett. Kjelde-ID `108` er utelaten med vilje, og holet i nummereringa skal stå.

## Éin kommando etter ei endring

Frå `traktat/`:

```sh
make all
```

Kommandoen kontrollerer kjeldene, byggjer LaTeX, kompilerer PDF-en og lagar nettutgåva. Først når heile byggjet har lukkast, er utgåva klar til å publiserast. Dette er eit lokalt byggjesteg som må køyrast etter redigering; det skjer ingen automatisk publisering berre ved å lagre tekstfila.

Etterpå skal dei endra kjeldefilene og heile `pdf/` leggjast i same commit. Dersom me har endra utforming eller byggjekode, må dei endringane òg vere med. Me redigerer aldri den genererte PDF-en eller LaTeX-fila for hand.

| Resultat | Rolle |
| --- | --- |
| `pdf/formlaere.pdf` | Utskriftsversjonen, kompilert med XeLaTeX. |
| `pdf/formlaere-latex.zip` | Portabel LaTeX-fil med dei figurane ho nyttar. |
| `pdf/release.json` | Kjeldehash, inngangsfiler, kontrolltal og hashar for utskriftsfilene. |
| `build/document.json` | Felles, validert dokumentmodell som begge framstillingane nyttar. |
| `build/latex/` | Mellombelse LaTeX-filer og kompileringsloggar. |
| `nettstad/dist/` | Ferdig nettutgåve med same PDF, LaTeX-pakke og kjeldehash. |

Berre utskriftsfilene i `pdf/` vert lagde i git. `build/` og `nettstad/dist/` er mellombelse byggjeresultat.

## Avhengnader

Byggjet krev Python 3.12, Node.js, GNU Make og XeLaTeX. Python-avhengnadene er festa i `requirements-build.txt`:

```sh
python3 -m pip install -r requirements-build.txt
```

På Ubuntu 24.04 kan TeX og kontrollverktøya installerast slik:

```sh
sudo apt-get update
sudo apt-get install --no-install-recommends texlive-xetex texlive-latex-extra texlive-lang-european texlive-fonts-recommended fonts-dejavu-core poppler-utils
```

PDF-byggjet nyttar mellom anna `fontspec`, `polyglossia` og `unicode-math`. Det stoppar ved manglande glyffar eller linjer som går ut over tekstfeltet. Figurane følgjer LaTeX-pakka, så ho kan kompilerast etter utpakking med same TeX-avhengnader:

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error formlaere.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error formlaere.tex
```

## Kontroll og publisering

| Kommando | Kva han gjer |
| --- | --- |
| `make check` | Kontrollerer parser, kjelder, migrering og lesarkode. |
| `make pdf` | Byggjer PDF, portabel LaTeX-pakke og utskriftsmanifest. |
| `make web` | Byggjer nettutgåva dersom utskriftsfilene høyrer til noverande kjelde. |
| `make check-generated` | Avviser manglande, endra eller utdaterte utskriftsfiler. |
| `make clean` | Fjernar mellombelse byggjefiler og nettbyggjet, men bevarer `pdf/`. |

Kjeldehashen tek med innhald, figurar, utforming og byggjekode. Nettstad og PDF ber den same hashen. `make web` nektar å kopiere ein gammal PDF inn i ei ny nettutgåve; løysinga er å køyre `make all` og committe dei oppdaterte utskriftsfilene.

GitHub-kontrollen køyrer `make check-generated` før han byggjer på nytt. Ein commit med tekstendringar og gammal PDF vert difor avvist. Deretter byggjer kontrollen heile utgåva og prøver å kompilere den portable LaTeX-pakka for seg. Ferdig nettutgåve og utskriftsfiler vert lagra som byggjeartefaktar. Kontrollen endrar ikkje git og publiserer ikkje nettstaden.

Nettutgåva vert publisert frå `nettstad/dist/`. Ho er éi side med føreordet på `/#introduksjon`, heile teksten og notat og referansar til slutt. Eldre lesaradresser peikar vidare til denne sida. PWA-filene vert genererte saman med utgåva, og opne leseøkter vert ikkje tvinga til å laste på nytt ved ei oppdatering.

På Vercel skal prosjektrota vere `traktat`. `vercel.json` i denne mappa er det eine aktive oppsettet for byggjekommando, resultatmappe, omdirigeringar og mellomlagring.

## Kvar den tidlegare teksten ligg

`archive/2026-11-01/` tek vare på migreringsgrunnlaget og det som ikkje var med i den publiserte utgåva. Testane nyttar dette som eit fast samanlikningsgrunnlag. Tidlegare LaTeX-oppsett og PDF-filer ligg i `archive/legacy-layout/` og `archive/legacy-pdf/`. Pensjonerte byggjarar og nettlesarfiler ligg i git-historia.

Vidare tekstarbeid skal gjerast i dei fire aktive innhaldsfilene over. Arkivet er dokumentasjon av tidlegare tilstand.
