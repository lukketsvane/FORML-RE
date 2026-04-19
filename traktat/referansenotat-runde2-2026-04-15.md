# Referansenotat — runde 2, 2026-04-15

**Føremål:** Plan for fem ko-relaterte tillegg som krev meir tekstlig avveging enn runde 1. Kvart blokk-forslag har:
- Eksakt formulering for både notat-tillegg og superscript-plassering
- Kritisk vurdering av risiko
- Krav til godkjenning før implementering

**Numrenes startpunkt:** [71]–[78]. Totalt åtte nye nummererte refs.

---

## Blokk A — Mereologi-fundament for 1.2 ([71] Varzi)

### Bakgrunn
Prop 1.2 hevdar: *"Eit objekt er den enklaste bestanddelen i ein konfigurasjon. Objektet er udeleleg og uforanderleg."*

Eksisterande notat for 1.2: *"Objektet er udeleleg i den forstand at vidare dekomponering øydelegg den kausale kapasiteten me er interesserte i."*

Klassisk mereologi (Simons 1987, Varzi SEP 2016, Smid 2015) definerer udelelegheit *formelt*: eit atom er det som ikkje har eigne deler. Traktatens udelelegheit er *operasjonell*: dekomponering øydelegg kausal rolle.

### Risiko
Å siter mereologi i sjølve prop 1.2 ville implisere at traktaten tar mereologiens ramme. Det gjer han ikkje. Han tar ein operasjonell variant. Mereologi-sitering høyrer i notatet, ikkje i proposisjonen.

### Forslag
**Numrenes utviding:** Berre éi ny ref — Varzi 2016 SEP som kanonisk inngang. Simons 1987 og Smid 2015 ligg i bib for vidare lesing.

```
[71] Varzi, A. (2016). Mereology. I The Stanford Encyclopedia of
     Philosophy. Metaphysics Research Lab, Stanford University.
```

**Notat-utviding (erstatt eksisterande 1.2-notat):**

> **1.2** Objektet er udeleleg i den forstand at vidare dekomponering øydelegg den kausale kapasiteten me er interesserte i. Under det nivået finst det framleis fysikk; men ikkje formgjeving. Den klassiske mereologien [71] definerer atomet formelt — det utan eigne deler; vår variant er operasjonell — det utan kausalt verksame deler i den valde klassen. Distinksjonen er substansiell, ikkje terminologisk: same fysisk gjenstand kan vere atom i éin klasse og samansett i ein annan.

**Inga superscript-tillegg i prop 1.2 sjølv** — notatet er nok.

### Vurdering
Sterk match. Tilfører filosofisk presisjon utan å forskuva traktatens ståstad. Klar å implementere etter godkjenning.

---

## Blokk B — Bateson 1979 *Mind and Nature* ([72])

### Bakgrunn
Prop 7.13 hevdar: *"Arkivet er ikkje ei skulding. Det er eit faktum. Same faktumet som gjer geologi leseleg, gjer design leseleg."*

Prop 6.111 hevdar: *"Reduksjonisme og holisme er komplementære. Begge er sanne; ingen er tilstrekkeleg åleine."*

Prop 1.13 hevdar: *"Forklaringa ligg i relasjonen mellom den manifesterte konfigurasjonen og det totale settet av konfigurasjonar som var moglege, men ikkje vart realiserte."*

Bateson 1979 *Mind and Nature: A Necessary Unity* argumenterer for at mønstera (pattern that connects) er felles på tvers av biologi, kognisjon, økologi. Hans "necessary unity" er nøyaktig den parallellen prop 7.13 påkalla.

### Risiko
Bateson har ein laus, essayistisk stil. Risikabelt å siter han som hovudkjelde for ein streng påstand. Best brukt som *parallell*-kjelde, ikkje som autoritet.

### Forslag
**Ny nummerert ref:**

```
[72] Bateson, G. (1979). Mind and Nature: A Necessary Unity. E.P. Dutton.
```

**Superscript-tillegg:**
- **7.13** (no utan ref) → `\textsuperscript{72}`
- **6.111** (no utan ref) → `\textsuperscript{72}`

**Notat-tillegg (ny entry):**

