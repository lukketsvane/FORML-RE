# Kvalitetskontroll av P1–P10 i designteori-korpuset

*7. november 2026. Revisjonsnotat, ikkje dom over dei faktiske artiklane. Kjelde: gransking/artikkel.tex og docs/data/corpus_quality.json på designteori main, kontrollert denne datoen.*

Det er eit vesentleg skilje mellom **korrekt berekna statistikk over metadata/algoritmiske tekstmarkørar** og ei **valid fagleg tolking** av kva markøren måler. Manuskriptet konkluderer med at alle ti meta-påstandane har sterk empirisk støtte. Samstundes viser corpus_quality.json at talet på fullførte *manuelle artikkelrelevanskontrollar* framleis er 0. Det trengst uavhengig kontroll av det underliggjande målet før desse talverdiane kan brukast som grunnlag for å erklære eit heilt fag ikkje-kumulativt.

| Påstand | Observert signal i artikkelutkastet | Kva signalet ikkje avgjer | Nødvendig motprøve |
|---|---|---|---|
| P1 forskingsprogram | 75,89 % av 61 066 siterte verk vert siterte berre éin gong; 1,23 % av PDF-ane har eksplisitt revisjonsspråk. | Eit fag kan ha mange einskildsiteringar og likevel ein stabil, liten kjerne; systematisk kritikk kan bruke andre ord enn detekterte. | Age-/feltjustert referansefordeling i samanliknbare fag; manuell revisjonskoding med konkrete sitat. |
| P2 kumulativitet | 94,13 % «semantisk amnesi» for likskapspar med cos≥0,80; svært få eksplisitte replikasjonsmarkørar. | Tekstlikskap er ikkje same problem og manglande sitering er ikkje manglande metodeoverføring. | Sidefesta kontroll av faktisk metodisk avhengigheit, direkte prøver, motseiingar og konseptbruk; baserate for siterelevans. |
| P3 hypotesar | 98,22 % av tekstane vert klassifiserte som utan formelle hypotesar. | Kvalitativ prosessanalyse kan prøvast utan ei ordrett H0/H1. | Blind, sjangerdelt koding av konkrete utsagn som kan fellast, med validerte gjenkjenningsratar for søkjestrengane. |
| P4 tverrfagleg eksport | 0,98 % av referansane frå ein stor ekstern kontrollkorpus går til nordisk designteori. | Dette er ikkje i seg sjølv «ingen verdi for andre fag» utan ein *eksponerings- og feltstorleiksjustert* samanliknar. | Sitering pr. relevant moglegheit, periodisert og samanlikna med andre smale forskingsfelt. |
| P5 effektkontroll | 95,86 % av prosessmetodiske tekstar manglar både detektert kontrollert effektmål og negativt utfall. | Ikkje alle fremjar ein kausal effektpåstand; nokre undersøker deskriptive eller forståande spørsmål. | Kod først typen kunnskapskrav, så om evidensmetoden er eigna til dette kravet. |
| P6 mandataffirmasjon | 120 av 122 finansierte mandattekstar koda affirmative; 0 eksplisitte reverseringar. | Maskinell positiv/negativ markør er ikkje sikker kode for resultat og etterrasjonalisering; finansiering er ikkje prov på binding. | Les original problemstilling, mandat, finansiering og avslutning manuelt; ha uavhengig kode og negative døme. |
| P7 doktorgradsliner | 0 PhD→PhD-kantar blant 201 avhandlingsregistreringar (24 i OpenAlex primærgrafen, 177 i nordiske arkiv). | Dersom 177 av 201 ikkje har same siteringskopling, betyr 0 lite om faktisk vidarebygging. Fråvær i lokal database er ikkje fråvær i vitskap. | Match avhandlingar og seinare verk mot eksterne DOI-/forfattaridentifikatorar; manuell fulltekstkontroll av avhandlingssiteringar. |
| P8 endogami | 40,55 % interninstitusjonelle siteringar; 4,23× gjensidig sitering mot ein gradbevarande nullmodell. | Gradbevarande null kontrollerer ikkje nødvendigvis felt, institusjonsstorleik, sampublisering, år og fagleg temalikskap; ingen «kartell» følgjer direkte. | Betinga nettverksnullar og kontroll av akademisk samband, ikkje insinuasjon frå topologien. |
| P9 etikk | 91,77 % manglar søkbar omtale av etisk komité i maskinkoda menneskestudiar. | Etisk godkjenning kan finnast i eksterne dokument, vere irrelevant for visse studietypar eller ha lovlege andre ordningar. Fråvær i PDF er ikkje brot på regelverk. | Skil studiedesign, land, etikkplikt, tidsregelverk og faktisk dokumentasjon; stadfest med primærkjelder. |
| P10 måleinstrument | 96,71 % manglar søkbare standardiserte skalaer og/eller psykometrisk reliabilitet. | Slik reliabilitet er ikkje nødvendig for kvar teoretisk eller kvalitativ metode; ein utvalsgyldig målestokk må vere metodepassande. | Skil mål av latent konstrukt frå geometriske, fysiske, tekstlege og historiske observasjonar. |

## Kva som kan publiserast før manuell validering

Dei faktiske prosentane kan rapporterast **som automatiske signal i dette avgrensa korpuset**, under vilkår om dokumentert kode, kjeldepopulasjon, sensitivitet og usikkerheit. Ein skal ikkje omtale markørfråvær som eit verifisert etikkbrot eller som eit bevis på at ingen empirisk designforsking finst. Tal i ei tabell er ikkje automatisk ein validert teori.

## Direkte følgje for Formlæra

Desse ti problemstillingane er legitime **forskningsspørsmål** som kan innlemmast i eit kumulativt forskingsprogram. Den sterkaste bruken av korpuset er:
1. Frys valid utvalsramme og manuelt kvalitetskontrollert gjeldande kjeldeversjon.
2. Trekk sannsynsutval, inkluder motdøme og sjanger- og periodekontroll.
3. Kod originalpåstandar, relevante operasjonar, prøvevilkår, faktisk resultat og seinare vidarebygging.
4. Omset dei som *påstandar med bevisplikt* til M, Π, SG, Λ og agentar.
5. Prøv om Formlæra sine nye følgjer held på held-ut-data og i nye domene, med same informasjonsnivå som sterke rivalar.

I tillegg kan det vere legitimt å vise at eit felt har svak standardisering eller manglar eit *felles disiplinomfattande program*, utan å hevde at alle einskildsatsingar har null forskingsverdi.

**Hovudregel:** Ingen negativ dom over heile designfaget skal brukast som positivt bevis for Formlæra. Formlæra må halde sjølv om dei beste eksisterande studiane er gode.
