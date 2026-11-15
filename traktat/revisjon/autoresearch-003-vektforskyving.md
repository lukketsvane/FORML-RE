# AutoResearch forsøk 003: vektforskyving ved fri og ved normalisert vekt

Dato: 2026-11-15. Oppdrag: GitHub-sak #29. Éi køyring, éin iterasjon.
Testfil: `traktat/revisjon/test_autoresearch_003.py` (berre standardbiblioteket).

## 0. Resultat og status

**Resultat.** Kovariansidentiteten i 6.673 og 6.674 held for ei fri vekt. Monotonisetninga «meir prioritering kan ikkje auke det estimerte avviket langs same omsyn» held ikkje når vektene er bundne til sum 1 som i 6.61. Då er ein auke i \(\omega_k\) ei flytting frå andre omsyn, og \(\mathbb E[\hat\Lambda_k]\) stig lokalt nett når \(\operatorname{Cov}(\hat\Lambda_k,\hat\Lambda_m)>\operatorname{Var}(\hat\Lambda_k)\). Den naive rivalen er felt av tre eksakte motdøme. Det same gjeld «meir omsorg» i 6.711 når omsorg vert lesen som omsorgsdelen \(\gamma_A\) i 6.701.

Forsøket gjev òg to nye, avgrensa påstandar som toler prøving:

- Differansen \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) kan aldri stige når vekt vert flytta frå m til k (T3).
- \(\mathbb E[\hat\Lambda_k]\) kan ikkje stige ved slik flytting for nokon grunnfordeling viss og berre viss \(\hat\Lambda_k\) og \(\hat\Lambda_k-\hat\Lambda_m\) ordnar alle par av former likt (T4).

**Status:** `needs-human-review`. Utleiingane er korte prov som eit menneske kan kontrollere. Dei er ikkje maskinverifiserte. Den numeriske delen fann 0 avvik, men det seier berre at formel og implementasjon er samde i dei fastsette modellane.

**Gjort**

- Lese 6.61, 6.6101, 6.672–6.6742, 6.675, 6.7–6.712 i `formlaere.tex`, punkt P1-c i den kritiske rapporten, heile `kontrollrekning-2026-11.py`, `framlegg-rettingar-2026-11.patch`, `autoresearch/program.md` og `0001-kumulativitet.json`.
- Utleia identitetane T1–T6 (kapittel 2), skrive protokollen inn i testfila og køyrt ho éin gong. Tala i kapittel 5 er frå den første køyringa.
- Køyrt den eksisterande kontrollrekninga og `autoresearch`-testane (kapittel 8).

**Ikkje gjort**

- Dei 491 proposisjonane er ikkje kontrollerte i denne runden. Saka avgrensar forsøket til proposisjonane over, og ho forbyr endringar i den kritiske rapporten.
- 6.71 og 7.1521 er ikkje granska på nytt. 7.1521 er ikkje lesen i denne runden.
- `formlaere.tex`, den kritiske rapporten, patchen, korpus og workflow er urørte.
- Ingen empiri. Resultatet gjeld modellen, ikkje formgjevarar.
- Forsøkskortet er ikkje lagra i `autoresearch/experiments/`, fordi saka tillèt berre to nye filer. Kortet står i kapittel 9.

## 1. Frosne kjelder

| Kjelde | Identitet |
| --- | --- |
| Git-commit | `fa49eccc55161b4806661f19d435e090d5a4917a` |
| `traktat/tekst/formlaere.tex` | sha256 `d38a7ffb…65b0b85c` (same som `harness.py status` melder) |
| `traktat/revisjon/kontrollrekning-2026-11.py` | sha256 `6a11fca1…bd9e910e` |
| `traktat/revisjon/test_autoresearch_003.py` | sha256 `d8dc99e9…5151e324` ved første køyring; ikkje endra etterpå |
| Python | 3.14.4 |

**Atterhald om frysinga.** Protokollen (frø, toleranse, modellsett, kriterium) vart skriven inn i testfila før første køyring og er ikkje endra sidan. Protokoll og resultat kjem likevel i same commit, så git-historia kan ikkje stadfeste rekkjefølgja. `program.md` ber om arbeid på greina `autoresearch/formlaere-designteori-20261115`; denne køyringa gjekk på greina workflowen oppretta, slik saka seier.

## 2. Utleiing

**Modell.** \(D\) er endeleg, \(\mu(x)>0\) er fast, og

