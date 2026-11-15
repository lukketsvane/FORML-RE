# Kritisk gransking av formlære, november 2026

Oppdrag: GitHub-sak #25. Kjelde: `traktat/tekst/formlaere.tex` slik ho står på commit `b9d86ed`. Dato: 15. november 2026. Granskar: Claude Fable 5.2 (maskinell gransking, ikkje fagfellevurdering).

## 0. Samandrag

**Omfang.** Manuskriptet har 491 proposisjonar, fordelte 118, 27, 20, 16, 145, 112 og 53 på del 1–7. Tala er talde maskinelt frå kjelda og stemmer med oppdraget. Etter type: 313 `t`, 97 `d`, 42 `a`, 21 `o`, 18 `i`. Alle 491 er lesne i originalrekkjefølgje, og kvar `t` er halden mot premissane han viser til. Kva dette ikkje omfattar, står i 0.2 og kapittel 11.

**Hovudkonklusjon.** Den matematiske kjernen i del 5–6 held under vilkåra som står i notata. Eg fann ingen reknefeil i likningane. Feila ligg i avstanden mellom likningane og dei verbale slutningane som vert dregne av dei, og i samanbindinga mellom laga. Fire verbale påstandar er beviseleg for sterke, grunnomgrepa landskap, form og mogleg vert brukte i fleire tydingar, og programmet har enno ikkje rapportert éi einaste gjennomført prøve av dei tolv føreseiingane.

**Dei viktigaste funna, prioriterte:**

| Nr. | Proposisjon | Funn | Status |
| --- | --- | --- | --- |
| P1-a | 6.76 | «Viss og berre viss» held ikkje når den som har innverknad, gjev heile vurderinga bort | Motdøme rekna; retting i patch |
| P1-b | 6.614 mot 5.711 | Eit nytt alternativ endrar grunnvekta, og dermed forholdet mellom to gamle, innanfor modellen sjølv | Motdøme rekna; retting i patch |
| P1-c | 6.673, 6.674, 6.711, 7.1521 | Dei verbale slutningane gjeld berre ei fri vekt; under normaliseringa i 6.61 og 6.701 kan dei snu | Motdøme rekna; retting i patch for 6.673 |
| P1-d | 6.72 | Påstanden gjeld estimert skade, ikkje skade; notatet seier det, proposisjonen ikkje | Motdøme rekna; retting i patch |
| P1-e | 3.1, 5.1301, 6.13, 6.613 | «Landskapet» er både valvektinga og det verkelege følgjelandskapet | Ikkje retta; krev forfattarval |
| P1-f | 1.5, 5.7, 6.6, 5.724 | Den epistemiske partisjonen står i femtuppelet, men ikkje i likningane | Ikkje retta; krev bruvilkår |
| P1-g | 7, 7.24 mot 7.02, 7.11, 6.671 | Hovudtesen seier meir enn underproposisjonane tillèt | Ikkje retta; krev forfattarval |
| P2 | sjå kapitla | 20 inkonsistensar og skjulte vilkår | Ikkje retta |
| P3 | sjå kapitla | Typebruk og ordval | Ikkje retta |

### 0.1 Kva som faktisk er gjort

- Lese heile `formlaere.tex`: føreord, lesekode og alle 491 proposisjonane.
- Lese heile `nettstad/kortversjon.tex` og `README.md`.
- Lese 65 av dei 105 notata i `kjelder.json`: alle som høyrer til proposisjonar med merknad her, og notatet til føreordet.
- Rekna etter likningane i 5.704, 5.711, 6.613, 6.62, 6.64, 6.642, 6.65, 6.6711, 6.672, 6.6722, 6.673, 6.674, 6.6741, 6.6742, 6.702, 6.711, 6.731, 6.741, 6.754 og 7.1521. Av desse er 12 stadfestingar og 10 motdøme prøvde numerisk i `revisjon/kontrollrekning-2026-11.py` (22 liner utdata, ingen uventa utfall). 6.602, 6.613, 6.62, 6.65, 6.6711, 6.6742, 6.702 og 6.714 er berre kontrollerte for hand.
- Køyrt dei eksisterande testane (kapittel 9).

### 0.2 Kva som ikkje er gjort

- **Ingen eksterne kjelder er lesne.** Eg har ikkje kontrollert at éi einaste av dei 150 kjeldene seier det teksten tilskriv henne. Alle `o`-proposisjonar som kviler på kjelder, er difor uprøvde her.
- 40 av 105 notat er ikkje lesne. Ein merknad kan difor vere dekt av eit notat eg ikkje har sett; det gjeld ikkje merknadene P1-a til P1-d, der notata er lesne.
- Ordlista: 5 av 38 oppslag lesne, resten berre som titlar.
- `figurar.json`, figurane, den genererte HTML-en, PDF-en og `traktat-en/` er ikkje granska.
- Eg har ikkje ført eit skriftleg prov for kvar av dei 313 `t`-proposisjonane. Kvar er lesen og vurdert; skriftleg grunngjeving finst berre der eg fann noko å merke.
- Ingen empirisk prøve er gjord. Kontrollrekninga prøver matematikk, ikkje verda.

### 0.3 Lesemåte

Kvar merknad har: proposisjon og type, kva som sviktar, korleis det kan prøvast, og minste retting. «Notat» viser til `kjelder.json`. Prioritet: P1 = påviseleg feil eller berande tvetyding, P2 = inkonsistens eller skjult vilkår, P3 = typebruk og ordval.

---

## 1. Del 1: form, substans, formrom og epistemisk partisjon (118)

**Samla vurdering.** Del 1 inneheld tre ulike ting under same nummerering: ein ontologi (1.2–1.246), eit formrom med materiell deling (1.3–1.43) og ei epistemisk deling (1.5–1.55), og dessutan formalgebraen (1.6). Ontologien er uprøvbar etter eige utsegn (1.23 [a], 1.2342 [t]) og ber ingen av dei formelle resultata i del 5–7. Dei to delingane har reelle inkonsistensar.

#### 1.52 [t] mot 1.54 [t] (P2)
- **Svikt.** 1.52 seier at slutningar frå det prøvde kan avgjere noko som ikkje er realisert. 1.54 seier at «berre ei prøve kan gjere eit tenkt alternativ kjent». Slutninga i 1.52 er ikkje ei prøve av alternativet. Anten er 1.54 for sterk, eller så tyder «prøve» to ting.
- **Test.** Finn éin posisjon som er avgjord ved rekning eller simulering utan å vere realisert (6.6411 nemner sjølv simuleringar). Han ligg i K etter 1.52 og i C etter 1.54.
- **Minste retting.** 1.54: «Berre ei prøve, eller ei slutning frå noko prøvd, kan gjere eit tenkt alternativ kjent.»

