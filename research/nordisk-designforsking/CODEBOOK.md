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
