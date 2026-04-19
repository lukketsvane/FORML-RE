# Revisjonsplan v2 — *Proporsjonsgrammatikk og formgjevarkompetanse*

**Dato:** 2026-04-15
**Kjernekrav frå brukaren:**
1. Boksane rundt omhug/blindflekk: stipla omriss, ingen fyllfarge, full spaltebreidd
2. Grundig søk på om andre har gjort det same (SG/CK på desse fire systema)
3. Kvantitative styrkingar der mogleg
4. Vis matematisk at SG og CK er *degenererte spesialtilfelle* av Formlære
5. Fjern Fields-Levin-sitat når det er unødig
6. Forklara meir direkte; vis matematikken
7. APA 7, knapp nynorsk

---

## 1. Kritiske forskingsfunn (nytt sidan v1)

### 1.1 Matrise: SG/CK per system (bekrefta)

| System | SG-formalisering? | CK-formalisering? |
|---|---|---|
| Modulor | *Ingen full SG*; parametrisk panel-enumerasjon (Watanabe, 2020) | **INGA** — ren nyheit |
| Palladio | Stiny & Mitchell (1978a) *kanonisk* + Benros m.fl. (2012) | **INGA** — ren nyheit |
| Van der Laan | **INGA** — ren nyheit | **INGA** — ren nyheit |
| Ken/tatami | Knight (1981) *ikkje Stiny 1980* — korrigering! | **INGA** — ren nyheit |
| SG ⊎ CK sameint | **Ingen publisert forsøk** — sterkaste nyheitskravet | |

### 1.2 Kvantitativ styrking tilgjengeleg

- **Stiny & Mitchell (1978b) *Counting Palladian plans*** — talde opp Palladios 10 eksisterande + 220 moglege konfigurasjonar fr\aa{} grammatikken. Dette er ein *hard kvantitativ referanse* som vi kan bygga p\aa{}.
- **Watanabe (2020)** — enumererte Modulor-panelkombinasjonar algoritmisk.
- Van der Laan og ken/tatami: ingen kvantitativ litteratur — vi kan introdusera f\o{}rste tellingar sj\o{}lv.

### 1.3 Feilsitering \aa{} retta opp
- **Stiny (1980) — Froebel-paperet — handlar om kindergarten-klossar, IKKJE tatami.** Vi feilsiterte han for tatami. Rett referanse er **Knight (1981) *The forty-one steps***, som gjeld japansk te-rom p\aa{} ken/tatami-gridet.
- Retta i bib: Knight 2000 → Knight 1981; fjern Stiny 1980 fr\aa{} tatami-seksjonen.

### 1.4 CK-formalisering \aa{} orientera seg mot
- Kazakci (2009) *Imagining Knowledge* — formaliserer CK med termlogikk (C-K-E). *Bruker ikkje SG*. Vi kan sitera som bevis p\aa{} at CK-sida har ein formell tradisjon som vi relaterer Forml\ae re til.

---

## 2. Matematisk kjerne: reduksjonsproposisjonen

**Nytt tillegg til § 2** (erstatttar Fields-Levin-formulering med ei strammare):

### Proposisjon 1 (reduksjon)
> Designrommet $\mathbf{D} = (M, \Pi, \mathbf{SG}, \mathcal{L}, A)$ reduserer til:
>
> **(i) Rein shape grammar** $\langle S, R, \omega\rangle$ n\aa r seleksjonstrykket forsvinn og agent-hierarkiet kollapsar:
> $$\nabla_{C(A)}\mathcal{L} \equiv 0, \quad |A| = 1, \quad \Pi = (M, \emptyset, \emptyset)$$
> D\aa{} gjev Form-likninga $\mathrm{Form} = \mathbf{SG}(0)$, dvs.\ heile det genererte spr\aa ket $L(\mathbf{SG})$ utan seleksjon.
>
> **(ii) Rein CK-teori** $\langle K, C, \{\delta_+, \delta_-, \kappa, \pi\}\rangle$ n\aa r den geometriske strukturen kollapsar:
> $$\mathbf{SG} = \mathrm{id}_M, \quad \mathcal{L}(x) = \mathbf{1}_K(x)$$
> D\aa{} blir rule-applikasjonen i $R$ redusert til fire CK-operatorar: utviding i $K$, utviding i $C$, disjunksjon $C\rightarrow K$, konjunksjon $K\rightarrow C$.

