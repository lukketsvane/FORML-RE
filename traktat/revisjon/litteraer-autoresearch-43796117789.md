# Litterær motlesing av FORMLÆRE, køyring 43796117789

Tredje redaksjonelle runde. Hovudteksten `traktat/tekst/formlaere.tex` er ikkje endra: ingen proposisjon, ikkje føreordet, ikkje lesekoden. Arbeidet ligg i dei to korte utgåvene. I `traktat/nettstad/kort.html` (tl;dr) er utvalet komponert om frå 54 til 67 proposisjonsnummer, rekkjefølgja er lagd om, og innleiingssetninga er bytt. I `traktat/nettstad/kortversjon.tex` er ni prosastader retta mot hovudteksten. Ingen formel er endra i nokon av filene.

**Framgangsmåte.** Eg las heile manuskriptet, kortversjonen og tl;dr-sida og laga eit eige arbeidskart, las så rapportane frå køyring 43789517081 og 43793380556, og tok ikkje opp att stadene som er avgjorde der. Tre uavhengige Agent-lesarar las same kjeldetekst utan tilgang til kvarandre eller til `traktat/revisjon/`. Førre rapport peika på at lesarar av same modell deler blindsoner. Denne gongen gjekk difor den litterære lesaren på same modell som redaktøren, den filosofiske på Opus og den kompromisslause på Sonnet. Dei fekk lista over avgjorde stader, det noverande tl;dr-utvalet, eitt framlegg til nytt utval og kandidatar i kortversjonen til dom. Eg hadde ikkje skal: bygg og testar er ikkje køyrde av meg. Eg har lese `check.py`, arbeidsflyten, `test_kort.mjs` (som krev at 1.31 og 5.7 står i utvalet, og at `groups` står på éi line) og `build.py` (der `make all` genererer `kortversjon.html` på nytt frå TeX-kjelda før kontrollane).

**Arbeidskartet, det som er nytt.** (1) tl;dr-sida er eit eige lite verk, og ho hadde ein annan komposisjon enn boka. Lesekoden seier at dei sju heiltalsproposisjonane kan lesast som eitt argument, men berre 1 var med. 1.43 tok opp att siste setning i 1.4. 1.55 brukte «det nærliggande moglege» utan 1.432, og «omsyn» vart brukt utan 1.324. 6.02 kalla designaren «ein formgjevar» utan 6.01. 6.7 gav måla «vekt i forma» før 6.6 og 6.67 hadde innført vekt. 7.24 stod utan 7.241, som i boka straks tek han attende. Utvalet slutta på 7.28 og vende aldri attende til byrjinga. (2) Kortversjonen hang etter rettingane i hovudteksten. `test_claim_consistency.py` låser «Meir fri vekt» og forbyr «meir omsorg» i hovudteksten, medan kortversjonen framleis sa «Meir prioritering betrar» og «kan meir omsorg ikkje auke». (3) I hovudteksten fann eg ingen ny komposisjon for føreordet, 5.72 til 5.724 eller 6.6 til 6.675 som let seg gjere innanfor låsane (rekkjefølgja av formlar og kjeldemerke står fast også i føreordet). Ingen av dei tre lesarane la fram noko nytt der heller. Del 1 til 4, som ingen runde har rørt, vart lesne særskilt. Dommen er at dei held.

### Behaldne

**tl;dr, innleiingssetninga**

- Før: «… under samtidige trykk, gjennom agentar med avgrensa omhug, omsorg og kapasitet.»
- Etter: «… under samtidige seleksjonstrykk, gjennom agentar med avgrensa omhug og kapasitet.»
- Funksjon: Grunnpåstanden fanst i tre ordlydar (føreord, kortversjon, tl;dr). No er han éi setning tre stader. Etter 5.281 er omsorg omhug langs aksane til ein annan, så «omhug, omsorg og kapasitet» talde same slag to gonger og fekk det til å sjå ut som om kvar formgjevar har omsorg, mot skiljet mellom 6.01 og 6.02. Omsorga kjem no som utviding i 5.28, ikkje som varsel.
- Motlesing: Den litterære og den filosofiske lesaren ville følgje føreordet ordrett. Den kompromisslause ville byte setninga mot ei skildring av sida («Eit utval proposisjonar, med ordlyden frå heile teksten …»).
- Tap: «Omsorg» står ikkje lenger i det fyrste lesaren ser. Forfattaren kan ha sett ordet der med vilje.

