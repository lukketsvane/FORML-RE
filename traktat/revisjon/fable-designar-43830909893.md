# Fable 5.2: rekonstruksjon av hovudargumentet fram mot designaren

Modell: berre Fable 5.2, utan underagentar, utan skal. Einaste endra manuskriptfil: `traktat/tekst/formlaere.tex`. 22 proposisjonar har ny prosa: 5.703, 6.001, 6.01, 6.1, 6.14, 6.311, 6.713, 6.7131, 6.76, heile rekkja 6.8 til 6.87 (elleve proposisjonar), 7.012 og 7.2. Ingen adresse, status eller rekkjefølgje er rørt. Ingen av dei endra proposisjonane inneheld matematikk, og `\kjelder{}` står på same stad i dei fire som har det (6.01, 6.1, 6.14, 6.311). Føreord, etterord, notar, `kjelder.json`, testar og genererte filer er urørte.

**Ikkje kontrollert:** Eg hadde ikkje skal i denne køyringa. Ingen test og inga bygging er køyrd. Det eg har gjort i staden: lese testane (`test_designar_order.py`, `test_claim_consistency.py`, `test_autoresearch_004.py`) og kontrollert for hand at dei verna proposisjonane (6.614, 6.673, 6.674, 6.711, 6.72, 7.1521) er urørte, at ingen av dei gamle adressene 6.02 til 6.027 står i teksten, at «(6.8, 6.801)» står att i føreordet, og at prosaen ikkje har TeX-spesialteikn utanfor matematikk. PDF, HTML og kortversjon er ikkje bygde på nytt og viser gammal ordlyd til nokon køyrer `make all`.

## Diagnose

Flyttinga av designaren til slutten av del 6 gjorde definisjonen til konklusjon i komposisjonen, men ikkje i argumentet. Tre ting mangla:

1. **Definisjonen sa mindre enn føreordet og mindre enn følgja si.** Føreordet gjev tre vilkår under «(6.8, 6.801)»: endra vilkår, måla til den andre tekne inn, og arbeid som kan rettast. 6.8 hadde to. Det tredje stod i 6.801 med status t. Etter 5.281 og 6.701 har ein agent med omsorgsvekt og feil bilete omsorg i formell meining, så rettinga følgjer ikkje.
2. **Rekkja 6.81 til 6.87 var merknader, ikkje steg.** Kvar proposisjon var sann for seg, men ingen av dei viste kvifor kriteriet har dei ledda det har, eller kva som fell utanfor.
3. **Tre spørsmål låg samanfiltra heile vegen frå 5.7:** kven forma verkar på, kven sitt mål som har vekt i valet, og kven sitt svar som kan rette biletet. Teksten har alle tre (5.222, 6.702, 6.713), men skilde dei aldri uttrykkjeleg, og difor kunne «designar» ikkje stå som staden der dei møtest.

## To fullstendige argumentforløp

### K: konservativt forløp

Rekkja står som ho er, og berre kjernen vert reparert.

1. 5.7 til 5.724: éin agent vel steg etter vurderinga si; tre lag, tre ledd.
2. 6 til 6.14: fleire agentar, fleire skalaer; formgjevaren er aldri åleine.
3. 6.6 til 6.68: fordelinga; vekt gjev styrke, estimat gjev retning.
4. 6.7 til 6.76: omsorg gjev måla til andre vekt; vekta treng ein veg.
5. 6.8: designar er formgjevar med verknad, omsorg og, nytt, retting.
6. 6.801 til 6.87: som før, med eitt ledd lagt til i 6.82 og éi setning i 6.86.
7. 7: forma viser kor langt omhugen rakk.

Inngrep: fire til fem proposisjonar (6.8, 6.82, 6.01, 6.86, kanskje 6.84).

Kva K løyser: gapet 6.8/6.801 formelt, og det manglande vilkåret i 6.82.

Kva K ikkje løyser: rekkja etter 6.8 er framleis ei liste. Motdømet «verknad med måling, utan omsorg» (styring med tilbakemelding) er ikkje handsama. Det står ikkje om delt spenning oppfyller kriteriet (merknaden frå kritisk gransking 2026-11, P3). Skiljet mellom bestilling og svar kviler på kven som talar, ikkje på at bestillinga er gjeven før forma har verka, så tilfellet der brukaren sjølv bestiller det som skadar han, står ope. 6.14 seier at formgjevaren møter andre, men ikkje at det å møte dei er noko anna enn å ha måla deira. Del 7 tek ikkje imot omgrepet. 7.2 kallar framleis all vilkårsendring «designhandlinga» og motseier dermed 6.8.

