# Første reelle teorianalyse: kva Formlæra bevarer, og kva ho må vinne

*7. november 2026. Resultatnotat 0.2. Skrive mot det lokale korpuset og den publiserte LaTeX-teksten. Ikkje ein fullstendig fagrevisjon.*

## 1. Den sterkaste matematiske motprøva (§6.6)

Fordelingsmodellen er

\[
P(x)=Z^{-1}\mu_{SG}(x)e^{-\beta\Phi(x)}, \qquad x\in D.
\]

**Representasjonssats.** For eit endeleg ikkje-tomt D, ei grunnfordeling \(\mu_{SG}\) med positiv vekt i heile D, ein fritt vald \(\Phi\), \(\beta>0\), og kvar målfordeling \(P^*(x)>0\) på D, set

\[
\Phi^*(x)=-\beta^{-1}\log\bigl(P^*(x)/\mu_{SG}(x)\bigr).
\]

Då er \(Z=1\) og \(P(x)=P^*(x)\). Følgja er at *samsvar etterpå ikkje er evidens for mekanismen* når \(\Phi\) kan tilpassast fritt. Dersom \(\Phi\) er fast avgrensa av målt agens, prediksjonar og prioriteringar, kan modellen derimot vere falsifiserbar. For nullsannsyn må ein undersøkje faktisk veto/støtte, ikkje berre setje ein uendeleg energi inn i ein modell som føreset endelege verdiar.

**Identifikasjonssats.** Dersom berre P vert observert, kan ein ikkje i alminnelegheit skilje (i) skalaen i \(\beta\) frå skalaen i \(\Phi\), (ii) additive konstantar i \(\Phi\), eller (iii) grunnfordelingsvurderingar frå seleksjonslandskapet. For ei vilkårleg funksjon \(h\) og ein normaliseringskonstant c gir transformasjonen

\[
\mu'_{SG}(x)=c^{-1}\mu_{SG}(x)e^{h(x)}, \qquad
\Phi'(x)=\Phi(x)+h(x)/\beta
\]

den same P. Eit finare samsvar med historiske former er difor ikkje eit bevis på at me har oppdaga dei faktiske trykka.

**Krav til motprøve:** Definer ein uavhengig genereringsprosess (\(\mu_{SG}\)), dokumenter faktisk tilgjengelege alternativ (D), mål eller registrer estimerte avvik og vekter *før* eit nytt val, og prøv sannsynsfordelinga på held-ut-val. Samanlikn med minst grammatikkåleine, historiefrekvensmodell og ein enkel multinomial/logistisk valmodell. Samanlikn resultat og kompleksitet, ikkje berre kurvetilpassing.

Sjå [test_identifiserbarheit.py](test_identifiserbarheit.py): sju køyrde syntetiske kontrollar, alle bestått.

## 2. C–K: Eit tilfelle der Formlæra ikkje enno har teke inn heile teorien