\[
P(x)\propto\mu(x)\exp\Bigl(-\Psi(x)-\sum_k\theta_k\hat\Lambda_k(x)\Bigr).
\]

\(\hat\Lambda_k=\hat e_k/\varepsilon_k\) er estimatet i toleranseeiningar (6.61). \(\Psi\) samlar alle ledd som vert haldne faste. Føresetnader: \(\mu\), \(D\), \(\Psi\) og estimata avheng ikkje av vektene. \(f\) er ein vilkårleg funksjon på \(D\) som heller ikkje gjer det.

**T1 (fri vekt, H_fri).** \(\partial\log P(x)/\partial\theta_k=-\hat\Lambda_k(x)+\mathbb E[\hat\Lambda_k]\). Difor er \(\partial\mathbb E[f]/\partial\theta_k=-\operatorname{Cov}(f,\hat\Lambda_k)\), og \(\partial\mathbb E[\hat\Lambda_k]/\partial\theta_k=-\operatorname{Var}(\hat\Lambda_k)\le0\) i kvart punkt. Fri auke av \(\theta_k\) kan då ikkje auke \(\mathbb E[\hat\Lambda_k]\), heller ikkje ved endelege steg. Dette er 6.673 og 6.674.

**T2 (bunden vekt, H_normalisert).** Lat \(\theta_k=\beta w\,\omega_k\) med \(\sum_k\omega_k=1\). Kvar tillaten endring har retning \(v\) med \(\sum_kv_k=0\). Langs \(\omega+tv\) er

\[
\frac{d}{dt}\mathbb E[f]=-\beta w\operatorname{Cov}\Bigl(f,\sum_kv_k\hat\Lambda_k\Bigr).
\]

Flytting frå m til k gjev \(-\beta w\operatorname{Cov}(f,\hat\Lambda_k-\hat\Lambda_m)\), som er 6.6742. Med \(f=\hat\Lambda_k\):

\[
\frac{d}{dt}\mathbb E[\hat\Lambda_k]=-\beta w\bigl[\operatorname{Var}(\hat\Lambda_k)-\operatorname{Cov}(\hat\Lambda_k,\hat\Lambda_m)\bigr].
\]

Det estimerte avviket langs k stig lokalt nett når \(\operatorname{Cov}(\hat\Lambda_k,\hat\Lambda_m)>\operatorname{Var}(\hat\Lambda_k)\). Ved proporsjonal nedskalering av dei andre vektene står \(\bar\Lambda_{-k}=\sum_{m\ne k}\omega_m\hat\Lambda_m/(1-\omega_k)\) i staden for \(\hat\Lambda_m\).

**T3 (det som alltid held under binding).** Med \(f=\hat\Lambda_k-\hat\Lambda_m\) er den deriverte \(-\beta w\operatorname{Var}(\hat\Lambda_k-\hat\Lambda_m)\le0\) i kvart punkt på vegen. \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) kan altså ikkje stige når vekt går frå m til k. Flyttinga betrar k *relativt til* m. Ho lovar ikkje noko om k åleine.

**T4 (eksakt vilkår for den naive påstanden).** Skriv \(g=\hat\Lambda_k-\hat\Lambda_m\). Desse to er likeverdige:

1. For kvar \(\mu>0\), kvar \(\Psi\), kvar \(\beta w\ge0\) og kvar startvekt er \(\mathbb E[\hat\Lambda_k]\) ikkje-stigande under flytting frå m til k.
2. For alle \(x,y\in D\) er \((\hat\Lambda_k(x)-\hat\Lambda_k(y))(g(x)-g(y))\ge0\).

Prov: \(\operatorname{Cov}_P(f,g)=\tfrac12\sum_{x,y}P(x)P(y)(f(x)-f(y))(g(x)-g(y))\). Under 2 er kvart ledd ikkje-negativt for kvar \(P\), så den deriverte i T2 er \(\le0\) overalt. Har eitt par negativt produkt, vel \(\mu\) slik at \(P\) samlar seg likt på dei to formene; då går kovariansen mot ein fjerdedel av produktet, og den deriverte er positiv for \(\beta w>0\).

Vilkår 2 held når omsyna står mot kvarandre (m ordnar alle par motsett av k), når \(\hat\Lambda_m\) er konstant, og når \(\hat\Lambda_m=c\hat\Lambda_k+\text{konst}\) med \(c\le1\). Det sviktar når eit par vert ordna likt av begge og m skil paret sterkare enn k, målt i toleranseeiningar.