### R: radikalt forløp (valt)

Eitt argument i tre trådar, som vert namngjevne der dei først kan skiljast, og samla i 6.8.

**Tråd 1, verknad: kven forma råkar.**
5.703 (ny setning): vurderinga tel berre aksane i lyskjegla; følgjene er ikkje avgrensa av henne. 6.001 (ny setning): den som skal leve med forma, treng ikkje vere nokon av dei tre som tenkjer, vil og maktar. 6.01: ein formgjevar kan ha berre eigne mål; forma vert like fullt vilkår for andre. 6.14: mange opphav seier ikkje kven forma er til for. 6.811 og 6.87: verknaden går vidare utan tilbakeføring og utanfor kriteriet. 7.01, 7.011: verknadskjegla.

**Tråd 2, vekt: kven sitt mål som tel.**
5.701 og 5.703: berre lyskjegla tel. 6.67 til 6.675: prioritering. 6.7 til 6.703: omsorg flyttar vekt. 6.76: vekt berre gjennom innverknad eller omsorgsveg, og (ny setning) vegen gjev vekt, ikkje retning.

**Tråd 3, svar: kven som kan rette.**
6.674: estimatet gjev retninga. 6.71 til 6.714: biletet, svarkurva; (ny i 6.713) svaret må gjelde det som faktisk held eller sviktar, og det den andre ventar, er òg eit bilete. 6.84 til 6.86: kva retting krev, kva som ber henne, og kva som ikkje er eit svar. 7.201, 7.25, 7.273.

**Samling.** 6.8 er ein tre-plassrelasjon (formgjevar, ein annan, eit omsyn) med tre namngjevne vilkår. Rekkja etter er eit argument for at definisjonen har rett tal ledd og rett omfang:

- 6.801: følgjer av indekseringa (ingen er designar utan vidare; same form, designar for éin og ikkje for ein annan; kriteriet krev ikkje at arbeidet lukkast).
- 6.81: verknad utan omsorg, også med måling, er bruk. Omsorga følgjer ikkje av dei to andre.
- 6.811: tilbakeføringa er ikkje gjeven med verknaden. Difor er retting eit eige vilkår og ikkje ein automatikk.
- 6.82: kriteriet er strukturelt og kan oppfyllast utan yrkesrolle; cella må oppfylle alle tre.
- 6.83, 6.831: grad, og korleis kvart vilkår kan prøvast.
- 6.84: verknad og omsorg utan retting kan ikkje utelukke formynderi. Rettinga følgjer ikkje av dei to andre.
- 6.85: delt spenning oppfyller omsorg og retting i eitt, men kriteriet krev ikkje så tett kopling.
- 6.86: bestillinga er eit bilete gjeve før forma; svaret kjem etter.
- 6.87: kriteriet avgrensar designaren, ikkje verknaden. Resten er det del 7 les.

Inngrep: 22 proposisjonar.

Kvifor R er valt: K tettar gapet ved å flytte eit ledd; R gjer i tillegg kvart ledd i definisjonen til enden på ein tråd lesaren alt har følgt, og gjev kvar proposisjon etter 6.8 ei oppgåve i argumentet. R legg ikkje til modellføresetnader. Kvar ny setning viser til ein proposisjon som alt står (5.22, 5.282, 5.284, 6.1213, 6.1214, 6.704, 6.71, 6.713, 6.714, 6.76, 3.401).

### S: strukturell plan, ikkje gjennomført

R er skriven inn i dei faste adressene. Eit endå reinare forløp krev flytting og statusendring og ligg utanfor vernet. Planen er ført her slik at han kan vurderast seinare. Ingenting av han står i manuskriptet.

| Ny adresse | Innhald | Frå |
| --- | --- | --- |
| 6.8 [d] | Kriteriet, tre vilkår | 6.8 |
| 6.801 [t] | Indeksering, ikkje krav om å lukkast | 6.801 |
| 6.81 [t] | Verknad utan omsorg: bruk | 6.81 |
| 6.811 [t] | Asymmetrien, inga tilbakeføring av seg sjølv | 6.811 |
| 6.82 [t] | Verknad og omsorg utan retting | 6.84 |
| 6.821 [t] | Kanalen over ei grense som står | 6.85 |
| 6.822 [t] | Bestilling er ikkje svar | 6.86, andre avsnitt |
| 6.83 [t] | Utanfor yrkesrolla: cella | 6.82 |
| 6.84 [t] | Grad og prøve | 6.83 |
| 6.841 [t] | Grad er ikkje rekkjevidd | 6.831 |
| 6.85 [t] | Resten: verknad utanfor kriteriet | 6.87 |
| 6.715 [t] | Teikn og protokoll | 6.86, første avsnitt |

