# Direkte teoriprøve: C–K og Formlæra

*Versjon 0.3, 7. november 2026. Kjeldenær originalgjennomgang og presise bevisplikter. Status: delvis omsetjing, ikkje stadfesta full innlemming.*

## Originalkjelder og påstandar

Armand Hatchuel og Benoît Weil, *A New Approach of Innovative Design: An Introduction to C-K Theory* (ICED 2003, 15 PDF-sider), lokal originalkopi: [original-PDF i referansearkivet](../../references/referansar/HatchuelWeil_2003_CK_Theory.pdf).

Hatchuel og Weil, *C-K Design Theory: An Advanced Formulation*, Research in Engineering Design, 19, 181–192 (volumår 2009; publisert digitalt 19. august 2008), DOI [10.1007/s00163-008-0043-4](https://doi.org/10.1007/s00163-008-0043-4), [lokal original-PDF](../../references/referansar/HatchuelWeil_2009_CK_DesignTheory.pdf).

**Viktig historisk korreksjon:** 2003-artikkelen framstiller allereie C–K som ei samlande designteori, og drøftar andre formelle teoriar som spesialtilfelle. Formlæra kan ikkje hevde prioritet for sjølve ideen om ein felles teori, og må difor overgå eit konkret, tidlegare samlingsforsøk.

I 2009-artikkelen er desse elementa sentrale:
- Konsept er utsegner om delvis ukjende objekt, som korkje kan stadfestast eller avkreftast med den gjeldande kunnskapen K (PDF-sider 1–2, 4–6).
- Konseptmengder er ikkje berre eit ferdig, listbart sett med kandidatprodukt. Forfattarane utviklar særlege C-set-omgrep om objekt som ikkje er fullstendig bestemte innan gjeldande kunnskap (PDF-sider 5–6).
- Fire operatorar koplar ekspansjon av konsept og kunnskap: C→C, C→K, K→C, K→K. Desse kan endre kva for eigenskapar som definerer ein objektklasse (PDF-sider 5–7).
- Eksempelet med Mg–CO2-motorar for Mars-oppdrag inneber nye scenario, omarbeidde konsept og ny kunnskap om når eit teknisk prinsipp kan fungere (PDF-sider 6–8).
- Proposisjon 1 knyter stabile, separate lukningsrom til regelbasert design; proposisjon 2 seier at innovative løysingar under visse vilkår er knytte til regenerering av lukningsrom (PDF-sider 10–11).

Dette er ein sterk originalkomparator. Å setje «C–K = kunnskapsdelen» i figur 6.66 ville vere ein dårleg rekonstruksjon.

## Typeproblemet

I §1.5 i Formlæra er den epistemiske partisjonen for agent A og omsyn k:

\[
\Pi_{A,k,t}=(K_{A,k,t},C_{A,k,t},U_{A,k,t}),\qquad
K_{A,k,t},C_{A,k,t},U_{A,k,t}\subseteq\mathbb M_t.
\]

Det er ein klassifikasjon av **formposisjonar** i eit operativt formrom, under oppgjevne prøvevilkår. I original C–K kan ein derimot ha ei udømd utsegn om *eksistensen av ein enno ukjend objekttype*. Ho kan ikkje utan tap reduserast til medlemskap i ei delmengd av ein på førehand uttømande liste med formposisjonar.

I C–K kan kunnskap òg gjelde proposisjonar om genereringsreglar, funksjonar og eigenskapar. Dersom ein ny regel gjer ei ny objektklasse mogleg, endrar det kva formrom som er operativt. Dette treng ei eiga kopling frå utsegnsrom til Formlæra sine formrom og grammatikkar.

**Minstekrav for ein typa bru:**

La \(\mathcal L_t\) vere eit ekspansibelt utsegnsspråk og \(\mathcal K_t\) ei kunnskapsbase. Eit kandidatkonsept \(c\) høyrer til \(\mathcal C_t\) berre når statusen til c ikkje er avgjord i \(\mathcal K_t\), under vald logisk og empirisk prøvepraksis. Definer ei *partiell* fortolkingsbru

\[
J_t:(\mathcal K_t,\mathcal C_t)\dashrightarrow
(\mathbb M_t,SG_t,\Pi_t).
\]

Ho må kunne la eit konsept vere **ennå ikkje representerbart** i \(\mathbb M_t\), i staden for å finne på eit ukjent formpunkt. Når nye eigenskapar, reglar eller objektklassar vert etablerte, må både \(\mathcal L_t\), \(SG_t\) og kanskje \(\mathbb M_t\) kunne endrast. Ei vanleg mengde med kjende alternativ er ikkje ein fullgod erstatning for denne ekspansjonen.

## Kva «innlemme» skal tyde

La \(T\) vere ei bru frå tilstandar i C–K til tilstandar i Formlæra, og la \(Q\) vere projeksjonen tilbake til C–K-språket. For **kvar** legitim C–K-operasjon \(o\) må me kunne vise eit endeleg spor av tilsvarande formoperasjonar \(F_o\) slik at

\[
Q(F_o(T(s)))\;\simeq\;o(s)
\]

for dei relevante utsegnene, kunnskapskrava og moglegheitene. Her tyder \(\simeq\) same observerbare logiske status og same relevante nye eigenskapar, ikkje at symbolstrengane er identiske.

Tre krav må haldast:
1. Ei udømd utsegn får ikkje på førehand sann/falsk status fordi me har valt eit endeleg formrom.
2. Ein overgang som endrar objektidentitet og kunnskapsstruktur, må ikkje tvingast inn som berre eit val mellom to kjende formpunkt.
3. Ein original C–K-operator må ikkje kunne gi ein følgje som den omsette modellen forbyr utan at avgrensinga er oppgjeven.

Berre dersom dette held, kan Formlæra kallast ei *konservativ utviding* av denne delen av C–K. Dette er eit beviskrav, ikkje noko me har vist ved ei tabellkopling.

## Den verkelege tilleggskrafta som Formlæra kan prøve

Om eit innovasjonsforløp har kome til eit *registrert* og avgrensa valsett D, kan Formlæra leggje seleksjon, innverknad og faktiske følgjer til C–K-tilstanden:

\[
P(x\mid D,\mu,\beta,\{\hat\Lambda_i,w_i\})
=\frac{\mu_{SG}(x)\exp[-\beta\sum_iw_i\hat\Lambda_i(x)]}{Z}.
\]

Denne modellen er **vilkårssett på at eit valsett finst**. Han seier ikkje åleine korleis C–K-prosessen produserte den nye objektkategorien eller konseptet som opna dette settet. Dei to delane må prøvast separat og deretter som kopla prosess.

Ei konkret, ny samanlikningsprøve kjem frå relativ innverknad:

Lat x og y vere to faste, materielt tillatne alternativ. Flytt ein liten del \(\delta\) av innverknaden frå agent j til agent i, slik at \(w_i'=w_i+\delta\) og \(w_j'=w_j-\delta\), medan D, \(\mu_{SG}\), \(\beta\), alle estimat og alle andre vekter er uendra. Då følgjer eksakt

\[
\log\frac{P_\delta(x)/P_\delta(y)}{P_0(x)/P_0(y)}
=-\beta\delta
\left[
\bigl(\hat\Lambda_i(x)-\hat\Lambda_j(x)\bigr)
-\bigl(\hat\Lambda_i(y)-\hat\Lambda_j(y)\bigr)
\right].
\]

Legg merke til at Z og \(\mu_{SG}\) fell bort i *endringa* av log-odds, når grunnfordelinga er den same. Dette er ei skarp prøve av **innverknad**, ikkje berre ei ommerking av makt.

Ho seier òg når skiftet skal ha **ingen direkte effekt**: Dersom skilnaden mellom agentane sine estimat er lik for x og y, er den føresagde endringa i log-odds null. Dette kan motprøvast gjennom reelle, randomiserte endringar i avgjerdsinnverknad med registrerte vurderingar før valet.

Følgja er rein algebra frå §6.6. Ho er ikkje ei dokumentert nyskaping i sannsynsteori. Det mogleg nye bidraget er den *same forklaringsarkitekturen* brukt på generering, kunnskapsendring, makt og seinare skade, med tverrfaglege utfall som ingen delteori predikerer åleine.

## Falsifikasjon, ikkje forteljing etterpå

Ein empirisk test må registrere:
- kva alternative former som faktisk var på bordet før avgjerda;
- kva kvar agent meinte om kvart alternativ, målt uavhengig av utfallet;
- kva innverknad kvar agent faktisk hadde, helst manipulert ved randomisering i eit legitimt oppsett;
- kva fysiske veto som gjaldt og kva normative avgjerder som skilde seg frå dei;
- om utfallet samsvara med prediksjonen ved tidsfesta test;
- endringar i mål, grammatikk, kunnskap og valsett mellom rundar.

Dersom D, estimata eller grunnfordelinga endrar seg mellom rundane, gjeld ikkje log-odds-formelen som isolert følgje av ei vektflytting. Desse endringane må få eigne ledd. Både C–K og dei andre formteoriane må få bruke sine eigne sterkaste, veldefinerte føresetnader i samanlikninga.

## Status

**Dokumentert:** Original C–K har eit tidlegare, eksplisitt samlingskrav; teorien si C-eining er ikkje ekvivalent med ein posisjon i eit fast formrom; og §6.6 har ei eksakt tilleggsprediksjon om vektflytting når vilkåra held.

**Ikkje dokumentert:** Full rekonstruksjon av dei fire operatorane og teorema hos Hatchuel og Weil; at Formlæra slår C–K på ny empirisk evidens; eller at denne algebraiske følgja ikkje kan utleiast av andre probabilistiske valmodellar.

**Konklusjon:** Konkurransen med C–K krev ei konservativ, typa omsetjing og eit separat bevis for *tilleggskraft*, ikkje ein metafor om at den gamle teorien ligg inni ei ny boks.