**T5 (to tilstandar).** Med \(D=\{x,y\}\) er \(\operatorname{Cov}_P(f,g)=P(x)P(y)\,\Delta f\,\Delta g\). Forteiknet avheng då ikkje av \(\mu\), \(\beta\) eller vektene: \(\mathbb E[\hat\Lambda_k]\) stig ved flytting frå m til k nett når \(\Delta\hat\Lambda_k\) og \(\Delta\hat\Lambda_m\) har same forteikn og \(|\Delta\hat\Lambda_m|>|\Delta\hat\Lambda_k|\).

**T6 (svarkurva i 6.711).** Innanfor ei nivåmengd \(\{\hat\Lambda=u\}\) er \(P(x\mid u)\propto\mu(x)e^{-\Psi(x)}\), utan \(\theta\). Difor står \(h(u)=\mathbb E[e\mid\hat\Lambda=u]\) fast når berre den frie vekta til biletet veks, og \(\partial\mathbb E[e]/\partial\theta=-\operatorname{Cov}(h(\hat\Lambda),\hat\Lambda)\le0\) når \(h\) ikkje fell nokon stad. Veks omsorgsdelen \(\gamma_A\) i 6.701 med éi omsorgsvekt, er retninga i staden biletet minus eigne omsyn:

\[
\frac{d}{d\gamma_A}\mathbb E[e_{B,j}]=-\beta w_A\operatorname{Cov}\Bigl(e_{B,j},\hat\Lambda_{A|B,j}-\sum_k\omega_k(A)\hat\Lambda_{A,k}\Bigr).
\]

Då står \(\Psi\) ikkje fast, så \(h\) kan flytte seg, og forteiknet er ikkje bunde av forma på \(h\).

## 3. Frosen protokoll

| Storleik | Verdi |
| --- | --- |
| Frø | 2026 (tilfeldig familie, same frø som kontrollrekninga), 2027 (T4), 2028 (svarkurve) |
| Modellar | 300 tilfeldige (2, 3, 5, 8 tilstandar; 2, 3, 4 omsyn; fast ledd \(\Psi\); \(\beta w\in[0{,}02,4]\)), 11 adversarielle fastsette for hand, 300 for T4, 200 for T6 |
| Numerisk derivert | sentraldifferanse, \(h=10^{-5}/\max(1,\text{spenn av retninga})\) |
| Toleranse | \(10^{-6}\cdot\max(1,\max\lvert f\rvert\cdot\text{spenn av retninga})\) |
| Endelege steg | fri: \(\Delta\theta\in\{0{,}1,\ 1,\ 10\}\); bunden: flytt \(\min(0{,}25,\ \text{tilgjengeleg vekt})\); margin \(10^{-9}\) |
| Eksakt del | `fractions.Fraction`, \(e^{-\beta w}=1/2\), heiltalseksponentar |

Adversarielle tilfelle: motdømet frå kontrollrekninga (A1), motstridande omsyn (A2), identiske estimat (A3), omsorgsdømet frå P1-c (A4), kolineære estimat (A5), \(\beta w=50\) (A6), \(\beta=0\) (A7), konstant estimat (A8), spenn 1000 med grunnvekter frå \(10^{-6}\) (A9), forteiknsskifte langs vegen (A10), randpunkt \(\omega_m=0\) (A11).

**Feilkriterium, fastsette før køyring.** Testen gjev sluttkode 1 dersom eitt av desse slår til:

| Kode | Utfall som feller | Kva som då er felt |
| --- | --- | --- |
| K1 | Eitt avvik over toleransen mellom numerisk derivert og kovariansformel, fri eller bunden | T1 eller T2, eller implementasjonen |
| K2 | \(\mathbb E[\hat\Lambda_k]\) stig ved fri auke av \(\theta_k\), derivert eller endeleg steg | H_fri |
| K3 | Null stigingar under binding i den tilfeldige familien, eller eit eksakt døme som ikkje stemmer | H_normalisert («kan stige»); den naive rivalen står |
| K4 | Forteiknet på den numeriske deriverte skil seg frå \(-\beta w(\operatorname{Var}-\operatorname{Cov})\) | T2 |
| N2 | \(\mathbb E[\hat\Lambda_k-\hat\Lambda_{\text{rest}}]\) stig ved flytting til k | T3 |
| N3 | Stiging i ein komonoton modell, eller eit brotpar der den konstruerte grunnfordelinga ikkje gjev stiging | T4 |
| S1, S3 | \(h\) flyttar seg under fri vekt, eller \(\mathbb E[e]\) går feil veg med monoton \(h\) | T6, 6.711 for fri vekt |
| S2 | \(h\) flyttar seg ikkje i nokon modell når \(\gamma\) endrar seg | påstanden i P1-c om at kurva flyttar seg |