Gevinst: dei tre «ikkje nok»-stega (verknad, omsorg, bestilling) står samla før omfang og grad, og teiknet vert innført saman med svaret i 6.71-rekkja. Følgjer som må gjerast i same vending: notane `prop-6-82` og `prop-6-811` i `kjelder.json`, tilvisinga «(6.81)» i noten til 6.751, «(6.83)» i føreordet, tilvisinga til 6.811 i siste proposisjon, `TAL`, `ADRESSE_SHA` og `FORDELING` i `test_autoresearch_004.py` (planen deler 6.86 i to, så talet vert 492 og del 6 får 113), teljinga i `test_claim_consistency.py`, `test_designar_order.py`, og utvalet i kortversjonen. Planen er ikkje validert mot byggjeprogrammet.

### Behaldne

**A. Kjernen og rekkja etter: 6.76 til 6.87**

Før (heile passasjen):

> **6.76** Målet til den andre har vekt i forma berre der han sjølv har innverknad, eller der det går ein veg av omsorg til han frå nokon som har.
>
> **6.8** Ein designar er ein formgjevar som endrar vilkåra ein annan agent navigerer under, og har omsorg for han.
>
> **6.801** Ingen er designar utan vidare. Den som er det, er det langs nokre omsyn og ikkje andre. Kriteriet krev eit arbeid som kan rettast av det som held eller sviktar hos den andre, ikkje at arbeidet alltid lukkast.
>
> **6.81** Verknad åleine er ikkje nok. Den som berre bruker avvika til den andre til å styre han mot eigne mål, formgjev vilkåra hans, men oppfyller ikkje designkriteriet langs dette omsynet.
>
> **6.811** Den som endrar vilkåra, treng ikkje bere følgjene eller gje den andre same moglegheit til å endre dei tilbake.
>
> **6.82** Designkriteriet gjeld også utanfor yrkesrolla. Ei celle som regulerer verksemda si etter mål-avviket hos ein nabo, oppfyller det langs dette omsynet.
>
> **6.83** Å vere designar er eit spørsmål om grad: kor mange aksar og kor mange andre lyskjegla femner. Profesjonen sjølv er designar berre langs dei aksane der kriteriet er oppfylt. Kva aksar det er, må han vise.
>
> **6.831** Kor mykje ein designar formgjev for, er ikkje kor langt omsorga hennar når i rom, men kor mange ulike målregionar til andre lyskjegla hennar femner.
>
> **6.84** Omsorg åleine er heller ikkje nok. Der biletet av den andre peikar feil, gjer sterkare omsorg avviket hans større i middel (6.71). Arbeidet må kunne rettast av eit svar ein ikkje alt har bestemt innhaldet i.
>
> **6.85** Observasjon og handling kan bere omsyn over ei grense utan å oppheve grensa mellom den som formgjev, og den som lever med forma.
>
> **6.86** Ein agent kan leggje spenninga si over på ein annan ved å omsetje henne til eit teikn den andre handlar på. Bestillinga er eit slikt teikn. Forma som svarar på henne, svarar på spenninga til bestillaren. Overføringa krev ein felles protokoll. Utan han er teiknet støy.
>
> **6.87** Formgjeving endrar vilkåra andre møter, også langs omsyn som låg utanfor lyskjegla til den som formgav. Asymmetrien i 6.811 gjeld difor òg følgjer ingen hadde som mål å skape.

Etter (heile passasjen):

