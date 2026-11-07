# STOLAR: første reelle morfologiske prøve av føresetnader i FORMLÆRE

*Utforskande rapport, 7. november 2026. Ikkje førehandsregistrert. Ikkje ein direkte test av fordelingsmodellen i §6.6. Full kode: [stolar_heldut.py](stolar_heldut.py).*

## 1. Spørsmålet

Kan opplysningar om materiale og historisk periode gje informasjon om eit formuttrykk i eit **nytt** museumsobjekt, utover å oppgje gjennomsnittsforma? Og har stilkategoriar sjølvstendig informasjon når periode og materiale er kjende?

Dette testar observerbare følgjer av at former har materielle og historiske vilkår. Det testar **ikkje** den fullstendige Formlæra, fordi historiske katalogpostar ikkje inneheld uavhengig grunnfordeling \(\mu_{SG}\), oppgjevne alternative kandidatsett, agentestimat, vekter eller faktisk valpolitikk.

## 2. Data og proveniens

Kjelde: STOLAR-arkivet, api.json, generert 19. mars 2026 kl. 17:22:14 UTC, tilgjengeleg i forskarens arkiv og knytt til [stolar-db](https://github.com/lukketsvane/stolar-db).

SHA-256 for den **eksakt analyserte lokale fila**:
29e478099eaf1b707fbd327a72396db7ba290677ba85993736ab2bbec12a73e6

- 2 300 kjelderegistreringar, 2 048 ulike objekt-ID-ar, 252 ekstra rader frå ID-gjentaking.
- 181 objekt-ID-ar har fleire registreringar; minst 17 av desse gruppene har avvikande year_from (frå manuell, programmatisk kontroll). ID-duplikat er ikkje automatisk fleire stolar.
- Éi rad per objekt-ID er vald etter mengd ikkje-tomme felt. Motstridande kjelder er **ikkje** adjudiserte.
- Registrert stil for 340 av 2 048 valde objekt, og etter utsiling for berre 326.
- Utvalet etter opne, faste målegrenser: **1 598 objekt** (1 541 frå V&A og 57 frå Nasjonalmuseet), 1 493 lekkasjekontrollgrupper.
- Krav: år 1500–2026, høgd 30–220 cm, breidd 20–200 cm, djupn 15–150 cm. Manglande, nullførte og grove måleavvik er ekskluderte. Tre ikkje-relevante søkjeord om arkitekturfotografi, dekorative gjenstandar og sportsutstyr er også ekskluderte når dei var registrerte.
- 3D-lenker er **ikkje** det same som kontrollerte originalskanningar. Utfallet her er katalogmål, ikkje 3D-morfometri.

Utvalsgrensene vart valde etter ei innleiande gransking av datakvalitet. Resultata er difor *eksplorative*, ikkje ei stadfesta, førehandsregistrert hypotese.

## 3. Modellar og utfall

Tre geometriske utfall per objekt:
- \(\log(H/W)\): høgd delt på breidd;
- \(\log(W/D)\): breidd delt på djupn;
- \(\log((HWD)^{1/3})\): logaritme av geometrisk middelstorleik.

Samanlikn nullmodell, årstal (tredjegradspolynom etter sentrering), materiale (frekvensavgrensa multi-hot-koding), årstal + materiale, og i **same** stilmerkte delutval: stil, årstal + stil og årstal + stil + materiale.

Alle modellar utanom null er multivariat ridge-regresjon med **same faste straff** (alpha 20). Inga parameteroptimering skjer på testdata. 12 gruppevise, repeterte 75/25 held-ut-splittar med frø 20261107. Ei gruppe er likt årstal, likt oppgjeve materiale og identiske mål, slik at kjende katalogkopiar med identisk målebilete ikkje hamnar i både trening og test. Resultatmålet er gjennomsnittleg kvadratfeil per geometriutfall, normalisert med variasjonen i treningsutvalet. Lågare er betre.

Dette er prognose av observerte mål, ikkje prediksjon av kva ein designar valde frå eit reelt sett med alternativ.

## 4. Resultat på ikkje-brukte objekt

### Fullt måleutval, N=1 598

| Modell | Middel normalisert testfeil over 12 splittar |
|---|---:|
| null | 0,9743 |
| årstal | 0,9588 |
| materiale | 0,9249 |
| årstal + materiale | **0,9196** |

Å leggje materiale til årstal reduserte feilen med 0,0392 i gjennomsnitt; betringa var i same retning i **12 av 12** splittar. Materiale åleine gav òg betre prognose enn null i 12 av 12.

Kjelde- og utvalsfølsamheit: Berre V&A (N=1 541) gav tilsvarande forbetring 0,0465 ved å leggje materiale til årstal, også i 12 av 12 splittar. Dette er viktig fordi svært få objekt i dette eksplorative utvalet kjem frå Nasjonalmuseet.

### Same stilmerkte utval, N=326

| Modell | Middel normalisert testfeil |
|---|---:|
| null | 1,1226 |
| årstal | 0,9554 |
| materiale | 1,0427 |
| stil | 0,9628 |
| årstal + materiale | 0,9396 |
| årstal + stil | 0,9202 |
| årstal + stil + materiale | **0,9154** |

**Motfunn:** Stiltillegget til årstal betra feilen med 0,0353, større enn materialtillegget til årstal i dette selekterte delutvalet (0,0159). Materiale i tillegg til årstal + stil gav berre ei marginal forbetring på 0,0048, med betring i 7 av 12 splittar.

Det er såleis usant at stil ikkje inneheld informasjon om geometri i dette utvalet. Ei forklaring må kunne skilje stil som *klassifikasjon og spor* frå stil som ein *eigen historisk mekanisme* når attkjenning, imitasjon og institusjonell seleksjon faktisk verkar (§§6.3–6.312).

### Éin separat, fast gruppesplitt med negativ kontroll

- Trening 1 207 objekt; test 391 objekt (374 testgrupper).
- Berre årstal: feil 0,97980.
- Årstal + materiale: feil 0,93794.
- Betra feil 0,04186, gruppevis bootstrap 95 % deskriptivt intervall **0,01305 til 0,07178**.
- 199 negative kontrollforsøk stokkar materialetikettar *i treningsutvalet* innan 50-årsbolkar. Ingen gav like stor betring som faktisk materialkopling. Kontrollfordelinga hadde middel −0,00769, intervall omtrent −0,02619 til 0,01247; øvre hale med +1-korreksjon gav **0,005**.

Denne kontrollen styrkjer observasjonen av at materialtermane ber signal utover det enkle polynomet for år. Men analyseretning og datavask vart valde etter datainspeksjon. 0,005 er difor **ikkje** grunnlag for å hevde ei førehandsregistrert hypotese på 5-promillenivå, og det gjev inga kausal identifisering.

### Negativ overføringsprøve mellom periodar

Tren på før-1900 (1 048), test på 1900+ (550):
- Nullmodell 1,269; år + materiale **2,554**.

Tren på 1900+ (550), test på før-1900 (1 048):
- Nullmodell 0,944; år + materiale **1,236**.

Dette er ein **tydeleg motprøve mot naiv tidsinvarians** for akkurat den valde polynommodellen. Polynom-ekstrapolasjon, utvalsskifte, målepraksis, materiale og produksjonsteknikk kan alle bidra. Det er ikkje eit bevis på skifte i formgrammatikk, og heller ikkje ei motbevising av Formlæra §6.6.

## 4b. Ikkje-lineær sensitivitet med like dataskilje

For å kontrollere om materialsignalet berre skuldast den valde tredjegradspolynommodellen, har eg også prøvd **histogram-basert gradient boosting** (80 iterasjonar, 10 maks bladnoder, læringsrate 0,05, L2-regulering 2,0, fast frø 20261107). Tre uavhengige regressorar lærer høgd/breidd, breidd/djupn og log-storleik. Modellane får dei same 12 gruppevise 75/25-splittane som over og elles same datavask.

| Ikkje-lineær modell | Normalisert MSE |
|---|---:|
| Årstal | 0,94038 |
| Årstal + materialkategoriar | **0,88522** |

Materialtillegget forbetra estimatet i **12 av 12 overlappande held-ut-splittar**, med absolutt gjennomsnittleg skilnad 0,05516. Kode: [stolar_nonlinear_sensitivity.py](stolar_nonlinear_sensitivity.py).

Dette er ein sterkare *sensitivitetskontroll av assosiasjonen* enn berre ridge-modellen. Men verken gradient boosting eller ridge skil mellom om materialar **produserer** form, om begge vert valde av ein tredje faktor, eller om museumsutvalet har selektert materialar og mål samtidig. Splittane er ikkje 12 uavhengige replikasjonar. Ingen av modellane er ei operasjonalisering av agentane og den registrerte grammatikken i den fulle §6.6-forma.

## 5. Kva resultata støttar

**Støttar som observasjon:** materiale og produksjonsår ber informasjon om grov geometrisk form utover eit globalt gjennomsnitt, og det kan gje betre held-ut-prognosar i den analyserte museumsprøva. Stil ber òg informasjon i det selekterte, stilmerkte underutvalet.

**Ikkje dokumentert:** at materialet kausalt bestemmer forma; at Formlæra sitt \(\mu_{SG}\) er identifisert; at stilar ikkje har kausal verknad; at Formlæra sine agentvekter forklarer vala; at modellen slår eksisterande designteori i ein kontrollert studie; eller at museumssamlinga representerer historisk produksjon.

**Viktig for manuskriptet:** §6.664 seier at historisk fråvær ikkje kan brukast som direkte bevis på materiell umoglegheit. STOLAR viser kvifor: Det finst duplikat, målefeil, stil-missingness, skeiv samlingsdekning og AI-genererte 3D-derivat. Eit museumskorpus viser registreringar av realiserte objekt, ikkje heile det opphavleg genererbare rommet.

## 6. Status og vidare krav

Første empiriske *deltest* er gjennomført, men ikkje nok til å stadfeste heile teorien. For den sentrale fordelingslikninga trengst ei **anna type data**: dokumenterte kandidatsett, genereringsreglar, førehandsestimerte følgjer, dokumentert agentinnverknad og faktisk val. Det eksisterer ein separat, syntetisk testbenk for slike data i [choice_benchmark.py](choice_benchmark.py).

**Kort slutsats:** Eit breiare forklaringsprogram enn rein stilklassifikasjon får støtte som metodeval, men både stilens informasjonsverdi og modellens manglande tidsoverføring viser kor lett ei for enkel forteljing kunne bli falsk.
