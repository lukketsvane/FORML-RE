# AutoResearch 004: motprøvande retting av formlære

**Merknad ved integrering 16.11.2026:** Fire av dei seks proposisjonane var alt presiserte i nyare main. Denne integreringa samordnar ordlyden i 6.614, 6.673, 6.674, 6.72 og 7.1521 med AutoResearch 004. Formuleringa i 6.711 var alt identisk. Dei andre 485 proposisjonane er urorte.

Dato: 2026-11-15. Oppdrag: GitHub-sak #32. Éi køyring, tre interne rundar (A avkreft, B rett og test, C motles).
Modell: Claude Fable 5.2. Status: **`needs-human-review`**. Ingenting er slått saman, og `main` er urørt.

Filer som er skrivne i denne køyringa, og ingen andre:

- `traktat/tekst/formlaere.tex` (sju linebyte i seks proposisjonar)
- `traktat/tests/test_autoresearch_004.py` (ny, frosen før manuskriptet vart endra)
- `traktat/revisjon/autoresearch-004-retting.md` (denne loggen)

## 0. Resultat

**Retta (utført, ikkje berre planlagt):** 6.614, 6.673, 6.674, 6.711, 6.72 og 7.1521. Alle seks er typen `t`, og alle hadde ei verbal følgje som eit eksakt motdøme feller. Likningane, kjeldemerka, adressene, typane og rekkjefølgja er uendra.

**Ikkje retta, med vilje:** 6.76 (krev forfattarval mellom to modellar, kapittel 5) og 5.711 (er rett som han står, kapittel 3.3).

**Rekneskap for målet i saka.** Sju setningar som motdøme feller, stod i baseline (to i 6.614, éi i kvar av 6.673, 6.674, 6.711, 6.72, 7.1521), i tillegg til «viss»-halvdelen av 6.76. Etter køyringa står éin att: 6.76. Dette er ei oppteljing av dei setningane sak #32 og P1-a til P1-d peikar på, ikkje av heile traktaten.

**Ikkje gjort:**

- **Dei 491 proposisjonane er ikkje kontrollerte på nytt.** Arbeidsflyten ber om det i ein fast innleiingstekst; saka ber uttrykkjeleg om målretta retting og ikkje om ny allmenn gransking. Eg følgde saka. Det einaste som gjeld alle 491, er den maskinelle kontrollen av adresse, type, rekkjefølgje og at teksten utanfor dei seks er byte-lik baseline.
- Lesne i denne køyringa: føreordet (delvis), 5.7–5.724, 6.6–6.63, 6.65–6.76, 7.15–7.153, og notata til 6.614, 6.673, 6.674, 6.71, 6.711, 6.72, 6.73, 6.702 og 7.174. Resten av manuskriptet er ikkje lese.
- Funna er ikkje skrivne inn i `kritisk-gransking-2026-11.md`, slik innleiingsteksten til arbeidsflyten seier. Saka avgrensar skrivinga til dei tre filene over.
- Ingen eksterne kjelder er lesne eller verifiserte. Ingen empiri.
- PDF, nettutgåve, `kjelder.json`, kortversjonen og `traktat-en/` er ikkje oppdaterte (kapittel 8).
- Forsøkskortet er ikkje lagra i `autoresearch/experiments/`; det står i kapittel 10.

## 1. Frosne kjelder og baseline

| Kjelde | Identitet |
| --- | --- |
| Git-commit ved start | `ead495918b9843b29eaa119eda7c3fd44e31b365` |
| `formlaere.tex` før | sha256 `d38a7ffb…65b0b85c` |
| `formlaere.tex` etter | sha256 `172c4d63…d117f9e0` (same som `harness.py status` melder) |
| `revisjon/test_autoresearch_003.py` | sha256 `d8dc99e9…5151e324`, uendra |
| `revisjon/kontrollrekning-2026-11.py` | sha256 `6a11fca1…bd9e910e`, uendra |
| `autoresearch/harness.py`, `test_harness.py` | `f227e431…`, `c5e83e0f…`, uendra |
| `tests/test_autoresearch_004.py` | sha256 `acffdd84…5d11a1d71` ved baselinekøyringa, ikkje endra etterpå |
| Python | 3.14.4 |

**Rekkjefølgje.** Testfila vart skriven og køyrd mot urørt manuskript før første endring. Baseline: 25 testar, 7 feil, alle i `test_felte_setningar_er_borte` (dei sju setningane over). Alle rekne- og strukturtestar var grøne på baseline. Det er det negative kontrolltilfellet for teksten: testen kan sjå feilen. Atterhald som i forsøk 003: test og retting kjem i same commit, så git-historia kan ikkje stadfeste rekkjefølgja.