**tl;dr, dei sju heiltala**

- Inn: 2, 3, 4, 5, 6, 7.
- Funksjon: Utvalet har no den ryggraden lesekoden lovar. 7 («Forma viser kor langt omhugen rakk») mangla heilt, og det er setninga boka går mot.
- Motlesing: To lesarar godtok. Den kompromisslause kalla 2 til 6 og 7.3 «polstring utan innhald» og ville berre ha 1 og 7. Usemja står. Eg har vege lesekoden tyngst: utan 2 til 6 er 7 ein påstand utan veg fram.

**tl;dr, rekkjefølgja**

- Før: gruppa «Omsorg og skala» (5.28 … 6.76) stod føre «Formgjeving og val» (5.7 … 6.67).
- Etter: 5.28 og 5.282 står sist i «Hinne, agens, omhug og kapasitet». 6.01 og 6.02 står saman i «Formgjeving og val», som no kjem før «Omsorg og skala» (frå 6.7).
- Funksjon: Heile utvalet står i stigande nummerorden, som boka. «Vekt i valet» (6.67) kjem rett før «får måla til andre vekt i forma» (6.7). At omsorgsdefinisjonane står under overskrifta om omhug, gjer det 5.281 seier. Framlegget kom frå den litterære lesaren.
- Tap: Omsorgsgruppa opnar ikkje lenger med definisjonen sin. Den fjerde gruppa har tolv nummer.

**tl;dr, byte og tillegg i utvalet**

- 1.22 ut, 1.222 inn. Valens vert ikkje brukt seinare i utvalet. «Det moglege er ikkje laga, men gjeve» er eit berande postulat og mangla.
- 1.43, 1.501 og 1.62 ut. 1.324, 1.432 og 1.63 inn. 1.43 var ei dobling, dei to andre namngjeving. 1.324 innfører «omsyn», 1.432 det 1.55 byggjer på, og 1.63 («Han avgjer ikkje om forma vil verke») er hengsla til del 2. Alle tre lesarane kom til same liste for denne gruppa. Den filosofiske ville i tillegg halde på 1.62.
- 2.211 ut, 3.11 inn. Stilen vert ikkje følgd opp i utvalet. 3.11 («gjev berre fordelinga eit nytt namn») vernar 3.1 mot sirkelen føreordet åtvarar mot. Framlegget om 3.11 kom frå den kompromisslause.
- 5.232 inn. Blindskap, likegyldigheit og avmakt er skiljet føreordet lovar.
- 6.73 ut, 6.713 og 6.7131 inn. 6.73 er ein formel med symbol utvalet ikkje innfører, og 6.732 står åleine. 6.713 er staden der eit svar frå den andre vert vilkår. 6.7131 er det einaste biletet boka lèt lesaren røyne (det mjuke setet), og er no det einaste biletet i utvalet.
- 7.011 ut, 7.01 inn. «Verknadskjegle» vert ikkje brukt i utvalet. 7.01 er andre halvdel av grunnpåstanden i føreordet. Tap: paret lyskjegle og verknadskjegle.
- 7.14 ut. Formelen treng horisontar utvalet ikkje har. Tap: sviktlatensen, som føreordet nemner.
- 7.241 og 7.273 inn. Med «Vekt er ikkje hald» er 7.24 friksjon, ikkje ei rekning som går opp. 7.273 («ein del av bestillinga») kom frå den kompromisslause.

**tl;dr, slutten**