> **7.13** Geologi/biologi/design-parallellen er Bateson [72] sin "pattern that connects" — at same forklaringsmønsteret (mønster i residue ber spor av prosessen som produserte det) gjeld på tvers av domena. Bateson argumenterer for ein "nødvendig einskap" mellom natur og tanke; vi tek ein svakare stilling — same lesningsapparatet kan brukast, utan å hevde ontologisk einskap.

**Inga ekstra notat for 6.111** — superscript tilstrekkeleg.

### Vurdering
God match for 7.13 (geologi-parallellen er signaturen til Bateson). 6.111-koplinga (reduksjonisme/holisme) er sekund\u00e6r men passar. Tilrår implementering.

---

## Blokk C — Hoffmeyer 2008 *Bateson + Peirce* ([73])

### Bakgrunn
Prop 2.14 (no allereie [12, 55, 56]): *"Ein klasse er avgrensa gjennom delt affordansestruktur."*

Brier 2020 [56] hevdar at affordansar er teikn (semiotisk). Hoffmeyer 2008 forklarar opphavet til denne påstanden — ho byggjer på Bateson sitt mønster-omgrep og Peirce sin semiotikk.

### Risiko
Prop 2.14 har allereie tre referansar (Gibson, RietveldKiverstein, Brier). Å legge til ein fjerde overbelaster proposisjonen. Hoffmeyer høyrer i notatet, ikkje i superscript.

### Forslag
**Ny nummerert ref:**

```
[73] Hoffmeyer, J. (2008). Bateson and Peirce on the pattern that
     connects and the sacred. I A legacy for living systems. Springer.
```

**Inga superscript-tillegg i prop 2.14.**

**Notat-tillegg (ny entry):**

> **2.14** Den semiotiske utvidinga av affordansomgrepet [56] har sin teoretiske rot i Hoffmeyer [73] si syntese av Bateson og Peirce. Hoffmeyer plasserer affordans i ei kjede objekt → mønster → teikn → tolking; Brier formaliserer dette for designkontekst. Vår bruk av "affordansestruktur" er nær Gibson [12] (objektivt relasjonell), men opnar for den semiotiske vidaref\o{}ringa når klassen krev det.

### Vurdering
Sek\unders\o{}rt match. Hoffmeyer er nyttig som genealogi for [56], men ikkje sjølvstendig nødvendig. Tilrår å implementere med tanke p\aa{} at notatet styrkar [56]-sitatet, ikkje erstattar det. Klar etter godkjenning.

---

## Blokk D — Kazakci/Ma/LeMasson for 5.72-noten ([74]–[76])

### Bakgrunn
Prop 5.72 (no [11, 17]): reduksjonsteoremet, viser SG og CK som degenererte spesialtilfelle.

Eksisterande 5.72-notat (mitt eige tillegg fr\aa{} forrige runde): *"Reduksjonsteoremet klargjer tilhøvet til dei to kjeldetradisjonane..."*

CK-tradisjonen er meir enn berre Hatchuel-Weil 2003/2009. Den har modnast gjennom:
- LeMassonWeilHatchuel 2010 *Strategic Management of Innovation and Design* (kanonisk bok)
- Kazakci 2015 *C-K, an engineering design theory?* (refleksiv kritikk)
- Ma 2023 *Simulating design theory using LLM agents* (moderne datasimulering)

Reduksjonsteoremet sin relevans aukar når CK-litteraturens rikdom blir synleg.

### Risiko
For mange CK-referansar i ein note kan tippe balansen — traktatens tese er at SG og CK er likeverdige delstrukturar. Å overdimensjonere CK kunne skuffe Stiny-tradisjonens vekt.

### Forslag
**Tre nye nummererte refs:**

```
[74] Le Masson, P., Weil, B. & Hatchuel, A. (2010). Strategic
     Management of Innovation and Design. Cambridge University Press.

[75] Kazakçi, A. O. (2015). C-K, an engineering design theory?
     Proceedings of the International Conference on Engineering Design.
     Design Society.

[76] Ma, M. (2023). Simulating design theory using LLM agents:
     A case study of C-K theory. Co-Design Lab, UC Berkeley.
```

**Inga superscript-tillegg i prop 5.72 sjølv** (ho har allereie [11, 17] frå runde 1).

**Notat-utviding (etter eksisterande 5.72-note):**

