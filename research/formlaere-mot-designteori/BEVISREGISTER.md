# Bevisregister: FORMLÆRE mot samla designteori

*Status 7. november 2026. Eit forskingsregister, ikkje ein annonsetekst.*

## Påstanden me faktisk kan prøve

Ei samlande forklaring må kunne **bevare** dei presise operasjonane og gyldigheitsvilkåra i eldre teoriar, **utleie** følgjer som ikkje berre repeterer dei, og **føreseie eller mekanismeforklare** nye tilfelle med like god informasjon og minst like høg etterprøvbarheit som konkurrerande modellar.

Me kan ikkje prove at Formlæra er betre enn alle hittil produserte teoriar ved å vise ei større omgrepsliste. Ein universell prioritetspåstand krev kontroll av heile den historiske teoripopulasjonen, og ingen endeleg korpussamling gjev dette åleine. Arbeidsmålet er dokumenterte lokale, kumulative sigrar på klart definerte problem.

### Evidensnivå

- **F (formell):** reint matematisk bevist under oppgjevne vilkår, programtesta med syntetiske data.
- **E (empirisk):** målt i objekt eller handlingar, med dokumentert utval og rivalmodell.
- **O (originalkjelde):** ein faktisk teoriinnsikt er dokumentert i den originale kjelda.
- **I (innlemming):** mekanisme- og slutningsbevarande omsetjing av originale operasjonar er vist.
- **T (tilleggskraft):** nye følgjer er førehandsfastsette og har overgått rimelege konkurrerande modellar på ubrukte data.

Ingen av desse nivåa impliserer automatisk dei andre.

| Påstand / mekanisme | Kva er vist | Kva er ikkje vist | Status |
|---|---|---|---|
| Gibbs-fordelinga kan rekonstruere alle positive endelege utfallsfordelingar ved fritt landskap | Utleiing §6.661, syntetiske kontrollar | At rekonstruksjonen er årsaksforklaring | F |
| Samme observerte P kan kome av fleire grunnfordelingar og landskap | Invarians ved omparametrisering §6.662 | Kva faktisk kjelde til variasjon som verka i ein historisk sak | F |
| Sterkare seleksjon flyttar P i KL frå fast generator; Shannon-entropy kan likevel auke | Utleiing §6.663, numerisk motdøme | At historisk formmangfald alltid minkar med seleksjon | F |
| Ingen endeleg prøvd, tillaten form har null sannsyn ved positiv mu og endeleg energi | §6.664 | At ikkje-observerte former er umoglege | F |
| Same stasjonære formfordeling kan kome frå ulike stegkjerner med ulik framkomsttid | Utleiing av \(T_\alpha=(1-\alpha)I+\alpha T\) i §6.666 og syntetiske overgangskontrollar | Kva for ein faktisk produksjonsprosess som verka | F |
| Ved uendra kandidatrom, grunnvekt og vurderingar endrar relative log-odds seg lineært med seleksjonsstyrken | §6.667, tre syntetiske kontrollar | Kontrollerte, reelle intervensjonar der \(\beta\) er operasjonelt målt | F |
| Ukjent arkivutval kan skjule eller etterlikne formseleksjon | §6.668, konstruktiv observasjonslikskap og seks syntetiske kontrollar | Faktiske museumsregistreringssannsyn og rekonstruert realiseringsfordeling | F |
| Agentvekter kan identifiserast frå val berre ved tilstrekkeleg rang i uavhengige vurderingsskilnader | §6.665 og fire syntetiske rangprøver | Kausalt legitim makt eller faktisk agentinnverknad i eit prosjekt | F |
| Ein på førehand registrert vektflytting gir ein eksakt endring i log-odds mellom to alternativ | §6.676 og syntetisk kontroll | At effekten er empirisk observert og betre predikert enn rivalar | F |
| Feilestimat kan gjere den faktiske skaden større når prioriteringa vert sterkare | §6.674 og synthetic negative-Kovarians-kontroll | Om, kvar og kor ofte dette skjer i designpraksis | F |
| Materialinformasjon held fram som svak til moderat predictor etter år, teknikk og geografi | 1 598 held-ut objekt; ekstra normalisert MSE-reduksjon 0,0297 i heile utvalet, 0,0451 før 1900 og 0,0044 frå 1900; fleksibel rival reduserer tilleggskrafta | Genereringsrestriksjonar, kausal rolle, historisk invarians og generell effekt | E, avgrensa |
| Materiale gir ekstra prediktiv informasjon om grov stolgeometri etter årstal | 1 598 objekt; held-ut 12/12, betring 0,0392 normalisert MSE; 199 placebo | Kausalitet, uavhengig genereringsrom, representativ historisk produksjon | E, avgrensa |
| Stil har ikkje geometrisk informasjon | Motdøme: på 326 stilmerkte objekt gjev stil ekstra prognoseverdi | At stil som mekanisme er ei sjølvstendig årsak i desse dataa | Avvist som generell nullpåstand |
| Dei same geometriske relasjonane er invariant gjennom periodane | Enkel polynommodell feilar klart mellom før og etter 1900 | Om feilen skuldast nye reglar, materialar, utval eller ekstrapolasjon | E, motprøve |
| Formlæra bevarer den fulle konsept/kunnskaps-ekspansjonen i C–K | Originalane 2003/2009 kontrollerte; nødvendig typa omsetjing forklart | Full operatorkonservasjon og fire korrekte overføringar | O, ikkje I |
| Deltakande design kan modellerast som agentvekter | Originalane Bødker–Kyng og Saad-Sulonen mfl. viser makt og tidsforløp som må bevarast | Kven som avgjer vektene og legitimiteten til makta | O, delvis |
| RtD kan modellerast som oppdatering av \(\Pi,SG,\Lambda\) | Raptis mfl. sitt empiriske prototypearbeid gjennomgått; spesifisert overgangsforslag | Kausal og generell overgangsmodell | O, delvis |
| Materielt umogleg og normativt uakseptabelt er ulike slags utsegner | Skiljet mellom V og separat avgjerdsakse klargjort | Full normativ teori som avgjer kva som er rett | Logisk skilje |
| Designteori har ingen kumulativ kunnskapsproduksjon | Tidlege studiar viser faktisk empirisk metodeutvikling, negative resultat og teori om overføring | Ein full, manuelt koda meta-analyse av kor utbreidd kumulativitet er | Absoluttpåstanden vert ikkje støtta |
| Formlæra er empirisk betre enn alle rivalar | Syntetisk valbenchmark syner både vinning og tap; sterk fleksibel rival er med | **Ei einaste validering av den fulle §6.6-modellen på ubrukte reelle val med målt mu, estimat og vekter** | T manglar |

