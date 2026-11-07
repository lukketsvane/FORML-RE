# STOLAR: kontroll av material-, teknikk- og geografisignal

Utforskande arbeid, 7. november 2026. Dette er ikkje direkte testing av valmodellen i §6.6.

**Kjelde:** STOLAR api.json, generert 2026-03-19T17:22:14Z. SHA-256 for den analyserte fila: 29e478099eaf1b707fbd327a72396db7ba290677ba85993736ab2bbec12a73e6.

Råarkiv: https://drive.google.com/drive/folders/1Bb11vGgjzpk-kNcuegjqYK7hHOtJsrP2

Utgangspunkt: 2 300 registreringar, 2 048 ulike objekt-ID-ar, 1 598 i målegyldig utval. Av desse har 663 registrert produksjonsteknikk og 326 registrert stil. Før 1900 er det 1 048 objekt (1 041 V&A, 7 Nasjonalmuseet), frå 1900 er det 550 (500 V&A, 50 Nasjonalmuseet).

## Metode

Alle utfall er kataloggeometri: log(høgd/breidd), log(breidd/djupn) og log(kubikkrot(høgd × breidd × djupn)). Modellen er ridge med alpha 20, tid som sentrert tredjegradspolynom og treningsbasert koding av materiale, produksjonsteknikk, produksjonsstad og nasjonalitet. 12 repeterte 75/25 gruppesplittar med random seed 20261107. Gruppe = same år, mål og oppgjeve materiale. Desse splittane overlappar og er ikkje 12 uavhengige replikasjonar. Kode: [stolar_robusthet.py](stolar_robusthet.py).

Tabellen viser **ekstra reduksjon i normalisert test-MSE** når materiale vert lagt til oppgjeven grunnmodell. Det er ikkje ein kausal effekt.

| Utval | N | Etter tid og teknikk | Etter tid, teknikk og produksjonsstad | Positive splittar i siste kolonne |
|---|---:|---:|---:|---:|
| Alle | 1598 | 0,0326 | 0,0297 | 12/12 |
| Før 1900 | 1048 | 0,0509 | 0,0451 | 12/12 |
| Frå 1900 | 550 | 0,0084 | 0,0044 | 7/12 |
| Teknikk registrert | 663 | 0,0132 | 0,0115 | 10/12 |

Nasjonalitetskontroll i staden for produksjonsstad: 0,0293 ekstra signal i heile utvalet, 0,0052 frå 1900. Desse kategoriane fangar ikkje same slags geografi.

### Kva geometrisk informasjon verkar materialet gjennom?

Etter tid og teknikk, i heile utvalet: høgd/breidd 0,0455, breidd/djupn 0,0196, samla storleik 0,0327. Før 1900: 0,0812, 0,0244, 0,0470. Frå 1900: 0,0269, **−0,0059**, 0,0042. Materialopplysningar kan dermed betre samla prediksjon og samstundes forverre ein av aksane.

### Éin gruppesplitt med parvis bootstrap

I eitt fast held-ut-utval, med årstal, teknikk og produksjonsstad som grunnmodell, vart resultatet:

| Periode | N test | Utan materiale | Med materiale | Betra MSE | Deskriptivt 95%-intervall |
|---|---:|---:|---:|---:|---:|
| Alle | 391 | 0,92975 | 0,89100 | 0,03875 | [0,01309, 0,06598] |
| Før 1900 | 263 | 0,88672 | 0,83063 | 0,05609 | [0,02512, 0,08925] |
| Frå 1900 | 135 | 1,09660 | 1,07326 | 0,02334 | **[−0,01000, 0,05537]** |

Intervallet for 1900+ omfattar null. Bootstrap resamplar testgrupper gitt dei valde modellane og datasplittane. Han fangar ikkje all usikkerheit kring museumsskjevheit, modellval, datavask eller historisk dateringsfeil.

### Formgjevargrupper

Ein separat gruppevis kontroll heldt alle objekt frå same namngjevne formgjevar saman. Kopiar med likt år/mål/materiale vart òg haldne samla, medan alle med «ukjent» formgjevar ikkje vart lagde i éi kunstig fellesgruppe. Etter tid, teknikk og produksjonsstad gav materiale ein ekstra MSE-reduksjon på 0,0304 i heile utvalet (12/12), 0,0367 før 1900 (12/12) og 0,0174 etter 1900 (9/12). Det motverkar nokre former for lekasje, men ikkje ukjend slektskap mellom objekt.

## Validitet og negative funn

- Stil er oppgjeve berre for 326 av 1598. Tidlegare delanalyse viste at stil har sjølvstendig geometrisk signal, men det er ikkje representativt for alle objekta.
- Teknikk er berre oppgjeve for 663 av 1598. Endring av analysen til denne delpopulasjonen er også eit utvalsskifte.
- Museumsregister har ikkje den faktiske lista av alternativ designaren kunne generere eller velje. Materialopplysningar om ferdig produkt er ikkje automatisk tidlegare produksjonsavgrensingar.
- Kopla datovariablar kan blande design-, produksjons- og katalogår, og bilet-/AI-berika metadata kan vere feil.
- Ein svak post-1900-effekt kan vere manglande statistisk styrke, annleis mål, andre materiale, utvalsskeivheit eller historisk endring. Me har ikkje identifisert årsaka.

## Kopling til §6.66

Datapiloten gjev empirisk støtte til at materiell og historisk kontekst er informative om **realiserte, arkivførte** former. Han dokumenterer ikkje ein bestemt grammatikk SG, grunnfordeling μ, agentestimert Λ eller vektene til agentane. Han viser nett kvifor desse ledda treng eigne observasjonar.

§6.668 gjer observasjonsproblemet eksplisitt: Dersom P er den faktiske fordelinga og r(x) er registreringssannsynet, er den observerte fordelinga Q(x) proporsjonal med r(x)P(x). Ukjend registrering kan likne eit seleksjonslandskap. Eit museumsarkiv er ikkje heile den genererbare verda.

**Status:** Reelt, avgrensa morfologisk resultat. Ikkje evidens for at heile Formlæra er betre enn sterkast eksisterande designteori.