Dei frosne hashane i testfila (adresseliste, tekst utanfor dei seks opne proposisjonane, likningar og kjeldemerke i dei seks) er rekna frå baseline. Lista over opne proposisjonar vart fastsett før endringane og inneheld ikkje 5.711 eller 6.76.

## 2. Runde A: avkrefting før retting

For kvar retting: påstanden slik han stod, vilkåra, motdømet, rivalen og kva som ville ha gjort rettinga unødvendig. Modellen er den i 6.6–6.61: \(D\) endeleg, \(\mu_{SG}>0\), \(P\propto\mu_{SG}e^{-\beta\Phi}\), estimat og faktiske avvik faste funksjonar på \(D\).

| Prop. | Påstand i baseline | Motdøme (eksakt) | Rival | Rettinga er unødvendig dersom |
| --- | --- | --- | --- | --- |
| 6.673 | «Meir prioritering kan ikkje auke det estimerte avviket langs same omsyn.» | \(\hat\Lambda_k=(0,4)\), \(\hat\Lambda_m=(0,8)\), \(\beta w=\ln2\), sum 1: \(\omega_k\) 1/4 → 1/2 gjev \(\mathbb E[\hat\Lambda_k]\) 4/129 → 4/65 | Setninga gjeld uendra for normaliserte vekter | omhugsvektene ikkje er bundne til sum 1. Då er 6.61 feil skildring |
| 6.674 | «Meir prioritering betrar det faktiske utfallet når estimatet følgjer avviket» | Same modell med \(e_j=\hat\Lambda_k\): estimatet følgjer avviket fullkome, og \(\mathbb E[e_j]\) stig 4/129 → 4/65 | Som over | som over |
| 7.1521 | «Meir prioritering av eit estimat som ordnar formene rett, kan ikkje auke sviktrisikoen.» | Same modell, \(\varepsilon_j=1\): \(R_j=P(x_2)\) stig 1/129 → 1/65 | Som over | som over |
| 6.711 | «Fell ho ingen stad, kan meir omsorg ikkje auke avviket hos den andre i middel.» | Eigne omsyn \((0,10,20)\), feilfritt bilete \((0,2,4)\), \(h(u)=u\): \(\gamma_A\) 0 → 1/2 → 1 gjev \(\mathbb E[e_B]\) 684/349867 → 44/1387 → 4/7 | «Omsorg» tyder alltid den frie vekta i 6.71 | 6.701 ikkje tok omsorgsdelen frå eigne omsyn |
| 6.614 | «Forholdet … avheng ikkje av kva andre former som finst»; «Flyttar eit nytt alternativ forholdet mellom to gamle, held ikkje modellen.» | Kjeda x–y, \(\Phi=(0,1)\), \(\beta=\ln2\): \(P(x)/P(y)=2\). Nytt z ved x: forholdet er 4, med uendra \(\Phi\) (5.711: \(N(x)\) går frå 1 til 2) | \(\mu_{SG}\) er gjeven utanfrå og avheng ikkje av grammatikken | 5.711 ikkje gjaldt, altså at grunnvekta ikkje følgde talet på opne steg |
| 6.72 | «Ved sterk seleksjon står skade som ingen vinn på, berre att der målet er utan vekt.» | \(\hat e_B=(0,1)\), \(e_B=(1,0)\), målet har vekt: forma med faktisk avvik 1 vert vald | «Skade» tyder estimert skade (slik notat 6.72 seier) | estimata alltid ordna formene som dei faktiske avvika. 6.674 og 7.11 føreset det motsette |
| 6.76 | «… viss og berre viss han sjølv har innverknad, eller det går ein veg av omsorg til han frå nokon som har.» | \(w_B=1\), \(\gamma_B=1\): vekta på B sitt eige mål er 0 | «Har innverknad» inneber at han held noko for seg sjølv | 6.701 kravde \(\gamma<1\) |

Alle motdøma er rekna om att i `test_autoresearch_004.py` med brøkar. Dei fire første stod alt i forsøk 003 eller kontrollrekninga; motdøma for 6.674 og 7.1521 under sum 1 er nye her, men følgjer av same modell (E1).

## 3. Runde B: rettingane

### 3.1 Proposisjon 6.673 [t]

Før:

> Meir prioritering kan ikkje auke det estimerte avviket langs same omsyn.

Etter:

> Meir fri vekt \(\theta_k\), med dei andre vektene faste, kan ikkje auke det estimerte avviket langs same omsyn. Summerer omhugsvektene seg til 1, er ein auke i éi av dei ei flytting frå andre omsyn. Då avgjer kovariansen mellom estimatet og skilnaden mellom det og estimatet vekta vert teken frå, forteiknet, og det estimerte avviket langs omsynet kan stige.

*Føresetnad.* \(D\), \(\mu_{SG}\) og estimata avheng ikkje av vektene.
*Slutning 1 (fri vekt).* \(\partial\mathbb E[\hat e_k]/\partial\theta_k=-\operatorname{Var}(\hat e_k)\le0\) i kvart punkt, så \(\mathbb E[\hat e_k]\) er ikkje-stigande òg for endelege steg.
*Slutning 2 (sum 1).* Ei tillaten endring har retning \(v\) med \(\sum_kv_k=0\). For flytting frå m til k er den deriverte av \(\mathbb E[f]\) lik \(-\beta w_i\operatorname{Cov}(f,\hat\Lambda_{ik}-\hat\Lambda_{im})\) for kvar vektuavhengig \(f\). Det er uttrykket i 6.6742, der \(f=e_j\). Med \(f=\hat\Lambda_{ik}\) vert det \(-\beta w_i[\operatorname{Var}(\hat\Lambda_{ik})-\operatorname{Cov}(\hat\Lambda_{ik},\hat\Lambda_{im})]\), som er positivt når \(\beta w_i>0\) og kovariansen er større enn variansen. At det «kan stige», er prova av E1.

Ordlyden følgjer 6.6742 («skilnaden mellom dei to estimata») og 7.153 («meir fri vekt»). Kjem vekta frå fleire omsyn, står det vekta snittet av estimata deira der 6.673 seier «estimatet vekta vert teken frå».

### 3.2 Proposisjon 6.674 [t] og 7.1521 [t]

| | Før | Etter |
| --- | --- | --- |
| 6.674 | Meir prioritering betrar det faktiske utfallet når estimatet følgjer avviket, … | Meir fri vekt \(\theta_k\) betrar det faktiske utfallet når estimatet følgjer avviket, … |
| 7.1521 | Meir prioritering av eit estimat som ordnar formene rett, kan ikkje auke sviktrisikoen. | Meir fri vekt på eit estimat som ordnar formene rett, kan ikkje auke sviktrisikoen. |

Desse to er ikkje på prioriteringslista i saka, men dei høyrer til same dokumenterte brot (P1-c), og den kritiske granskinga gav minste retting: ordet «fri». Dei er eigne linebyte og kan takast ut kvar for seg.

*Føresetnad.* Som 3.1, og \(e_j\) er målt uavhengig av estimatet. *Slutning.* Likningane i proposisjonane er partielle deriverte med omsyn til éi fri vekt. For 7.1521: ordnar \(\hat e_k\) formene som \(e_j\) (svakt), er \((\mathbf 1[e_j(x)>\varepsilon_j]-\mathbf 1[e_j(y)>\varepsilon_j])(\hat e_k(x)-\hat e_k(y))\ge0\) for alle par, så kovariansen er ikkje-negativ under kvar fordeling, og \(R_j\) kan ikkje stige, heller ikkje ved endelege steg.

### 3.3 Proposisjon 6.614 [t] (og 5.711 [t], urørt)

Før:

> Forholdet mellom sannsyna for to former avheng ikkje av kva andre former som finst: [likning] Flyttar eit nytt alternativ forholdet mellom to gamle, held ikkje modellen.

Etter:

> Når forholdet mellom grunnvektene \(\mu_{SG}(x)/\mu_{SG}(y)\) står fast, avheng forholdet mellom sannsyna for to former ikkje av kva andre former som finst: [likning, uendra] Flyttar eit nytt alternativ forholdet mellom to gamle annleis enn det flyttar forholdet mellom grunnvektene deira, held ikkje modellen.

*Føresetnad.* 6.6 gjeld før og etter at alternativet kjem til, med same \(\beta\) og same \(\Phi(x)\), \(\Phi(y)\); både x og y ligg i \(D\) begge gonger.
*Slutning.* \(\Delta\log[P(x)/P(y)]=\Delta\log[\mu_{SG}(x)/\mu_{SG}(y)]\). Står grunnforholdet fast, står sannsynsforholdet fast. Flyttar det seg, skal sannsynsforholdet flytte seg nett like mykje.

