# Rapport 0.3: Valbenchmark mot fire rivalmodellar

*7. november 2026. Alle tala her kjem frå syntetiske, datagenererande mekanismar. Ikkje empirisk bevis for Formlæra.*

## Kva som faktisk vert samanlikna

Femtuppelet i §6.66 er ikkje automatisk ein valprediktor. Denne prøva gjeld **den avgrensa §6.6-fordelinga** etter at eit endelig D er registrert:

\[
P_F(x\mid c)=\frac{\mu_c(x)\exp[-\beta\sum_{i=1}^{2}w_{i,c}\hat e_{i,c}(x)]}{Z_c}.
\]

Motpartane får dei same tilboda og same førehandsmålte eigenskapane:
1. Uniform: alle alternativa i D får same sannsyn.
2. Grammatikk: sannsyn proporsjonale med registrert \(\mu_c\).
3. Vekting utan grunnfordeling: sannsyn proporsjonale med eksponentialvekta, med uniform \(\mu\).
4. Formlæra: den oppgjevne grunnfordelinga og førehandsvekta agentestimat, med éin estimert \(\beta\geq0\).
5. Fleksibel vilkårslogit: same \(\mu\) og dei same to agentestimata, men to fritt estimerte, signerte koeffisientar. Dette er ein viktig rival, ikkje ein stråmann.

Skiljet mellom form og vilkårslogit er særleg informativt: Formlæra får ei **restriksjon** frå vektene som skal vere fastsette før vala. Den fleksible rivalen kan lære at eit estimat har motsett forteikn. Difor er ikkje eit stort treningssamsvar for Formlæra noko bevis for verdi.

## Køyreform og evaluering

Program: [choice_benchmark.py](choice_benchmark.py). Det vert brukt tre mekanismar og 800 uavhengige syntetiske valsett i kvar, kvart sett med fire alternativ: 440 i trening, 120 i validering og 240 i test. Agentvektene er 0,7 og 0,3. Data er genererte med fast frø 20261107.

Form-parameteren blir estimert på trening; den fleksible rivalen får regularisering vald på validering. Testdata vert ikkje brukt til modelltilpassing. Evalueringsmålet er gjennomsnittleg negativ log-sannsyn (log loss) på faktisk val. Lågare er betre. Multiklasse-Brier-skår og topp-1-nøyaktigheit blir òg berekna. Skilnader i log loss har 95 % persentilintervall frå 2000 gruppevise bootstrap-resamplar. Desse intervalla er deskriptive, ikkje multiplicitetsjusterte.

### Resultat

| Modell | Mekanisme: Form | Mekanisme: uniform | Mekanisme: misvisande estimat |
|---|---:|---:|---:|
| Uniform | 1,386 | **1,386** | 1,386 |
| Grammatikk | 1,266 | 1,678 | 1,375 |
| Vekting åleine | 1,052 | 1,388 | 1,386 |
| Formlæra | 0,884 | 1,679 | 1,375 |
| Fleksibel vilkårslogit | **0,883** | 1,677 | **0,670** |

**Les resultata som konstruerte motdøme, ikkje som funn om designfaget.** Når data vert genererte etter Formlæra, vinn både Formlæra og den fleksible rivalen stort over dei enklare modellane. Den fleksible rivalen har om lag same log loss som Formlæra, og skilnaden har 95 % bootstrapintervall som kryssar null.

Når alternativa vert valde uniformt, vinn den uniforme modellen. Når faktiske val følgjer eit mønster som går mot eitt av agentestimata, vinn den fleksible rivalen klart. Den negative følgja er viktig: Ein modell som ikkje kan tape i relevante situasjonar, er ikkje ein empirisk konkurransedyktig modell.

I Form-mekanismen er log-loss-skilnaden grammatikk minus Formlæra 0,382 (95 % bootstrapintervall 0,284 til 0,477). Skilnaden mellom den fleksible modellen og Formlæra er omtrent -0,0004 (95 % bootstrapintervall omtrent -0,0034 til 0,0023). Dette viser ikkje at Formlæra slår ein sterk modell med like mykje informasjon.