> **5.72 (forts.)** CK-tradisjonen har modnast gjennom tre tiår: fr\aa{} dei opphavlege artiklane [16, 17] gjennom den kanoniske boka [74], til refleksive kritikkar av om CK er ein \textit{engineering} eller meir generell teori [75], til moderne dataeksperiment med LLM-agentar [76]. Reduksjonsteoremet vårt relaterer seg til heile denne tradisjonen — kvart steg i CK-modninga er framleis innanfor det same grensetilfellet av kjerne-likninga. Tilsvarande modning på Stiny-sida ([11, 13, 18]) gjer den parallelle påstanden gyldig: båe tradisjonane utviklar seg innanfor sitt eige grensetilfelle, ikkje på tvers.

### Vurdering
Sterk historisk forankring. Note-utvidinga gjev spesifikt det poenget brukaren spurde etter: at båe tradisjonane modnast i sin eigen grensesituasjon. Risikoen for ubalanse er låg fordi noten eksplisitt nemner Stiny-sidas parallelle modning. Tilrår implementering.

---

## Blokk E — Michl-serien ([77] 1989, [78] 2014)

### Bakgrunn
Eksisterande [15] Michl 1995 er den kanoniske kjelda for traktaten sin form-følger-funksjon-kritikk.

Michls produksjon spenner over 25 \aa r:
- 1989 *On forms following functions and post-modernism* (norsk røter)
- 1995 *Form follows WHAT?* (kanonisk midtpunkt — eksisterande [15])
- 2002 *On seeing design as redesign* (skandinavisk konsolidering)
- 2007 *\AA{} se design som redesign* (norsk variant)
- 2009 *En sak mot det modernistiske apartheidregimet* (politisk konsolidering)
- 2014 *A case against the modernist regime in design education* (engelsk konsolidering)
- 2024 SNL-innf\o{}ring *form f\o{}lger funksjon* (oppslagsverk)

### Risiko
\AA{} sitere alle sju Michl-tekstar overdriv ein kjelde. Best: behold [15] som hovudreferanse, og legg til to som dekker historisk-genealogisk spenn — den f\o{}rste norsk-spr\aa{}klege artikkelen (1989, røter) og den engelske konsolideringa (2014).

### Forslag
**To nye nummererte refs:**

```
[77] Michl, J. (1989). On forms following functions and post-modernism.
     Pro Forma, 1, 5--15.

[78] Michl, J. (2014). A case against the modernist regime in design
     education. Archnet-IJAR, 8(2), 36--46.
```

**Superscript-tillegg:**
- **2.101** (no `\textsuperscript{15}`) → `\textsuperscript{15,\,77,\,78}`
- **4.51** (no utan ref) → `\textsuperscript{15,\,78}`

Begrunnelse: 2.101 er den prinsipielle Michl-tesen ("forma er det som st\aa r att n\aa r trykka har utelukka alt anna"); 4.51 er Michl-tesen i operasjonell form ("\aa{} redusere alle seleksjonstrykk til eitt er systematisk blindskap"). Andre Michl-relevante prop (6.3, 6.32) har allereie nok sitat.

**Notat-tillegg (ny entry):**

> **15, 77, 78** Michl-serien dekkjer 25 \aa r: norsk r\o{}ter [77], kanonisk midtpunkt [15], engelsk konsolidering [78]. Saman utgjer dei den teoretiske basen for traktaten sin form-f\o{}lger-funksjon-kritikk. Den fulle bibliografien (Michl 1989, 1995, 2002, 2007, 2009, 2014, 2024) er tilgjengeleg i \texttt{references.bib}.

### Vurdering
Klassisk balanse: utvid utan \aa{} bl\o{}re. Norsk-engelsk-spennet er meiningsfullt for ein nynorsk traktat som vil markere internasjonal relevans. Tilr\aa r implementering.

---

## Samla budsjett: 8 nye numrar [71]–[78]

| Nr | Ref | Plassering |
|---|---|---|
| [71] | Varzi 2016 SEP Mereology | notat 1.2 |
| [72] | Bateson 1979 *Mind and Nature* | superscript 7.13, 6.111 + notat 7.13 |
| [73] | Hoffmeyer 2008 | notat 2.14 |
| [74] | LeMassonWeilHatchuel 2010 | notat 5.72 |
| [75] | Kazakci 2015 | notat 5.72 |
| [76] | Ma 2023 | notat 5.72 |
| [77] | Michl 1989 | superscript 2.101 + notat 15/77/78 |
| [78] | Michl 2014 | superscript 2.101, 4.51 + notat 15/77/78 |