K4 følgjer av K1 og er ikkje eit uavhengig prov. Negativ kontroll: den frie formelen \(-\beta w\operatorname{Cov}(f,\hat\Lambda_k)\) vert brukt uendra på dei bundne retningane. Gjev ho null avvik, kan evalueringa ikkje skilje hypotesane.

## 4. Konkrete modellar, før og etter

Alle tal i 4.1–4.3 er eksakte brøkar med \(\beta w=\ln2\).

### 4.1 E1: to tilstandar

\(\mu=(1,1)\), \(\hat\Lambda_k=(0,4)\), \(\hat\Lambda_m=(0,8)\). Begge omsyna talar mot form 2, og m gjer det dobbelt så sterkt.

| Vekt på k | Bunden (\(\omega_m=1-\omega_k\)): \(\mathbb E[\hat\Lambda_k]\) | Bunden: \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) | Fri (vekt på m fast lik 3/4): \(\mathbb E[\hat\Lambda_k]\) |
| --- | --- | --- | --- |
| 0 | 4/257 ≈ 0,0156 | −4/257 | – |
| 1/4 | 4/129 ≈ 0,0310 | −4/129 | 4/129 ≈ 0,0310 |
| 1/2 | 4/65 ≈ 0,0615 | −4/65 | 4/257 ≈ 0,0156 |
| 3/4 | 4/33 ≈ 0,1212 | −4/33 | 4/513 ≈ 0,0078 |
| 1 | 4/17 ≈ 0,2353 | −4/17 | 4/1025 ≈ 0,0039 |

Frå same startpunkt (1/4, 3/4) halverer fri auke til 1/2 det estimerte avviket, medan bunden auke til 1/2 doblar det. I startpunktet er \(\operatorname{Var}(\hat\Lambda_k)=2048/16641\) og \(\operatorname{Cov}(\hat\Lambda_k,\hat\Lambda_m)=4096/16641\). Den frie deriverte har forteikn som \(-\operatorname{Var}<0\), den bundne som \(-(\operatorname{Var}-\operatorname{Cov})=+2048/16641>0\).

| Påstand | Føreseiing for bunden auke 1/4 → 1/2 | Utfall |
| --- | --- | --- |
| Naiv rival | \(\mathbb E[\hat\Lambda_k]\) stig ikkje | Felt: 4/129 → 4/65 |
| H_normalisert (T2, T5) | Stig, fordi \(\Delta\hat\Lambda_m=8>\Delta\hat\Lambda_k=4>0\) | Stemmer |
| T3 | \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) fell | Stemmer: −4/129 → −4/65 |

Lukka form: \(\mathbb E[\hat\Lambda_k]=4/(1+2^{8-4\omega_k})\), strengt stigande i \(\omega_k\). Dette er eit prov for dømet, ikkje berre fem målepunkt.

Det opphavlege motdømet i kontrollrekninga (\(\hat e_k=(0,1)\), \(\hat e_m=(0,2)\), \(\beta=2\)) i flyttal: bunden auke 0,2 → 0,8 gjev 0,0266 → 0,0832. Fri auke av \(\theta_k\) frå 0,4 til 1,6 med \(\theta_m=1{,}6\) fast gjev 0,0266 → 0,0082.

### 4.2 E2: tre tilstandar, omsorgsdelen i 6.701

Eigne omsyn \((0,10,20)\). Biletet er feilfritt: \(\hat\Lambda_{A|B}=e_B=(0,2,4)\). Kvar form har sitt eige nivå, så svarkurva er \(h(u)=u\), stigande og uendra for alle \(\gamma\).

| | \(\mathbb E[e_B]\) |
| --- | --- |
| \(\gamma_A=0\) | 684/349867 ≈ 0,0020 |
| \(\gamma_A=1/2\) | 44/1387 ≈ 0,0317 |
| \(\gamma_A=1\) | 4/7 ≈ 0,5714 |
| Fri vekt på biletet 0, 1, 2, 3 (eigne omsyn faste) | 0,0020 → 0,00049 → 0,00012 → 0,00003 |

