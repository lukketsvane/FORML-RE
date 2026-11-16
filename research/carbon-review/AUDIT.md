# Kvalitetsgjennomgang av Carbon-utkastet

**Kjelde:** https://aistudio.google.com/prompts/1XbVeLZDspUaRJPUyoAfDDd-TYB8Jzhm (Google AI Studio, Gemini 4 Carbon, Antigravity Agent Preview).
**Status:** Arbeidsutkast; inga innfletting eller publisering.
**Kanonisk manus SHA-256:** 484d995133f4716f1840d54484b3276606bc1aba323766cfb801307b9ab5dbe6.
**Carbon-utsnitt SHA-256:** 55f853d53e52150d20b92e7ed157d82ad8fdce10e184808fbf51c4cea376389c.

## Kva Carbon gjorde annleis

Carbon leverte eit sammenhengande alternativ frå proposisjon 1 til 7.34, i motsetning til dei svært lokale endringane som den betalte Fable-sløyfa oftast godkjende. Det viser breiare kompositorisk ambisjon, men er ikkje i seg sjølv prov for høgare tekstkvalitet.

## Teknisk og fagleg kontroll

- Kanonisk manus inneheld 491 proposisjonar, Carbon-teksten har 486 attkjende adresser.
- Manglar: `1.2343`, `1.2354`, `2.202`, `2.211`, `2.2011`, `2.2021`, `3.401`, `5.7221`, `5.72312`.
- Ekstra adresser: `2.22`, `3.304`, `3.305`, `3.412`.
- Statusendringar: `1.2341` a til t, `5.722` a til t, `5.724` t til d.
- Kjelder avvik på minst tre stader: 5.401 (92 på main, 69 i Carbon), 6.01 (22,40,41 mot 22,32,33) og 6.753 (22,85,173 mot 22,62,144). Desse kan skuldast ulike kjeldeversjonar; dei er ikkje verifiserte mot kjeldelista.
- I 6.76 kjem «viss og berre viss» tilbake, sjølv om den gjeldande utgåva har fjerna ekvivalensen etter eit motdøme. Dette er ein logisk regresjon.
- Raw Mode er Markdown med matematiske symbol og fotnotetal, ikkje den autoritative LaTeX-kjelda. Matematikk og kjelder kan ikkje overførast mekanisk.
- Utkastet manglar fullstendig føreord og etterord i same autoritative dokument.

## Redaksjonelle kandidatar

| Proposisjon | Main (utdrag) | Carbon (utdrag) | Vurdering |
|---|---|---|---|
| `4` | Landskapet ligg ikkje fast. Det vert endra av nye vilkår og av formene som vert realiserte i det. | Landskapet ligg ikkje fast. Nye vilkår og realiserte former endrar det for kvart seinare steg. | Meir direkte tilbakeverknad. Må prøvast mot vilkår og historie. |
| `6` | Forma oppstår i samspelet mellom grammatikk, kunnskap og agens på fleire skalaer. | Fleire agentar fører steg, kunnskap og omhug inn i same form; det éin realiserer, vert vilkår for ein annan. | Agentane handlar og påverkar kvarandre. Risikerer å miste den generative rolla til grammatikken. |
| `6.661` | Læra seier ikkje kva forma vert; ho seier kva ein må sjå etter. | Læra er inga oppskrift på éi enkeltform. Ho føreseier ikkje kva strek handa trekkjer neste gong, men korleis vala samlar seg, kva som flyttar dei, og kvar det realiserte vil svikte. | Godt forsøk på å skilje fråvær av einskildprognose frå etterprøvbare relasjonar. |
| `1.2341` | Den relasjonelle strukturen i den fysiske skildringa kan vere ordning i oppleving. Opplevinga strekkjer til som indre natur utan at dei målte relasjonane må endrast. | Å dikte eit stoff utan innside bak relasjonane forklarer ingen storleik; det skaper berre gåta om korleis ei innside sidan skal springe ut av det innsidelause. Det som skal forklarast,  | Meir bastant ontologi. Status a vert t: ikkje akseptabelt utan ny filosofisk grunngjeving. |
| `5.721` | Formgrammatikken gjev det generative laget, tanke-kunnskapsskiljet det epistemiske laget, og agentanalysen laget for mål og gjennomføring. | Dei eldre delteoriane isolerer kvart sitt ledd ved å setje dei andre til null eller uendeleg. Kvar tradisjon åleine manglar ikkje detaljar; han manglar eit lag. | Tre verkande lag vert meir aktive. Kan miste den nødvendige koplinga til 1.131. |
| `5.722` | Historisk formgjeving bind dei tre laga saman. Ei avgrensa undersøking held eitt lag fast; eit fundament forklarer overgangane mellom dei. Kvar tradisjon åleine manglar ikkje detaljar.  | Den allvitande og allmektige agenten er eit slikt grenseomgrep. Verkelege agentar teiknar med ufullstendige reglar, ser med endeleg lyskjegle og handlar med avgrensa hald. | Premiss og status endra. Må ikkje kopierast direkte. |
| `5.724` | Formrommet [formel] er grunnen i modellen. | Femtuppelet [formel] held frå kvarandre grunnen [formel] , landskapet [formel] og dei tre verksame laga utan å gjere dei til isolerte ting. | Femtuppel-argumentet flyttar status frå t til d. Treng omskriving med matematisk kjelde intakt. |
| `6.76` | Målet til den andre har vekt i forma berre der han sjølv har innverknad, eller der det går ein veg av omsorg til han frå nokon som har. | Målet til den andre har vekt i forma viss og berre viss han sjølv har innverknad, eller det går ein veg av omsorg til han frå nokon som har. | Forkast slik det står: gjeninnfører motbevist ekvivalens. |

## Kvifor automatisk Fable-sløyfe ikkje fungerte

Fable fekk forbod mot å endre nummerhierarki, status, formlar og kjelder. Dei største alternative disposisjonane vart derfor skildra i rapportar, medan berre lokale inngrep kunne flettast. Dei formelle byggjetestane verifiserte ikkje litterær kvalitet. Modellen motlas ofte seg sjølv, og automatisk godkjenning ignorerte gjentekne tilrådingar om å stanse.

## Konkret komposisjonseksperiment: Plan D

Eg har òg gjennomført ei prøveflytting av dei elleve proposisjonane om designaren (6.02 til 6.027) til slutten av del 6, etter 6.76. Proposisjonane og kjeldemerka er bevarte i ei fullstendig arbeidskopi, men referansane må oppdaterast før nokon kan byggje henne som utgåve. Sjå PLAN_D_VURDERING.md, PLAN_D_REFERANSEKART.tsv og PLAN_D_ARBEIDSKOPI_491.tex.txt. Dette er eit reelt, men enno ikkje kvalitetsgodkjent ombyggingsforsøk.

## Neste fagleg forsvarlege arbeid

1. Bruk Carbon til å definere eit alternativt hovudargument for 1 til 7, særleg 4 og 6, men ikkje bruk han som fasit.
2. Mapp alle adresser, statusar, kjelde-ID-ar, note-ID-ar, figurar og matematiske uttrykk før kandidattekst vert sett inn i LaTeX.
3. Lag ei eiga 491-proposisjonsutgåve ved medviten redigering, ikkje automatisk erstatting av alt.
4. Prøv større strukturelle grep mot modellens eigne premissar og konkrete motdøme; innhent menneskeleg vurdering av desse før samanslåing.
5. Bygg og test PDF/nett og publiser først etter ei reell kvalitetsavgjerd.

**Fable AutoResearch er deaktivert. Ingen nye betalte modellkall vart gjorde her.**
