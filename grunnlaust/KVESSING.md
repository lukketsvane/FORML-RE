# KVESSING — køyrebok for levande-prosa-passet over GRUNNLAUST

Dette er den einaste sanningskjelda for kvessepasset av boka. Kvar autonome
køyring les denne fila fyrst, tek **neste** kapittel som ikkje er gjort, kvessar
det mot standarden under, oppdaterer status-tabellen, og stoppar. Ingen køyring
treng minne om førre; alt som trengst, står her.

> **Kalibrering, les fyrst:** Boka er alt sterk høgregister-nynorsk, ikkje flat
> LLM-prosa. Dette er **kvessing, ikkje riving.** Kutt flab, drep tics, fjern
> strekar, kvess flate parti, varier rytmen. Skriv **ikkje** om sterke avsnitt
> berre for å gjere dei annleis. Behald dei styrande figurane og argumentet. Er
> du i tvil, lat det stå. Den andre døden er like nær som den fyrste: tettleik er
> ikkje løyve til tåke. Kvar vanske må vere fortent. Les høgt.

---

## Harde reglar (bryt dei aldri)

1. **Berre brødtekst og kasus-forteljing.** Rør aldri: `\chapter`/`\section`/
   `\subsection`-struktur, `\cite`/`\autocite`/`\textcite`/`\fullcite`-nøklar,
   `\label`/`\ref`, matematikk, miljønamn, eller innhaldet i `\laeringsmal`,
   `\ovingar` og `\vidarelesing` (pedagogisk apparat — berre lett retting der
   det trengst). Ikkje rør figurfiler, preamble eller `grunnlaust.tex`.
2. **Behald fagvokabularet til boka.** Desse er presise termar, ikkje daude
   figurar — forenkl dei aldri: «form som posisjon i eit rom av moglegheiter»,
   «samtidige seleksjonstrykk», «**navigert av agentar på fleire skalaer**»,
   «formgrammatikk», «tilpassingslandskap», «kognitiv horisont», likninga
   $\mathrm{Form}=SG(\nabla_{C(A)}L(c,t))\cap\lozenge$, «den dobbelte
   bokføringa», «knowing how / knowing that». NB: «navigere» som **daud figur**
   (å «navigere eit landskap av omsyn») skal kuttast; «navigert av agentar» som
   **term** skal stå.
3. **Aldri em-strek (—).** Konverter kvar `—` og kvar dramatisk `–` til komma,
   kolon, semikolon eller punktum. Hald att éin en-strek (`–`, med mellomrom)
   berre for eit ekte langt innskot som alt har komma inni seg. Mål: nær null
   strek per kapittel.
4. **Hald nynorsk-registeret.** fyrst, ikkje, korleis, kva, vert/vart, merksemd,
   augneblink, difor, soleis. Hermeteikn «», enkle ‘ ’ inni. **Inga seriekomma**
   før «og». Sin-genitiv framfor s-genitiv — *unntak:* behald ein s-genitiv når
   han er ein medviten retorisk landing (t.d. «krevje vitskapens stilling på
   handverkets grunnlag»).
5. **Kjønn — sjekk kvart usikre substantiv.** I denne boka: metode (han, *ein*
   metode → «ingen delt metode»), etikk (han, *ein* etikk), språk/fagspråk (det,
   *eit* fagspråk → «ikkje noko felles fagspråk»), line/rørsle/form/hand (ho).
   Den vanlegaste feilen er «inga» på hankjønnsord og hankjønnsbøying av
   hokjønnsord.
6. **Lever som fil, vis diffen.** Helst `Edit` (reine, små diffar). Etter kvart
   kapittel: kontroller at ingen `—` står att, at alle sitatnøklar er urørte, og
   at klammer/miljø balanserer (ikkje bryt byggjet).

---

## Kvessepasset, steg for steg (per kapittel)

1. Les heile `.tex`-fila.
2. Last skillen `levande-prosa` om han finst i miljøet (full standard +
   `references/`). Finst han ikkje, bruk den distillerte standarden under.
3. Køyr tic-jakta (under) og rett kvar treff.
4. Les kvart avsnitt: ber det meir enn éin ting? Varierer rytmen (lang
   oppbygging mot kort dom)? Gjer figuren arbeid? Er det flatt, kvess; er det
   sterkt, lat det stå.
5. Skriv endringane med `Edit`. Behald alle LaTeX-/sitat-/term-token.
6. Verifiser: `grep` etter `—` i fila skal gje 0; sitatnøklar uendra.
7. Oppdater **statustabellen** (sett `✓`, dato, ein-line-notat) og legg ei line i
   **Logg**.
8. Om `bash`/`git` er tilgjengeleg: commit (`kvessing: <fil>`). Elles berre lagre
   — filene ligg trygt på disk uansett.
9. Gjer **1–2 kapittel per køyring** (berre **1** om kapitlet er langt/tett).
   Stopp så. Aldri gjer eit kapittel som alt er `✓`.

### Tic-jakta (distillert standard)

- **Strekar:** sjå regel 3. Dette er det største enkeltgrepet (sjå sensus).
- **Signpost-tics:** «Det er verdt å …», «Legg merke til …», «Sjå kva …», «til
  sjuande og sist», «det handlar eigentleg om». Stryk innleiinga, sei tinget;
  eller bytt til spørjande vending («Men kva slags utsegn er dette?»). Behald
  høgst éin imperativ-peikar («Sjå kva …») per kapittel.