Med stigande svarkurve og rett bilete stig avviket hos den andre når omsorgsdelen veks. Det agenten gav opp, verna den andre betre enn biletet gjer. For den frie vekta fell avviket, slik 6.711 seier.

### 4.3 E3: tre tilstandar, forteiknet snur

\(\hat\Lambda_k=(0,4,8)\), \(\hat\Lambda_m=(0,12,0)\). For \(\omega_k=0,\ 1/4,\ 1/2,\ 3/4,\ 1\) er \(\mathbb E[\hat\Lambda_k]=4,\ 684/427,\ 44/91,\ 2/11,\ 24/91\). Verdien fell til 3/4 og stig så (0,182 → 0,264). \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\) fell heile vegen: 10920/2731, 680/427, 40/91, 0, −40/91. Under binding finst det altså ingen global monotoniregel for k åleine, berre den lokale forteiknsregelen i T2 og strukturvilkåret i T4.

## 5. Numerisk resultat

Tala er frå første køyring. Sluttkode 0, «Uventa utfall: ingen». Ei kontrollkøyring etterpå, med uendra fil, enda på same sluttline; resten av utskrifta vart ikkje jamført line for line.

| Kriterium | Tilfeldige (300 modellar) | Adversarielle (11 modellar) |
| --- | --- | --- |
| K1 fri: avvik frå \(-\operatorname{Cov}(f,\hat\Lambda_k)\) | 0 av 3800 | 0 av 72 |
| K1 bunden: avvik frå \(-\beta w\operatorname{Cov}(f,\hat\Lambda_k-\hat\Lambda_{\text{rest}})\) | 0 av 12800 | 0 av 153 |
| K2 fri monotoni broten, derivert / endeleg | 0 av 900 / 0 av 2700 | 0 av 23 / 0 av 69 |
| K4 forteikn feil | 0 av 2900 | 0 av 37 |
| N2 differansen stig, derivert / endeleg | 0 av 2900 / 0 av 2900 | 0 av 48 / 0 av 47 |
| K3 \(\mathbb E[\hat\Lambda_k]\) stig, parflytting, derivert / endeleg | 236 av 2000 / 244 av 2000 | 5 av 26 / 5 av 25 |
| K3 \(\mathbb E[\hat\Lambda_k]\) stig, proporsjonal, derivert / endeleg | 76 av 900 / 77 av 900 | 3 av 22 / 4 av 22 |
| Negativ kontroll: fri formel på bunden vekt, avvik | 12800 av 12800 | 131 av 153 |

| Kriterium | Utfall |
| --- | --- |
| N3 tilstrekkeleg: stiging i komonotone modellar | 0 av 201 |
| N3 naudsynt: brotpar der konstruert grunnfordeling ikkje gjev stiging | 0 av 296 |
| N3, teljing: frie modellar som er komonotone av seg sjølv / som stig med si eiga grunnfordeling | 12 av 99 / 19 av 99 |
| S1: \(h\) endra under fri vekt | 0 av 200 |
| S3: brot på 6.711 for fri vekt med monoton \(h\) | 0 av 66 (26 stigande, 40 fallande) |
| S2: \(h\) flyttar seg når \(\gamma\) går 0,2 → 0,8 | 200 av 200 |
| S4, teljing: \(h\) stigande ved begge \(\gamma\), \(\mathbb E[e]\) stig likevel | 4 av 17 |

Merknader til tala:

- Andelane 236/2000 og 76/900 er eigenskapar ved generatoren (uavhengige, jamt fordelte estimat). Dei seier ikkje kor ofte dette hender i formgjeving.
- A10 gav inga stiging i den deriverte i det fastsette punktet (0,75; 0,25) med \(\beta w=2\). Forteiknsskiftet kjem seinare på vegen og syner berre i det endelege steget til \(\omega_k=1\). Ikkje-monotonien er difor dokumentert av E3, ikkje av A10. Modellen er ikkje justert.
- Éi av dei fem adversarielle stigingane i den deriverte er A11, der \(\omega_m=0\). Den retninga går ut av simpleksen og er ikkje ei tillaten flytting. Innanfor simpleksen er talet 4 av 25.
- A6, A7 og A8 er svake prøver: dei deriverte er nær null eller nøyaktig null.
- Fordelinga av stigingane per adversariell modell er rekna i ei eiga hjelpekøyring som importerte testfila utan å endre ho.