## Grunnlag i kilder og kode

**Formell kjerne:** §§1.542, 6.6–6.665, 6.673–6.676. Proposisjonar som er avhengige av eksponentialfamilien, er gyldige berre når D, mu, Φ og dei relevante variablane held dei oppgjevne vilkåra.

**Syntetiske matematiske programtestar:** [test_6_6.py](test_6_6.py), [test_identifiserbarheit.py](test_identifiserbarheit.py), [test_identifisering.py](test_identifisering.py), [test_informasjon.py](test_informasjon.py), [test_choice_benchmark.py](test_choice_benchmark.py), [test_dynamisk_identitet.py](test_dynamisk_identitet.py) og [test_arkivutval.py](test_arkivutval.py), 5 + 7 + 4 + 5 + 14 + 6 + 6 = **47** syntetiske kontrollar. Dei seks nye arkivkontrollane er køyrde; samlinga vert ikkje her framstilt som 47 sjølvstendige empiriske forsøk. Dette er ikkje 35 eksperiment med designarar.

**Empiriske kjelder:** [STOLAR-resultatet](STOLAR_EMPIRI_20261107.md), [strengare tids-/teknikk-/geografikontrollar](STOLAR_ROBUSTHET_20261107.md), [reproduksjon av grunnanalysen](stolar_heldut.py), [placebo og tidsmotprøve](stolar_kontroll.py). Fleire utforskande held-ut-evalueringar er ikkje det same som eit uavhengig prospektivt replikasjonsforsøk.

**Kjeldenær teoriinnlemming:** [22 teoriar med eksplisitte bevisplikter](TEORIMATRISE_22.md), [operasjonalisering av §6.66-figuren](FIGUR_666_TESTPLAN.md), [kritisk revisjon av P1–P10-proxyar](P1_P10_VALIDITET.md) og [C–K-originalsamanlikning](CK_DIREKTE_PROEVE.md) og [første originaltekstpilot](MOTPROVER_01.md). Bødker–Kyng (2018), Saad-Sulonen mfl. (2018), Raptis mfl. (2017), Baskerville–Pries-Heje (2014) og Fiore (2020) er lesne på originalnivå i ein innleiande pilot. Dette er ikkje ei uttømmande systematisk oversikt.

**Meta-forsking på litteratur:** Eldre [datastatus](../nordisk-designforsking/results/RAPPORT.md), [sannsynsutval på 600](../nordisk-designforsking/results/UTVALSPLAN.md), [siteringsmotprøver](../nordisk-designforsking/results/MOTPROVER.md) og [konkrete motdøme med empirisk forsking](../nordisk-designforsking/results/KJELDEKRITISK_PILOT.md). Desse er eldre, tidsstempla uttrekk; dei kan ikkje kombinerast ukritisk med den nyare main-versjonen av designteori-korpuset. Dei manuelle fulltekstkodane i 600-utvalet var ikkje ferdige ved siste kontroll.

## Den avgjerande konkurransen

Eit sterkare, felles forskingsprogram skal kunne gje svar på same sak frå fire sider:

1. **Kva kunne bli generert?** Oppgje SG, starttilstand, steg og materielle veto. Å sjå ein ferdig stol gjev ikkje denne informasjonen.
2. **Kva vart kunnskap og konsept undervegs?** Bevar C–K-operatorane og kunnskapsstatus til utsegnene, ikkje berre kategoriar av formpunkt.
3. **Kven fekk faktisk innverknad og kva vart valt?** Mål agentar, estimerte konsekvensar og dokumenterte vekter før valet, samanlikn §6.6 med sterke logit-/grammatikkrivalar.
4. **Kva skjedde etter gjennomføringa?** Følg skade, ny kunnskap, vedlikehald, feil og kven som bar kostnadene. Ei statisk Gibbs-fordeling gjev ikkje den historiske materialkjernen eller normativt ansvar.

Før desse fire laga er prøvde **i same dokumenterte designforløp**, kan me ikkje skrive at Formlæra har innlemma og empirisk overgått heile designteorien. Me har derimot ein eksplisitt og etterprøvbar **veg til å undersøkje dette**, med reelle matematiske følgjer og ein første empirisk pilot.

**Fagleg mål:** Samle *bevart innsikt + ny følgje + motprøve* for kvar rival. Opphav skal framleis krediterast. At Formlæra kan kode eit eldre resultat betyr ikkje at ho eig eller har oppdaga det.