- Før: utvalet slutta på 7.28.
- Etter: 7.28, 7.3, 7.31, 7.32.
- Funksjon: «Teksten held noko utanfor» er bokstavleg sant om eit utval, og 1.01 («å halde noko anna utanfor») står i fyrste gruppe. Utvalet vender attende til byrjinga utan å seie det. «Svar» har ei bane i utvalet: 5, 5.11, 6.713, 7.25, og til sist «Lesinga er eit svar.» Ved å slutte der held utvalet 7.33 og 7.34 utanfor, så siste biletet i boka er ikkje brukt opp.
- Motlesing: Den litterære kalla dette verknad, ikkje pynt, så lenge 1, 1.01 og 7 er med. Den filosofiske meinte at slutten er ærleg berre med alle tre, fordi 7.31 nektar å bruke utelatinga som orsaking, og at det då bind utvalet sjølv: ei glippe i tl;dr kan ikkje orsakast med at ho er retta i fullteksten. Den kompromisslause ville stryke 7.3 som pretensiøs i eit samandrag og halde på 7.31 og 7.32.
- Tap: Den harde, utoverretta slutten på 7.28. Andre setning i 7.31 er tung i eit samandrag.

**Kortversjonen, ni prosastader (ingen formel endra)**

- Samandraget: «under samtidige trykk» til «under samtidige seleksjonstrykk» (2.1 og føreordet).
- Hinne. Før: «Ei hinne (Markov-teppe) er ei mengd tilstandar som skil …». Etter: «Ei hinne er ei grense av tilstandar mellom eit indre og eit ytre. I ein oppgjeven stokastisk modell er ho eit Markov-teppe når …». Følgjer 5.02 og 5.0201 («Ei statistisk grense er ikkje dermed ein membran»). Berre den filosofiske lesaren reiste dette.
- Substrat. Før: «sjølve substratet (… utan modell og politikk) er ein agent av nullte orden.» Etter: «Substratet sjølv (…) har korkje modell eller politikk; som «agent av nullte orden» markerer det grensa der berre den materielle verknaden står att.» Originalen kalla noko utan modell og politikk ein agent, midt i definisjonen som krev begge. Ordlyden følgjer 5.4. To lesarar.
- Stilart. Før: «Formene si sverming rundt eit felles tyngdepunkt i Λ er ein stilart.» Etter: «Ei vedvarande samling av former som ligg nær kvarandre i eit oppgjeve empirisk formrom, er ein stilart; kva som er nært, kjem an på aksane og avstandsmålet.» Følgjer 3.3 og held stilen unna sirkelen i 3.11. Alle tre lesarane. I same avsnitt «fast beregeometri» til «liknande beregeometri» (2.202).
- Bifurkasjon. Før: «… som i formhistoria viser seg som brå skifte (radiasjon etterfølgd av konvergens) etter lange periodar med stillstand.» Etter: «I formhistoria kan det vise seg som eit brått skifte etter lange periodar med små synlege endringar; eit slikt forløp kan òg kome av brå vilkårsendringar eller av val mellom dalar som framleis finst.» Følgjer 4.2 og 4.21. «Stillstand» stridde mot 4.1. Alle tre lesarane.
- Kovarians. Før: «Meir prioritering betrar … og skadar når det er vendt feil.» Etter: «Meir fri vekt θ_k betrar … og gjer det verre når estimatet peikar feil.» Ordlyden frå 6.674.
- Svarkurve: «kan meir omsorg ikkje auke» til «kan meir fri vekt på biletet ikkje auke» (6.711).
- Føreseiing 3: «meir prioritering» til «meir fri vekt på estimatet». Føreseiing 8: «meir omsorg» til «meir fri vekt på biletet». Føreseiing 7 står, sidan ho ikkje seier noko om forteikn.
- Tap i dei fire siste: «prioritering» og «omsorg» er orda ein lesar kjenner att. «Fri vekt» er teknisk. Det er same pris hovudteksten alt har betalt.

### Forkasta