## 6. Prov og demonstrasjon

| Slag | Kva | Styrke |
| --- | --- | --- |
| Prov | T1–T6 i kapittel 2 | Held for alle endelege modellar under føresetnadene. Kontrollerte for hand, ikkje maskinverifiserte |
| Eksakt rekning | E1, E2, E3 | Brøkrekning utan flyttal. Provar at motdøma finst, og dermed at den naive rivalen er falsk som allmenn påstand |
| Numerisk demonstrasjon | K1, K2, K4, N2, N3, S1–S4 | Samsvar innanfor toleranse i eit fastsett modellsett. Kan avsløre feil i utleiing eller kode. Provar ikkje setningane |
| Teljing | K3-andelane, S4, N3 for frie modellar | Skildrande. Ingen krav knytte til tala |

Hypotesane vart utleia før testen vart skriven, og dei adversarielle modellane er valde med kjennskap til teorien. A1 og A4 er dei kjende motdøma frå kontrollrekninga. Den numeriske delen er difor ein kontroll av rekning og kode, ikkje uavhengig støtte.

## 7. Framlegg til minste retting

Ikkje utført. `formlaere.tex` er urørt.

### 7.1 Proposisjon 6.673

```diff
-Meir prioritering kan ikkje auke det estimerte avviket langs same omsyn.
+Meir fri vekt kan ikkje auke det estimerte avviket langs same omsyn. Er vektene bundne til sum 1 som i 6.61, er auken ei flytting frå andre omsyn, og 6.6742 avgjer forteiknet.
```

Første setning er identisk med rettinga som alt ligg i `framlegg-rettingar-2026-11.patch`. Ho er nok til å gjere proposisjonen sann. Andre setning er tillegget frå dette forsøket. Tilråding: ta med begge. Utan den andre setninga får lesaren ikkje vite kva som gjeld for prioritering slik 6.61 definerer ho, og svaret står alt i 6.6742. Tillegget fører ikkje inn ny matematikk.

Grunngjeving: T1 dekkjer den første setninga, T2 og E1 den andre.

### 7.2 Proposisjon 6.711

```diff
-Ho endrar seg ikkje når berre vekta til biletet veks. Fell ho ingen stad, kan meir omsorg ikkje auke avviket hos den andre i middel. Stig ho ingen stad, kan meir omsorg ikkje minske det.
+Ho endrar seg ikkje når berre vekta til biletet veks. Fell ho ingen stad, kan meir fri vekt på biletet ikkje auke avviket hos den andre i middel. Stig ho ingen stad, kan meir fri vekt på biletet ikkje minske det.
```

Proposisjonen er rett dersom «meir omsorg» tyder det same som «berre vekta til biletet veks» i setninga før. Lesen saman med 6.701, der omsorg er delen \(\gamma_A\) som vert teken frå eigne omsyn, er han feil (E2). Rettinga fjernar tvitydet og brukar same ordlag som 6.71 («den frie vekta til biletet»).

Eit mogleg tillegg, som ikkje høyrer til den minste rettinga: «Veks omsorgsdelen \(\gamma_A\) i 6.701, minkar vekta på eigne omsyn samstundes. Då kan både kurva og forteiknet flytte seg.» Det fører ein ny påstand inn i proposisjonen, og forfattaren bør avgjere om han høyrer heime der eller i notatet.

### 7.3 Ikkje foreslått

T3 og T4 er nye resultat. Dei er ikkje foreslåtte som proposisjonar, fordi `program.md` krev at ei utviding først toler uavhengig kontroll. 6.674, 6.6741 og 6.675 har same ordbruk («meir prioritering», «kvar auke av vekta»). Saka ber berre om 6.673 og eventuelt 6.711, så dei er ikkje tekne med her.

## 8. Eksisterande kontrollar