**Bevis-skisse (~40 ord, kan st\aa{} i \S 2.3 eller som fotnote):**
(i) Utan seleksjonstrykk kan alle $s \in L(\mathbf{SG})$ realiserast likt; Form kollapsar til grammatikken sitt spr\aa k. (ii) Utan geometrisk struktur i $M$ er rule-applikasjonen ekvivalent med boolsk partisjonsendring; CK-operatorane er akkurat desse fire partisjonsoperatorane p\aa{} $(K, C)$.

**Hovudargumentet artikkelen so gjer synleg:** Formlære = SG + CK + kompetanse-lag; dei to historiske teoriane er det ein får n\aa r ein sl\aa{}r av seleksjonstrykket eller den geometriske strukturen. Verken Stiny-Gips eller Hatchuel-Weil kan uttrykka den andre sine operasjonar innanfor seg sj\o{}lv.

---

## 3. Strukturelle endringar (per seksjon)

### 3.1 Abstract
- Legg til eitt kvantitativt anker: "230 palladianske villaer i Stiny \& Mitchell (1978b) er den einaste systemet med formell tellingsresultat i litteraturen." Dette gjer nyheitskravet konkret.

### 3.2 § 1 Innleiing
- **Fjern Fields-Levin fr\aa{} likning (1)-framlegg.** Ny formulering:
  > Formlære (Finne, 2026) inneheld shape grammars og CK-teori som delstrukturar (Proposisjon 1) og tillegg eit kompetanselag som predikerer svikt.
  
- Kjerneformelen blir innf\o{}rt *etter* Proposisjon 1, ikkje f\o{}re. Les\aa{}ren f\aa{}r f\o{}rst logikken, so formalismen.

### 3.3 § 2 Teoretisk rammeverk — ny struktur
- **§ 2.1** Designrommet (uendra tabell av komponentar)
- **§ 2.2 NY**: *Proposisjon 1 (reduksjon)* — den over. Dette er artikkelen sitt matematiske hjarta.
- **§ 2.3** Form-likninga presenterast som *det full-kompetente tilfellet*: $\mathrm{Form} = \mathbf{SG}(\nabla_{C(A)}\mathcal{L})$. Proposisjon 1 viser kva som skjer n\aa r ein kollapsar delar av trippelet.
- **§ 2.4** Omhug og Proposisjon 7 (uendra, kortare)
- Slett den noverande tabell 1 "Operasjonar SG/CK/Komp/FL" — han repliserer Proposisjon 1 utan \aa{} leggja til noko. Erstatt han med Proposisjon 1-boksen.

### 3.4 § 4 Fire saker
- Kvar sak f\aa{}r eit **kvantitativt anker** der det finst:
  - Modulor: refereer Watanabe (2020) sitt tal p\aa{} panelkombinasjonar
  - Palladio: Stiny-Mitchell 1978b — 10 realiserte + 220 grammatiske, dvs.\ $|K|/|L(\mathbf{SG})| \approx 0{,}043$. Dette er f\o{}rste gong dette forholdstalet namngjevast formelt som CK-maskulatur.
  - Van der Laan: Padovan-sekvens-telling: n $\in \{3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 21\ldots\}$; kva rekken faktisk brukar (Abdij van Vaals) vs.\ kva han tillet.
  - Ken/tatami: $N$ tatami-matter per rom, kombinatorikk av layoutar for gitt $N$ (Knight 1981 har enumerasjon for $N=4{,}5{,}6$).

- **Boksstilen byt ut**: stipla omriss, ikkje fyllt, full spaltebreidd. Ny TeX:
  ```latex
  \newtcolorbox{omhugboks}{
    enhanced, breakable, colback=white, colframe=black!60,
    boxrule=0.4pt, borderline={0.4pt}{0pt}{black!60, dashed},
    arc=1pt, left=4pt, right=4pt, top=3pt, bottom=3pt,
    width=\columnwidth
  }
  ```
  Evt.\ enklare løysing utan `tcolorbox`: `\noindent\fbox{\parbox{\dimexpr\columnwidth-2\fboxsep-2\fboxrule}{...}}` med `\setlength{\fboxrule}{0.3pt}` og stipla-hack via `dashbox`.

