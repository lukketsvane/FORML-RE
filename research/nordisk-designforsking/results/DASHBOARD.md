# Nordisk designforsking 2000–2026 — datavitskapleg oversikt

Dette er ein **eksplorativ metadatastudie**, ikkje ei ferdig metaanalyse av fulltekstforsking.
Alle tal gjeld den delvis utvida, rangsorterte OpenAlex-databasen.

## Utval og datakvalitet

| Målepunkt | Målt |
|:--|--:|
| Unike OpenAlex-kandidatar | 7 300 |
| Automatiske tittelinkluderingar | 3 729 |
| Med samandrag i lokal database | 2 922 |
| Søkjesider henta utan feil | 96 |
| Søkjesider avbrotne av rategrense | 1 |
| Interne siteringskantar | 3 159 |
| Referansetilvisingar til alle OpenAlex-arbeid | 126 356 |
| Par med minst tre felles referansar etter filtrering | 16 916 |
| Sterkare bibliografisk kopla par | 1 022 |

## 1. Kva søka faktisk fann

![Publikasjonar i utvalet per år](figures/01-sokjeutval-per-aar.png)

![Søkjetema per årsbolk](figures/02-sokjetema.png)

Tidsseriane er **ikkje** vekstestimater for forskingsfeltet; OpenAlex-søka er
avgrensa til dei mest rangerte treffa innan kvar frase og ikkje fullstendige årspopulasjonar.

![Siteringstal etter år](figures/03-sitering-per-aar.png)

![Nordiske institusjonstilknytingar](figures/04-land.png)

## 2. Nettverk og kumulativitet

![Referansar mellom søkjetema](figures/05-kryssitering.png)

Observasjonen at 49,8 % av dei 3 159 interne siteringane koplar same operative
temagruppe, mot ein stratifisert nullmedian på om lag 21,1 %, viser struktur i
det innhenta siteringsnettverket. I eit førehandsavgrensa delutval på 382
publikasjonar frå utvalde designtidsskrift er talet 43,4 % mot 18,8 %.

Dette **må ikkje** forvekslast med kumulativitet: ei sitering kan vere ein
kontrast, ein laus omtale, ein kritikk, eit metodisk lån eller ein replikeringsstudie.
31,0 % av dei observerte interne kantane er mellom arbeid som deler minst éin
forfattar. Robustheitssjekkane testar også sitering utan slike kantar.

![Bibliografisk kopling](figures/11-bibliografisk-kopling.png)

**Bibliografisk kopling** er eit anna mål: to publikasjonar som siterer dei same
tredje kjeldene. Den analysen nyttar også referansar som ikkje er i vårt
publikasjonsutval. Sterke koplingar er ikkje prøver av sanningsverdi.

![Siteringskohortar](figures/10-sitering-kohortar.png)

## 3. Tekstrom, klassifisering og stabilitet

![LSA-tekstrom](figures/06-lsa-tekstrom.png)

![Semantisk endring](figures/07-tekstdynamikk.png)

![Stabilitet mellom initialiseringar](figures/12-klynge-stabilitet.png)

K-means har median justert Rand-indeks om lag 0,55 mellom åtte initialiseringar.
Det er **ikkje grunnlag** for å handsame desse ni klyngene som naturgjevne
eller stabile teoretiske skular.

## 4. Strengtreff for metodologisk språk

![Metodesignal](figures/13-metodeord-i-samandrag.png)

![Metodesignal over tid](figures/14-metodeord-over-tid.png)

Av 2 922 tilgjengelege samandrag har 72 treff på valde hypoteseuttrykk
og 25 på replikasjons-/reproduksjonsuttrykk. Desse treffa er **ikkje ein
estimator for faktisk hypoteseprøving eller replikasjon**. Eit abstrakt kan
mangle slike ord sjølv om fullteksten demonstrerer metodane, og vise dei
sjølv om studien ikkje utfører dei. Språk og sjanger varierer.

## 5. Kontroll av utvals- og modellskjevleik

![Utval etter OpenAlex-rangering](figures/09-rangering-og-bias.png)

![Tidlegare nullmodell](figures/08-siterings-nullmodell.png)

Søkerangeringa, kjernevenyutvalet, manglande samandrag og
kontroll av forfattaroverlapp kan endre resultata. Full metodisk oversikt:

- [Avansert analyse](AVANSERT_ANALYSE.md)
- [Datakvalitet](DATAKVALITET.md)
- [Språksignal](ABSTRAKT_SIGNAL.md)
- [Hovudrapport](RAPPORT.md)
- [Nullmodell og siteringskopling](robustness.json)
- [Kodebok for etterprøving](../CODEBOOK.md)

## 6. Går siteringane til liknande argument?

![Semantisk kontrollert siteringslikskap](figures/15-siteringssemantikk-mot-nullmodell.png)

![Endring i siteringskontinuitet mellom kohortar](figures/16-siteringssemantikk-over-tid.png)

Ved 2 180 siteringskoplingar utan felles forfattarar er semantisk likskap i LSA-modellen
i gjennomsnitt 0,199 høgare enn for jamførte alternative publikasjonar
(bootstrap, klynga på siterande artikkel, 95 % intervall 0,188–0,210).
Dette er **ikkje** prov for replikerte eller vidareutvikla teoriar.

- [Siteringssemantikk og kontrollar](SITERINGSLINJER.md)
- [200 kandidatpar til verifisering](lineage_review_queue.csv)
- [Lokal nettlesar for uavhengig gransking](review.html)

## 7. Frå ufullstendig bibliografi til testbare hypotesar

![Stratifisert sannsynsutval av automatisk inklusjonsramme](figures/17-sannsynsutval-600.png)

Eit separat tilfeldig uttrekk på 600 postar, fordelt over 54 fag- og tidsstrata,
vert nytta til faktisk, uavhengig fulltekstkoding. Det er eit sannsynsutval
frå **dei 3729 automatisk tittelinkluderte postane**, ikkje frå heile den nordiske
forskingspopulasjonen. Kish-tilnærma effektivt utval ut frå vektene er 567.
Per no er **0 av 600** kodingspar fullførte; ingen faglege kategoriar er funne på.

- [Kodingsprotokoll og utvalsvekter](UTVALSPLAN.md)
- [600-arbeids utvals- og kodeark](probability_sample_600_double_coder.csv)
- [Faktisk kodingsstatus](CODING_PROGRESS.md)

## 8. Forsøk på tilbakevising av hovudhypotesen

Me har også søkt aktivt etter moglege motdøme. Av 1475 interne
siteringspar utan felles forfattar og med begge samandrag tilgjengelege,
blei 150 par valde ut for å granske mogleg eksplisitt prøving,
replikasjon, teoriutvikling og kritikk. Ordtreff og tekstlikskap er
berre kriterium for prioritering, ikkje stadfesta evidens.

![Kandidatar til motprøving, berre ordtreff](figures/18-motprovesignal.png)

- [Metode og trefftall for motdøme](MOTPROVER.md)
- [150 kandidatpar til manuell vurdering](possible_counterexamples_to_non_cumulative_design.csv)

**Vitskapleg konklusjon:** Strukturen i forskingslitteraturen kan målast,
men påstanden om at designteori er ikkje-kumulativ er enno **ikkje testa
med eit tilstrekkeleg validert mål**. Neste steg er eksplisitt, blind
fulltekstkoding av prøvbare påstandar, korleis dei vert testet i seinare
arbeid og eventuelle negative resultat. Ei streng hypotese må kunne
verte tilbakevist.

## 9. Tverrtiårige referanselinjer og kjeldekritisk kalibrering

I det avgrensa siteringsnettverket har me **712** vegar der eit arbeid
publisert 2020–26 siterer eit arbeid frå 2010–19 som igjen siterer eit
arbeid frå 2000–09. Berre **99** mellomarbeid ber slike vegar; dei fem
største står for **40,2 %**. Eitt dominerande knutepunkt er ei
*handbok*, ikkje ein rapportert replikeringsstudie.

Med omstokking av eldre referansetilvisingar innan **eksakt mellomår og
operativ temagruppe** er nullmedianen **292** vegar, mot observerte **712**.
Etter eksklusjon av ti største mellomarbeid er tala **203** mot **308**.
Dette er berre ein *utforskande* strukturell nullmodell av eit skeivt,
ufullstendig datasett. Resultatet seier ikkje noko åleine om eksistensen
eller omfanget av kumulativ, prøvbar kunnskap.

- [Full permutasjonsanalyse og konsentrasjonssjekk](SITERINGSBRUER.md)
- [Kjeldekritiske døme på bakgrunn, metodebruk og empirisk testing](KJELDEKRITISK_PILOT.md)
- [Relevant eksisterande metascience om design og replikasjon](EKSTERN_METAVITSKAP.md)