Likninga er ikkje svekt. Prøva er heller ikkje svekt: ho gjeld no også når grunnvektene flyttar seg, og seier då kor mykje forholdet skal flytte seg. Patch-ordlyden («utan å endre grunnvektene deira») ville ha gjort prøva tom i nett det tilfellet 5.711 skildrar, der nesten kvart nytt naboalternativ endrar \(N\).

**5.711 er ikkje endra.** Han er rett: med like sannsyn for kvart ope steg er \(\mu(x)/N(x)\) konstant, og den stasjonære fordelinga til ei tilfeldig vandring på ein samanhengande graf er proporsjonal med gradtalet. Testen løyser den stasjonære fordelinga eksakt frå kjernen i 5.7 med \(r_A\) frå 5.702 og får \(N(x)/\sum N\). Vilkåret saka ber om, høyrer heime i 6.614.

### 3.4 Proposisjon 6.711 [t]

Før: «Fell ho ingen stad, kan meir omsorg ikkje auke avviket hos den andre i middel. Stig ho ingen stad, kan meir omsorg ikkje minske det.»

Etter: «Fell ho ingen stad, kan meir fri vekt på biletet ikkje auke avviket hos den andre i middel. Stig ho ingen stad, kan meir fri vekt på biletet ikkje minske det.»

*Føresetnad.* Berre vekta \(\theta\) på biletet endrar seg; alle andre ledd \(\Psi\) står faste. *Slutning.* Innanfor \(\{\hat e=u\}\) er \(P(x\mid u)\propto\mu_{SG}(x)e^{-\Psi(x)}\), utan \(\theta\). Då står \(h\) fast, og \(\partial\mathbb E[e]/\partial\theta=-\operatorname{Cov}(h(\hat e),\hat e)\), som er \(\le0\) når \(h\) ikkje fell nokon stad og \(\ge0\) når ho ikkje stig nokon stad. Sidan \(h\) står fast, gjeld forteiknet langs heile vegen.

Parameterretninga \(\gamma_A\) i 6.701 er no utanfor setninga. Der er retninga biletet minus eigne omsyn (notat 6.71), \(\Psi\) står ikkje fast, og begge slutningane kan snu: E2 feller den første, og spegelbiletet \(e\mapsto4-e\) av same modell feller den andre (resonnement; spegelbiletet er ikkje med i testfila).

### 3.5 Proposisjon 6.72 [t]

Før: «Ved sterk seleksjon står skade som ingen vinn på, berre att der målet er utan vekt.»

Etter: «Ved sterk seleksjon står estimert skade som ingen vinn på, berre att langs estimat eller bilete utan vekt. Faktisk skade kan stå att også der målet har vekt, når estimatet ordnar formene feil.»

*Føresetnad.* \(D\) endeleg, \(\beta\to\infty\), \(\Phi=\sum_k\theta_kf_k\) med \(\theta_k\ge0\), der \(f_k\) er estimata og bileta. «Skade som ingen vinn på» ved \(x\): det finst \(y\in D\) med \(f_k(y)\le f_k(x)\) for alle \(k\) og streng ulikskap for minst eitt.
*Slutning.* Lat \(x^*\) minimere \(\Phi\), og lat \(y\) dominere \(x^*\). Hadde eit strengt betra \(f_k\) positiv vekt, var \(\Phi(y)<\Phi(x^*)\). Altså er betringa berre langs \(f_k\) med \(\theta_k=0\). Andre setning er ein eksistenspåstand og følgjer av motdømet i tabellen.

Orda «der målet er utan vekt» er bytte med «langs estimat eller bilete utan vekt» fordi patch-ordlyden vart felt i runde A (kapittel 6, F1).

## 4. Runde C: motlesing

### 4.1 Eigne forsøk på å velte dei nye formuleringane

