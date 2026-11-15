# Forsøk 01: Kan den samla Formlæra føreseie eit nytt designval?

*Protokollutkast 7. november 2026. Ikkje gjennomført, ikkje førehandsregistrert i eit offentleg register. Målet er ein reell test, ikkje ein illustrasjon der modellen genererer sitt eige fasitsvar.*

## Kasus

Eitt avgrensa fysisk designprosjekt: eit sittemøbel av flate 12 mm bjørkefinerplater, innanfor 500 × 500 × 500 mm, utan lim, skruar og dyvlar. Utvalet av lovlege CNC-operasjonar, materiale, toleransar, samanbindingsreglar, monteringsrekkjefølgje og sikkerheitskrav skal låsast før datainnsamling. Unngå tab-og-spor-boksar, T/X-former og tett ribbegitter som skjuler lastvegen; desse er estetiske/formale prosjektrestriksjonar, ikkje universelle fysiske lover.

**Særskilt regel:** Ingen deltakar eller brukar skal sitje på ein eksperimentell stol før han har gjennomgått forsvarleg, dokumentert mekanisk belastningskontroll. Oppgåva skal ikkje krevje brot på tryggleik eller deltakarrettar.

## 1. Førehandsregistrer generering

- Arkiver datert grunnform, grammatikk SG=(S,R,s0), operasjonar og materielle veto V.
- Definer førehandsbestemt genereringssannsyn: anten eksakte sannsyn for kvar regelkjede eller ei uavhengig Monte Carlo-estimering av μ_SG.
- Lås tilfeldige frø og alle kandidat-ID-ar. Lag minst fire konkurrerande former i kvart valsett utan å sjå prøveresultata.
- Dokumenter både lovlege kandidatar og eit eige register over avviste former med faktisk grunngjeving; ikkje bland materielt umogleg med normativt avvist.
- Hald eigne data om konsept og utsegner, slik at C–K kan kodast i sitt eige språk, ikkje som eit framprovosert punkt i ein endeleg formtabell.

## 2. Mål agentane før valet

To eller fleire deltakarar registrerer kvar si vurdering av alle kandida­tar. Mål avvik langs førehandsspesifiserte aksar, til dømes:
- sitjetryggleik og observerbar lasteveg;
- produksjonsavvik, CNC-tid og materialsvinn;
- ergonomisk sitjefunksjon og transport;
- formleg samanheng og forståeleg monteringsrekkjefølgje.

Kvar aksedefinisjon må ha eit eige, faktisk måle- eller vurderingsopplegg. Dei toleranseskalerte estimata e_ik og den relative omhugsprofilen omega_ik vert lagra **før** deltakarane kjenner den endelege avgjerda. Registrer kva som var ukjent for dei.

Den faktiske innverknaden w_i kan ikkje erklærast ut frå eit spørjeskjema etterpå. Bruk ei dokumentert, legitim avgjerdsordning; randomiser høveleg **innverknadsregel** mellom samanliknbare grupper der deltakarane på førehand har samtykt. Registrer både tildelt avgjerdsmakt og faktisk følgd framgangsmåte. Dersom tildelt og faktisk innverknad ikkje stemmer overeins, er dette eit resultat, ikkje eit tal som må korrigerast til teorien passar.

## 3. Frys modell og rivalar

Etter pilotutvalet, men før det endelege held-ut-utvalet vert opna, skal:
- seleksjonsstyrke beta og metodar for estimatfeil frysast;
- nullmodell, grammatikk-berre, estimat-berre, Formlæra §6.6 og fleksibel vilkårslogit spesifiserast;
- kandidatfamiliar og deltakargrupper få ein konfliktfri train/validation/test-fordeling;
- hypotesen om log-odds-skiftet i §6.676 registrerast;
- negative resultat og feil i sjanger/operasjonalitet vere tillatne utfall.

Eit val framkalla av ein algoritme som sjølv trekkjer frå Gibbs-fordelinga er **ikkje** empirisk stadfesting av Gibbs-modellen. Testutfallet må kome frå uavhengig menneskeleg praksis og faktisk avgjerd.

## 4. Utfall og motprøver

**Val:** Gjennomsnittleg held-ut log loss og multiklasse-Brier på kjende kandidatsett, med kalibrering og gruppevis usikkerheit. Formlæra får ikkje ekstra forklaringsvariablar som rivalen ikkje får.

**Påverknad:** Med dei same alternativa, estimata, grunnvektene og beta: kontroller om endra innverknad gjev den førehandsspesifiserte log-odds-endringa. Manglar kontroll av eitt av vilkåra, kan ikkje avviket tolkast som isolert vektflytting.

**Generering:** Kontroller sjølvstendig at kandidatar og utførte kutt faktisk kan nåast med dei registrerte reglane. Ei ny føresetnad eller oppdaga produksjonsteknikk som utvidar SG må førast som eit nytt steg, ikkje som ei stille omdefinering av D.

**Kunnskapsutviding:** La C–K sine fire operatorar kodast ut frå dokumenterte konsept, nye utsegner og prøvehandlingar. Bevar kva som vart udømt, kva som vart kjent, og om eigenskapsspråket vart utvida. Test konservativ omsetjing før me tel C–K som innlemma.

**Faktisk gjennomføring:** Registrer prototypeutfall, målt mekanisk styrke, ressursbruk og nye problem. Ei føreseiing om val er ikkje ei føreseiing om faktisk skade; negative utfall må registrerast utan etterpåtilpassa vekter.

## 5. Dataskjema og proveniens

Éi rad per kandidat og per valsett, som i [choice_benchmark.py](choice_benchmark.py): case_id, group_id, split, option_id, chosen, feasible, mu, e1, e2, w1, w2.

Separate, tidsstempla tabellar:
- generator_rules: SG-versjon, s0, regel, regel-sannsyn, kandidat-ID, tid og veto;
- epistemic_propositions: utsegn, agent, dato, status K/C/U, prøvevilkår, kjelde;
- opinions: agent, kandidat, aksedefinisjon, toleranse, estimat og vurderingsdato;
- actual_decisions: tildelt avgjerdsordning, faktisk framgangsmåte, kven som avgjorde, resultat;
- realizations: produksjonslogg, målingar, feil, omarbeiding, bruksprøve og etterfølgjande konsekvens;
- archive_selection: kva som vart lagra og kvifor, slik at §6.668 sitt registreringsledd kan prøvast, ikkje berre føresetjast.

## 6. Siger- og tapskriterium

Eit lokalt **positivt resultat** for §6.6 krev betre held-ut log loss enn grammatikkåleine, og ikkje dårlegare prediktiv kvalitet enn ein like-informert fleksibel rival utan at dette kjem frå meir etterpåtilpassing. Ein reell framgang i den allmenne modellen krev i tillegg dokumentert kopling frå kunnskapsendring til ny generering, val og seinare konsekvens.

Eit **negativt resultat** er at Formlæra er svakare enn den fleksible modellen, at vektene ikkje kan identifiserast, at det ikkje finst ei stabil grunnfordeling, eller at C–K-operasjonane ikkje kan bevarast utan å leggje inn nye primitive. Alle desse funna skal stå att i rapporten.

Den endelege utvalsstorleiken må fastsetjast etter ei simulert styrke-/presisjonsanalyse basert på pilotvarians, før hovudutvalet vert undersøkt. Ikkje finn på eit N som høyrest stort nok ut.

**Status:** Gjennomførbar protokoll, **ingen** gjennomførte deltakarval eller fysiske belastningsresultat. Ein foreslått syntese er ikkje det same som empirisk stadfesting.