> **6.76** Målet til den andre har vekt i forma berre der han sjølv har innverknad, eller der det går ein veg av omsorg til han frå nokon som har. Vegen gjev vekt, ikkje retning: i kvart ledd avgjer biletet kva veg vekta verkar (6.71).
>
> **6.8** Ein formgjevar er designar for ein annan agent, langs eit omsyn, når tre vilkår held.
> Verknad: forma endrar vilkåra den andre navigerer under.
> Omsorg: formgjevaren har teke avviket til den andre inn som mål (5.282).
> Retting: arbeidet kan rettast av det som held eller sviktar hos den andre.
>
> **6.801** Ingen er designar utan vidare. Den som er det, er det for nokon og langs noko, og kan vere det for éin utan å vere det for ein annan som den same forma råkar. Kriteriet krev eit arbeid som kan rettast, ikkje eit arbeid som alltid lukkast.
>
> **6.81** Verknad åleine er ikkje nok, heller ikkje når han vert målt. Den som måler avvika til den andre for å styre han mot eigne mål, formgjev vilkåra hans og rettar arbeidet etter målinga. Men avvika er då brukte, ikkje tekne inn som mål (5.282): det som vert retta, er middelet. Designkriteriet er ikkje oppfylt langs dette omsynet.
>
> **6.811** Den som endrar vilkåra, treng ikkje bere følgjene eller gje den andre same moglegheit til å endre dei tilbake. Det som sviktar hos den andre, vert difor ikkje ført tilbake til formgjevaren av seg sjølv (6.1213).
>
> **6.82** Kriteriet spør etter verknad, omsorg og retting, ikkje etter yrke, medvit eller intensjon. Det gjeld difor også utanfor yrkesrolla.
> Ei celle er designar for nabocella langs eit omsyn der alle tre held: verksemda hennar høyrer til vilkåra naboen svarar på, avviket hos naboen set arbeid i gang i henne, og koplinga fører tilbake om avviket fall. At cella regulerer etter avviket hos naboen, viser berre det andre. Om alle tre held i eit gjeve vev, må visast der.
>
> **6.83** Å vere designar er eit spørsmål om grad: for kor mange andre og langs kor mange omsyn dei tre vilkåra held. Yrkestittelen avgjer det ikkje.
> Profesjonen er designar berre der kriteriet er oppfylt, og kvar det er, må han vise: verknaden mot alternativa som stod opne, omsorga i val mellom former som berre skil seg i biletet av den andre (6.704), rettinga i at eit svar som går imot biletet, endrar arbeidet.
>
> **6.831** Graden følgjer ikkje rekkjevidda. Ei form kan nå mange og vere formgjeven for få. Det som tel, er ikkje kor langt omsorga til designaren når i rom, men kor mange ulike målregionar hos andre lyskjegla hennar femner, og kor fint svaret skil dei (6.714).
>
> **6.84** Verknad og omsorg er heller ikkje nok. Omsorga verkar gjennom biletet. Peikar biletet feil veg, vert avviket til den andre større i middel når biletet får meir fri vekt (6.71), og innanfrå er det ikkje til å sjå (6.713). Omsorg som ikkje kan rettast, kan difor ikkje utelukke at ho er formynderi (5.284).
> Rettinga krev eit svar ein ikkje alt har bestemt innhaldet i, og at svaret endrar arbeidet. (Formgjevaren i 6.7131 vert designar langs dette omsynet først med prøvesitjinga.)
>
> **6.85** Der spenninga er delt, er omsorg og retting gjevne med koplinga: avviket og tilbakeføringa kjem same vegen, utan adresse (6.1214). Kriteriet krev ikkje så tett ei kopling. Observasjon og handling kan bere omsyn og svar over ei grense utan å oppheve grensa mellom den som formgjev, og den som lever med forma. Då må kanalen byggjast og haldast: svaret kjem ikkje av seg sjølv (6.811).
>
> **6.86** Ein agent kan leggje spenninga si over på ein annan ved å omsetje henne til eit teikn den andre handlar på. Overføringa krev ein felles protokoll. Utan han er teiknet støy.
> Bestillinga er eit slikt teikn. Ho er gjeven før forma finst, og ber spenninga til bestillaren og det han ventar av forma. Svaret kjem etter forma og ber det som held eller sviktar hos den som lever med henne. Ei form kan difor oppfylle bestillinga utan at nokon har svart. Er bestillaren ein annan enn den som lever med forma, ber bestillinga måla til den siste berre så langt bestillaren har teke dei inn (6.76). Er dei den same, er bestillinga likevel eit bilete, gjeve før forma har verka (6.713).
>
> **6.87** Kriteriet avgrensar designaren, ikkje verknaden. Formgjeving endrar vilkåra òg for dei ingen tok inn og ingen spurde, og langs omsyn som låg utanfor lyskjegla til alle som formgav (5.703). Asymmetrien i 6.811 gjeld difor òg følgjer ingen hadde som mål å skape.

Kvifor dette heng betre saman:

- **Definisjonen ber no det følgja treng.** Rettinga er eit ledd i 6.8, ikkje ei følgje. 6.801 seier berre det som følgjer av at relasjonen har tre plassar og at tredje vilkår er «kan rettast». Ordlyden i 6.8 ligg tett på føreordet, som er verna og alt siterte tre vilkår.
- **Kvart vilkår er vist som uavhengig av dei to andre.** 6.81 held verknad og måling fast og tek bort omsorga. 6.84 held verknad og omsorg fast og tek bort rettinga. 6.87 held verknaden fast og tek bort begge. Det er dette som gjer rekkja til eit argument for definisjonen og ikkje ei liste under henne.
- **6.81 dekkjer eit motdøme den gamle ordlyden slapp gjennom.** Den som måler åtferda til brukaren og justerer etter henne, har både verknad og ei form for retting. Den gamle 6.81 sa «berre bruker», og ein lesar kunne svare at måling er meir enn bruk. No står det at det som vert retta, er middelet.
- **6.811 er ikkje lenger eit laust faktum.** Asymmetrien grunngjev kvifor retting må stå som eige vilkår: utan tilbakeføring (6.1213) kjem svikten ikkje attende.
- **6.84 er rett om fri vekt.** Den førre ordlyden («sterkare omsorg gjer avviket større») er den forma kritisk gransking felte i 6.711 (P1-c): ein auke i omsorgsdelen er ei flytting frå eigne omsyn, og forteiknet er då eit anna spørsmål. Ny ordlyd følgjer 6.71 og 6.711.
- **6.86 skil bestilling og svar på to aksar.** Kven (bestillaren eller den som lever med forma) og når (før forma finst, eller etter at ho har verka). Den andre aksen er ny og følgjer av tillegget i 6.713. Han dekkjer tilfellet der den som bestiller, er den som skal sitje: også då er bestillinga eit bilete.

**B. Opninga av del 6: 6.001, 6.01, 6.1, 6.14**

Før:

> **6.001** Den som tenkjer forma, den som vil ha henne, og den som maktar henne, treng ikkje vere same agent. Fleire agentar fører kvar sin politikk inn i same form [...]
>
> **6.01** [...] Cella, bia, treet, handverkaren og ingeniøren er formgjevarar. Definisjonen nemner ingen annan.
>
> **6.1** [...] Korleis kontrollen er fordelt, er eit spørsmål om verknad, ikkje berre om kor mange som var til stades. [...]
>
> **6.14** I samansett praksis verkar ingen formgjevar åleine. Han møter andre agentar som har eigne mål, og materielle prosessar utan mål. Kompetansen ligg ikkje i å late som om alle vil det same, men i å finne former som kan halde fleire omsyn under dei faktiske vilkåra.

Etter:

> **6.001** Den som tenkjer forma, den som vil ha henne, og den som maktar henne, treng ikkje vere same agent. Den som skal leve med henne, treng ikkje vere nokon av dei. Fleire agentar fører kvar sin politikk inn i same form [...]
>
> **6.01** [...] Cella, bia, treet, handverkaren og ingeniøren er formgjevarar. Ein formgjevar kan navigere etter berre eigne mål. Forma han realiserer, vert like fullt eit vilkår for andre (3.401).
>
> **6.1** [...] Korleis kontrollen er fordelt, er eit spørsmål om innverknad, ikkje berre om kor mange som var til stades. [...]
>
> **6.14** I samansett praksis verkar ingen formgjevar åleine. Han møter materielle prosessar utan mål og andre agentar med eigne. Kompetansen ligg ikkje i å late som om alle vil det same, men i å finne former som kan halde fleire omsyn under dei faktiske vilkåra.
> Å møte ein annan agent er ikkje å ha måla hans. Avviket hos den andre kan formgjevaren føreseie, bruke eller ta inn som mål (5.282). At mange har verka inn på ei form, seier difor ikkje kven ho er til for.

Grunn: dei tre rollene i 6.001 svarar til dei tre spørsmåla i 5.723 (fanst steget, var det tenkt, ville og makta nokon). Den fjerde rolla er den dei tre ledda ikkje dekkjer, og ho ber resten av del 6: 6.703, 6.76, 6.8, 7.211. I 6.01 er metasetninga bytt med to påstandar om saka: klassen rommar agentar med berre eigne mål, og forma verkar på andre uansett. Det er avstanden mellom dei to setningane som 6.8 seinare måler. I 6.1 er «verknad» bytt med «innverknad», som er ordet 6.601 og 6.76 bruker om vegen frå agent til form. «Verknad» er då fritt til vegen frå form til den andre (6.8, 7.011).

**C. Premissen i kjernelikninga: 5.703**

- Før: `Kjernelikninga føreseier ei fordeling over steg, ikkje følgja av dei.`
- Etter: `Kjernelikninga føreseier ei fordeling over steg, ikkje følgja av dei. Vurderinga tel berre aksane i lyskjegla til agenten; følgjene av steget er ikkje avgrensa av henne (5.22).`

Grunn: at summen i 5.701 berre går over lyskjegla, stod i indeksen og ingen annan stad. Det er premissen for både vekt-tråden og verknad-tråden. 6.87 viser no hit.

