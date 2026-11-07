# Formlære mot designteori: innlemming, motprøver og målbar tilleggskraft

*Forskingsprotokoll 0.1, 7. november 2026. Arbeidsdokument, ikkje eit stadfesta resultat.*

## 1. Påstanden som skal prøvast

Formlæra har ikkje vist seg overlegen fordi fem omgrep kan plasserast kring ein figur. Ei sterkare utsegn krev **tre ulike resultat**:

1. **Innlemming:** For ei presist identifisert utsegn i teori T finst ei eksplisitt omsetjing til Formlæra som bevarer originalutsegna, vilkåra og det forfattaren meinte å forklare.
2. **Tilleggskraft:** Frå same omsetjing kan me utleie minst éi ny, ikkje-triviell følgje som ikkje kjem frå T utan nye føresetnader.
3. **Empirisk framgang:** Den nye følgja gjev minst like godt kalibrerte, og helst betre, føreseiingar eller mekanismeforklaringar på ubrukte data enn ein rimeleg formulert komparator med same informasjonsgrunnlag.

Innlemming er ikkje det same som likskap i ordtilfanget. «Deltaking» vert ikkje innlemma ved å gi folk agentindeksar; «makt» vert ikkje forklart berre ved å skrive ein vekt; «kunnskapsdanning» vert ikkje forklart ved å gi ein kategori namnet K. Rekonstruksjonen må vise dei relevante mekanismane og kva som kan få henne til å feile.

Universalkravet «betre enn all tidlegare designteori» kan ikkje følgje frå eit endeleg litteraturutval. Kvar dokumentert seier er lokal og avgrensa. Ein streng teori kan vinna mange slike prøver utan å krevje at alle rivalar er verdilause.

## 2. Korpusstatus og utval