**Tre nye superscript-tillegg i proposisjonar.tex:**
- 6.111 → \textsuperscript{72}
- 7.13 → \textsuperscript{72}
- 2.101 → \textsuperscript{15,\,77,\,78}
- 4.51 → \textsuperscript{15,\,78}

**Fire nye notat-entryar i traktat.tex:**
- 1.2 (utvida — erstattar eksisterande)
- 2.14 (ny)
- 7.13 (ny)
- 5.72 (forts., bygd p\aa{} eksisterande)
- 15/77/78 (ny — Michl-serie kommentar)

---

## Risikoanalyse

| Blokk | Risiko | Mitigering |
|---|---|---|
| A Mereologi | Filosofisk omveg | Hold i notat, ikkje proposisjon |
| B Bateson | Essayistisk autoritet | Markert som "parallell", ikkje "fundament" |
| C Hoffmeyer | Tredjeparts genealogi | Hold i notat, styrkar [56] |
| D CK-utviding | CK-overvekt mot SG | Eksplisitt parallellpåstand om Stiny-modning |
| E Michl-serie | Sjølv-sitering av kjelde | Avgrensa til 2 nye refs (norsk r\o{}ter + engelsk) |

---

## Bonus-kandidatar oppdaga under granskinga (Blokk F–I)

Under arbeidet med Blokk A–E vart fire ekstra sterke kandidatar synlege. Dei fyller \o{}penberre hol som ikkje sto i opphavelege lista.

### Blokk F — Niche construction ([79] Odling-Smee, Laland, Feldman 2003)

**Bakgrunn.** Allereie i bib som `OdlingSmeeLalandFeldman2003`, men utan nummerert oppf\o{}ring og aldri sitert i proposisjonane. Dette er eit stort hol: nicheconstruction-teori (organismar konstruerer sj\o{}lv seleksjonsmilj\o{}et sitt) er nesten ein-til-ein parallell til prop 4.4 ("formrommet ekspanderer kumulativt; ... materialstraumar driv landskapsendringa") og prop 6.4 ("kvar realisert form utvidar det kjende og forskyver grensa til det n\ae rliggande moglege"). Stiavhengigheit (Arthur [14]) gjev tids\-mekanismen; nicheconstruction gjev den evolusjonsteoretiske parallellen.

**Forslag:**

```
[79] Odling-Smee, F. J., Laland, K. N. & Feldman, M. W. (2003).
     Niche Construction: The Neglected Process in Evolution.
     Princeton University Press.
```

- **4.4** (no `\textsuperscript{13,\,59,\,60}`) → `\textsuperscript{13,\,59,\,60,\,79}`
- **6.4** (no utan ref) → `\textsuperscript{14,\,79}`

**Notat-tillegg (ny entry):**

> **4.4 / 6.4** Nicheconstruction-teorien [79] formaliserer at organismar (eller agentar) modifiserer dei seleksjonstrykka som verkar p\aa{} dei sj\o{}lv. P\aa stand 4.4 generaliserer dette til formverda: kvar realisert konfigurasjon endrar tilpassingslandskapet for den neste agenten. Distinksjonen mellom passiv navigasjon og aktiv landskapsutviding er fundamental.

**Vurdering.** \O{}penberre forbetring; overraskande at den ikkje var med fr\aa{} starten. Sterkt tilr\aa dd.

---

### Blokk G — Pye 1968 *Workmanship* — superscript-tillegg utan ny nummer

**Bakgrunn.** Allereie [26] i nummerert liste, men sitert berre i kommentarfeltet (5.4-noten). Risiko/vissheits-handverk-distinksjonen er direkte relevant for prop 5.4 (substratet som null-ordens agent) og prop 5.5 (l\ae ring som ekspansjon).

**Forslag:** ingen ny nummer, berre superscript:
- **5.4** (no utan ref) → `\textsuperscript{26}`

**Vurdering.** Null-kostnads-tillegg som ankrar 5.4 i etablert handverkslitteratur. Tilr\aa dd.

---