## Eksakt følgje av innverknad, §6.676

Den nye identiteten er prøvd numerisk, inkludert nullresultatet når agentane sine vurderingsskilnader er like for to alternativ. Den sterkaste empiriske bruken er ikkje å samanlikne to tilfeldig ulike prosjekt, men å halde alternativa og estimata faste og manipulere relativ avgjerdsinnverknad legitimt.

Ein mogleg design er eit preregistrert valforsøk i eit studio der fleire designvurderarar registrerer estimerte følgjer på førehand. Prosjekta får randomisert avgjerdsordning, medan kandidatenes eigenskapar held seg like. Då vert endringa i log-odds mellom to alternativ ei konkret test av relativ innverknad. Deltakarane må samtykkje, og eventuelle legitime veto og rettar må ikkje overstyrast for eksperimentets skuld.

## Kva data som krevst for verkeleg prøving

Éi rad per alternativ i eit valsett. For to agentar krev programmet:

case_id, group_id, split, option_id, chosen, feasible, mu, e1, e2, w1, w2.

- Alle alternativ må dokumenterast **før** valet. Selected/chosen=1 berre for eitt faktisk valt alternativ.
- Feasible viser materiell og operativ tilgjenge, ikkje moralsk godkjenning.
- Mu skal vere ei uavhengig, positiv grunnvekt knytt til den registrerte genereringsprosessen.
- e1/e2 er på førehand tidsfesta, toleranseskalerte agentestimat, ikkje etterpåmålt skade.
- w1/w2 er på førehand dokumentert faktisk relativ innverknad, ikkje moralsk rettferd.
- group_id samlar val frå same aktør, prosjekt eller organisasjon for lekkasjefri validering.
- split skal vere bestemt på førehand. Ingen group_id kan finnast i meir enn eitt datasplitt.
- Ettervalsmåling av faktisk skade krev ein annan tabell og kan ikkje vere førehandsestimatet.

Dette er eit **strengare datakrav** enn dei fleste studiar som berre dokumenterer ferdig form eller sluttintervju. Dersom me manglar eit reelt alternativsett og førehandsestimat, kan me ikkje konstruere desse frå sjølve utfallet og kalle det valprediksjon.

## Uavhengig empirisk spor: STOLAR

Brukaren sitt historiske STOLAR-materiale er nyttig for å prøve **morfologiske hypotesar**, ikkje i seg sjølv agens- og valmodellen. Dei eksisterande forskingsnotata rapporterer svake samband mellom stil-etikettar og geometriske klynger, og variasjon i formrommet over tid. Desse resultata må kontrollerast mot rådata og dataproveniens før dei vert førte som nytt resultat.

Eit Drive-arkiv for STOLAR inneheld ei CSV-fil og eit eldre api.json som er generert 19. mars 2026. I den arkiverte JSON-fila er det 2300 registreringar, men ikkje alle er unike eller faktiske stolar; berre 524 registreringar har stilfelt. Ei annan deskriptiv forskingsutgåve omtalar 2048 stolar. Dataversjonar, datering og inklusjon må samordnast før ei ny statistisk prøve. Eit morfologisk samband kan ikkje utan vidare forklare kva designarar trudde, eller kva alternativ dei såg.

## Neste verkelege komparatorprøve

1. Frys éin publiserbar korpusversjon og rett stadfesta kjeldekoplingsfeil.
2. Vel ei verkeleg designoppgåve med registrerte alternativ og fleire aktørar, helst også faktiske følgjer seinare.
3. Frys vilkår og dataskilje. Køyr testbenken med sterke rivalar og grunnmodellar.
4. Rapporter alle resultat, inklusive tap for Formlæra og brot på føresetnadene.
5. Prøv den same mekanismen i eit nytt domene utan å hente parameterar eller val frå testutfalla.

Status: Ein konkret, brukbar testbenk er levert. At teorien er betre enn eldre designteori er **enno ikkje stadfesta**.
