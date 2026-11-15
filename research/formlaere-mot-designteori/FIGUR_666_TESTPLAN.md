# §6.66 som forskingsapparat: seks relasjonar, seks motprøver

*7. november 2026. Operasjonalisering av den innsendte figuren. Ei illustrert pil er ikkje i seg sjølv ei utleidd årsak. Dette er ein testplan, ikkje empirisk validering.*

Den allmenne forma har fem ulike objekt: formrom \(\mathbb M\), epistemisk tilstand \(\Pi\), grammatikk \(SG\), landskap \(\Lambda\) og agentar \(\{A_i\}\). Omgrepa må ikkje bytast mot kvarandre. Særleg er ein **genererbar** form ikkje det same som ein **valt**, **produsert**, **brukt** eller **museumsregistrert** form.

## Relasjonar i figuren, med falsifikator

| Relasjon i §6.66 | Operasjon som må observerast | Kva kan velte forklaringa? |
|---|---|---|
| SG → M, «genererer» | Lagra starttilstand \(s_0\), lovlege reglar R, overgangslogg og form-id. Spor om genererte kandidatar verkeleg tilhøyrer språket \(L(SG)\). | Produkt som er hevda generert av ein oppgjeven grammatikk, men ikkje kan nåast med dei registrerte reglane utan etterpåretting. |
| Π → M, «epistemisk deling» | K, C, U må registrerast per agent, omsyn og tidspunkt. Dette er **klassifikasjon av moglegheiter**, ikkje ein sjølvstendig fysisk årsak til nytt materiale. | Ei klassifisering som ikkje kan koplast til spesifikke kriterium eller som forvekslar ukjent med umogleg. |
| Λ → SG, «vala vert vekta» | Under fast kandidatrom vert utfallet modellert som \(P(x)\propto\mu_{SG}(x)e^{-\beta\Phi(x)}\). Vekting av *kandidatar* er ikkje ei endring av sjølve produksjonsreglane. | Held-ut log loss ikkje betre enn \(\mu_{SG}\) eller like-informerte rivalar, eller estimerte agentvekter vert fabrikerte etter valet. |
| A → SG, «vel og utfører steg» | Val og faktiske produksjonshandlingar skal tidsstemplast separat. Registrer forslag, avgjerd og realisering av \(s_t\to s_{t+1}\). | Påstått realisert form er berre ei skisse, eller faktisk utført steg manglar i registrert grammatikk. |
| A → Λ, «estimerer og svarar» | Lagra \(\hat\Lambda_i(x)\) *før* valet og målt ettertidseffekt \(e_i(x)\) *etter* gjennomføring. Registrer mål og toleransar. | Estimat er ikkje uavhengig av observert utfall eller korrigerer systematisk i feil retning under førehandsbestemt prøve. |
| Λ → Π, «prøving endrar kunnskap» | Det som faktisk endrar \(\Pi\), er observasjonar, testar og tolking av konsekvensar, ikkje pila som grafisk objekt. Logg **kva som vart undersøkt**, av kven, med kva epistemisk kriterium. | Klassifisering endrar seg utan ny evidens, ny regel eller forklarleg sosial læringsmekanisme. |

## Det sjette, underkommuniserte objektet

Den viste femdelte figuren manglar eit eige **registrert resultat og konsekvens** \(E_t\). Ho teiknar tilbakekoplinga indirekte. Skal figuren gjere påstanden «det gjennomførte» sann, treng den empiriske protokollen dessutan:

\[
(\mathbb M_t,\Pi_t,SG_t,\Lambda_t,\{A_{i,t}\})
\xrightarrow{\text{val, steg, realisering}}
(x_{t+1},E_{t+1})
\xrightarrow{\text{observasjon og revisjon}}
(\Pi_{t+1},SG_{t+1},\Lambda_{t+1},\{A_{i,t+1}\}).
\]

Det er ein **protokoll for data**, ikkje ein påvist allmenn dynamikklov. Ein kan ikkje rekne med at alt oppdaterer seg etter kvar intervensjon. Ei observasjon kan ikkje endre naturen sin fysikk, men kan endre kunnskapen, vurderinga og seinare praksis. Ei skråpil frå landskap til grammatikk bør ikkje sjølvstendig tolkast som at preferansar konstituerer generering. Dersom preferansar **faktisk endrar reglar**, krev det dokumentert lærings- eller institusjonsmekanisme.