### Blokk H — Norman 2013 *Design of Everyday Things* ([80])

**Bakgrunn.** Norman gjorde affordans-omgrepet til allmenneige i designfaget. Hans skilje mellom designar-perspektiv og brukar-perspektiv er nett kjernen i prop 6.31: *"For brukaren er stilarten ikkje eit symptom; han er eit grensesnitt."* Norman har den kanoniske formuleringa av denne distinksjonen (signifier vs.\ affordance fr\aa{} brukarens st\aa{}stad).

**Forslag:**

```
[80] Norman, D. A. (2013). The Design of Everyday Things (Revised
     ed.). Basic Books.
```

- **6.31** (no utan ref) → `\textsuperscript{80}`
- **6.311** (no utan ref) → `\textsuperscript{80}`

**Vurdering.** Kanonisk i designfaget; eit slikt sitat manglar i traktaten utan tilhengar-grunn. Sterkt tilr\aa dd.

---

### Blokk I — CussatBlanc, Harrington & Banzhaf 2018 *Artificial Gene Regulatory Networks* ([81])

**Bakgrunn.** Prop 5.4 hevdar at substratet er ein null-ordens agent. Prop 5.41 illustrerer: *"Biologisk vev navigerer via bioelektrisk polarisering;\textsuperscript{22, 24} menneskeleg praksis via materiell friksjon..."*. Levin-refsane dekkjer bioelektrisk; men sjølve substrat-som-agent-arkitekturen er lengst utvikla i kunstig-GRN-litteraturen (gene regulatory networks som beregner og navigerer). Cussat-Blanc-Harrington-Banzhaf 2018 er den kanoniske oversiktsartikkelen.

**Forslag:**

```
[81] Cussat-Blanc, S., Harrington, K. & Banzhaf, W. (2018). Artificial
     gene regulatory networks---A review. Artificial Life, 24(4).
```

- **5.4** (no utan ref) → `\textsuperscript{26,\,81}` (saman med Pye [26] fr\aa{} Blokk G)

**Vurdering.** Tilf\o{}rer datalogisk-biologisk fundament for substrat-som-agent. Komplementerer Levin-refsane. Tilr\aa dd.

---

## Samla budsjett etter Blokk A–I: 11 nye numrar [71]–[81]

| Nr | Ref | Plassering |
|---|---|---|
| [71] | Varzi 2016 SEP | notat 1.2 |
| [72] | Bateson 1979 | superscript 7.13, 6.111 + notat 7.13 |
| [73] | Hoffmeyer 2008 | notat 2.14 |
| [74] | LeMassonWeilHatchuel 2010 | notat 5.72 |
| [75] | Kazakci 2015 | notat 5.72 |
| [76] | Ma 2023 | notat 5.72 |
| [77] | Michl 1989 | superscript 2.101 + notat 15/77/78 |
| [78] | Michl 2014 | superscript 2.101, 4.51 + notat 15/77/78 |
| [79] | OdlingSmee mfl 2003 | superscript 4.4, 6.4 + notat 4.4/6.4 |
| [80] | Norman 2013 | superscript 6.31, 6.311 |
| [81] | CussatBlanc mfl 2018 | superscript 5.4 |

**+ Pye [26] → superscript 5.4** (ingen ny nummer)

**Totalt:** 11 nye nummererte refs, 9 nye superscript-tillegg, 5 nye notat-entryar.

---

## Krav til godkjenning

For kvar blokk: bekreft eller juster:

- **Blokk A** Varzi mereologi → notat 1.2
- **Blokk B** Bateson 1979 → superscript 7.13, 6.111 + notat
- **Blokk C** Hoffmeyer 2008 → notat 2.14
- **Blokk D** Le Masson + Kazakci + Ma → notat 5.72
- **Blokk E** Michl 1989 + 2014 → superscript 2.101, 4.51 + notat
- **Blokk F** Odling-Smee → superscript 4.4, 6.4 + notat *(NY)*
- **Blokk G** Pye [26] → superscript 5.4 *(NY, ingen ny nummer)*
- **Blokk H** Norman 2013 → superscript 6.31, 6.311 *(NY)*
- **Blokk I** Cussat-Blanc → superscript 5.4 *(NY)*

Etter godkjenning: implementer i ei \o{}kt, bygg PDF, ferdig.