#### 1.54 [t], 1.541 [t] (P2)
- **Svikt.** «Den epistemiske rørsla har fire retningar» er ført som følgje, men er henta frå C–K-teorien (notat 1.54), der U ikkje finst. Med tre mengder finst ni overgangar. Teksten sjølv nyttar to som ikkje er med: tap av kunnskap (4.41 [t], 5.5212 [t], 7.041) og avgjerd utan førehandstanke, når eit uhell i materialet avgjer noko ingen hadde tenkt (U til K).
- **Test.** Klassifiser eit dokumentert handverkstap og eit dokumentert tilfeldig funn i dei fire retningane. Går det ikkje, er lista ufullstendig.
- **Minste retting.** Endre typen til `d`, eller skriv «fire retningar som utvidar», og nemn tapet som eiga rørsle.

#### 1.41 [d], 1.432 [d] mot 1.411 [t], 4.41 [t] (P2)
- **Svikt.** Det busette er alt som «er eller har vore» realisert (1.41). Det nærliggande moglege er det opne som grensar til det busette (1.432). Men 1.411 krev at kvar realisering startar i ein realisert tilstand, og 4.41 seier at tap av stoff og handlag stengjer vegar. Ein posisjon som var realisert, men er tapt, gjev då «nærliggande» naboar ingen kan nå. I tillegg kan ein busett posisjon vere forboden no (1.4 [d]), så busett og forbode overlappar; føreordet omtalar dei likevel som ei tredeling.
- **Test.** Vel ein tapt teknikk. Naboane hans er nærliggande etter 1.432 og utilgjengelege etter 4.41.
- **Minste retting.** 1.432: «grensar til det busette som framleis kan takast opp att».

#### 1.62 [d], 1.622 [d] mot 1.4 [d], 1.2453 [d] (P2)
- **Svikt.** Grannskap, tilgang og det nærliggande moglege er definerte ved eitt steg i den historiske grammatikken, altså reglane som er «kjende og i bruk» (1.62). Etter 1.2453 er det som avheng av kva som er kjent, epistemisk. Den «materielle» delinga er dermed delvis epistemisk. Kortversjonen kallar henne likevel «materiell (ontologisk)».
- **Test.** Lat ein agent lære ein ny regel utan at noko materiale endrar seg. Det nærliggande moglege endrar seg.
- **Minste retting.** Stryk «(ontologisk)» i kortversjonen, og sei i 1.4 at grannskapen er relativ til stegrepertoaret.

#### 1 [d], 1.212 [d], 1.31 [d], 1.32 [d] (P2)
- **Svikt.** Ordet form tyder tre ting: ordning av skilnader (1), strukturen til ein konfigurasjon teken abstrakt (1.212), og eit punkt i formrommet (2 [a], 6.6 [a]). Etter 1.2122 [t] kan to konfigurasjonar dele form; etter 1.32 er kvar konfigurasjon eitt punkt. Det er uavklart om punkta er einskildting eller typar. Dermed er det uavklart kva \(P(x)\) i 6.6 er ei fordeling over: tilverka eksemplar, modellar eller avgjerder. Notat 1 og 1.31 tek det ikkje opp.
- **Test.** Tel eitt masseprodusert møbel og eitt unikt. Gjev dei to observasjonar eller éin million og éin? Svaret endrar kvar empirisk fordeling.
- **Minste retting.** Éi setning i 1.32 om at eit punkt er ein formtype, og éi i 6.601 om observasjonseininga.

#### 1.31 [d], 1.42 [d], 1.2451 [t] (P3)
«Mogleg» tyder logisk skildra (1.42), gjeve i feltet (1.222 [a]) og materielt tillate. Formrommet er «alle moglege konfigurasjonar», men rommar forbodne posisjonar. Retting: skriv «alle skildra konfigurasjonar» i 1.31.

#### 1.23 [a]–1.246 [t], samla (P2)
- **Svikt.** Ingen formell følgje i del 2–7 nyttar opplevingsontologien som premiss. Stryk 1.23–1.246, og 5.7, 6.6, 6.673 og 7.152 står uendra. Ontologien er dermed eit tillegg, ikkje eit grunnlag, og han kan ikkje felle eller verte felt av noko i programmet (7.171 [a] nemner han heller ikkje i den harde kjernen). 1.244 [t] utleier at mønster kan vere lukka for kvarandre innanfrå, men det er nett det 1.241 [a] postulerer; følgja legg ingenting til.
- **Test.** Merk kvar `t` i del 2–7 som siterer 1.23–1.246, og sjå om noka likning eller føreseiing er mellom dei.
- **Minste retting.** Éi setning i lesekoden eller 1.2342 om at del 2–7 ikkje føreset 1.23–1.246.

#### Typebruk i del 1 (P3)
- **1.232 [o]** og **1.2331 [o]** er filosofiske tesar, ikkje observasjonar. Bør vere `a`.
- **1.245 [t]** definerer naturlov. Bør vere `d`.
- **1.411 [t]** og **1.243 [t]** har ingen premiss dei følgjer av. Bør vere `a`.
- **1.12 [t]** føreset at «er tilfelle» er tovalent; det er ei fastsetjing, ikkje ei følgje av 1.11.
- **1.0121 [t]** går frå «kan verke før namnet» (1.012 [o]) til at oppdaging aldri er laging. Slutninga held berre for skilnader som fanst på førehand.
- **1.53 [t]**: U heiter «det utenkjelege», men rommar det som enno ikkje er tenkt. Kortversjonen skriv «utenkt» éin stad. Eitt ord bør veljast.
- **1.4311 [t]**: «utan materialskifte» bør vere «utan skifte i materiale eller operasjonar», jf. 1.422.

**Utan merknad i del 1:** 1.5 [d] er ein gyldig partisjon (notat 1.5 seier det uttrykkjeleg), 1.51 er vist ved døme, 1.6–1.611 følgjer formgrammatikken slik teksten attgjev han (kjelda ikkje kontrollert).

---

## 2. Del 2: seleksjonstrykk (27)

**Samla vurdering.** Definisjonane er greie. Kjerneargumentet mot funksjonslæra kviler på ei tvetyding.

#### 2.141 [t] og føreordet (P2)
- **Svikt.** «Affordansestrukturen er konstant innanfor klassen, og ein konstant forklarer ingen skilnad.» Det er sant fordi klassen er definert ved affordansestrukturen (1.3, 2.14; notat 2.14 seier at dette er «teksten sitt grep»). Argumentet treffer funksjon som medlemskapskriterium. Det treffer ikkje funksjon som gradert omsyn: kor godt ei form fyller funksjonen, varierer innanfor klassen og er etter 1.324 eit omsyn \(X_k\) med avvik \(e_k\). Andre setning i 2.141 vedgår dette: funksjonen seier «kvar formene samlar seg og kor trongt». Då forklarer han noko av variasjonen.
- **Test.** Mål funksjonsoppfylling som eitt omsyn, og sjå om det predikerer formskilnader ut over grunnmodellen. Gjer det det, er påstanden i føreordet for sterk.
- **Minste retting.** 2.141: «... og som konstant forklarer han ingen skilnad.» Føreordet bør skilje funksjon som klassekriterium frå funksjon som omsyn.