1. **Heiltalsproposisjon 6, «Forma oppstår mellom grammatikk, kunnskap og agens, på fleire skalaer.»** (mitt eige). Tanken var at «mellom» alt ber 1.01, 2.112, 5.234 og 6.002, og at «i samspelet» er det slappaste leddet i dei sju heiltala. Tre lesarar, tre dommar. Den litterære ville ha «mellom» utan komma. Den filosofiske kalla «mellom» ein kategorifeil, fordi forma då liknar ein skilnad mellom forklaringslag og ein mistar at laga verkar på kvarandre (5.721, 6.632), og ville berre setje eit komma før «på fleire skalaer». Den kompromisslause heldt på originalen. Originalen står.
2. **1.6103, «svarar på geometrien» til «kviler på geometrien»** (litterær). Diagnosen er god: «svar» er ordet boka sluttar på, 5.013 krev ei grense for at noko skal vere eit svar, og i del 1 til 4 står verbet berre her og i 3.2. Med bytet ville «agentar som svarar på landskapet» i 5 vere ein terskel. Ikkje utført. Lesaren var sjølv usikker på verbet, dei to andre har ikkje sett framlegget, og ein regelbruk som tek geometrien inn og gjev ei ny form ut, kan lesast som ei tilsikta førebuing av svaret. Dette er det sterkaste uprøvde sporet i hovudteksten.
3. **tl;dr med fjellet: 1.321 og 1.3211 tidleg, 7.34 sist.** 7.34 verkar fordi heile boka ligg mellom dei to fjellsetningane. Over seksti setningar vert gjentakinga eit triks, og boka mistar sistebiletet sitt til samandraget.
4. **Den kompromisslause si liste på 54.** Ho tok ut 1.24, 2.12, 4.3, 5.02, 5.14, 5.234, 6.6, 6.67, 6.7, 7.03, 7.17 og 7.3, og sette inn 1.13, 2.141, 3.302, 4.31, 5.284, 6.68, 7.12, 7.15 og 7.21. Eg har teke 3.11, 7.273 og strykinga av 6.73 og 7.14 derfrå. Resten er avvist av to grunnar: lista manglar heiltala 2 til 6, og ho byter ut formlane 6.6 og 6.67 med prosa, slik at utvalet ikkje lenger viser at læra har ein valmodell. Innvendinga hennar står likevel: 67 nummer er meir enn eit samandrag pla ha.
5. **Tillegg eg vurderte og lét liggje for lengda si skuld:** 1.21 (struktur, filosofisk), 1.62 (filosofisk), 1.13 og 2.141 (kompromisslaus). 2.141 er hovudargumentet i føreordet og den eg er minst trygg på å ha halde utanfor.
6. **1.221, stryke andre setning, og 3.122, stryke «Utan dei er «optimal» tomt.»** (kompromisslaus). 3.122 svarar på 2.1311 («suboptimal»), og gjentakinga er eit omkved. 1.221 er eit atterhald av same slag som dei førre runde lét stå i 1.2222 og 1.2451, av same grunn.
7. **Kortversjonen, ei ekstra setning i teoremet «Kovarians»** om at prioritering er ei flytting av fri vekt (kompromisslaus). Rett, men teoremet seier alt «frie vekter», og setninga ville ha fortalt 6.673 om att.
8. **Kortversjonen, «då er den deriverte −Var(ê)» til «−Var(h(ê))».** Den filosofiske lesaren og eg kom uavhengig til at uttrykket slik det står, er rett berre om ê tyder det nye biletet h(ê). Ikkje endra: likningar ligg utanfor denne redaksjonen. Det same gjeld merknaden hennar om at «maksimerer den relative entropien til μ_SG» truleg skal lesast som minimal KL-avstand. Begge bør gå til sporet med rekneprøver, saman med 6.602 og 5.2001 frå førre rapport.
9. **Føreordet, 5.72 til 5.724 og 6.6 til 6.675.** Eg leita etter ein ny komposisjon i alle tre og fann ingen som ikkje anten er avgjord i tidlegare rundar eller krev flytting av proposisjonar. Null endringar der er resultatet av leitinga, ikkje ei unnlating.

### Heilskap