**D. Svaret: 6.713 og 6.7131**

- 6.713, tillegg: `Svaret må gjelde det som faktisk held eller sviktar. Det den andre ventar av ei form han ikkje har levd med, er òg eit bilete.`
- 6.7131: `Designaren ventar` er no `Formgjevaren ventar`.

Grunn: svarkurva er definert ved det faktiske avviket (6.711), så tillegget er ei utfalding, ikkje ein ny føresetnad. Det gjer skiljet i 6.86 utleidd. I 6.7131 stod «Designaren» før definisjonen, og etter den nye 6.8 er ordet dessutan feil for henne før prøvesitjinga. 6.84 hentar dømet inn att.

**E. Mottaket i del 7: 7.012 og 7.2**

- 7.012, tillegg: `Designkriteriet i 6.8 kan berre vere oppfylt der dei overlappar, og der berre så langt svaret rekk.`
- 7.2, før: `Designhandlinga endrar vilkåra ein annan agent navigerer under: [...]`
- 7.2, etter: `Ei realisert form endrar vilkåra ein annan agent navigerer under: [...] Det gjeld anten nokon var designar for han eller ikkje.`

Grunn: 7.012 set omgrepet frå 6.8 inn i dei to kjeglene del 7 arbeider med. 7.2 tilskreiv designhandlinga det som etter 6.87 gjeld all formgjeving; kritisk gransking peika på same motseiinga (P3).

**F. 6.311**

- Før: `Designaren som ignorerer grensesnittet, ignorerer agenten ho formgjev for.`
- Etter: `Den som formgjev for andre og ignorerer grensesnittet, ignorerer agenten ho formgjev for.`

Grunn: ordet stod før definisjonen, og ein designar etter 6.8 ignorerer per definisjon ikkje den andre langs omsynet. «Den som formgjev for andre» er uttrykket frå 5.125.

### Forkasta

- **Å halde 6.8 på to vilkår og utleie rettinga i 6.801.** Slutninga krev at «omsorg» gjeld det faktiske avviket. 5.281 seier det motsette: biletet er agenten sitt. Ei slik 6.801 ville framleis vere ei ikkje-utleidd følgje med status t.
- **6.8 som substantivdefinisjon utan indeks** («Ein designar er ein formgjevar som ...» med tre ledd). Då må 6.801 leggje til «for nokon og langs noko» som nytt innhald. Relasjonsforma gjev det i definisjonen.
- **Lang omskriving av 5.7 til 5.724.** Prøvd som spørsmål: kva manglar denne rekkja for at del 6 skal kunne byggje på henne? Svaret var éin premiss (lyskjegla avgrensar vurderinga, ikkje følgjene) og éi rolle (den som lever med forma). Resten ber alt: 5.723 stiller dei tre spørsmåla 6.001 fordeler på tre agentar. Ei lengre omskriving ville forklart strukturen med fleire ord.
- **Lang omskriving av 6.11 til 6.13.** Rekkja gjev dei tette utgåvene av dei tre vilkåra (styring i 6.111, delt spenning i 6.121, tilbakeføring i 6.1213). Det som mangla, var koplinga frå 6.8-rekkja attende hit. Ho står no i 6.811 og 6.85.
- **Vegvisar i 5.724** («Kjernelikninga gjeld éin agent ...»). Flat programerklæring; 6.001 gjer arbeidet.
- **Lyskjegle-setninga i 5.701.** Flytta til 5.703, som alt handlar om kva likninga ikkje seier.
- **«Verknaden går éin veg» som opning i 6.811.** For sterkt: 6.811 seier «treng ikkje», ikkje «kan ikkje».
- **«Der spenninga er heilt delt, finst ingen annan» i 6.85.** For sterkt og eit døme på poetisk trykk: to hinner står att. Erstatta med det 6.1214 faktisk seier.
- **«Omsorg utan svar kan ikkje skiljast frå formynderi» i 6.84.** Feil i éin retning: eit bilete kan peike feil fordi agenten tek feil av verda, ikkje av målet (5.284). Ny ordlyd: «kan ikkje utelukke».
- **«Det første vilkåret er oppfylt langt oftare enn dei to andre» i 7.2.** Empirisk påstand utan grunnlag i teksten.
- **6.752 som beleg for første vilkår i 6.82.** Observasjonen gjeld eitt forsøkssystem, og kjeldene er merkte som ikkje kontrollerte i kritisk gransking. 6.82 er no reint vilkårsbunden.
- **«føretaket» inn i lista i 6.01** for å svare til føreordet. Ordet ville kome under `\kjelder{22,40,41}`, som ikkje dekkjer det, og eit føretak som agent føreset 6.123.
- **«Å kunne rettast er å kunne ta feil» i 6.801.** Aforisme som ikkje legg noko til «ikkje eit arbeid som alltid lukkast».
- **Endring av 7.201, 7.21, 7.24 og 7.25.** Dei ber alt dei tre vilkåra i tur og orden (svar, omsorg, vekt, retting). Etter 7.012 og 7.2 treng dei ikkje meir.
- **Endring av 6.7, 6.703, 6.714, 6.4.** Lesne på nytt mot den nye rekkja; dei held.
- **«Viss og berre viss» i 6.76.** Ikkje sett inn att; `Omsorgsveg`-testane dokumenterer kvifor.
- **Omskriving av «meir omsorg» i 6.7131.** 6.71 kallar sjølv den frie vekta «styrken i omsorga», og illustrasjonen ber inga slutning. Sjå Uvisse 9.
- **Plan S.** Dokumentert over, ikkje gjennomført.

