# Siteringsfunksjon: fyrste kontroll av nedlasta fulltekstar

**Dato:** 2. november 2026. **Status:** Førebels, éin lesar, ikkje blind. Ingen av desse klassifikasjonane er del av 600-utvalet med to kodarar. **Ingen replikeringsstudie er påvist i dette pilotutvalet**, men det kan ikkje generaliserast til feltet.

## Omfang og metode

Av 100 målretta siteringspar frå den automatisk rangerte kandidatlista fekk me lesbar PDF for 14 par (13 unike siterande dokument). OpenAlex-oppføringa av ei OA-lenkje var ikkje tilstrekkeleg: 64 av forsøka gav HTTP 403, 18 returnerte ikkje PDF, eitt var over 14 MB, eitt vart stoppa av URL-kontrollen og to gav andre problem.

Ein strengare andrepass fann fire par med *både* kandidat til referanseidentitet og forfattar-år i hovudteksten, ni par med berre kandidat i litteraturdelen og eitt utan relevant identifisert treff. Regelen stoppar ved ny linje, semikolon eller ein annan fire-sifra årgang og kan difor òg gje falske negative treff. Den manuelle kontrollen fann mellom anna ein korrekt forfattar-år-sitering som den nye regelen ikkje fanga. Dette er **søkje- og lokaliseringssignal**, ikkje verifiserte teori- eller metodefunksjonar.

Eit eige lesegjennomgangsutval på sju av desse para er vurdert ved å lese aktuelle tekststader i siterande PDF og kontrollere den identifiserte bibliografien. For kvar post vart det notert kva siteringa ser ut til å gjere, men fullteksten til den eldre publikasjonen vart ikkje alltid kontrollert. Kodane er frå CODEBOOK.md og må rekast som **førebelse éinkodar-vurderingar**, ikkje ein reliabel, validert studie.

## Dei sju pilotpara

| Seinare publikasjon → eldre publikasjon | PDF-side (seinare tekst) | Førebels funn | Kode |
|---|---:|---|---|
| Kristiansen og Gausdal (2018) → de Goey mfl. (2017), design-driven innovation | 2; referanse s. 18 | Den tidlegare studien vert omtala som ei utviding av DDI til andre kontekstar, som del av litteraturbakgrunnen. Eit bestemt funn vert ikkje sjølvstendig prøvd i det siterte avsnittet. | L0 |
| Postdigital co-design (2025) → Vartiainen mfl. (online 2024, journal 2025) | 2; ref. s. 39 | Studiet vert trekt inn som bakgrunn for teoretiske spørsmål om GenAI og agens. Den nyare teksten viser år **2025**, medan OpenAlex lagrar **2024**. Det kan vere ulik bibliografisk årspolitikk, ikkje feil DOI. | L0 |
| Cash og Kreye (2017) → *Designing for perceptual crossing* (2012) | ref. s. 36 | Referansen kan identifiserast, men in-text forfattar-år-kopling vart ikkje stadfesta. Fyrste automatiske regel fekk falskt treff ved å tolke den indekserte strengen «Deckers, EJL Eva» som etternamnet «Eva». | LNA |
| Fernaeus og Lundström (tidsskriftvolum 2015, indeksert 2023) → Fällman (2008) | 3; ref. s. 11 | Den eldre artikkelen vert sitert som konseptuell avgrensing av utforskande design. Sitatet er ikkje presentert som ein kontrollert prøving av ein empirisk hypotese. | L1 |
| Design-thinking entrepreneurship education (2019) → *DesUni* (2015) | 2–3; ref. s. 11 | Eldre tilnærming vert brukt til å motivere eit undervisningsopplegg. Dette viser fagleg bruk, men utgjer ikkje automatisk replikasjon av ei tidlegare evaluering. | L1 |
| Design fiction as critical pedagogy (2026) → Light (2021) | 3 og 11; ref. s. 14 | Eit tidlegare kritisk omgrep om snevre framtidsførestillingar vert brukt i tolkinga av eigne verkstadobservasjonar. Det er mogleg konseptuell vidareføring, men ikkje ein forhåndsspesifisert test av kjelda si påstand. | L1 |
| Same design-fiction-artikkel (2026) → *Speculative approaches ... uncertainty* (2022) | ref. s. 14 | Referansen er funnen i bibliografien, men det konkrete avsnittet vart ikkje sikkert identifisert i automatisk søk. Ingen epistemisk funksjon er fastslått. | LNA |

## Kjelder og lenkjer

- Kristiansen og Gausdal (2018), <https://doi.org/10.7577/formakademisk.1856>; de Goey mfl. (2017), <https://doi.org/10.1080/14606925.2017.1352998>.
- Cash og Kreye (2017), <https://doi.org/10.1017/dsj.2017.28>. Ope, 41-siders PDF-dokument i institusjonsarkiv.
- Fernaeus og Lundström, «Practicing Design Judgement through Intention-Focused Course Curricula», **Design and Technology Education 20(1), 47–58 (2015)**: <https://files.eric.ed.gov/fulltext/EJ1119540.pdf>; Fällman (2008), <https://doi.org/10.1162/desi.2008.24.3.4>.
- University entrepreneurship education (2019), <https://doi.org/10.1186/s13731-018-0098-z>; DesUni (2015), <https://doi.org/10.1108/et-09-2014-0121>.
- GenAI co-design (2025), <https://doi.org/10.1007/s42438-025-00595-4>; Vartiainen mfl., <https://doi.org/10.1016/j.tsc.2024.101742>. Tidsskriftvolum 56 i juni 2025, men online-first frå 2024.
- Design fiction as critical pedagogy (2026), <https://doi.org/10.3389/feduc.2026.1692366>; Light (2021), <https://doi.org/10.1016/j.futures.2021.102855>; Speculative approaches (2022), <https://doi.org/10.1177/14687941221129808>.

## Kvifor dette endrar datavitskapen

To feilklassar vart faktisk avdekte: **(i)** eit falskt positivt forfattar–år-treff frå feilparsing av personnamn, og **(ii)** ulike legitime årsfelt/feilaktig indeksering av eldre publikasjon. I nettverket kan begge forvrenge teljingar som skal handle om teoretisk vidareføring over tid.

Det er også nødvendig å skilje **påstandar** frå **siteringskanter**: ei sitering kan vere korrekt, men berre gje historisk bakgrunn. Eit arbeid kan nytte ein metode frå ein eldre tekst og samstundes produsere ny empiri, utan dermed å ha prøvd den eldre teksten si primære hypotese. Resultat om «manglande kumulativitet» må difor baserast på eksplisitt, dokumentert og uavhengig koding av *relasjonen* mellom arbeida.

**Viktig:** Klassifikasjonane ovanfor er gjort på eit lite målretta pilotutval. Dei er ikkje ein prevalensstudie. Fullt representative frekvensar skal ikkje bereknast før det 600-postars utvalet er dobbeltkoda.

## Tekniske dokument

- [Returstatistikk og figur](OA_TILGANG.md)
- [Kandidatar frå automatisk referansesøk](oa_reference_crosscheck.csv)
- [Manuelt merkt pilotutval](oa_manual_pilot.csv)
- [Årsfelt-sensitivitetsanalyse](AARSKJELDEKRITIKK.md)