## Det sjuande, ofte usynlege leddet: registrering

Når eit realisert objekt dukkar opp i ein katalog eller eit museum, har det gått gjennom endå eitt utval. Dette er ikkje den same pila som frå generator til val. §6.668 gjev, for ei registreringssannsyn \(r(x)\),

\[
Q_{\mathrm{arkiv}}(x)
=\frac{r(x)P_{\mathrm{realisert}}(x)}
{\sum_y r(y)P_{\mathrm{realisert}}(y)}.
\]

Det observerte korpuset kan derfor ikkje utan vidare identifisere korkje generatoren, landskapet eller kva som var materielt mogleg. Samle objekt-ID, kjelde, registreringsgrunn, eventuell duplikathistorikk og fråfallsforklaring separat frå formdata. STOLAR-piloten dokumenterer at dette er nødvendig i praksis. Sjå [STOLAR_ROBUSTHET_20261107.md](STOLAR_ROBUSTHET_20261107.md).

## Fire skilje som ikkje må glattast over

1. **Formrom vs listbare alternativ.** C–K-teori opnar ukjende objektidentitetar. Ei finitt, kjend kandidatliste kan berre vere eit mellombels lokalt snitt. Sjå [CK_DIREKTE_PROEVE.md](CK_DIREKTE_PROEVE.md).
2. **Materielt veto vs normativ avvising.** I manuskriptet er V materielt utelukka. Eit vedtak som forbode form, gjer ikkje forma fysisk umogleg; skil \(\mathrm{Reach}(SG,s_0)\setminus V\) frå avgjerdsorganets godkjenningssett.
3. **Sannsyn vs faktisk produksjon.** Gibbs-fordelinga gjeld val under vilkår. Berre tidsstempla steg og resultat dokumenterer realisering. Eit museumskorpus er eit kraftig selektert ettertidssnitt.
4. **Kunnskapsstatus vs verdi.** K, C, U er ikkje moral og ikkje ei enkel 1:1-omsetjing av Hatchuel–Weil sine proposisjonar; dei er status for vurderingar langs spesifiserte kriterium.

## Ei gjennomførbar, førehandsfrosen kasusprøve

Bruk ei konkret CNC-oppgåve med avgrensa emne og operasjonar: 12 mm bjørkefiner, målkube på høgst 500 × 500 × 500 mm, inga liming eller mekaniske festemiddel. I eit registrert valeksperiment skal alle genererte alternativ, kutt og steg vere arkiverte. To eller fleire vurderarar registrerer individuelle estimat før ein av tre regelbundne avgjerdsordningar vert randomisert, innan etisk og praktisk forsvarlege grenser. Alle har uendra reell rett til å reservere seg; innverknad er ikkje identisk med moralsk legitimitet.

**Førehandsutleiinga:** §6.676 gjev ei eksakt odds-endring ved endring av vekter når kandidatenes eigenskapar og genereringsgrunnlag er faste. §6.665 gjev rangvilkår for å skilje agentbidraga. §6.667 kan prøve linearitet ved kontrollert seleksjonsstyrke når det er operasjonelt definert. Faktisk brot og montering kan i tillegg etterprøvast med eksplisitte steg, medan bruksprøver med last, slitasje og langtidseffekt må gjennomførast separat.

**Lik konkurranse:** la C–K forklare kunnskaps- og konseptutvikling; formgrammatikk forklare genererbarheit; ein enkel logistisk valmodell forklare val; og den samankopla Formlæra få prøve **om ho gjev eit betre og meir føreseieleg samsvar mellom desse prosessane**. Ingen konkurrent skal straffast for ikkje å vere utvikla til ei anna oppgåve enn si eiga.

## Konklusjon

Formlæra si styrke, **dersom ho held**, er ikkje at ho har fleire boksar, men at kvar pil kan bindast til ein målt prosess, ein kontrollmodell og eit mogleg motbevis. Statiske formar i STOLAR støttar delar av morfologisk forklaring; dei kan ikkje åleine stadfeste agent- og kunnskapsdelane i figuren.
