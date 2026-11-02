# Kodebok for å teste kumulativitet (versjon 0.1, ikkje validert)

Dette dokumentet skil bibliometrisk metadataarbeid frå ein eigentleg
vitskapsteoretisk test. Ingen av variablane nedanfor vert automatisk utfylte
på grunnlag av berre tittel, samandrag eller siteringsnettverk.

## Studiedesign

**Eining:** éin fulltekstpublikasjon. Population: definerte designrelevante
forskingstekstar tilknytte nordiske institusjonar frå 2000 til 2026. Populasjonen
er førebels ufullstendig; nasjonale register må kontrollerast mot OpenAlex.

Kvar post må få dokumentert kjelde, permanent ID, år, sjanger og fulltekststatus.
Minst to blindkoda forskarar skal fylle skjemaet uavhengig av kvarandre.
Uvisse kodast NA og kan aldri feilaktig telje som fråvær av kvalitet.

## Kodingsvariablar

| Kode | Operasjonalisering | Verdiar |
|---|---|---|
| D1 | Hovudproduktet er konseptuell utforsking, metode, modell eller empirisk påstand | konsept/metode/teori/empiri/blanda/NA |
| H1 | Forfattaren set fram ein identifiserbar, spesifikk påstand som kan vurderast som sann eller falsk | 0/1/NA |
| H2 | Forfattaren gjev ein operasjonell definisjon av minst eitt utfall eller omgrep | 0/1/NA |
| H3 | Ei testbar føreseiing er utleidd frå teorien uavhengig av same observasjonane som vart nytta til teoriutvikling | 0/1/NA |
| E1 | Minst eitt dokumentert datagrunnlag med innsamlingskriterium | 0/1/NA |
| E2 | Metode og utval er tilstrekkeleg skildra til at ein annan kan forsøkje replikasjon | 0/1/NA |
| E3 | Negative resultat, avgrensingar eller moglege motfunn er eksplisitt rapporterte | 0/1/NA |
| C1 | Fagleg relevant tidlegare påstand er identifisert og presist referert | 0/1/NA |
| C2 | Ein tidlegare påstand er empirisk prøvd eller formelt vurdert, ikkje berre nemnd | 0/1/NA |
| C3 | Studien rapporterer replikeringsforsøk eller uavhengig etterprøving av eit eldre funn | 0/1/NA |
| C4 | Tidlegare teori vert uttrykkeleg revidert, avgrensa eller tilbakevist etter prøving | 0/1/NA |
| C5 | Studien tek med seg ein etterprøvd prediksjon, metode eller relasjon til nytt materiale/domene | 0/1/NA |

Definer eit primært utfall før koding: til dømes delen av empiriske publikasjonar
med C2=1, og sekundært C3=1, C4=1 og C5=1. Ein studie kan vere god, viktig
og nyskapande sjølv om alle desse variablane er null: det er feil å omdefinere
kumulativitet til eit totalmål for «god forsking».

## Revisjonskrav

1. Publiser kriterium for inklusjon, eksklusjon, populasjon og nullhypotese.
2. Lag trekt, stratifisert tilfeldig utval etter år, sjanger og temagruppe.
3. La to kodarar arbeide uavhengig med dokumenterte sidetilvisingar.
4. Rapporter Cohen's kappa eller Krippendorff's alpha på kvar sentral variabel.
5. Løys usemje ved dokumentert tredjehands vurdering, utan å overskrive originalsvar.
6. Presenter usikkerheit, sensitivitet for manglande fulltekst, og kontroll for
   ulik tid til sitering/replikasjon.
7. Samanlikn med eit relevant referansefag med same prosedyrar.
8. Offentlegg datakode og anonymiserte kodingsdata slik at funnet kan korrigerast.

## Tolking

**Manglande sitat er ikkje manglande kumulativitet.**
**Mange sitat er ikkje prov på kumulativitet.**
**Likskap i embeddings er ikkje oppfølging av ein hypotese.**
**Konseptstudium er ikkje ugyldig vitskap fordi dei manglar prediksjon.**

Hypotesen om liten systematisk teoriprøving må kunne forkastast dersom
mange publikasjonar viser eksplisitt vidareutvikling, replikasjon, revisjon
og overførbare resultat. Nett dette gjer påstanden forskbar.

## Status

Kodebok og skjema er eit nytt, eksplisitt utkast. Kodingskvaliteten er
**ikkje** validert og menneskeleg klassifisering er **ikkje** gjennomført.

## Tillegg 0.2 — skil dokumentasjon, replikasjon og teoretisk framgang

Dette tillegget vart formulert **etter** den første bibliometriske analysen.
Det er ein *prospektiv metoderevisjon*, ikkje ei påstand om førehandregistrert
analyse. Den opphavlege kodingsramma H/E/C og det trekte 600-utvalet vert
bevarte uendra; tilleggskodane kan prøvast i ein separat valideringspilot.