Samanlikningsgrunnlaget er det nordiske, søkbare korpuset i [lukketsvane/designteori](https://github.com/lukketsvane/designteori), ikkje ei påstått fullstendig liste over all designteori i verda.

Lokal analysestatus frå 2026-11-07T03:56:13Z:
- 34 029 søkbare registreringar; 24 812 frå OpenAlex og 9 217 frå separate nordiske arkivlag.
- 11 958 automatisk tittelinkluderte OpenAlex-registreringar; 12 854 avventar manuell relevansvurdering.
- 7 422 lokale PDF-filer, 7 305 med utvunne tekstlag og 346 431 indekserte tekstbolkar.
- 33 295 interne siteringskant-ar i det innsamla materialet.
- Dokumentert manuell artikkelrelevanskontroll: 0 i statusfilene. Ingen av desse tala er eit teljemål for validerte teoriar.

Korpuset inneheld også ikkje-designfaglege treff. Designrelevans skal vere ei eksplisitt, uavhengig manuell avgjerd. Den historiske og internasjonale teorikanonen er ein **separat komparator**, ikkje noko som skal skrivast inn i det publiserte nordiske metadatautvalet.

## 3. Formell kjerne og kva ho faktisk gjev

For eit endeleg operativt formrom og den fastsette konteksten i §§6.6–6.64:

\[
D = \{x : x\text{ kan nåast frå }s_0\text{ med tillatne steg utanfor }V\},
\qquad
P(x)=\frac{\mu_{SG}(x)\exp[-\beta\Phi(x)]}{Z},
\qquad
\Phi(x)=\sum_i w_i\hat{\Lambda}_i(x).
\]

Her er SG genereringsreglane, \(\mu_{SG}\) den oppgjevne grunnfordelinga over D, V harde veto og \(w_i\) faktisk relativ innverknad i denne valmodellen. For kvar agent kjem omhugsprofilen og estimerte avvik inn i \(\hat{\Lambda}_i\). Fordelinga gjeld **val**, ikkje automatisk faktisk skade eller gjennomføring.

For ei eksponentialfamilie der \(\beta\Phi(x)=\sum_k\theta_k\hat e_k(x)\), og D, grunnmål, estimat og faktisk utfallsmål står fast, følgjer frå §§6.673–6.674:

\[
\frac{\partial\mathbb E[e_j]}{\partial\theta_k}
=-\operatorname{Cov}_P(e_j,\hat e_k).
\]

Dette er matematisk etterprøvbart. Ved negativ kovarians kan sterkare prioritering av eit *feil* estimat auke den faktiske skaden. Ein endring av normaliserte omhugsvekter må reknast som ei vektflytting, ikkje som fri endring av berre éin \(\theta_k\). Ein test må òg respektere at irreversible produksjonssteg ikkje har den stasjonære reversible overgangskjernen i §6.64 som generell modell (§6.641).

**Det som ikkje er vist:** at desse parameterane er identifiserbare i verkelege prosjekt, at ei samanliknbar rivalmodell predikerer dårlegare, eller at det fullstendige innhaldet i C–K-teori, deltakande design, kritisk design eller forsking gjennom design allereie følgjer av femtuppelet.

## 4. Første originalkjelde-pilot

Dei fem kjeldene er identifiserte i korpuset og kontrollerte i lokalt lagra original-PDF. Nedanfor er ein *innleiande* mekanismelesnad basert på samandrag og opningssider. Ingen er fullstendig koda. Eit kjennemerke ved Formlæra tyder førebels **mogleg omsetjing**, ikkje stadfesta innlemming.

| ID | Originalkjelde | Faktisk bidrag som må bevarast | Mogleg plass i Formlæra | Uoppfylt bevisplikt |
|---|---|---|---|---|
| W2794258710 | Bødker & Kyng (2018), *Participatory Design that Matters*, DOI [10.1145/3152421](https://doi.org/10.1145/3152421) | Demokratisk kontroll, alliansar, fungerande prototypar og oppskalering som vilkår for innverknad | Agentar, \(w_i\), V, tilgjengelege politikkar, §6.632 | Forklar **kven som bestemmer** vekter og veto, ikkje berre kor store dei er |
| W2791285506 | Saad-Sulonen mfl. (2018), *Unfolding Participation over Time*, DOI [10.1080/15710882.2018.1426773](https://doi.org/10.1080/15710882.2018.1426773) | Fem tidslinser: fase, framvekst, tilbakesyn, framsyn og langtidsverknad | \(A_i(t)\), oppdatering av \(\Pi\), tidsavhengige kjerner, §6.641 | Vis kva ved deltaking som held fram og endrar makta etter prosjektperioden |
| W2624621937 | Raptis mfl. (2017), *Aesthetic, Functional and Conceptual Provocation in Research Through Design*, DOI [10.1145/3064663.3064739](https://doi.org/10.1145/3064663.3064739) | Feltstudie med fire familiar, ein provoserande prototype, utforsking av endra førestillingar og praksis | Endring i \(\Pi\), mål og landskap etter materiell intervensjon, §§3.11 og 6.4 | Formaliser korleis eit grep **endrar spørsmålet**, ikkje berre optimaliserer eitt fast mål |
| W144692220 | Baskerville & Pries-Heje (2014), *Design Theory Projectability*, DOI [10.1007/978-3-662-45708-5_14](https://doi.org/10.1007/978-3-662-45708-5_14) | Projectability og entrenchment som kjenneteikn ved overførbar teknologisk kunnskap | Invarians i mekanismar ved byte av formrom og kontekst | Prøv prediksjon på nye prosjekt med førehandsvalde omsetjingar og mål |
| W3004790496 | Fiore (2020), *Ethics of Technology and Design Ethics in Socio-Technical Systems*, DOI [10.7577/formakademisk.2201](https://doi.org/10.7577/formakademisk.2201) | Verdiorientert design og krav/ytelse-tenking anvendt på tilkopla produkt | Harde plikter i V, graderte omsyn i \(\Lambda\), ansvar hos agentar | Skil normativ rettferd frå deskriptive prioriteringsvekter |

Raptis mfl. er eit konkret motdøme til absoluttpåstanden om at empirisk undersøking ikkje skjer i designforsking. Baskerville & Pries-Heje er eit motdøme til påstanden om at spørsmålet om overførbar designteori ikkje har vore handsama. Desse døma seier ikkje kor vanleg slike praksisar er i heile faget.

## 5. Innlemming som krev vidare utvikling

**C–K-teori:** Formlæra sine K, C og U er ikkje utan vidare Hatchuel og Weil sine kunnskaps- og konseptrom. Ei sann rekonstruksjon må behalde operasjonane som endrar konsept og kunnskap, med vilkår for når noko vert avgjort som kunnskap. Faste kategoriar i \(\Pi\) er utilstrekkelege. Legg fram konkrete operatorkoplingar og vis at desse bevarer rørsla, i staden for å erklære heile C–K-teorien som eit trivielt grensetilfelle.

**Formgrammatikk:** SG kan generere og avgrense alternativ. Ein matematisk genererbar form er ikkje nødvendigvis materielt tilgjengeleg eller faktisk sannsynleg. Det styrkjer Formlæra berre dersom D, V, \(\mu_{SG}\) og stegprosessen vert fastsette utan bruk av utfallet som skal forklarast.

**Deltakande og kritisk design:** Ei agentvekt er ikkje ein demokratisk prosedyre, og ei fast kostnadsfunksjon forklarer ikkje ei handling som avdekkjer at sjølve målet var feil. Det trengst eit grunngjeve uttrykk for endring av \((G_i,\Pi,SG,V,\Lambda)\) over tid, med empiriske indikatorar for kven som fekk innverknad.

**Forsking gjennom design:** Dokumenter kva prototypen konkret gjer synleg som ikkje var kjent før. Skil tolking og lokalt situert innsikt frå generelle årsakspåstandar. Ei casebasert innsikt kan vere verdifull sjølv om ho ikkje er eit estimat av ein universell effekt.

**Etikk:** V må ha ein etterprøvbar normativ grunngjeving. Å setje høg verdi på noko er ein psykologisk eller institusjonell faktaopplysning; å ha rett til vern er ei anna type utsegn. Desse må ikkje likestillast ved normalisering av vektene.

## 6. Førehandsbestemd testprotokoll

**I. Utval og originalkjelde.** Trekk eit representativt, stratifisert utval frå den manuelt relevansvurderte ramma etter periode, sjanger, teoriart og domene. Ha i tillegg ei separat, eksplisitt vald internasjonal kanonprøve. Merk utilgjengeleg fulltekst som uavklart, aldri som ein negativ teoriskår. Registrer DOI, arbeids-ID, rett utgåve, eksakte sider og kjeldestatus.

**II. Uavhengig rekonstruksjon.** To kodarar les originalarbeidet utan å sjå Formlæra-vurderinga. Dei registrerer problem, premiss, sentral mekanisme, operasjonalisering, evidenstype, avgrensingar og mogleg motdøme. Legg særleg vekt på vellykka og sterke eldre teoriar, ikkje berre dei lettaste måla. Mål samråd på relevante variablar og bevar usemje.

**III. Formell omsetjing.** For kvar teorieining T registrer ei eksplisitt avbilding til \(M,\Pi,SG,\Lambda,\{A_i\}\), tilleggsføresetnader, kjelder til vekter/estimat, oppgjevne overgangar og kva som fell bort. Skår status: *bevart*, *delvis bevart*, *ikkje bevart*, *ikkje avgjort*. Berre *bevart* kan gå vidare som kandidatar for streng innlemming.

**IV. Ny følgje.** Utlei ei ny, presist formulerbar konsekvens frå den omsette modellen. Førehandregistrer kva observasjon som ville gjere denne utleiinga eller bruken av modellen feil. Ei ommerking av eit kjend funn tel ikkje som ei ny følgje.

**V. Lik prøve.** Frys datasplitt og vurderingsreglar. Samanlikn originalmodellen, relevante rivalar, ein enkel nullmodell og Formlæra med identiske treningsobservasjonar og testtilfelle. Rapporter sannsynsskår (log loss / Brier ved sannsyn), kalibrering, feiltypar, variasjon, konfidensintervall og modellkompleksitet. For ikkje-probabilistiske spørsmål: førehandsdefiner observerbare mekanismespor og uavhengig vurdering av forklaringskvalitet. Prosessinnsikt, normative argument og prediktive påstandar må ikkje blandast til éin kunstig totalskår.

**VI. Overføring.** Vel eit nytt materiale eller domene på førehand. Dokumenter kva variablar som får same rolle og kva som må estimerast på nytt. Ingen omdefinering etter at testutfallet er kjent. Dette er prøva av projectability.

**VII. Negative resultat.** Publiser også teoriar som ikkje kan innlemmast utan tap, og prøveprosjekt der Formlæra ikkje vinn. Ei slik motprøve kan vise kva for ei utviding som trengst, men utvidinga tel ikkje som ein førehandsstadfesta siger.

## 7. Fire konkrete forsøkslinjer

1. **Val av genererbare alternativ.** På eit registrert formrom med genereringsspor samanlikn grammatikkåleine \(\mu_{SG}\) med eksponentialvektinga i §6.6. Avklar om \(\Phi\) gir betre held-ut-prediksjon, utover fleire parameterar.
2. **Feil målestokk.** Mål agentestimat \(\hat e\) før realisering og skade/avvik \(e\) seinare. Manipuler eller observer særskilt prioriteringsstyrke. Prøv forteiknet frå \(-\operatorname{Cov}(e,\hat e)\), med faste vilkår og korrekt handsaming av normaliserte vekter.
3. **Deltaking og etisk veto.** Mål både faktisk innverknad og dokumentert legitim avgjerdsmakt over tid. Samanlikn utfall og skade med og utan grunngjeve veto, og mot ein modell som berre har mjuke vekter.
4. **Overføring mellom domene.** Formuler sams mekanisme på minst to tydeleg ulike prosjekt før resultata er kjende. Test om dei same relasjonane held med førehandsregistrerte avgrensingar.

## 8. Minste revisjonsspor for kvar påstand

Éi rad per konkret originalutsegn, ikkje per publikasjonsmetadata:
source_id, doi, publication_year, source_pages, original_claim, original_conditions, evidence_type, scope, candidate_mapping, mapping_assumptions, retained_mechanism, omitted_mechanism, novel_derivation, falsifier, comparator, preregistration, heldout_dataset, result, uncertainty, independent_coder_1, independent_coder_2, adjudication.

Gje statusen *uavklart* når noko ikkje er dokumentert. Revider ikkje gamle kodar utan ny sporbar versjon. Legg ikkje opphavsrettsleg verna PDF-filer eller lengre fulltekstutdrag inn i dette forskingsdokumentet. Metadata og konkrete DOI-lenkjer er tilstrekkelege for revisjonsspor.

## 9. Status ved første levering

- **Gjennomgått:** den gjeldande formelle kjernen i Formlæra §§6.6–6.674 og innleiande delar av fem originaltekstar frå det lokale PDF-korpuset.
- **Verifisert i kode:** syntetiske matematiske kontrollar av normalisering, veto, fortegnet i kovariansidentiteten og detaljert balanse ved symmetrisk forslag. Sjå test_6_6.py.
- **Ikkje påvist:** at Formlæra er empirisk meir treffsikker enn dei fem kjeldene, at kvar kjelde er fullt innlemma, eller at heile designteorien manglar kumulativ vitskap.
- **Prinsipp:** Dette arbeidet høyrer til i FORML-RE. Det publiserte nordiske korpuset i designteori skal halde fram som ein uavhengig og allment brukbar forskingsressurs.

**Føremålet er ikkje å telje kor mange teoriar me kan erklære underordna, men å finne kva frå dei som faktisk overlever ei streng omsetjing, og kva ekstra Formlæra kan vise når omsetjinga kan fellast.**