### 3.5 § 5 Komparativ diagnose
- Legg til eit lite tal-tabell f\o{}r Figur 5 (kognitiv lyskjegle):

  | System | Skaar | Blindflekkar ($\leq 3$) | Sviktsignatur (historisk) |
  |---|---|---|---|
  | Modulor | 55/81 | Industr., Antrop., Ergon. | Industr., Antrop., Ergon. |
  | Palladio | 57/81 | Konstr., Antrop., Urban | Konstr., Antrop., Urban |
  | VdL | 45/81 | Komm., Industr., Antrop. | Komm., Industr., Antrop. |
  | Ken/tatami | 64/81 | Estetisk gen., Univ.\ overf. | Estetisk gen., Univ.\ overf. |

  Dette er den *operasjonelle* form av Proposisjon 7: kolonne 3 = kolonne 4. $4/4$ saker stadfestar; ingen falsifiserer. (Dette er ikkje statistisk test, men predikasjon-matching.)

### 3.6 § 6 Diskusjon
- **Kutt § 6.1 "Smal omhug som designstyrke"** — repliserer konklusjon. Spar 8 linjer.
- Behald § 6.2 (Neufert-prediksjon) og § 6.3 (N=4-kalibrering).

### 3.7 § 7 Konklusjon
- Kort: to setningar om reduksjonsproposisjonen er det mest varige bidraget.

---

## 4. APA 7-tilpasningar

- Sitat-stil: forfattar-år med komma: `(Stiny & Mitchell, 1978a)`. Noverande `(Stiny and Mitchell 1978)` m\aa{} gjennomg\aa{}.
- Tal: bruk siffer $\geq 10$, ord for 0-9 (APA 7 regel).
- Bibliografi: alfabetisk, hengeinnrykk 0,5 tommar, italic boktitlar og tidsskriftnamn, DOI som https-lenke.

**Omorganiser bib alfabetisk:** Benros · Buzzi · Cohen · Duarte · Engel · Fields & Levin · Finne · Hatchuel & Weil · Kazakci · Knight · Krishnamurti · Lorenzo-Palomera · March & Stiny · Morse · Padovan 1994 · Padovan 2002 · Proietti & den Biesen · Rozhkovskaya · Stiny 1980 *(fjern fr\aa{} tatami-seksjon)* · Stiny & Gips · Stiny & Mitchell 1978a · Stiny & Mitchell 1978b *(ny)* · Van der Laan · Watanabe *(ny)* · Wittkower.

### Nye bib-innf\o{}ringar

```
Benros, D., Hanna, S., & Duarte, J. P. (2012). A new Palladian shape
  grammar: A subdivision grammar as alternative. International Journal of
  Architectural Computing, 10(4), 521–540.
  https://doi.org/10.1260/1478-0771.10.4.521

Kazakci, A. O. (2009). Imagining knowledge: A formal account of design as
  a C-K process [Working paper]. HAL.
  https://minesparis-psl.hal.science/hal-00983061

Knight, T. W. (1981). The forty-one steps. Environment and Planning B:
  Planning and Design, 8(1), 97–114. https://doi.org/10.1068/b080097

Stiny, G., & Mitchell, W. J. (1978b). Counting Palladian plans.
  Environment and Planning B: Planning and Design, 5(2), 189–198.
  https://doi.org/10.1068/b050189

Watanabe, M. S. (2020). Exploring the panel exercises in the Modulor as
  presented by Le Corbusier. Japan Architectural Review, 3(4), 442–453.
  https://doi.org/10.1002/2475-8876.12147
```

### Slett frå bib
- Stiny, G. (1980) — ikkje relevant; ikkje tatami
- Knight, T. W. (2000) — erstatt med Knight 1981

---

## 5. Tekstlege grep for klarleik og knapp stil

### 5.1 Forkort
- Innleiinga: fr\aa{} 3 avsnitt til 2. Kutt "Fr\aa{} Vitruvius sine reguleringslinjer..." — historisk setting er ikkje naudsynt.
- Fjern alle "eksplisitt"/"konsekvent"/"n\o{}yaktig" som ikkje ber informasjon.
- "Proposisjon 7 predikerer at svikten klyngjer seg n\o{}yaktig p\aa{} dei urepresenterte aksane" → "Proposisjon 7: svikten klyngjer seg p\aa{} dei urepresenterte aksane."