Boka er den same. Det som er annleis, er inngangane til henne.

tl;dr-sida var ei ordliste: den litterære lesaren talde 29 definisjonar av 54, og inga setning tok opp att ei tidlegare. No går sju heiltal gjennom utvalet, og lesaren kan følgje argumentet frå «Form er ei ordning av skilnader» til «Forma viser kor langt omhugen rakk». Tre ting skjer i utvalet som ikkje skjedde før. Vendinga om at omsorg kan gjere skaden større, kjem med ein kropp (6.7131), slik ho gjer i boka. 7.24 vert teken attende av 7.241. Og slutten gjer det byrjinga definerer: 1.01 seier at å skilje noko ut er å halde noko anna utanfor, og 7.31 seier at teksten held noko utanfor, på ei side som er skild ut av 491 proposisjonar. Dette er det næraste denne runden kjem det programmet ber om, at noko som såg ut som ein definisjon, viser seg som ei handling. Det er utvalet som demonstrerer det, ikkje nye ord.

Rekkjefølgja er no boka si. Omsorg vert innført som omhug langs aksane til ein annan, under overskrifta om omhug, og får vekt fyrst etter at vekt finst.

Kortversjonen seier ikkje lenger meir enn hovudteksten på dei stadene som er retta: stilen er ei samling i eit empirisk formrom og ikkje eit trekk ved landskapet, substratet er ei grense og ikkje ein agent, eit brått skifte kan ha fleire årsaker, og det er fri vekt, ikkje omsorg eller prioritering, teorema gjeld. Dei tre tekstane seier grunnpåstanden med same ord.

Det som ikkje er endra: føreordet fortel framleis boka på førehand, 5.721 til 5.7231 kommenterer framleis det 5.72 har gjort, og heiltal 6 er framleis det mjukaste av dei sju.

### Uvisse

- Alt ovanfor er litterær og redaksjonell dom, ikkje prov. Ingen målevariabel er nytta.
- **Lengda.** Utvalet har gått frå 54 til 67 nummer. Dei fleste tillegga er einlinjarar, og to formelproposisjonar er ute, men éin lesar meinte klårt at dette er for langt for noko som heiter tl;dr. Ho kan ha rett. Vert sida kjend som tung, er 3, 6.11, 5.14 og 7.3 dei fyrste eg ville prøve å ta ut.
- **6.7131 i utvalet er mi avgjerd åleine.** Lesarane fekk ikkje framlegget til dom. «Svarkurva» er dessutan ikkje innført i utvalet, heller ikkje i 6.713.
- **Utvalet ber seg framleis ikkje heilt sjølv.** «Struktur» i 1.212 og symbola i 5.7, 6.6 og 6.67 er ikkje innførte. 5.7 og 1.31 må stå fordi `test_kort.mjs` hentar dei.
- **Innleiingssetninga.** Om «omsorg» stod der med vilje, er bytet eit tap forfattaren bør rette.
- **Hinne i kortversjonen** kviler på éin lesar og på mi lesing av 5.02 og 5.0201.
- Lesarane er språkmodellar. Tre ulike modellar gav meir usemje enn i førre runde (om heiltal 6, om lengda, om 7.3), men dei er av same familie. Ingen menneske har lese endringane.
- Eg har ikkje køyrt bygg eller testar. `check.py` skal passere sidan hovudteksten er uendra. `kortversjon.html` vert generert på nytt av `make all`. Det nye i TeX-kjelda er hermeteikna « » kring «agent av nullte orden» og eitt nytt inline-uttrykk (θ_k). Feilar Pandoc på noko av dette, fell heile køyringa.
- Seinare arbeid kan øydeleggje dette: vert 1.01, 7.31 eller 7.32 omskrivne i hovudteksten, fell slutten på utvalet saman utan at nokon rører `kort.html`. Vert grunnpåstanden i føreordet endra, må innleiingssetninga og samandraget i kortversjonen følgje etter for hand.

**Estimert API-kostnad:** 8.099601499999999 USD.