#### 2.201 [o] (P2)
- **Svikt.** «Systematisk langsamare» kviler på eitt døme. Dessutan må eit materiale finnast før ei form i materialet; rekkjefølgja er logisk gjeven, og berre lengda på etterslepet er empirisk.
- **Test.** Mål etterslepet for eit førehandsfastsett utval materiale og klassar.
- **Minste retting.** «I dømet under kom forma lenge etter materialet.»

#### 2.21 [t] (P3)
«Stilperioden er ein slik variabel» er ein empirisk påstand og same hypotese som 2.202 [a]. Bør ikkje stå som følgje.

#### 2.13 [a] (P3)
Første setning er ein definisjon av konflikt. 2.131 [t] følgjer av han, så typen bør vere `d`.

**Utan merknad:** 2.1, 2.11, 2.122 og 2.1311 er konsistente med 3.1 («berre skilnader tel»). 2.202 er rett merkt som hypotese, og notatet gjev prøvevilkåra.

---

## 3. Del 3: landskapet (20)

#### 3.1 [d], 5.1301 [t], 6.13 [t], 6.613 [t] (P1-e)
- **Svikt.** Etter 3.01 og 3.1 er landskapet minus logaritmen av vektinga fordelinga faktisk får. Etter 6.613 er det \(\beta\Phi+\lambda_{SG}+c\), der \(\Phi\) er bygd av *estimerte* avvik. Då er det å gå ned i estimert avvik det same som å gå ned i landskapet, same kor feil estimatet er. Men 5.1301 seier at estimert nedgang fører ned i «det verkelege landskapet berre så langt estimatet er rett», og 6.13 set agenten som vel, opp mot landskapet som filtrerer. Her er landskapet noko anna: det faktiske avviket. Skrivemåten \(\hat\Lambda\) forsterkar forvekslinga, for \(\hat\Lambda_{A,k}\) er ikkje eit estimat av eit ledd i \(\Lambda\) slik 6.613 definerer det.
- **Test.** To former, \(\hat e=(0,1)\), \(e=(1,0)\). Etter 6.613 ligg den første lågast i landskapet. Etter 5.1301 ligg ho høgast.
- **Minste retting.** Gje dei to kvar sitt namn, til dømes vallandskap (3.1, 6.613) og følgjelandskap (5.1301), og skriv «det faktiske avviket» i 5.1301.

#### 3.01 [a] mot 7.172 [d] (P2)
- **Svikt.** Kvar positiv omvekting kan skrivast som eit produkt av faktorar. Postulatet har innhald berre dersom faktoren til eitt trykk står fast når eit anna kjem til. Notat 3.01 opnar for at samspel «må skiljast ut som eigne ledd». Med den utvegen kan additiviteten ikkje fellast, medan 7.172 fører han opp som ein hjelpehypotese som kan det.
- **Test.** Mål \(f_1\) åleine, \(f_2\) åleine og begge saman. Additiviteten held dersom produktet treffer innanfor oppgjeven feilmargin, utan samspelsledd.
- **Minste retting.** Sei i notatet at eit samspelsledd som vert lagt til etter prøva, tel som tap etter 7.173.

#### 3.12 [a] (P3)
«Eit landskap har fleire lokale minimum» er ein allpåstand. Motdøme: \(\Lambda(x)=x^2\) med steg \(\pm1\). Retting: «kan ha».

#### 3.302 [t], 3.303 [t] (P3)
At stilperiodar er gradientar og ikkje øyar, er empirisk og følgjer ikkje av 3.3. Bør vere `a`.

#### 3.41 [t] (P3)
Konvergens er indisium, ikkje «prøva». Andre setning og føreseiing (xii) gjev dei rette atterhalda; første setning bør dempast til «ei prøve».

**Utan merknad:** 3.101 er rett (notat 3.1 nemner at gradientretninga avheng av skaleringa). 3.11 og 3.122 er gyldige atterhald mot sirkelslutning.

---

## 4. Del 4: dynamikk (16)

#### 4.12 [t] (P3)
Ei gradvis forskyving *kan* få ein dal til å forsvinne. Proposisjonen seier at ho gjer det. 4.21 har det rette vilkåret. Retting: «kan hope seg opp».

#### 4.33 [t] mot 6.64 [t] (P2)
- **Svikt.** Ei kjede som konvergerer mot \(P\) (6.64), gløymer starten. Stiavhengigheit som «grunntrekk» og likevektsfordelinga gjeld difor ikkje same prosess. Teksten løyser dette i 6.641 og notat 6.641, men då må kvar empirisk bruk av 6.6 først vise at prosessen er reversibel og vilkåra faste. Det vilkåret står ikkje i føreseiingane (i)–(vi).
- **Test.** Start same søk frå to ulike former. Skil fordelingane seg etter lang tid, gjeld ikkje 6.6 der.
- **Minste retting.** Legg vilkåret til registeret i notat 7.174.

**Utan merknad:** 4.5 er ei gyldig slutning. 4.2 og 4.21 er varsamt formulerte.

---

## 5. Del 5: agent, kapasitet og kjernelikning (145)

**Samla vurdering.** Definisjonane i 5.21–5.2312 er velforma, og 5.2102 følgjer av dei. Kjernelikninga er rett merkt som hypotese. 5.704 er kontrollert: Monte Carlo gav drift \((-0{,}00111, -0{,}00222)\) mot føresagt \((-0{,}00125, -0{,}00250)\); avviket på 11 % har forteiknet andreordensleddet gjev, og notat 5.704 seier at uttrykket er ei førsteordens tilnærming.

