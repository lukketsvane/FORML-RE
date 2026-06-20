# Plan: neste runde — GRUNNLAUST mot 500–600 sider

## Status no (commit 62d60aa)
- **295 sider**, 32 kapittel i 7 delar. Reint bygg (xelatex + biber), 0 feil, 0 manglande glyfar.
- Modulær apparatur (`\laeringsmal` + `\ovingar` + `kasus`) på **24/32** kapittel.
- **3 illustrasjonar** (tidslinje, stil-mot-form, greine-tabell). ~230 kjelder i `referansar.bib`.
- Verktøykjede installert (xelatex, biber, EB Garamond, Symbola, DejaVu). `make` byggjer på minutt.

## Mål
500–600 sider, rikt illustrert, modulær hovudlærebok for eit femårig masterløp. Kvar setning skal gjere arbeid (kvesse medan vi utvidar).

---

## RUNDE (neste) — prioritert

### 1. Fullfør modulær apparatur  *(rask, konsistens)*
Legg `\laeringsmal` + `\ovingar` på dei seks innhaldskapitla som manglar dei:
`12-designmetode`, `16-forsking-utan-objekt`, `21-kan-ikkje-seie-nei`,
`25-grunnen`, `greinene`, `siste-metoden`, `innvendingane`.
(`00-til-lesaren` og `26-etterord` treng dei ikkje.) Audit til slutt: alle innhaldskapittel har begge.

### 2. Modulær semesterstruktur
- Merk kvar **del** med tilrådd semester (t.d. Del I–III = 1.–2. semester, IV–V = 3., VI–VII = 4.–5.).
- Legg ein kort **«Til undervisaren»**-bolk i `00-til-lesaren` med tre leseløp (historisk, kritisk, teoretisk).

### 3. Djupne-pass A — historiske kapittel (Del I–III)
+1000–1500 ord berande kasus per kapittel. Konkrete kandidatkasus:
- *01 Form før faget:* laugsvedtektene; mester–svenn-prøva.
- *03 Utstilling/reform:* «Chamber of Horrors» (Cole, 1852) i detalj; South Kensington-modellen.
- *04 Arts & Crafts:* Morris & Co.-rekneskapen (luksusparadokset i tal).
- *06 Bauhaus:* Vorkurs-oppgåver (Albers' papirøvingar); Hannes Meyer-strida.
- *08 Ulm:* Ulm-modellen og HfG-pengane; Braun SK-serien.
- *09 Styling:* Brooks Stevens' eigne ord om «planned obsolescence» (1954); Loewy MAYA.
- *10 Skandinavisk:* Stockholmsutstillinga 1930 / *acceptera*; «Design in Scandinavia»-vandringa 1954–57.

### 4. Illustrasjonar (runde 2) — 8–10 nye figurar
- Sullivan/funksjon-tautologien som diagram (to lesingar).
- Bauhaus-organisasjonskart (Vorkurs → verkstad).
- Ulm-kurvet (oppgang/fall 1953–68).
- «Knowledge funnel» (Martin) som mottak for slakt.
- Fogg Behavior Model (B = MAT) + Eyal-sløyfa.
- NASAD: ressurs vs. kvalitet (kva akkreditering måler / ikkje måler).
- Bibliometrisk søyle: h-indeks for «dei ti namna».
- Formlære-likninga som lagdelt diagram (grammatikk/landskap/lyskjegle).
- Ev. reelle bilete frå `../figures/` (STOLAR-stolane) der relevant.

---

## RUNDE +2 (skissert)
5. **Djupne-pass B** — Del IV–VII (same metode, +1000–1500 ord/kapittel).
6. **Litteraturapparat mot ~400 kjelder** (brukartesta-/STS-/utdanningslitteratur; «vidare lesing» fyllast ut).
7. **Indeks** (`makeidx`) + **ordliste** over nøkkelomgrep.
8. **Linje-for-linje kvessepass:** kutt flab, ned til kvart ord; samkøyr stemme på tvers av agent-skrivne parti.

---

## Måltal (omtrentleg)
| Pass | Lagt til | Sum sider |
|------|----------|-----------|
| No | — | 295 |
| Modular + djupne A + figurar | ~80–110 | ~390–400 |
| Djupne B + apparat + indeks | ~110–150 | ~520–550 |

## Risiko / avhengnad
- Agent-sesjonsgrense (nullstiller 12:20 UTC) avgrensar parallell skriving; djupne-pass kan delast over fleire økter.
- Kvessing vs. lengd er i spenn — kvar utviding må vere berande (kasus/evidens), ikkje fyll.
- Halde sitatnøklar i synk med `referansar.bib` (verifiser etter kvar runde: `comm -23` brukte mot definerte nøklar).
