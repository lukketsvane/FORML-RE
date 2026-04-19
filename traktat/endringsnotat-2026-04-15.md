# Endringsnotat — 2026-04-15

**Redaktør:** Claude (under rettleiing av Iver Raknes Finne)
**Utgåve:** Andre klargjering før ekstern lesing (sjå `traktat copy.pdf` for førre versjon)

---

## Kvifor desse endringane

Ein teknisk artikkel (proporsjonsgrammatikk.tex) bygd på traktaten kravde at éin formel proposisjon vart siterbar: at shape grammars (Stiny & Gips, 1972) og tanke-kunnskapsteorien (Hatchuel & Weil, 2009) er degenererte grensetilfelle av Formlære. Under granskinga viste det seg at traktaten alt inneheldt alle komponentane som trengdest for å formulere proposisjonen, men at tre avgjerande grep mangla:

1. **Kjerne-likninga** stod berre i kommentarfeltet (prop 6.12 i kommentar-seksjonen), ikkje som ein nummerert hovudproposisjon i hovudteksten.
2. **Reduksjonsteoremet** var antyda i prop 5.31 ("Grammatikkoperasjonen er ein C→C-partisjon") men aldri eksplisitt formulert. Utan det kunne ingen artikkel sitere traktaten for påstanden.
3. **Meta-teoremet** — at ein teori utan kompetanse-lag ikkje kan predikere sviktsignatur — var implisitt i prop 7.1 men ikkje eksplisitt. Dette er det diagnostiske kjernebidraget.

Kvart av dei tre er i seg sjølv ein liten endring; saman lukkar dei argumentasjonen i traktaten og gjev designteorifaget det formelle fundamentet det til no har mangla.

---

## Endringar i `proposisjonar.tex`

### Lagt til etter prop 5.641 (slutten av kapittel 5)

- **5.7 (d)** — Kjerne-likninga: Form = SG(∇_{C(A)} L(c, t)). Promotert frå kommentarfeltet til hovudtekst. Dette er den matematiske kulminasjonen av kapittel 5.
- **5.71 (o)** — Strukturelt skjema; namngjev komponentane, spesifiserer ikkje den funksjonelle forma.
- **5.72 (t)** — Reduksjonsteoremet. Tabellform. Grensetilfelle (i) rein SG når ∇L ≡ 0, |A| = 1, Π = (M, ∅, ∅); (ii) rein CK når SG = id_M, L = 𝟙_K.
- **5.721 (t)** — Konsekvens: SG og CK er degenererte grensetilfelle, ikkje konkurrerande rammeverk.
- **5.722 (t)** — Konsekvens: kvar av dei to åleine er systematisk utilstrekkeleg for ikkje-degenererte designsituasjonar.
- **5.723 (t)** — Lukkingspåstand: likninga har akkurat tre lag, ikkje fleire og ikkje færre.

### Lagt til etter prop 7.14 (midt i kapittel 7)

- **7.15 (t)** — Meta-teoremet: teori utan lyskjegle kan ikkje predikera sviktsignatur.
- **7.151 (t)** — Grunnen: utan representasjonsgrense finst inga akse å peike ut som urepresentert.
- **7.152 (t)** — Spesifisert for dei to grensetilfella: rein SG kan generere språket men ikkje utpeike svikt; rein CK kan partisjonere men ikkje utlede signatur.
- **7.153 (t)** — Konsekvens: sviktsignaturen er prøvesteinen, ikkje ein bonus. Ein teori som ikkje predikerer han, forklarer ikkje form.

## Endringar i `traktat.tex` (kommentarfeltet)

- **6.12-notatet** (gammal kommentar om kjerne-likninga) → omskrive til **5.7-notat**, no med F = ma-analogien plassert som kommentar til den nye hovudproposisjonen.
- **Ny 5.72-kommentar** — plasserer reduksjonsteoremet i historisk kontekst: forklarer kvifor Stiny-tradisjonen og Hatchuel-tradisjonen har utvikla seg uavhengig.
- **Ny 5.722-kommentar** — praktiske konsekvensar: analysar som siterer berre ein tradisjon kvalifiserer seg som grensetilfelle.
- **Ny 7.15-kommentar** — bind meta-teoremet til 5.722: at ingen tidlegare designteori har begge lag er den historiske diagnosen.
- **CK-kritikk-notat** — utvida med referanse til reduksjonsteoremet: innvendinga mot CK er ein diagnose av grensetilfellet, ikkje ein feil.

## Ikkje endra

- Dei sju hovudproposisjonane og kapittelinndelinga.
- Etterordet, føreordet, appellen.
- Referanselista, ordlista.
- Formalismen for SG (5.301) og agent-Lyapunov (etter 5.11) — desse var tilstrekkelege.
- Den normative proposisjonen 7.2 og oppfølgjarane.

---

## Konsekvensar for tilhøyrande tekstar

### `proporsjonsgrammatikk.tex`
Kan no sitere `(Finne, 2026, prop. 5.72)` for reduksjonsproposisjonen i staden for å føra bevisskisse sjølv. Dette frigjer plass i den firesiders-artikkelen og gjer arkitekturen reinare: traktaten bevisar, artikkelen instansierer.

### Framtidige anvendte artiklar
Meta-teoremet (7.15) gjev direkte sitat for diagnostiske argument: "Per Finne (2026, prop. 7.15), ein teori utan omgrep for kognitiv lyskjegle kan ikkje predikera sviktsignatur." Dette forventast å vera hyppig sitert i kritikk av einsidige designrammeverk.

### For lesarar utan matematisk bakgrunn
Reduksjonsteoremet sin tabellform (prop 5.72) er laga så lesaren kan forstå poenget utan å løyse det matematisk: SG er det som blir att når seleksjonstrykket forsvinn; CK er det som blir att når geometrien forsvinn. Den verbale forklaringa kjem i 5.721–5.723.

---

## Revideringspotensial (lågare prioritet, sidan teknisk-arbeidet i artikkelen går først)

- **Prop 5.31** kan styrkast: noverande "Grammatikkoperasjonen er ein C→C-partisjon" er no delvis redundant med 5.72. Kunne forenklast til ein enkel peikar på 5.72.
- **Prop 6.12** i hovudteksten (multiskalar agens) har same nummer som den gamle kommentaren. Det har aldri vore ein konflikt, men tydelegaste versjon ville fjerna gamle 6.12-kommentar-referansen heilt. *Gjort no.*
- **Appendiks** med formelt skisse-bevis av 5.72 kunne leggjast til for lesarar som krev det. Ikkje prioritert sidan hovudteksten er skrive for filosofisk, ikkje matematisk, strenghet.
- **Glossary** kan oppdaterast med ny entry for "reduksjonsteorem" som peikar til 5.72.

---

## Versjonsmerknader

- Linjetaljing og skuttlan: endringane legg til 11 proposisjonar, fjernar 0, omformulerer 1 kommentar.
- PDF-vekst: forventa ~1 side (proposisjonane er tette, tabellar er små).
- Kompileringskommando: `xelatex -output-directory=build traktat.tex` to gonger for å løyse kryssrefer
anse.