| Kommando | Utfall |
| --- | --- |
| `python traktat/revisjon/test_autoresearch_003.py` | Sluttkode 0, ingen uventa utfall |
| `python traktat/revisjon/kontrollrekning-2026-11.py` | Sluttkode 0, 22 liner, «Uventa utfall: ingen». Motdøma til 6.673 (0,0266 → 0,0832) og 6.711 (0,0152 → 0,1844) er uendra |
| `python -m unittest discover -s autoresearch -p "test_*.py"` | 5 testar, OK |
| `python autoresearch/harness.py status` | 491 proposisjonar (118, 27, 20, 16, 145, 112, 53), 150 kandidatpar, 0 fulltekstvalideringar |
| `python autoresearch/harness.py check` på kortet i kapittel 9, lagra i ei mellombels fil utanfor repoet | `structurally_valid: true`, 0 evidenspostar |

`harness.py check` kontrollerer strukturen på kortet, ikkje innhaldet.

## 9. Forsøkskort

```json
{
  "id": "0003-vektforskyving",
  "proposition": "6.673",
  "claim": "Monotonisetninga i 6.673 gjeld fri vekt. Under sum 1 (6.61) stig E[Λ̂_k] lokalt nett når Cov(Λ̂_k, Λ̂_m) > Var(Λ̂_k); berre differansen E[Λ̂_k − Λ̂_m] er garantert ikkje-stigande.",
  "rival": "Den frie monotonisetninga gjeld uendra for normaliserte vekter: E[Λ̂_k] kan ikkje stige når ω_k aukar.",
  "falsifier": "Eitt avvik over toleransen mellom numerisk derivert og kovariansformel; fri auke som hevar E[Λ̂_k]; flytting m→k som hevar E[Λ̂_k − Λ̂_m]; stiging i ein komonoton modell; eller null stigingar under binding.",
  "measurement": "python traktat/revisjon/test_autoresearch_003.py, frø 2026/2027/2028, toleranse 1e-6, eksakte brøkdøme E1–E3.",
  "baseline": "Den frie formelen −βw·Cov(f, Λ̂_k) brukt uendra på bunden vekt (avvik i 12800 av 12800 tilfeldige tilfelle).",
  "status": "needs-human-review",
  "evidence": []
}
```

## 10. Kva som kan felle utvidinga, og kva som står uvisst

**Resultat som feller, innanfor modellen**

1. Ein endeleg modell med fast \(\mu\), fast \(D\) og vektuavhengige estimat der fri auke av \(\theta_k\) hevar \(\mathbb E[\hat\Lambda_k]\). Det feller T1 og 6.673.
2. Ein modell der flytting frå m til k hevar \(\mathbb E[\hat\Lambda_k-\hat\Lambda_m]\). Det feller T3.
3. Eit komonotont par \((\hat\Lambda_k,\hat\Lambda_k-\hat\Lambda_m)\) med stiging, eller eit brotpar der inga grunnfordeling gjev stiging. Det feller T4.
4. Ein reknefeil i E1–E3. Dømene er små nok til å reknast for hand.

**Vilkår som avgrensar rekkjevidda**

- Estimata må stå fast når vektene endrar seg. Dersom meir prioritering òg gjev betre estimat, gjeld verken T1 eller T2. Teksten held omhug og kunnskap frå kvarandre (6.674), men seier ikkje at dei er uavhengige i praksis.
- Grunnfordelinga og rommet må stå fast. Dette er same vilkåret som P1-b peikar på for 6.614.
- \(D\) er endeleg i alt som er rekna her. For kontinuerlege rom krevst integrerbarheit. Det er ikkje prøvd.
- T4 er eit vilkår over alle grunnfordelingar. For ei gjeven \(\mu\) kan \(\mathbb E[\hat\Lambda_k]\) falle heile vegen sjølv om vilkåret er brote. Av dei 99 frie modellane braut 87 vilkåret, og 68 av dei synte inga stiging med si eiga grunnfordeling.
- Jamføringa mellom \(\operatorname{Cov}\) og \(\operatorname{Var}\) er i toleranseeiningar. Eit omsyn med trong toleranse skil formene sterkare og vernar lettare andre omsyn som sideverknad.

**Uvisse**

- Om vektene til verkelege agentar er bundne til ein sum, er eit empirisk spørsmål som dette forsøket ikkje rører. Er dei frie, står 6.673 som han er. Men då er 6.61 og 6.701 feil skildring.
- Provet for T4 er nytt i denne køyringa og er lese av éin kontrollør. Det bør lesast av ein til før det vert brukt i teksten.
- Sentraldifferansen har avkortingsfeil av orden \(h^2\). Toleransen er vald med om lag fire tiarpotensar margin i dei fastsette modellane. For estimat med mykje større spenn enn 1000 er ho ikkje prøvd.