| Randtilfelle | Utfall |
| --- | --- |
| \(\beta=0\) | 6.673: alle deriverte er null; «kan stige» er ein eksistenspåstand og held. 6.614: forholdet er lik grunnforholdet, likninga held. 6.72: gjev ingen garanti (dominert form held grunnvekta si, 5/31 i testen); «ved sterk seleksjon» er eit naudsynt vilkår og står i setninga |
| Normaliserte vekter | 6.673, 6.674, 7.1521: den gamle ordlyden gjev brot i 2187-familien, den nye er avgrensa til fri vekt. \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) stig aldri (0 brot) |
| Ikkje-flat \(\mu_{SG}\) | 6.614: med faste, skeive grunnvekter \((1,3,5,7)\) flyttar ikkje noko nytt alternativ forholdet, kvar det enn vert festa (0 avvik). 6.72: massen samlar seg på minimum også med \(\mu=(1,5,25)\) |
| Endra alternativ | 6.614: 384 utvidingar av fire grafar; \(\Delta\log P\)-forholdet er eksakt lik \(\Delta\log\mu\)-forholdet i alle par |
| Feil estimat | 6.72 andre setning; 6.673 første setning gjeld estimatet og er urørt av feilen; «eit feilvendt estimat kan» i 7.1521 gjev stiging i familien |
| \(\gamma_A=1\), flate eigne omsyn | 6.711: skil ikkje eigne omsyn formene, er \(\gamma_A\) i røynda ei fri vekt, og motdømet forsvinn (0 brot). Motdømet mot «meir omsorg» krev altså at agenten gjev opp noko som skil formene |
| Éin agent, eitt omsyn | 6.673 andre setning er tom (vekta kan ikkje auke); ingen motseiing |

Éi formulering vart justert i denne runden, etter at ho var skriven inn i manuskriptet: første utkast til 6.673 sa «skilnaden mellom dei to estimata» utan at to estimat var nemnde. Alle testane er køyrde på nytt etter justeringa. Patch-ordlyden for 6.72 vart felt alt i runde A og har aldri stått i manuskriptet (F1).

### 4.2 Uavhengig motlesar

Ein eigen modellinstans (billegare modell, utan tilgang til resonnementet mitt) fekk dei seks nye formuleringane og avgjerda om 6.76, med oppdrag om å velte dei. Atterhald: han fekk parafrasane mine og grunngjevinga for 6.76, så lesinga er ikkje fullt uavhengig.

| Prop. | Dom | Merknad | Følgje |
| --- | --- | --- | --- |
| 6.673 | Held | Eige motdøme rekna (\(\hat e_m=2\hat e_k\)) | Ingen |
| 6.711 | Held | Eigen modell rekna; \(h\) uendra | Ingen |
| 6.674 | Tvitydig | «Følgjer avviket» kan lesast som kovarians under noverande fordeling eller som lik ordning. \(e=(0,1,2)\), \(\hat e=(0,2,1)\): kovariansen er \(+1/3\) under jamn fordeling og negativ under \((0{,}01;\,0{,}495;\,0{,}495)\) | Ordlaget stod i baseline og er ikkje endra. Setninga er lokal; 6.6741 dekkjer endelege steg. Ført opp i kapittel 9 |
| 7.1521 | Tvitydig | «Ordnar formene rett» må gjelde \(e_j\), same avvik som terskelen | Stod i baseline. Kapittel 9 |
| 6.614 | Tvitydig | «Held ikkje modellen» føreset at \(\Phi\) og \(\beta\) ikkje avheng av \(D\) | Same føresetnad som i baseline. I modellen er \(\Phi\) ein funksjon av forma åleine; ei \(D\)-avhengig vurdering er ein annan modell. Kapittel 7 |
| 6.72 | Tvitydig | «Sterk seleksjon» er ikkje definert som grensa; med \(\mu=(1,10^6)\) held den dominerte forma nesten all masse ved \(\beta=10\). «Ingen vinn på» er ikkje definert | Begge ordlaga stod i baseline; notat 6.72 seier \(\beta\to\infty\). Kapittel 9 |
| 6.76 | Ikkje motsagt | Fann eit ekstra tilfelle der dei to modellane skil lag (kapittel 5) | Avgjerda står |

Ingen formulering vart velta, og ingen retting vart reversert. Motlesaren rekna berre nokre av tilfella; resten er resonnement. Motlesinga er ikkje eit prov.

## 5. Proposisjon 6.76 [t]: ikkje redigert

Påstanden: målet til den andre har vekt i forma **viss og berre viss** han sjølv har innverknad, eller det går ein veg av omsorg til han frå nokon som har.

**«Berre viss» følgjer.** Etter 6.702 er \(W_{B,j}>0\) berre når \(w_B>0\) eller \(w_Ac_{A\to B,j}>0\) for ein \(A\). Etter 6.731 er vekta \(\omega_j(B)\sum_Aw_A\chi_{AB}\), som er positiv berre når ein \(A\) med \(w_A>0\) når B. Kontrollert uttømmande for tre agentar (216 omsorgsmatriser, fem innverknadsfordelingar): 0 brot.

**«Viss» følgjer ikkje.** Tre eksakte motdøme:

1. \(w_B=1\), \(\gamma_B=1\): B har all innverknad, og vekta på hans eige mål er 0 (6.702).
2. Omsorgsvektene i 6.701 er per mål. A med \(w_A=1\) har omsorg for B langs \(j'\), ikkje langs \(j\): det går omsorg til «han», og målet \(j\) har vekt 0.
3. I 6.731: A har omsorg for B, og B gjev alt vidare (\(\gamma_B=1\)). Då er \(\chi_{AB}=0\).

**Kvifor ei retting krev forfattarval.** Dei to omsorgsmodellane i teksten gjev ulike eksakte vilkår:

| Modell | Eksakt vilkår for vekt på målet til B langs j |
| --- | --- |
| 6.701/6.702 (bilete av avviket) | \(w_B(1-\gamma_B)\omega_j(B)>0\), eller \(w_Ac_{A\to B,j}>0\) for ein \(A\ne B\). Berre direkte omsorg tel, og B treng ikkje halde målet sjølv |
| 6.73/6.731 (heile vurderinga) | \(\omega_j(B)>0\) og \(\gamma_B<1\), og anten \(w_B>0\) eller ein veg av omsorg frå ein \(A\) med \(w_A>0\). Vegar tel, men B må halde målet sjølv (0 avvik i den uttømmande kontrollen) |

Dei skil lag i eit konkret tilfelle: A (\(w_A=1\)) har omsorg 1/2 for B langs \(j\), og \(\omega_j(B)=0\). Vekta er 1/2 etter 6.702 og 0 etter 6.731. Motlesaren fann eit til: \(c_{A\to B}=1\) og \(\gamma_B=1\) gjev vekt 1 etter 6.702 og 0 etter 6.731. Teksten har inga likning for den blanda modellen (bilete langs ein veg); notat 6.73 seier berre at feila legg seg saman.

Det som står att for forfattaren:

1. Kva modell 6.76 oppsummerer. Ordet «veg» peikar mot 6.731, «målet» mot 6.702.
2. Kva «har vekt i forma» tyder: \(W_{B,j}>0\), eller verknad på fordelinga. Ved \(\beta=0\), eller når estimatet ikkje skil formene, er vekta positiv utan verknad.
3. Om «målet til den andre» føreset \(\omega_j(B)>0\), og kva som svarar til «held det som sitt eige» (\((1-\gamma_B)\omega_j(B)>0\)).

To moglege rettingar, ingen utført:

- Patch-ordlyden frå 2026-11 («… og held målet som sitt eige, eller det går ein veg av omsorg til målet frå nokon som har innverknad») er rett etter 6.702 dersom «veg» tyder eitt steg, og etter 6.731 berre dersom «veg til målet» er definert som ein veg som endar i eit mål B sjølv held.
- Å stryke «viss og» gjev ei setning som er sann i begge modellane og under begge lesingane av «vekt». Ho seier mindre enn forfattaren ville seie.

## 6. Forkasta rettingar og negative funn

| Nr. | Kva | Kvifor forkasta |
| --- | --- | --- |
| F1 | 6.72 etter patchen: «estimert skade … der målet er utan vekt» | Eksakt motdøme: B utan innverknad, eige estimat \((1,0)\); A med \(w_A=1\) har omsorg 1/2 gjennom biletet \((0,1)\). Målvekta etter 6.702 er 1/2, likevel står skaden B estimerer. Vekta ligg på biletet, ikkje på estimatet. Ny ordlyd nemner difor estimat og bilete |
| F2 | 6.614 etter patchen: «Ved fast grunnfordeling …» | Ei normalisert fordeling kan ikkje stå fast når \(D\) får eit nytt element; det som må stå fast, er forholdet mellom to grunnvekter. «Utan å endre grunnvektene deira» gjer dessutan prøva tom under 5.711 |
| F3 | 6.673 etter forsøk 003: «… som i 6.61 … og 6.6742 avgjer forteiknet» | Ingen av dei 491 proposisjonane viser til ein annan med nummer. Innhaldet er halde, tilvisinga er skriven ut i ord |
| F4 | Tillegg i 6.711 om at slutningane ikkje gjeld når \(\gamma_A\) veks | Ny påstand i proposisjonen; minste retting er å avgrense til fri vekt. Påstanden er sann (3.4) og kan leggjast til av forfattaren |
| F5 | Tillegg i 5.711: «eit nytt steg frå x aukar grunnvekta til x» | Feil for den normaliserte fordelinga: i kjeda x–y er \(\mu(x)=1/2\) både før og etter at z kjem til ved x. Berre forholdet til y endrar seg |
| F6 | Redigering av 6.76 | Kapittel 5 |

Negative funn: runde C fann ingen brot i dei nye formuleringane. Det er ikkje ei stadfesting; det seier at éin forfattar og éin motlesar ikkje fann noko i dei tilfella dei prøvde.

## 7. Føresetnader rettingane kviler på

Alle seks formuleringane føreset stillteiande det same som likningane dei står under:

- Estimata, dei faktiske avvika, \(D\) og \(\mu_{SG}\) endrar seg ikkje når vekta gjer det (notat 6.673 og 6.674 seier dette; proposisjonane seier det ikkje). Gjev meir prioritering òg betre estimat, gjeld verken den gamle eller den nye ordlyden.
- I 6.614 er \(\Phi\) og \(\beta\) dei same før og etter at alternativet kjem til. Vurderingar som avheng av kva andre alternativ som finst, er utanfor modellen, og eit slikt brot er nett det prøva skal fange.
- 6.711 gjeld den reversible, stasjonære fordelinga; innanfor ei nivåmengd må alle andre ledd stå faste.
- 6.72 gjeld grensa \(\beta\to\infty\) på endeleg \(D\), og «ingen vinn på» er lese som dominans i estimata og bileta.
- Under omsorg er svarstyrken for eigne omsyn \(\beta w_i(1-\gamma_i)\omega_k\). Ved \(\gamma_i=1\) flyttar inga omfordeling av eigne omsyn noko. 6.6742 har same avgrensing.

## 8. Testresultat

Køyrde etter siste endring i manuskriptet.

| Kommando | Baseline | Etter |
| --- | --- | --- |
| `python traktat/revisjon/test_autoresearch_003.py` (uendra) | sluttkode 0, «Uventa utfall: ingen» | same |
| `python traktat/revisjon/kontrollrekning-2026-11.py` (uendra) | sluttkode 0, 22 resultatliner, «Uventa utfall: ingen» | same |
| `python -m unittest discover -s autoresearch -p 'test_*.py'` (uendra) | 5 testar, OK | same |
| `python autoresearch/harness.py status` | 491; 118, 27, 20, 16, 145, 112, 53 | same tal; ny manuskripthash |
| `python traktat/tests/test_autoresearch_004.py` | 25 testar, 7 feil (alle «felte setningar») | 25 testar, OK |
| `python3 -m unittest discover -s tests` i `traktat/` | 72 testar, 3 feil | 97 testar, dei same 3 feila |
| `python3 scripts/build.py check-generated` | ikkje køyrd | **feilar**: «Print release is stale. Run make all» |

Dei tre feila i `traktat/tests` kjem av miljøet og er dei same før og etter: `pandoc` manglar (éin test), og `pypdf` manglar, så `test_book_layout` og `test_print_assets` lèt seg ikkje importere. Kontrollrekninga melder framleis motdøma mot 6.673, 6.711, 6.614, 6.72 og 6.76; ho reknar på modellen, ikkje på ordlyden, og skal difor ikkje endre seg.

**`check-generated` feilar no, og det er venta.** Manuskriptet inngår i kjeldehashen, og PDF og nettutgåve er ikkje bygde på nytt (saka forbyr genererte filer, og XeLaTeX og Pandoc manglar her). Eit menneske må køyre `make all` og leggje utdata i same PR før sammenslåing.

Innhaldet i den nye testfila:

| Klasse | Eksakte motdøme | Endeleg familie | Negativ kontroll |
| --- | --- | --- | --- |
| Struktur | – | 491 adresser, type, rekkjefølgje; tekst utanfor seks proposisjonar; likningar og kjeldemerke | sju felte setningar (feila på baseline) |
| Vektforskyving | E1 med varians og kovarians | 4374 modellar med fri vekt: 0 brot for estimat, rett ordna avvik og risiko; forteiknsregel for to tilstandar | 2187 modellar under sum 1: den gamle setninga gjev brot, differansen gjev 0 |
| Svarkurve | E2 | 5832 modellar: \(h\) uendra, 0 brot | \(\gamma_A\)-retninga: \(h\) flyttar seg, og avviket stig med stigande kurve |
| Uavhengigheit | kjeda x–y–z | 384 grafutvidingar, stasjonær fordeling løyst frå kjernen | gammal påstand felt i kjeda |
| SterkSeleksjon | faktisk skade; bilete mot eige estimat; \(\beta=0\) | 13824 modellar: 0 dominerte minimum langs estimat med vekt | – |
| Omsorgsveg | tre motdøme mot «viss» | 216 omsorgsmatriser: «berre viss» 0 brot, «viss» brot | modellane 6.702 og 6.731 skil lag |

### Slag av belegg

| Slag | Kva |
| --- | --- |
| (a) Eksakt prov eller motdøme | Prova i kapittel 3 (korte, kontrollerte for hand, ikkje maskinverifiserte). Motdøma i kapittel 2, 5 og 6 (brøkrekning) |
| (b) Numerisk konsistens | Dei endelege familiane i testfila. Aritmetikken er eksakt, men familiane er små og valde av meg; 0 brot der provar ikkje dei allmenne setningane |
| (c) Empirisk resultat | Ingen. Ingenting her seier noko om formgjevarar, og ingen effektpåstand kviler på syntetiske data |

Testane krev ikkje at den nye ordlyden står i manuskriptet. Grøn test seier at dei felte setningane er borte, at resten er urørt, og at rekninga stemmer med det loggen hevdar. Om den nye ordlyden er rett norsk for det prova seier, må eit menneske vurdere.

## 9. Det som står att

1. **6.76**: forfattarval, kapittel 5.
2. **Følgjeendringar utanfor omfanget.** Notat 7.174 (i) og føreseiing (i) i kortversjonen seier framleis at forholdet «endrar seg ikkje når andre alternativ kjem til eller fell bort», utan vilkår; dei må følgje 6.614. Notat 7.174 (viii) seier «meir omsorg» og bør følgje 6.711. Notat 6.614 nemner ikkje grunnvektene. `traktat-en/`, PDF og nettutgåve er ikkje oppdaterte.
3. **Same ordbruk andre stader, ikkje retta.** 6.6741 («kvar auke av vekta»), 6.675 og 7.11 («meir prioritering») er sanne under begge lesingane eller arvar «fri vekt» frå 6.674, og er ikkje rørte. 6.7131 [i] seier «meir omsorg»; illustrasjonar ber inga slutning. Føreordet seier at «meir omhug og sterkare prioritering» vil «systematisk auke skaden» når kovariansen er negativ; setninga nemner \(\theta_k\), men «systematisk» er sterkare enn ein lokal derivert.
4. **Tvitydige ordlag frå baseline** som motlesaren peika på: «følgjer avviket» (6.674), «ordnar formene rett» utan å seie kva avvik (7.1521), «sterk seleksjon» og «ingen vinn på» (6.72).
5. **Einingar.** 6.673 skriv \(\beta\Phi=\sum_k\theta_k\hat e_k\), medan 6.6101 definerer \(\theta_{ik}\) per toleranseeining (\(\hat\Lambda=\hat e/\varepsilon\)). Forteikna er dei same; storleikane skil seg med \(\varepsilon_k\). Ikkje retta.
6. **«Grunnvekt»** er \(\mu_0\) i 6.613 og \(\mu_{SG}(x)\) i 6.65. 6.614 skriv difor symbolet ut. Ordbruken elles er ikkje rydda.
7. P1-e, P1-f, P1-g og alle P2- og P3-funn i den kritiske granskinga er urørte.
8. Prova i kapittel 3 er lesne av éin forfattar og delvis av éin motlesar. Dei bør lesast av eit menneske før sammenslåing.

## 10. Forsøkskort

Ikkje lagra i `autoresearch/experiments/`, fordi saka avgrensar skrivinga til tre filer.

```json
{
  "id": "0004-retting-verbale-folgjer",
  "proposition": "6.673",
  "claim": "Seks t-proposisjonar (6.614, 6.673, 6.674, 6.711, 6.72, 7.1521) hadde verbale følgjer som eksakte motdøme feller innanfor modellen sjølv. Dei retta formuleringane er avgrensa til fri vekt, fast grunnforhold og estimert skade, og toler dei same motdøma.",
  "rival": "Dei opphavlege setningane gjeld uendra under sum 1 (6.61), omsorgsdelen i 6.701, grunnvekta i 5.711 og feil estimat.",
  "falsifier": "Ein endeleg modell med vektuavhengige estimat der fri auke av theta_k hevar E[e^_k]; der sannsynsforholdet flyttar seg annleis enn grunnforholdet med uendra Phi og beta; der eit minimum av Phi er dominert langs eit estimat med positiv vekt; eller der h flyttar seg under fri vekt på biletet.",
  "measurement": "python traktat/tests/test_autoresearch_004.py (eksakt brøkrekning, ingen frø), saman med dei uendra testane frå forsøk 003 og kontrollrekninga.",
  "baseline": "Urørt manuskript ved commit ead4959: sju felte setningar står, 7 av 25 testar feilar.",
  "status": "needs-human-review",
  "evidence": []
}
```