#### 1.5 [d], 5.7 [a], 6.6 [a], 5.72311 [t], 5.724 [t] (P1-f)
- **Svikt.** Føreordet seier at laga vert «samla i éin stokastisk overgangsprosess». Partisjonen \(\Pi=(K,C,U)\) står i femtuppelet, men ikkje i 5.7, 5.701, 5.702 eller 6.6; fordelinga er skriven \(P(x\mid\{A_i\},SG,V)\). 5.72311 seier i ord at kunnskapsstanden avgrensar kva som kan føreslåast og kor rett det vert vurdert, men ingen likning seier korleis. Den einaste formelle koplinga er grensetilfellet 6.65, som notat 5.72 sjølv seier ikkje er ei utleiing av tanke-kunnskapsrørsla. Det epistemiske laget er altså ikkje bunde saman med dei to andre.
- **Test.** Endre \(K\), \(C\) og \(U\) i modellen utan å røre \(q\) og \(\hat e\). Ingen føreseiing endrar seg.
- **Minste retting.** To bruvilkår: (a) \(q_A(x,x')>0\) berre for \(x'\) som forslaget gjer tenkt, jf. 1.63; (b) for \(x\in K_{A,k}\) ordnar \(\hat e_{A,k}\) formene slik prøva gjorde. Då vert (b) prøvbar: estimatfeil skal liggje i C, ikkje i K.

#### 5.7231 [a], 5.72311 [t], 5.72312 [t], 5.721 [t] (P2)
- **Svikt.** Dei «tre laga» er grammatikk, kunnskap og agentar (5.721, 5.724). Dei «tre ledda» er generering, vekting og gjennomføring, borne av grammatikk, landskap og kapasitet (5.72311). Det er to ulike tredelingar: kunnskapslaget er ikkje eit ledd, og landskapet er ikkje eit lag. 7.171 legg til eit skilje mellom val og følgje, og føreordet nemner fem feilstader. Kva som ville vere eit «fjerde ledd», er difor uklart, og sidan \(q\) og \(\Phi\) er frie funksjonar, kan kvar ny faktor plasserast i eitt av dei. Notat 5.7231 svarar delvis: plasseringa skal fastsetjast før prøva.
- **Test.** Føreseiing (x) held berre meining med ei førehandsliste over kandidatar til fjerde ledd. Ho finst ikkje.
- **Minste retting.** Før opp minst éin namngjeven kandidat i registeret.

#### 5.232 [d] og føreordet (P2)
- **Svikt.** Føreordet seier at «manglande hald deler seg» i blindskap, likegyldigheit og avmakt. 5.232 deler berre det som fell utanfor \(H_0\). Hald kan òg mangle når aksen ligg i \(H_0\): ved konflikt (5.2102), ved feil estimat (6.674) og når politikken agenten faktisk nyttar, ikkje er den som held (5.2312). 7.11 [t] har den rette, lengre lista. 5.521 [t] kallar dessutan ei einsidig lære «blindskap» sjølv om ho etter 5.232 er likegyldigheit så lenge kapasiteten finst.
- **Test.** Føreseiing (vii) krev at dei tre inngrepa er uttømmande. Eit tilfelle der svikten vert retta av betre estimat åleine, viser at dei ikkje er det.
- **Minste retting.** Føreordet: «det som fell utanfor haldet, deler seg».

#### 5.4 [d] og kortversjonen (P2)
Substratet er «agent av nullte orden» i hermeteikn i 5.4, og notat 5.4 seier at rein materiell motstand fell utanfor agensdefinisjonen. Kortversjonen skriv utan atterhald at substratet «er ein agent av nullte orden». Det motseier 5.11 [d] og 5.1111. Retting i kortversjonen: «grensetilfelle, ikkje ein agent etter definisjonen».

#### 5.72 [t] og føreordet (P2)
Føreordet kallar dei tidlegare delteoriane «degenererte spesialtilfelle av modellen». Notat 5.72 seier at binær vekting «ikkje er ei utleiing av heile C–K-teorien». Tilfelle (i) og (iii) er reelle grensetilfelle. (ii) og (iv) er tolkingar. Føreordet seier meir enn notatet. Retting: «grensetilfella isolerer det kvar tradisjon held fast».

#### 5.702 [d], 5.711 [t] (stadfesta, med merknad)
Er \(\mu_{SG}\) den reversible fordelinga til forslaga, slik 5.711 seier, er \(r_A=1\) i begge tilfella i 5.702; skiljet mellom «direkte» og «reversibel» utforsking har då innhald berre når \(\mu_{SG}\) er gjeven på anna vis. Med \(r_A=1\) og skeive forslag er den stasjonære fordelinga ikkje Gibbs-forma (rekna: avvik 0,12). Notat 5.7 seier dette. Følgja er at heile 6.67–6.76 gjeld berre den reversible søkjekjernen.

#### Mindre merknader i del 5 (P3)
- **5.028 [t]**: «Biletet følgjer det det er bilete av» set ei retning 5.0281 [o] ikkje kan bere; observasjonen er samvariasjon (notat 5.0281 vedgår det). Setninga er postulatet 1.23 sagt om att.
- **5.026 [t]**: at fleire sjølv deler éi verd, følgjer av 1.24, ikkje av at dei har eit felles ytre.
- **5.132 [t]**, **5.15 [d]**, **5.152 [d]**: tre ulike kjenneteikn på kompetanse. Ein agent i eit landskap med éin dal kan ha høg \(\nu\) utan å kunne gå oppover.
- **5.4011 [t]**: «strukturparametrar» og «funksjonsparametrar» er ikkje innførte før dei vert brukte.
- **5.5102 [t]**: læringsomgrepet i 5.51 er definert substratuavhengig. At det held frå celle til vitskap, er då ein eigenskap ved definisjonen. Bør vere `i` eller strykast.
- **5.52 [t]**: læring som berre rettar estimatet, endrar ikkje \(\kappa\) slik 5.21 definerer han. «Læring kan endre».
- **5.5212 [t]**: at handlag forvitrar under ei einsidig lære, er ein empirisk hypotese. Bør vere `a`.
- **5.6 [d]**: definisjonen manglar stoffskifte og formeiring og femner difor ein organisasjon som held seg sjølv ved like. Notat 5.6 vedgår at han ikkje er biologisk semje. Følgja bør seiast eller avgrensast.
- **5.118 [t]** er ei fastsetjing; 1.5 nyttar «agent» før 5.11 definerer ordet.

---

## 6. Del 6: fordeling, detaljert balanse, kovarians og omsorg (112)

**Samla vurdering.** Dette er den sterkaste delen matematisk. 6.64, 6.673, 6.674, 6.6741, 6.711, 6.731, 6.741 og 6.754 er stadfesta numerisk. Funna gjeld overgangen frå likning til ord. Notata er ofte meir presise enn proposisjonane; i fire tilfelle seier proposisjonen noko notatet ikkje dekkjer eller motseier.

#### 6.76 [t] (P1-a)
- **Svikt.** «Viss og berre viss han sjølv har innverknad, eller ...». Etter 6.702 er eigenleddet \(w_B(1-\gamma_B)\omega_j(B)\). 6.701 tillèt \(\gamma_B=1\). Då har B innverknad, og målet hans har inga vekt. Notat 6.73 gjev same svar: B tel med \(\sum_A w_A\chi_{AB}\), og \(\chi_{AB}=0\) når \(\gamma_B=1\).
- **Test.** To agentar, \(w_B=1\), \(\gamma_B=1\), \(c_{BA}=1\), \(\gamma_A=0\). Rekna: vekta på B sine eigne mål er 0.
- **Minste retting (i patch).** «... har innverknad og held målet som sitt eige, eller det går ein veg av omsorg til målet frå nokon som har innverknad.» Formelt: \(w_B>0\), \(\gamma_B<1\) og \(\omega_j(B)>0\).

#### 6.614 [t] mot 5.711 [t] (P1-b)
- **Svikt.** Formelen er rett. Orda «avheng ikkje av kva andre former som finst» er det ikkje, for \(\mu_{SG}\) står i formelen, og etter 5.711 er \(\mu_{SG}(x)\propto N(x)\), talet på opne steg frå \(x\). Eit nytt alternativ ved sida av \(x\) aukar \(N(x)\). Prøva i siste setning ville då felle modellen på noko modellen sjølv føreseier. Notat 6.614 nemner valaksiomet, men ikkje dette.
- **Test.** Kjeda x–y: \(N(x)=N(y)=1\). Legg til z ved x: \(N(x)=2\). Forholdet \(P(x)/P(y)\) doblar seg med uendra \(\Phi\). Rekna.
- **Minste retting (i patch).** «Ved fast grunnfordeling avheng forholdet ...» og «... utan å endre grunnvektene deira, held ikkje modellen.» Same retting trengst i føreseiing (i) i kortversjonen og i notat 7.174.

#### 6.673 [t], 6.674 [t], 6.71 [t], 6.711 [t], 7.1521 [t] (P1-c)
- **Svikt.** Identitetane er rette for ei fri vekt. Men 6.61 normaliserer omhugsvektene til 1, og 6.701 skalerer eigne omsyn med \(1-\gamma_A\). Innanfor desse definisjonane kan ein agent ikkje prioritere eitt omsyn meir utan å prioritere eit anna mindre. Då held ikkje dei verbale slutningane. Notat 6.673 og 6.71 seier dette, men proposisjonane og føreordet («vil meir omhug ... systematisk auke skaden») seier «meir prioritering» og «meir omsorg» utan atterhaldet.
- **Test 1.** \(\hat e_k=(0,1)\), \(\hat e_m=(0,2)\), \(\beta=2\). Flytt omhug frå m til k (0,2 til 0,8). \(\mathbb E[\hat e_k]\) stig frå 0,027 til 0,083. Det motseier «meir prioritering kan ikkje auke det estimerte avviket langs same omsyn» slik setninga står.
- **Test 2.** Biletet er feilfritt og svarkurva stigande: \(e_B=\hat\Lambda_{A|B}=(0,1,2)\), eigne omsyn \(\Phi^0_A=(0,5,10)\). Auk \(\gamma_A\) frå 0,2 til 0,8. \(\mathbb E[e_B]\) stig frå 0,015 til 0,184. Meir omsorg med rett bilete skadar den andre, fordi det agenten gav opp, verna betre. Svarkurva flyttar seg òg under denne endringa (rekna).
- **Minste retting (i patch for 6.673).** «Meir fri vekt kan ikkje auke ...», same ordbruk som 7.153 alt har. For 6.674, 6.711 og 7.1521 er minste retting å setje «fri» framfor «prioritering» og «omsorg»; dette er ikkje teke med i patchen fordi det rører formuleringar forfattaren bør velje sjølv.

#### 6.72 [t] (P1-d)
- **Svikt.** Proposisjonen seier «skade». Notat 6.72 seier at optimaliteten «gjeld estimata; for dei faktiske avvika gjeld ho berre så langt estimata ordnar formene rett». Proposisjonen motseier dermed 6.674 og 7.11.
- **Test.** To former, \(\hat e_B=(0,1)\), \(e_B=(1,0)\), ingen andre bryr seg, \(\beta=50\). Målet har vekt, ingen vinn på skaden, og det faktiske avviket er 1,0000.
- **Minste retting (i patch).** «... står estimert skade som ingen vinn på ...». Vilkåret om at det betre alternativet ligg i \(D\), står i notatet.

#### 6.63 [t] og føreordet (P2)
- **Svikt.** \((\mu_{SG},\Phi)\) og \((\mu_{SG}e^{\beta g},\Phi+g)\) gjev same fordeling (rekna). Utfalla åleine kan difor ikkje seie om feilen ligg i grunnfordelinga eller vurderinga. Notat 6.6731 seier dette for vektene. Når ei samla føreseiing slår feil, veit ein at konjunksjonen fall. Føreordet lovar at forklaringa kan «rettast nøyaktig der slutninga sviktar».
- **Test.** Kvart ledd må ha si eiga prøve: \(\mu_{SG}\) ved \(\beta=0\), estimata ved direkte utspørjing, kapasiteten ved forstyrring.
- **Minste retting.** 6.63: «... og vert kvart ledd prøvd for seg, kan ein feil finnast i eitt ledd.»

#### 6.633 [t] mot 5.7 [a] og føreseiing (v) (P2)
- **Svikt.** Samrøystes godkjenning gjev rett stasjonær fordeling (rekna, og notat 6.633 gjev vilkåra). Men aksepten er eit produkt av minimum, ikkje minimumet i 5.7. Med \(\Delta\Phi_1=+1\), \(\Delta\Phi_2=-1\) er samla skilnad 0 og aksepten 0,368, ikkje 1. For ein samansett agent fell aksepten difor ikkje «eksponentielt med den estimerte skilnaden», og opphaldstida i 6.642 vert lengre enn \(e^{\beta h}\) tilseier.
- **Test.** Mål aksept for forslag der agentane er usamde, men summen er null.
- **Minste retting.** Avgrens føreseiing (v) til éin agent, eller før opp produktforma som eiga føreseiing.

#### 6.1231 [t], 7.28 [t] mot 6.123 [d], 6.111 [a], 6.751 [t] (P2)
- **Svikt.** 6.123 definerer éin agent ved 5.11 åleine. 6.1231 seier at delt spenning er nødvendig. Men 6.111 og 6.751 skildrar ein heilskap som held seg ved styring, utan at avviket vert delt «utan merke om kven det høyrer til». Ein slik heilskap oppfyller 5.11. Nødvendet er altså postulatet i 6.12 (notat 6.12: «teksten si presisering»), ikkje ei følgje. 7.28 arvar veikskapen.
- **Test.** Ein kommandostyrt organisasjon som held eit mål under forstyrring, er éin agent etter 6.123 og ikkje etter 6.1231.
- **Minste retting.** 6.1231 til `a`, eller legg kravet inn i 6.123.

#### 6.672 [t], 6.6722 [t] (P3)
Skalarforma i 6.672 er ei nedre grense når krumminga har kryssledd: med \(H_{12}=0{,}8\) er variansen 2,78, ikkje 1 (rekna). Likskapsteiknet i 6.6722 held på eit vidt, fint rom; med grove steg gav rekninga 1,45 og med avkorta rom 0,75 mot formelen sin 2. 6.62 føreset endeleg \(D\). Notata nemner vilkåra; teiknet bør vere \(\approx\).

#### 6.02 [d], 6.022 [t], 6.1214 [t], 7.2 [t] (P3)
6.02 er ein normativ definisjon: den som formgjev utan omsorg, er ikkje designar. Teksten er open om det (6.023). Men 6.1214 skil omsorg, der agenten veit kven avviket høyrer til, frå delt spenning utan adresse, og cella i 6.022 er døme på det siste. 7.2 definerer designhandlinga utan omsorgsvilkåret. Retting: sei i 6.02 om delt spenning oppfyller kriteriet.

#### Mindre merknader i del 6 (P3)
- **6.732 [t]**: to som berre vil det den andre vil, har ei *ubestemt* vurdering, ikkje ingen. Kortversjonen og notat 6.741 seier det rett.
- **6.112 [t]**: «difor» følgjer av 6.111 [a], ikkje av første setning.
- **6.704 [t]**: vala fastset berre produktet \(\beta w_A c\) (notat 6.704), og bruk kan ikkje skiljast frå omsorg når biletet fell saman med eit eige omsyn. 5.283 gjev prøva i ord; ho bør inn her.
- **6.74 [t]**: held ved felles grunnfordeling. Notatet har det viktige atterhaldet at prøva berre kan avkrefte.
- **6.752 [o]**: kjeldene er ikkje kontrollerte.

**Utan merknad:** 6.602, 6.612, 6.62, 6.64, 6.641, 6.6411, 6.642, 6.65, 6.6711, 6.6731, 6.6741, 6.6742, 6.675, 6.702, 6.714, 6.73, 6.731, 6.741 og 6.754 held slik dei står, med vilkåra i notata.

---

## 7. Del 7: sviktsignatur, falsifikasjon og sjølvbruk (53)

#### 7 [t], 7.24 [t] mot 7.02 [t], 7.11 [t], 6.671 [t] (P1-g)
- **Svikt.** «Forma viser kor langt omhugen rakk» og «Kor mykje den andre talde, viser forma». Men 7.02 seier at fire ulike vegar kan ende i same form og at forma viser omhugen «først når ho vert lesen saman med forløpet». 7.11 seier at «forma åleine skil dei ikkje». 6.671 seier at eit omsyn utan vekt kan få godt utfall, og 6.674 at eit omsyn med vekt kan få dårleg. Hovudtesen og 7.24 er difor ikkje følgjer; dei vert motsagde av underproposisjonane sine.
- **Test.** Lag to prosessar med same fordeling over former: éin der målet har vekt og estimatet er rett, og éin der målet ikkje har vekt, men estimatet fell saman med eit anna vekta omsyn (6.6731). Forma skil dei ikkje.
- **Minste retting.** 7.24: «... viser forma først når ho vert lesen saman med forløpet.» For 7 må forfattaren velje; «Forma ber spor etter kor langt omhugen rakk» held.

#### 7.1 [a] mot 6.671 [t], 7.013 [d] (P2)
- **Svikt.** Utelatingar gjev systematiske feil berre der omsynet òg er uverna. 7.013 og føreseiing (vi) seier det rett; 7.1 har ikkje vilkåret.
- **Test.** Føreseiing (vi) slik ho står.
- **Minste retting.** «... under dei trykka som vart utelatne og ikkje verna på anna vis.»

#### 7.152 [d], 7.1521 [t] og observasjonsgrunnlaget (P2)
- **Svikt.** \(R_k\) og kovariansane er tekne over \(P\), ei fordeling over mange val under faste vilkår. Ei einskild designavgjerd gjev eitt trekk. Føreseiingane (ii), (iii) og (vi) krev difor populasjonar av jamførbare avgjerder med same \(D\), same agentar og same estimat. Kvar slike finst, seier teksten ikkje.
- **Test.** Namngje eitt datasett der vilkåra i notat 6.673 held.
- **Minste retting.** Legg kravet til 7.151.

#### 7.171 [a], 7.172 [d], 7.173 [d], 7.174 [d] (P2)
- **Svikt.** Alt kvantitativt er hjelpehypotesar. Den harde kjernen er eit sett skilje. Skilje kan vere ufruktbare, men ikkje falske. Kravet i føreordet om å «seie kva røynsle som kan felle påstandane» er dermed oppfylt for hjelpehypotesane og ikkje for kjernen, og 7.173 seier ikkje kor mange tap som feller han. Det er i samsvar med kjelda teksten nyttar for omgrepet (notat 7.17), men svakare enn føreordet lovar.
- **Vidare.** Registeret (notat 7.174) har tolv føreseiingar og ingen utfall. Etter 7.153 har læra då «ikkje vist forklaringsarbeidet sitt» enno. Notatet til føreordet seier det same. Det bør stå i sjølve teksten.
- **Minste retting.** Éi setning i 7.174: ingen av føreseiingane er prøvde per denne utgåva.

#### 7.15 [t] (P3)
«Ein teori som ikkje føreseier sviktsignaturen, forklarer ikkje form» er eit normativt krav til forklaring. Bør vere `d` eller `a`.

#### 7.142 [i] (P3)
Påstanden om nedbrytingstida til plast er ikkje kontrollert mot kjelda. Som illustrasjon ber han inga slutning.

**Utan merknad:** 7.141 og reknestykket i 7.142 (\(\rho=8\)) er rette. 7.1521 er rett som identitet (sjå P1-c for ordlyden). 7.153, 7.273 og 7.274 er gode prøvekrav. 7.3 og 7.31 inviterer til nett denne typen retting.

---

## 8. Tverrgåande: typebruk, føreord og kortversjon

**Typen `t`.** Lesekoden seier at ei følgje «står og fell med premissane sine». Av dei 313 `t`-proposisjonane fann eg fire slag: (a) utfalding av ein definisjon, (b) matematiske følgjer under oppgjevne vilkår, (c) følgjer av eit postulat, og (d) påstandar utan premiss i teksten. Slag (d) er dei som er lista under «typebruk» i kvart kapittel: 1.243, 1.245, 1.411, 2.21, 3.302, 3.303, 4.12, 5.5102, 5.5212, 6.1231 og 7.15. Eg har ikkje ført ei fullstendig klassifisering av alle 313.

**Føreordet.** Tre påstandar er sterkare enn proposisjonane og notata:
1. At det akademiske designfaget ikkje har etablert noko forskingsprogram. Teksten byggjer sjølv på formgrammatikk og tanke-kunnskapsteori, som er formelle program frå designforskinga. Notatet til føreordet seier at tilvisingane «ikkje [viser] at det er bevist at ingen samlande teori finst». Føreordet bør seie det same.
2. «Degenererte spesialtilfelle» (sjå 5.72).
3. «Rettast nøyaktig der slutninga sviktar» (sjå 6.63).

Påstandane om namngjevne forskarar og jamføringa med raseantropologien er ikkje kontrollerte mot kjeldene. Dei bør kontrollerast av nokon som har lese dei, sidan dei gjeld personar.

**Kortversjonen.** Tre stader avvik frå hovudteksten: «agent av nullte orden» utan atterhald, «materiell (ontologisk) deling», og føreseiing (i) utan vilkåret om fast grunnfordeling.

---

## 9. Rettingar og testar

**Ingen endring er gjord i `formlaere.tex`.** Grunnen er at kjeldehashen omfattar manuskriptet, og `make check-generated` avviser ei tekstendring utan ny PDF. XeLaTeX og Pandoc finst ikkje i køyremiljøet, så PDF-en kunne ikkje byggjast på nytt. Ei endring i manuskriptet ville difor ha brote kontrollen i `formlaere.yml`.

I staden ligg dei fire sikre rettingane som eiga fil:

- `revisjon/framlegg-rettingar-2026-11.patch`: fem linebyte i 6.614 (to), 6.673, 6.72 og 6.76. Kontrollert: `git apply --check` godtek patchen mot rein kjelde, og parseren i `scripts/content.py` les det retta manuskriptet utan feil. Etter `git apply` må `make all` køyrast og `pdf/` leggjast i same commit. Kortversjonen og notat 7.174 må følgje 6.614 for hand.
- `revisjon/kontrollrekning-2026-11.py`: kontrollrekninga. `python3 revisjon/kontrollrekning-2026-11.py` gjev 22 liner og avsluttar med kode 0.

Mappa `revisjon/` inngår ikkje i kjeldehashen (`input_manifest` i `scripts/content.py` les berre `scripts/`, `layout/`, `nettstad/` og dei kanoniske filene).

**Testar som vart køyrde:**

| Kommando | Utfall |
| --- | --- |
| `python3 revisjon/kontrollrekning-2026-11.py` | 22 av 22 som venta |
| `make check` (72 Python-testar) | 70 greidde, 1 hoppa over, 1 feil: `test_native_formula_and_edit_reach_mathml_and_pdf_from_same_source` stoppar på at `pandoc` manglar. Feilen kjem av miljøet, ikkje av endringane her. |
| `node --test tests/*.mjs` | Køyrde, men gav ingen lesbar oppsummering. Rekn dei som ikkje kontrollerte. |
| `make all`, `make check-generated` | Ikkje køyrde. XeLaTeX og Pandoc manglar. |

Python-avhengnadene i `requirements-build.txt` vart installerte utan feilmelding. Miljøet har Python 3.14, medan README krev 3.12.

**Grein og PR.** Arbeidet ligg på `claude/issue-25-43766813182`. PR kan opprettast frå
`https://github.com/lukketsvane/FORML-RE/compare/main...claude/issue-25-43766813182?expand=1`.
Eg har ikkje oppretta eller slått saman nokon PR.

---

## 10. Dekningsoversikt

Lista er laga maskinelt frå manuskriptet. «Med merknad» er proposisjonar som er nemnde med nummer og type i kapitla over. «Lesne utan merknad» er lesne og vurderte utan at eg fann noko å føre opp. Ingen proposisjon er hoppa over.

| Del | Proposisjonar | d | a | t | o | i | Med merknad | Lesne utan merknad |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 118 | 38 | 11 | 61 | 3 | 5 | 51 | 67 |
| 2 | 27 | 3 | 5 | 16 | 2 | 1 | 7 | 20 |
| 3 | 20 | 4 | 3 | 12 | 1 | 0 | 6 | 14 |
| 4 | 16 | 0 | 2 | 12 | 2 | 0 | 3 | 13 |
| 5 | 145 | 32 | 10 | 86 | 9 | 8 | 26 | 119 |
| 6 | 112 | 10 | 8 | 88 | 4 | 2 | 28 | 84 |
| 7 | 53 | 10 | 3 | 38 | 0 | 2 | 16 | 37 |
| **Sum** | **491** | 97 | 42 | 313 | 21 | 18 | **137** | **354** |

Proposisjonane 1.23–1.246 er merkte samla (sjå kapittel 1).

**Del 1 (118).**

Med merknad (51): 1 [d], 1.012 [o], 1.0121 [t], 1.12 [t], 1.212 [d], 1.2122 [t], 1.222 [a], 1.23 [a], 1.231 [d], 1.2311 [t], 1.232 [o], 1.2321 [t], 1.233 [d], 1.2331 [o], 1.2332 [d], 1.2333 [a], 1.234 [a], 1.2341 [a], 1.2342 [t], 1.2343 [t], 1.235 [d], 1.2351 [t], 1.2352 [t], 1.2353 [t], 1.2354 [t], 1.24 [a], 1.2401 [t], 1.241 [a], 1.242 [t], 1.243 [t], 1.244 [t], 1.245 [t], 1.2451 [t], 1.2452 [d], 1.2453 [d], 1.246 [t], 1.31 [d], 1.32 [d], 1.4 [d], 1.41 [d], 1.411 [t], 1.42 [d], 1.4311 [t], 1.432 [d], 1.5 [d], 1.52 [t], 1.53 [t], 1.54 [t], 1.541 [t], 1.62 [d], 1.622 [d].

Lesne utan merknad (67): 1.01 [d], 1.011 [t], 1.0111 [i], 1.02 [d], 1.021 [t], 1.0211 [i], 1.1 [a], 1.11 [d], 1.111 [i], 1.13 [d], 1.131 [t], 1.2 [d], 1.201 [t], 1.2011 [i], 1.202 [a], 1.2021 [t], 1.2022 [a], 1.203 [d], 1.2031 [t], 1.204 [t], 1.21 [d], 1.211 [i], 1.2121 [t], 1.2123 [t], 1.2124 [t], 1.22 [d], 1.221 [t], 1.2221 [t], 1.2222 [t], 1.223 [t], 1.2231 [t], 1.2232 [t], 1.3 [d], 1.311 [t], 1.321 [t], 1.3211 [t], 1.322 [t], 1.3221 [t], 1.323 [t], 1.324 [d], 1.412 [a], 1.413 [d], 1.421 [t], 1.422 [t], 1.43 [d], 1.431 [d], 1.4321 [t], 1.501 [d], 1.502 [d], 1.503 [t], 1.51 [t], 1.511 [t], 1.512 [t], 1.521 [t], 1.522 [t], 1.531 [t], 1.5311 [d], 1.55 [d], 1.6 [d], 1.61 [d], 1.6101 [d], 1.6102 [d], 1.6103 [t], 1.611 [t], 1.621 [t], 1.63 [t], 1.631 [t].

**Del 2 (27).**

Med merknad (7): 2 [a], 2.13 [a], 2.131 [t], 2.141 [t], 2.201 [o], 2.202 [a], 2.21 [t].

Lesne utan merknad (20): 2.01 [t], 2.011 [o], 2.02 [t], 2.021 [t], 2.1 [d], 2.101 [t], 2.102 [t], 2.11 [t], 2.111 [t], 2.112 [a], 2.12 [a], 2.121 [t], 2.122 [t], 2.1311 [t], 2.14 [d], 2.15 [t], 2.2 [d], 2.2011 [i], 2.2021 [t], 2.211 [t].

**Del 3 (20).**

Med merknad (6): 3.01 [a], 3.1 [d], 3.12 [a], 3.302 [t], 3.303 [t], 3.41 [t].

Lesne utan merknad (14): 3 [t], 3.101 [t], 3.102 [o], 3.11 [t], 3.121 [d], 3.122 [t], 3.2 [t], 3.21 [t], 3.3 [d], 3.301 [t], 3.31 [t], 3.4 [a], 3.401 [t], 3.411 [d].

**Del 4 (16).**

Med merknad (3): 4.12 [t], 4.33 [t], 4.41 [t].

Lesne utan merknad (13): 4 [a], 4.01 [t], 4.1 [a], 4.101 [t], 4.11 [o], 4.2 [o], 4.21 [t], 4.3 [t], 4.31 [t], 4.32 [t], 4.4 [t], 4.5 [t], 4.51 [t].

**Del 5 (145).**

Med merknad (26): 5.026 [t], 5.028 [t], 5.0281 [o], 5.11 [d], 5.118 [t], 5.1301 [t], 5.132 [t], 5.15 [d], 5.152 [d], 5.232 [d], 5.4 [d], 5.4011 [t], 5.5102 [t], 5.52 [t], 5.521 [t], 5.5212 [t], 5.6 [d], 5.7 [a], 5.702 [d], 5.711 [t], 5.72 [t], 5.721 [t], 5.7231 [a], 5.72311 [t], 5.72312 [t], 5.724 [t].

Lesne utan merknad (119): 5 [a], 5.01 [t], 5.011 [t], 5.012 [o], 5.013 [t], 5.02 [d], 5.0201 [t], 5.021 [d], 5.022 [d], 5.0221 [o], 5.0222 [t], 5.023 [t], 5.024 [a], 5.025 [t], 5.0251 [t], 5.027 [t], 5.1 [a], 5.1101 [d], 5.1102 [d], 5.1103 [d], 5.1104 [t], 5.1105 [o], 5.111 [t], 5.1111 [i], 5.112 [t], 5.113 [t], 5.1131 [i], 5.114 [d], 5.1141 [a], 5.1142 [t], 5.1143 [d], 5.1144 [t], 5.115 [t], 5.116 [t], 5.117 [t], 5.12 [o], 5.121 [i], 5.122 [i], 5.123 [i], 5.124 [i], 5.125 [i], 5.13 [a], 5.131 [t], 5.14 [d], 5.141 [t], 5.142 [t], 5.143 [t], 5.144 [a], 5.1441 [o], 5.151 [t], 5.153 [t], 5.2 [d], 5.2001 [d], 5.201 [t], 5.21 [d], 5.2101 [d], 5.2102 [t], 5.2103 [t], 5.211 [t], 5.22 [d], 5.2201 [d], 5.221 [i], 5.222 [t], 5.223 [t], 5.2231 [t], 5.23 [t], 5.231 [d], 5.2311 [d], 5.2312 [d], 5.2321 [t], 5.2322 [t], 5.233 [t], 5.234 [t], 5.24 [t], 5.241 [t], 5.25 [t], 5.26 [t], 5.261 [t], 5.2611 [t], 5.2612 [t], 5.262 [t], 5.263 [t], 5.27 [d], 5.271 [t], 5.272 [t], 5.28 [d], 5.281 [t], 5.282 [d], 5.283 [t], 5.284 [t], 5.285 [t], 5.3 [t], 5.301 [t], 5.31 [t], 5.32 [t], 5.401 [o], 5.402 [t], 5.403 [t], 5.5 [o], 5.51 [d], 5.5101 [o], 5.511 [t], 5.5211 [t], 5.53 [t], 5.61 [t], 5.62 [t], 5.63 [d], 5.631 [t], 5.632 [t], 5.6321 [t], 5.64 [t], 5.641 [a], 5.701 [d], 5.703 [t], 5.704 [t], 5.71 [d], 5.722 [a], 5.7221 [t], 5.723 [t].

**Del 6 (112).**

Med merknad (28): 6.02 [d], 6.022 [t], 6.111 [a], 6.112 [t], 6.1214 [t], 6.123 [d], 6.1231 [t], 6.13 [t], 6.6 [a], 6.613 [t], 6.614 [t], 6.63 [t], 6.633 [t], 6.64 [t], 6.671 [t], 6.672 [t], 6.6722 [t], 6.673 [t], 6.674 [t], 6.704 [t], 6.71 [t], 6.711 [t], 6.72 [t], 6.732 [t], 6.74 [t], 6.751 [t], 6.752 [o], 6.76 [t].

Lesne utan merknad (84): 6 [t], 6.001 [t], 6.002 [t], 6.003 [t], 6.01 [d], 6.0201 [t], 6.021 [t], 6.0211 [t], 6.023 [t], 6.0231 [t], 6.024 [t], 6.025 [t], 6.026 [t], 6.027 [t], 6.1 [a], 6.11 [a], 6.1111 [t], 6.113 [t], 6.114 [t], 6.12 [a], 6.121 [d], 6.1211 [t], 6.1212 [t], 6.1213 [t], 6.122 [a], 6.1221 [t], 6.131 [o], 6.132 [t], 6.1321 [t], 6.1322 [t], 6.14 [t], 6.2 [o], 6.201 [t], 6.21 [o], 6.211 [t], 6.3 [t], 6.31 [t], 6.311 [t], 6.312 [t], 6.32 [t], 6.4 [t], 6.5 [t], 6.51 [t], 6.511 [t], 6.5111 [t], 6.601 [d], 6.602 [t], 6.61 [d], 6.6101 [d], 6.611 [t], 6.612 [t], 6.62 [t], 6.631 [t], 6.632 [t], 6.641 [t], 6.6411 [t], 6.642 [t], 6.65 [t], 6.66 [t], 6.661 [t], 6.67 [d], 6.6711 [t], 6.6721 [i], 6.6731 [t], 6.6741 [t], 6.6742 [t], 6.675 [t], 6.68 [t], 6.7 [t], 6.701 [d], 6.702 [d], 6.703 [t], 6.712 [t], 6.713 [t], 6.7131 [i], 6.714 [t], 6.73 [t], 6.731 [t], 6.741 [t], 6.742 [t], 6.75 [t], 6.753 [a], 6.754 [t], 6.755 [a].

**Del 7 (53).**

Med merknad (16): 7 [t], 7.013 [d], 7.02 [t], 7.1 [a], 7.11 [t], 7.142 [i], 7.15 [t], 7.152 [d], 7.1521 [t], 7.171 [a], 7.172 [d], 7.173 [d], 7.174 [d], 7.2 [t], 7.24 [t], 7.28 [t].

Lesne utan merknad (37): 7.01 [t], 7.011 [d], 7.012 [t], 7.021 [t], 7.03 [t], 7.031 [t], 7.04 [t], 7.041 [t], 7.12 [a], 7.13 [t], 7.14 [d], 7.141 [t], 7.143 [t], 7.144 [t], 7.151 [d], 7.153 [t], 7.16 [t], 7.17 [d], 7.201 [t], 7.21 [t], 7.211 [t], 7.22 [t], 7.23 [d], 7.241 [t], 7.25 [t], 7.26 [t], 7.27 [t], 7.271 [t], 7.272 [t], 7.273 [t], 7.274 [t], 7.275 [t], 7.3 [t], 7.31 [t], 7.32 [t], 7.33 [i], 7.34 [t].

---

## 11. Det som står att

1. Kjeldekontroll: ingen av dei 150 kjeldene er lesne. Det gjeld særleg dei 21 `o`-proposisjonane og påstandane om namngjevne forskarar i føreordet.
2. Dei 40 ulesne notata og 33 ulesne ordlisteoppslag.
3. Ei fullstendig, skriftleg klassifisering av alle 313 `t`-proposisjonar etter slaga i kapittel 8.
4. Den engelske utgåva, figurane og dei genererte utgåvene.
5. Byggjekontroll av patchen med XeLaTeX og Pandoc.
6. Empirisk prøving. Ingen av dei tolv føreseiingane er prøvde, korkje her eller, så langt eg kan sjå av manuskriptet og notata, andre stader i `traktat/`. Mappene `research/`, `data-descriptor/` og `foundational-paper/` i rota er ikkje opna.