### Heilskap

Hovudargumentet kan no seiast i fem steg, og kvart steg har ei adresse:

1. Det som vert valt, vert valt etter vurderingar som berre tel det agentane har som mål (5.701, 5.703, 6.6).
2. Forma verkar på meir enn det, og på andre enn dei som valde (5.703, 6.001, 6.01, 7.01).
3. Målet til ein som ikkje har innverknad, har vekt berre gjennom omsorga til andre, og då som bilete (6.703, 6.76).
4. Om biletet peikar rett, kan ikkje avgjerast innanfrå; berre det som faktisk held eller sviktar hos den andre, kan vise det (6.71, 6.713).
5. Designar er formgjevaren der dei tre fell saman for ein bestemt annan langs eit bestemt omsyn (6.8). Alt anna forma gjer, er verknad utan designar (6.87), og det er det del 7 les.

**6.8 og 6.801.** Gapet er lukka ved å flytte rettinga inn i definisjonen. Det er ei stipulering, ikkje eit prov, og teksten gjev seg ikkje ut for noko anna: 6.8 har status d. Det som er argument, er at stipuleringa ikkje er vilkårleg: 6.84 viser at rettinga ikkje følgjer av dei to andre vilkåra, og at tilfellet utan henne er eit anna tilfelle (det kan vere formynderi og kan ikkje sjå det). 6.801 inneheld no berre det som følgjer. Eg vurderer dette som retta.

**6.82.** Cella må oppfylle alle tre vilkåra, og teksten seier kva kvart er i eit vev. Setninga «At cella regulerer etter avviket hos naboen, viser berre det andre» er svaret på spørsmålet om kva dømet viser. Dømet viser at kriteriet kan oppfyllast utan yrkesrolle, medvit eller intensjon. Det viser ikkje at celler er designarar; det må visast vev for vev. Noten til 6.82 (ikkje moralsk ansvar) høver framleis. Eg vurderer dette som retta, med atterhaldet i Uvisse 3.

**6.14.** Proposisjonen skil no mellom å møte ein annan agent og å ha måla hans, med 5.282 som grunn. Siste setning («seier difor ikkje kven ho er til for») er skiljet mellom det allment formgjevande systemet i 6.01 og 6.1 og den relasjonelle designaren i 6.8. Kompetansesetninga står uendra. Eg vurderer 6.14 som den viktigaste skøyten i opninga.

**6.76.** Proposisjonen var siste setning i del 6 og er no hengsla inn mot 6.8. Første setning er uendra og er framleis berre eit nødvendig vilkår. Tillegget («Vegen gjev vekt, ikkje retning») er 6.71 brukt på vegen, og det er grunnen til at 6.8 treng eit tredje vilkår. 6.76 har dermed mista sluttrytmen og fått ei oppgåve. Om det er eit godt byte, er eit lesarspørsmål.

**Delskifta.** Frå 5 til 6: 5.723 (tre spørsmål til éin agent) og 6.001 (tre roller, pluss den fjerde) heng no saman utan vegvisar, og 5.703 gjev grunnen til at den fjerde rolla finst. Frå 6 til 7: 6.87 sluttar med det kriteriet ikkje dekkjer, 7 seier at forma viser kor langt omhugen rakk, og 7.01 seier korleis. 6.87 og 7.01 overlappa før; no handlar 6.87 om kven (dei ingen tok inn og ingen spurde) og 7.01 om kva (heile ordninga). 7.012 og 7.2 tek omgrepet inn i del 7.