### A. Kvifor studien vart skriven

Før C2–C5 vert vurderte, registrer publikasjonen sin **faktiske sjanger**:
`teoretisk argument`, `konseptstudium`, `metodeframlegg`,
`empirisk observasjon`, `eksperiment`, `replikasjonsforsøk`,
`systematisk oversyn` eller `anna/blanda`. Eit konseptstudium skal
ikkje få trekk berre fordi det ikkje utfører ein prediktiv eksperimenttest.
Falsifiserbarheit er ikkje det einaste legitime vitskapskriteriet.

### B. Fem punkt ved metodepåstandar

For **metodeframlegg**, kode kvart evidensledd uavhengig som
`påvist` / `mangelfullt` / `ikkje relevant` / `ikkje vurdert`:

| Kode | Etterprøvbar dokumentasjon |
|---|---|
| M1 | *Motivasjon:* avgrensa problem, målgruppe og eksisterande mangel dokumentert |
| M2 | *Natur:* presis framstilling av metodeføremålet og kva slags resultat han skal gje |
| M3 | *Utvikling:* dokumenterte grunnar for stega og avgrensingane som vert valde |
| M4 | *Innhald:* framgangsmåten kan rekonstruerast, og kopling til eldre arbeid er presisert |
| M5 | *Påstandar:* påstand om nytte/verknad knytt til mål, data eller eksplisitt argumentasjon |

Operasjonaliseringa er inspirert av Cash, Daalhuizen og Hekkert (2023),
[DOI 10.1016/j.destud.2023.101204](https://doi.org/10.1016/j.destud.2023.101204).
Deira systematiske gjennomgang av 18 metodeartiklar frå seks tidsskrift i 2020
er *ikkje* ei måling av heile disiplinen. Forsøk først ein to-kodar-pilot
for å teste om M1–M5 kan nyttast på nytt materiale utan store tolkningsavvik.

### C. Replikasjon må kodast for retningsbestemde siteringspar

For kvar seinare tekst A som refererer til eldre tekst B:

| Kode | Observerbar relasjon |
|---|---|
| L0 | Bakgrunn, sjangeromtale, teori som historisk referanse |
| L1 | Omgrepsbruk utan prøving |
| L2 | Metodebruk utan testing av ein spesifikk eldre påstand |
| L3 | Vidareutvikling av teori eller metode; presiser *kva* som er nytt |
| L4 | Eksplisitt prøve av ein identifisert eldre påstand, med utfall |
| L5 | Uavhengig replikasjonsforsøk: samanliknbare mål, ny datainnsamling |
| L6 | Eksplisitt avgrensing, tilbakevising eller fagleg motfunn |
| L7 | Reproduksjon av analysen frå same data/kode; ikkje nytt forsøk |
| LNA | Uavklart utan fulltekst eller utilstrekkeleg informasjon |

Dette er **ulike observasjonar**, ikkje ein rangstige frå dårleg til godt.
Ein tekst kan ha fleire relevante funksjonar, men evidens for kvart utfall
må peike på konkrete sider og operasjonaliserte variablar i *begge* tekstane.
Ikkje kod L5 dersom det einaste belegget er ordet «replication» i samandraget.

Brendel mfl. (2021),
[DOI 10.1177/02683962211006429](https://doi.org/10.1177/02683962211006429),
gjev ei meir detaljert replikasjonstypologi for design science innan
informasjonssystem. Kategoriane skal ikkje overførast direkte til arkitektur,
industridesign og kunstnarleg forsking utan ein test av deira faglege gyldigheit.

### D. Effekt og uvisse i publiserte replikeringsforsøk

Registrer påstand, effektstorleik, konfidensintervall, utval, måleinstrument,
primæranalyse og utvida/endra kontekst. Skil signifikansen til kvar einskild
studie frå ein formell test av **forskjellen** mellom studiane. «Signifikant i
originalen, ikkje-signifikant i replikasjonen» er ikkje ei påvist motseiing.
Sjå Rode mfl. (2024),
[DOI 10.1017/pds.2024.14](https://doi.org/10.1017/pds.2024.14),
og den avgrensa [Fisher-z-kontrollen](replication_effect_checks.py).

### E. Falsifikasjon av hypotesen om svak kumulativitet

Eit funn av L4–L7 med dokumentert utfall er eit mogleg **motdøme** til
fråværsformuleringar. Hyppigheita av slike funn må estimerast frå eit relevant,
representativt og *faktisk koda* utval, ikkje frå eigendefinerte siteringsklustrar.
Siteringsmengd, søkjerangering, tekst-cosine, OR-diagram og etterfølgjande
permutasjonstestar er **ikkje** direkte mål på kumulativ vitskap.

I denne utgåva er alle tilleggskodar uvaliderte og ingen av dei 600
publikasjonane er dobbeltkoda. Negative eller uleselege fulltekstar skal
registrerast som `LNA`, ikkje som fråvær av kunnskap.