- **Daude figurar / kalkar:** «navigere eit landskap», «dykke ned i», «eit teppe
  av», «i kjernen ligg», «i lys av». Anten ein figur som tenkjer, eller bokstav.
- **Akkresjon:** to avsnitt som seier det same → eitt ryk.
- **Parade:** namn → parafrase → same konklusjon → neste namn. Lat éin tenkjar
  bere djupt, eller gjer rekkja til ein figur.
- **Tese-landinga:** kvart avsnitt som sklir mot same førehandsgitte konklusjon.
  Lat avsnitt lande på ekte vendingar.
- **Ferdiglaga kasus-opnar:** «Prøv eit lite tankeeksperiment …» → start rett i
  tinget.
- **Substantivsjuke / hedging / engelsk syntaks:** skriv kring verbet; tål den
  direkte påstanden; norsk periode, ikkje em-strek-engelsk.

---

## Sensus (frå diagnosen 2026-06-21)

- **Em-strek (`—`, U+2014): 747 treff over 33 filer** — pluss mange en-strekar
  brukte som dramatisk pause. Det dominerande grepet; rett i kvart kapittel.
- **Signpost-tics: 93 treff over 26 filer** (mest «Det er verdt å», «Sjå kva»).
- **Daud-figur-kalkar: 21 treff over 7 filer** (tyngst i 14 og 25 — men i 25 er
  «navigert av agentar» term, ikkje figur).

Em-strek per fil (rettleiande mengd, ikkje uttømande): 02:35 · 03:31 · 04:32 ·
06:34 · 07:30 · 08:29 · 09:35 · 10:36 · 11:28 · 12:16 · 13:24 · 14:17 · 15:21 ·
16:16 · 17:23 · 18:27 · 19:20 · 20:17 · 21:13 · 22:21 · 23:20 · 24:27 · 25:33 ·
26:9 · mislukka-fundamenta:19 · siste-metoden:14 · greinene:27 · dei-ti-namna:38 ·
innvendingane:20 · ordliste:14.

---

## Statustabell (rekkjefølgje som i `grunnlaust.tex`)

Status: `✓` ferdig · `⟳` står for tur · `—` ikkje starta.

| # | Fil | Del | Status | Notat |
|---|-----|-----|--------|-------|
| 00 | 00-til-lesaren | front | ✓ | Strek/kjønn/tics retta; comma-run oppløyst (2026-06-21). |
| 01 | 01-form-for-faget | I | ✓ | Strek→teikn; «Stiltaiande»-overskrift retta; kjønn; tics (2026-06-21). |
| 02 | 02-industri-og-skilje | I | ⟳ | Tyngst på strek (35). |
| 03 | 03-utstilling-og-reform | I | — | |
| 04 | 04-arts-and-crafts | II | — | |
| 05 | 05-werkbund | II | — | |
| 06 | 06-bauhaus | II | — | |
| 07 | 07-funksjonalismen | II | — | |
| 08 | 08-ulm | III | — | |
| 09 | 09-amerikansk-styling | III | — | |
| 10 | 10-skandinavisk | III | — | |
| 11 | 11-gute-form-rams | III | — | |
| 12 | 12-designmetode | IV | — | |
| 13 | 13-simon-vitskap | IV | — | |
| -- | mislukka-fundamenta | IV | — | mellomspel |
| 14 | 14-vrange-problem | IV | — | |
| 15 | 15-atelieret | IV | — | |
| 16 | 16-forsking-utan-objekt | IV | — | |
| -- | siste-metoden | IV | — | mellomspel |
| 17 | 17-semantisk-vending | V | — | |
| 18 | 18-brukaren-skjermen | V | — | |
| 19 | 19-design-thinking | V | — | |
| 20 | 20-merksemd-ekstraksjon | VI | — | |
| 21 | 21-kan-ikkje-seie-nei | VI | — | |
| -- | greinene | VI | — | mellomspel |
| 22 | 22-fravaeret | VI | — | |
| 23 | 23-sjolvbedraget | VI | — | |
| -- | dei-ti-namna | VI | — | mellomspel |
| 24 | 24-avleggaren | VII | — | |
| -- | innvendingane | VII | — | mellomspel |
| 25 | 25-grunnen | VII | — | tett; gjer åleine. «navigert av agentar» = term. |
| 26 | 26-etterord | VII | — | |
| -- | ordliste | bak | — | definisjonar: hald klåre, IKKJE tette. Lett pass. |

Når alle er `✓`: gjer eitt **harmoniseringspass** per del (samkøyr stemme på
tvers av kapittel, fjern att-att av same figur), så set heile passet til ferdig
og noter det i Logg.

### Ein ting å verifisere undervegs
«Boka har sju delar og tjuesju kapittel» (00) og README («27 kapittel») stemmer
ikkje med det faktiske talet `\input` i `grunnlaust.tex`. Ikkje gjett eit nytt
tal; flagg det i Logg så forfattaren kan avgjere den endelege teljinga.

---

## Logg
- 2026-06-21 — Diagnose + mal sett: 00 og 01 kvessa for hand som referanse.
  Køyrebok oppretta. Planlagd vidareføring sett opp.