**Det som ikkje er løyst innanfor grensene.** Rekkjefølgja i 6.81 til 6.87 er ikkje den beste: dei to uavhengigheitsstega (6.81 og 6.84) står med tre proposisjonar mellom seg. Eg har skrive rekkja i tre grupper (6.81 til 6.82 om verknad og omsorg, 6.83 til 6.831 om grad, 6.84 til 6.87 om svaret og resten), og det ber, men plan S ville vore reinare. Statusen til 6.1231 (kritisk gransking, P2) er urørt.

### Uvisse

1. **Ingen test er køyrd.** Sjå øvst. Dersom ein kontroll samanliknar matematikk og kjeldemerke proposisjon for proposisjon, skal han halde: ingen endra proposisjon har matematikk, og dei fire kjeldemerka står der dei stod.
2. **Rettinga er stipulert, ikkje utleidd.** Den som meiner at «designar» bør dekkje alle med verknad og omsorg, vil lese 6.8 som for trong. Teksten gjev grunnen (6.84), ikkje eit tvingande argument for ordbruken.
3. **Omsorg utan adresse.** 6.82 og 6.85 reknar delt spenning som nok for omsorgsvilkåret. Det byggjer på 5.28 lesen funksjonelt (avviket hos ein annan set arbeid i gang) og på at 6.1214 kallar delt spenning «omsorg utan adresse». Les forfattaren 6.1214 slik at omsorg krev adresse, må 6.82 krevje at cella skil naboen ut, og første setning i 6.85 må snuast. Dette er mi tolking, ikkje noko teksten avgjer eintydig.
4. **Minimale system.** Kriteriet arvar breidda i 5.11 og 5.28. Ein regulator som tek imot rettingar frå den han regulerer for, kan kome nær å oppfylle det langs eitt omsyn. 6.83 (grad) er einaste brems. Om det er ønskt, veit eg ikkje.
5. **«Kan rettast» er ein disposisjon.** 6.84 les han som to krav: svaret kunne gått imot biletet, og det endrar arbeidet. Noten til 6.714 gjev eit mål for kor mykje kanalen ber, men ingen terskel. Kor grov ein kanal kan vere før rettingsvilkåret ikkje held, er ope.
6. **6.83 ber fram ei prøve for kvart vilkår.** Prøva for verknad («mot alternativa som stod opne») bruker ordlyden frå 7.011, som kjem seinare. Prøva for retting er formulert her og står ikkje som eiga føreseiing i registeret til 7.174.
7. **6.86 og gjentekne bestillingar.** Der bestillaren reagerer på ein prototyp, er reaksjonen eit svar frå bestillaren etter 6.801. Proposisjonen seier det ikkje uttrykkjeleg.
8. **6.1 er eit postulat, og eitt ord i det er bytt** («verknad» til «innverknad»). Eg meiner innhaldet er det same, sidan første setning seier «verkar inn på». Forfattaren bør sjå på det.
9. **6.7131 seier framleis «meir omsorg».** Det er laus tale for «meir fri vekt på biletet». Testane vernar berre 6.711 mot uttrykket.
10. **Føreordet og 6.01.** Føreordet nemner «føretaket» under (6.01); lista i 6.01 har det ikkje. Avviket stod før denne køyringa og er ikkje retta, sidan føreordet er verna (sjå Forkasta).
11. **Noten til 6.14** omtalar «koordinering av lyskjegler», ein ordlyd proposisjonen ikkje hadde før denne køyringa heller. Notane er verna.
12. **Noten til 7.174, punkt (viii)** seier «meir omsorg» der 6.711 seier «meir fri vekt på biletet». Ikkje rørt.
13. **«Designhandlinga» er borte frå traktaten.** Ordet stod berre i 7.2. Forskingsnotatet `fagleg-kartlegging-designteori-norden-2000-2026.md` bruker det i eigen samanheng og er urørt.
14. **Rytmen.** 6.8 er no fire korte avsnitt i staden for éi setning, og 6.86 er den lengste proposisjonen i rekkja. Eg har ikkje funne noko å stryke utan å miste eit steg, men det bør prøvast på lesarar. Kortversjonen hentar 6.8 etter adresse og får den nye forma ved neste bygging; korleis fire avsnitt tek seg ut der, er ikkje sett.
15. **Kjelde 93 under 6.14** er ikkje lesen på nytt. Setninga kjeldemerket står til, er uendra.

**Kostnad:** budsjetteljaren i køyringa viste om lag 7,1 USD før denne rapporten vart skriven. Sluttsummen ligg litt over.

**Estimert API-kostnad:** 8.3173234 USD.