### 5.2 Vis matematikk direkte
- Van der Laan-seksjonen: legg til dei f\o{}rste termane av Padovan-sekvensen ($1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21\ldots$). Enkelt, konkret.
- Modulor-seksjonen: vis dei to f\o{}rste ledda: raud $r_n = 1{,}130 \cdot \varphi^n$, bl\aa{} $b_n = r_n \cdot \varphi$. Konkrete tal.
- Palladio-seksjonen: vis eit reellt tilh\o{}ve — t.d.\ Villa Rotonda har $26 \times 26 \times 32$ fot med kvadrat og 4:3-kammer.
- Ken/tatami: $1\text{ ken} = 2\text{ tatami} \approx 1{,}82\text{ m}$; romstorleik er alltid $N$ tatami, $N \in \{2, 3, 4{,}5, 6, 8, 10\ldots\}$.

### 5.3 Fjern redundans
- "Kompetanse-laget." som st\aa r aleine p\aa{} line f\o{}re kvar boks blir teken inn i avsnittet f\o{}r: "Kompetanse-laget syner ..."

---

## 6. Endringar p\aa{} figurar

- **Fig 1-4 (inline saks-figurar):** uendra
- **Fig 5 (kognitiv lyskjegle):** uendra — fungerer godt
- **Fig 6 (konturlandskap):** flytt "Van der Laan"-label lenger inn; fiks det vesle visuelle rotet
- **Fig 7 (CK-kvadrat):** uendra

---

## 7. Arbeidsrekkje

1. Oppdater bib (slett Stiny 1980 og Knight 2000; legg til Knight 1981, Watanabe 2020, Stiny-Mitchell 1978b, Benros 2012, Kazakci 2009)
2. Skriv om § 1 med fjerna Fields-Levin-redundans
3. Skriv § 2.2 Proposisjon 1 med skisse-bevis; slett noverande Tabell 1
4. Introduser Form-likninga *etter* Proposisjon 1
5. Legg til kvantitative anker i kvar saks-underseksjon
6. Byt ut fargeboksane med stipla omriss, full spaltebreidd
7. Legg til predikasjon-matching-tabell i § 5
8. Kutt § 6.1; innrykk § 6.2 og § 6.3
9. Fiks Fig 6 label-plassering
10. Kompiler, verifiser 4 sider
11. APA-gjennomg\aa{}ing av alle sitat og bib-innf\o{}ringar

---

## 8. Ein kandidat-setning for hovudtesen

Noverande abstract har: *"Fordi Forml\ae re inneheld shape grammars og CK-teori som delstrukturar..."* — OK, men h\o{}rer heime som krav, ikkje resultat. Ny formulering:

> **Proposisjon 1 viser formelt at shape grammars og CK-teori er degenererte spesialtilfelle av Forml\ae re, kvar fr\aa{} eit distinkt kollapspunkt (seleksjonstrykk = 0 for SG; geometrisk struktur = triviell for CK). Komparativ diagnose av fire historiske proporsjonssystem demonstrerer at begge delstrukturane samstundes er n\o{}dvendige for \aa{} predikera sviktsignaturen empirisk.**

Dette er styrkande fordi:
- "Degenerert spesialtilfelle" er presist: kollapspunktet er namngjeve
- "Formelt" binder til Proposisjon 1
- "Empirisk" binder til dei fire sakene
- "Begge samstundes n\o{}dvendige" er det ingen tidlegare arbeid gjer

---

## 9. Det som *ikkje* treng endrast

- Tabell 2 (aksane) — riktig og knapp
- Figurvala (Fig 1-7) — greie
- Hovudstrukturen (intro → framework → saker → diagnose → diskusjon → konklusjon)
- Nynorsk-valet og tittelen

---

**Tilråding:** Godkjenn planen punkt for punkt, s\aa{} eg eksekverer. Alternativt vel punkt 1-7 som f\o{}rste b\o{}lge; resten kan venta til andre iterasjon.