Hatchuel og Weil ([C–K-teori, 2003 og 2009](https://doi.org/10.1007/s00163-008-0043-4)) skil mellom eit kunnskapsrom av utsegner med logisk status og eit konseptrom av utsegner som ikkje er avgjorde i dette kunnskapsrommet. Operasjonane verkar på utsegnene og kan utvide både konsept- og kunnskapsmengda.

Formlæra §1.5 definerer derimot \(K_{A,k,t}, C_{A,k,t}, U_{A,k,t}\) som **delmengder av konfigurasjonar i \(\mathbb M\)**, klassifiserte etter kva som er avgjort langs eit kriterium. Dette er ei nyttig epistemisk inndeling, men ikkje same type objekt som C–K-teorien sitt utsegnsrom.

**Motdøme:** Ny kunnskap kan vere «denne produksjonsregelen krev ikkje skruer». Det er kunnskap *om ein regel*, ikkje medlemskapen til eitt formpunkt i \(K_k\). Ho kan endre \(SG\) og deretter alle tilgjengelege formpunkt. Å kalle dette \(K\to K\) i eit punktpartisjonert rom gjev ikkje åleine eit operativt bilete av regelen som vart lært. Eit konsept som «ein stol utan plate med fire bein» er eit predikat som skildrar mange moglege former, ikkje éin formposisjon.

**Prøvbar innlemming krev** ei typa omsetjing:
- eit eksplisitt utsegnsspråk \(\mathcal L\) for krav, eigenskapar, tilverkningsreglar og relasjonar;
- \(K_t^{prop}\subset\mathcal L\), med oppgjeven logisk status og gyldigheitsvilkår;
- \(C_t^{stmt}\subset\mathcal L\), konsept som enno ikkje kan avgjerast i \(K_t^{prop}\);
- ei tolking \(\llbracket c\rrbracket_{K_t^{prop}}\subseteq\mathbb M_t\), med uttrykkelege avgrensingar;
- fire dokumenterte operasjonsklassar: \(K\to C\), \(C\to C\), \(C\to K\), \(K\to K\), der endringar kan gjelde både utsegnsrom, \(SG_t\) og \(\mathbb M_t\).

Ein omsetjing som ikkje bevarer desse operasjonane, er ei analogi. §6.65(ii) i dagens manuskript seier presist at fordelingsgrensa er ei føreseiing om val og **ikkje** ei utleiing av C–K-rørsla. Dette bør haldast fast.

**Nytt krav:** Vis på eitt gjennomarbeidd designdøme at dei fire operasjonane i original C–K kan rekonstruerast, at dei produserer same rekkje kunnskaps-/konseptutvidingar, og kva ny prediksjon Formlæra gjev etter at seleksjon, materiell gjennomføring og seinare følgjer er lagde til.

## 3. Deltakande design: Makt kan ikkje lesast frå ein sum

Frå Bødker og Kyng, *Participatory Design that Matters—Facing the Big Issues* (2018), DOI [10.1145/3152421](https://doi.org/10.1145/3152421):

**Bevar:** Partnarskap med brukarar, alternativ til rådande løysingar, alliansar, fungerande prototypar, demokratiske avgjerder og oppskalering.

Formlæra sine \(w_i\) er effektive påverknadsvekter **gitt** ein bestemt valmodell. At eit oppdrag har tre agentar med positive vekter, fortel ikkje korleis representasjonen oppstod, kven som er utelaten, kven som kan krevje innsyn eller kven som eig avgjerda. Auka vekt til ein aktør er ikkje automatisk ei demokratisk legitimering.

Frå Saad-Sulonen mfl., *Unfolding Participation over Time* (2018), DOI [10.1080/15710882.2018.1426773](https://doi.org/10.1080/15710882.2018.1426773):

**Bevar:** Deltaking gjennom og mellom arrangement, og etter prosjektet. Artiklane introduserer fem analytiske tidslinser. Tidsvariasjon er ikkje berre ei tidsetikett på det same møtet.

**Forslag til avgrensa formalisering:**

\[
w_{i,t+1}=F_i(w_t,\mathrm{representasjon}_t,\mathrm{avgjerdsmakt}_t,
\mathrm{konflikt}_t,\mathrm{ressursar}_t),
\]

der F ikkje kan estimerast fritt i etterkant. Dokumenter kven som tok avgjerder, endra kva som var tilgjengeleg, og kva som vart oppretthalde etter overlevering. Ein streng test er om eit skifte i kontroll føreseier eit skifte i realiserte former *og* relevante utfall, utover oppgåva sine opphavlege krav.

Køyr ikkje ein statisk §6.6-modell på ei faktisk historisk prosesskjede utan overgangsmodellen i §6.641.

## 4. Forsking gjennom design: Grepet endrar sjølve spørsmålet

Frå Raptis, Jensen, Kjeldskov og Skov, *Aesthetic, Functional and Conceptual Provocation in Research Through Design* (2017), DOI [10.1145/3064663.3064739](https://doi.org/10.1145/3064663.3064739):

**Bevar:** Ein konkret feltstudie av fire familiar og ein provoserande prototype, utvikla for å undersøkje endringar i oppfatningar og energibruk. Dette er eit faktisk empirisk bidrag.

Eit eksisterande målbilete \(G\) og \(\Phi\) kan seie kva alternativ ein aktør vil velje *når kriteriet er fast*. Prototypen kan derimot gjere aktøren merksam på eit nytt kriterium, endre kva som er eit legitimt problem, eller avdekkje at føresetnadene var feil. Slik endring kan skildrast gjennom ein oppdateringsmekanisme

\[
(\Pi_t,G_t,SG_t,\Lambda_t)\xrightarrow{\text{møte med prototype}}
(\Pi_{t+1},G_{t+1},SG_{t+1},\Lambda_{t+1}).
\]

Dette er førebels eit **forslag til testbar dynamikk**, ikkje ei allmenn utleiing av eksisterande §6.6. For kvart tilfelle må ein skilje rapportert refleksjon frå observerte atferdsendringar og frå stadfesta effekt etter tid.

Frå *Doing Things with Research through Design* (2019; W2942602604): Bruken av artefaktar i forsking har fleire relevante funksjonar enn ferdige produkt i felttest. Dokumentasjon av korleis eit objekt *framkallar* kunnskap kan vere nødvendig sjølv når kunnskapen ikkje har form av ei kvantitativ prediksjon.

## 5. Etikk: Berre det fysiske høyrer i V

I gjeldande manuskript §1.42 er V definert som **materielt utelukka** former. Det er difor feil å plassere moralske rettar i V berre fordi ein rett er ufråvikeleg. Ei moralsk uakseptabel form kan framleis vere fysisk mogleg og faktisk bli produsert.

Frå Fiore (2020), *Ethics of Technology and Design Ethics in Socio-Technical Systems*, DOI [10.7577/formakademisk.2201](https://doi.org/10.7577/formakademisk.2201), og Öz, Dindler og Lindberg, *The Turn to Practice in Design Ethics* (publiserte metadata 2026; lokalt undersøkt fortrykk frå 2025), DOI [10.1016/j.ijhcs.2026.103779](https://doi.org/10.1016/j.ijhcs.2026.103779):

**Bevar:** Rettar og verdiar, konkret fordeling av ansvar, og måten etiske spørsmål oppstår og vert forhandla i situert praksis. Etikk er ikkje berre eit vektparameter for dei som allereie har makt.

**Operasjonell skilnad:**

\[
D_t^{mat}=\operatorname{Reach}(SG_t,s_{0,t})\setminus V_t^{mat}
\]
\[
D_t^{dec}=D_t^{mat}\cap N_t
\]
\[
P_t^{dec}(x)\propto \mathbf 1_{D_t^{dec}}(x)\,\mu_t(x)\,
  e^{-\beta_t\Phi_t(x)}.
\]

Her er \(N_t\) det som eit **spesifisert avgjerdsorgan** faktisk godkjenner eller nekter å ta vidare. N er ikkje det objektivt moralske gode, og det er ikkje eit ontologisk veto. Ein etisk kritikk må i tillegg kunne utfordre legitimiteten til sjølve organet og grunnlaget for avgjerda. Manglar organet makt til å stanse eit vedtak, skal nektingsregelen ikkje modellerast som effektivt eksklusjonsveto.

\(\Phi_t\) kan framleis modellere mjuke preferansar og faktiske insentiv, men er i seg sjølv ikkje ei etisk grunngjeving.

## 6. Sterke motdøme til absoluttpåstanden om at faget ikkje gjev noko vidare

Cronholm, Göbel og Drechsler (2025), *Creating Design Knowledge: The Interplay Between Kernel Theory and Practice* (lokal PDF knytt til W7120466491), studerer samspelet mellom etablerte teoriar og praksis i eit prosjekt med **ni føretak**. Dette er eit eksplisitt forsøk på å produsere overførbar designkunnskap gjennom teoretisk og empirisk grunngjeving. Originalen har ikkje DOI i den lokale posten.

Baskerville og Pries-Heje (2014), *Design Theory Projectability*, DOI [10.1007/978-3-662-45708-5_14](https://doi.org/10.1007/978-3-662-45708-5_14), utviklar prosjektbarheit og bruk på tvers av tilfelle som analytiske spørsmål. Dei gir eit eksisterande fagleg komparatorkriterium, ikkje eit vakuum som Formlæra åleine har oppdaga.

Muashekele mfl. (2023), *Ancestral and Cultural Futuring: Speculative Design in an Indigenous ovaHimba Context*, DOI [10.1145/3593743.3593761](https://doi.org/10.1145/3593743.3593761), er eit motdøme til at framtidsrom utan vidare er kultur-uavhengige. Ei omsetjing må bevare aktørane sine eigne tidsforståingar og normgrunnlag, ikkje berre gi dei same aksane som forskaren.

Det finst faglege bidrag som Formlæra må gjere reie for. Ein absolutt nullpåstand om eit heilt fag vert svekt av eitt gyldig motdøme. Påstanden om **fråvær av eit samla, etterprøvbart forskingsprogram på tvers av designteoretiske tradisjonar** er derimot eit vidare, avgrensa spørsmål som krev systematisk dokumentasjon.

## 7. Oppdatert korpusaudit: to ulike, tidsstempla versjonar

Etter protokoll 0.1 vart lagd til, har ein annan prosess oppdatert lukketsvane/designteori på main. **Dette er ikkje eit kontrollert før/etter-eksperiment.**

| Måling | Eldre lokalt uttrekk 03:56 UTC | Ny lokal main 05:27 UTC |
|---|---:|---:|
| OpenAlex-registreringar | 24 812 | 4 709 |
| Nordiske arkivregistreringar | 9 217 | 1 745 |
| Alle søkbare registreringar | 34 029 | 6 454 |
| PDF-registreringar i manifest | 7 422 | 1 477 |
| Manuelt kontrollerte relevanspostar | 0 | 0 |

Nyaste commit ved kontroll: 6717199 («Enforce 100% strict design-theory eligibility and iOS Safari UI overhaul»). Arbeidstrea var reine då statusen vart undersøkt. Endringa kan kome av strengare maskinell filtrering og påfølgjande PDF-synkronisering. **Me veit ikkje enno** om alle bortfiltrerte arbeid er irrelevante; ein kontroll mot ein uavhengig gullstandard trengst før «100%» kan tolkast som presisjon eller tilbakekalling.

Eitt **stadfesta feilkopla dokument** står framleis i den nye manifesten:
- W7169835608: metadata *Conceptual Foundations for Learning in Complexity Part 1: Designing systems oriented design learning* (2026, DOI 10.58279/v3006).
- Tilordna PDF: https://winbev.pbworks.com/f/LS-1988.pdf, med tittelen *Learning and Teaching Styles in Engineering Education* av Richard M. Felder og Linda K. Silverman, publisert 1988. Innhaldet er feil kjelde.
- Issue [designteori #4](https://github.com/lukketsvane/designteori/issues/4) oppretta; inga fil vart endra i Antigravity si arbeidsmappe.

Ei reproduserbar, førehandssådd kontrollprøve av **220 av 1 378** lokale OpenAlex-PDF-ar i den nye manifesten gav 205 eksakte titlar i dei tre første sidene, 10 sterke ikkje-eksakte teksttreff, 2 tvitydige, 2 mistenkelege og 1 uleseleg tekstuttrekk. Klassifiseringa er reprodusert med [audit_pdf_manifest.py](audit_pdf_manifest.py), utvalsfro 20261107. Desse automatiske flagga er **ikkje** manuell validering eller måling av kor mange PDF-ar som er feil. Det uleselege treffet hadde eit øydelagt tekstuttrekk; eit anna flagga dokument inneheldt konferanseproceedings framfor ein enkelt artikkel. Feilkoplinga ovanfor vart funnen ved særskild manuell originalkontroll og låg ikkje i den tilfeldige 220-prøva.

## 8. Kva som faktisk kan stå som hovudresultat no

1. Den finitte fordelingsmodellen er matematisk konsistent på dei testa døma. Testar av normalisering, veto, kovariansidentitet og detaljert balanse er gjennomførte.
2. Fri etterpåtilpassing gjer den statiske modellen metta. Evna til å rekonstruere gamle utfall er ikkje ny forklaringskraft.
3. C–K-teorien og Formlæra sitt punktpartisjonerte kunnskapsrom har ei reell **typeulikskap**, ikkje berre ulike namn på same struktur.
4. Deltaking over tid, institusjonell makt og normativ legitimitet treng eksplisitte overgangar og styringsmekanismar, ikkje berre fleire agentar i summen.
5. Fleire originale designforskingstekstar gjev empiriske, metodiske og teoretiske bidrag. Ei oppgåve for Formlæra er å vise kva meir som vert mogleg når slike bidrag vert kombinerte under testbare vilkår.
6. Ei empirisk siger over eksisterande modellar på held-ut-data er **enno ikkje dokumentert**.

**Neste dokumenterbare mål:** Eitt førehandsregistrert, kontekstuelt designeksperiment med verifisert alternativmengde, registrerte agentestimat og modellval, og minst to uavhengige baselinemodellar. Då kan me for første gong samanlikne forklaringskraft, ikkje berre symbolsystem.
