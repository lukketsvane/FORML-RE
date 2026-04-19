# Revisjonsplan: `check_or_checkers`

Skriven 2026-04-15. Kjelder: foundational-paper/03-theory-nn, tre parallelle researchagentar (CK/SG-på-spel, lyskjegle/Pavlov/simulering, journalspesifikasjonar).

## 0. Diagnose av noverande versjon (4 sider, tokolonne)

### Det som held
- Kjernepåstanden (SG og CK er degenererte spesialtilfelle av Formlære) er formelt korrekt og står igjen etter agent-researchen; ingen har publisert denne sameininga.
- 8-spel-utvalet er riktig skala; BGG-korrelasjonen er eit legitimt eksternt mål.
- Proposisjon 7-operasjonaliseringa (n_θ som leseleg arkiv over kompromiss-dimensjonalitet) er konsistent med foundational paperet.

### Det som må vekk eller byggjast om

**(1) "Eleganse" som ramme kan ikkje stå.** Browne publiserte "Elegance in Game Design" i 2012 med definisjonen `elegance ≈ depth / complexity`. Ei ny eleganseavhandling utan å nemne Browne vil sjå uinformert ut; verre, den eksisterande definisjonen er ein nær konkurrent til n_θ × S. Brukar si oppmoding om å droppe elegansefornen er difor dobbelt motivert: terminologien er oppteken, og ramma kamuflerer det faktiske bidraget.

**(2) Sicart (2023, DiGRA) hevdar allereie CK-teorien for speldesign.** Utan sitering/avklaring er argumentet om CK-mangel tom retorikk. Sicart leverer ikkje SG eller landskap; det er der Formlære set inn, men skilnaden må skrivast eksplisitt.

**(3) Ludii/ludeme-litteraturen (Piette, Soemers, Stephenson, Browne 2020 ECAI) er ein kompositt generativ spelformalisme.** Reviewer vil spørje: kvifor ikkje ludeme i staden for SG? Svar: ludeme er grammatikken utan landskapet og lyskjegla.

**(4) Rammelitteraturen er 2002–2010.** Ingen spor av AlphaZero, MuZero, Sutton, Levin 2019/2022, Sicart 2023, Browne 2012, Piette 2020, Lantz 2017. Kjeldegrunnlaget er 10–15 år bak.

**(5) Figurapparatet er tynt.** Éin scatter + éin statisk brettillustrasjon. Brukar si instruksjon (multi-system comparison, contour fitness landscape, lyskjegle failure signatures, CK Design Square) krev fire figurfamiliar med reelt informasjonsinnhald.

**(6) Spel-som-simulering-argumentet manglar heilt.** Det er her lyskjegla og Pavlov kjem inn; ingen av desse dimensjonane er nemnde i noverande tekst.

---

## 1. Ny ramme: frå "eleganse" til "spel som lyskjegleoperasjonar"

### Sentral omrigging

Artikkelen skal no ikkje argumentere for ein eleganseindeks. Han skal argumentere for at **Formlære leverer nøyaktig det SG og CK ikkje leverer kvar for seg, og at spel er den reinaste testcasen fordi det å spele eit spel _er_ å utføre lyskjegleoperasjonar**.

Kjernepåstand (omformulert):

> Formlære = SG(∇_{C(A)} L(c,t)) inneheld formgrammatikken (sett L flat) og CK-teorien (sett SG trivial) som degenererte spesialtilfelle. Det som skil Formlære frå begge er lyskjegla C(A); dimensjonaliteten til det agenten faktisk representerer. Spel er den ideelle testklassen fordi brettspel tvingar spelarar til å utføre eksplisitte lyskjegleoperasjonar (simulere motstandarens trekk); "å spele" _er_ å navigere ∇_{C(A)} L(c,t) i sanntid. Over åtte brettspel frå tripp-trapp-tresko til Go korrelerer omhugsbreidda n_θ med BGG-vekt ved ρ_s = 0,929 (p < 0,01), konsistent med at forma (regelsettet) er eit leseleg arkiv over kor mange motstridande trykk designet navigerer.

Merk: indeksen n_θ × S overlever, men han er ikkje lenger "eleganse". Han er **lyskjeglevolum-diagnose** eller **formkompetansediagnose**. Kall han berre $\mathcal{D}$ eller namngje han etter det han måler: `lyskjeglevolum`.

### Ny tittelkandidatar

1. **_Dam eller sjakk: ein lyskjegleanalyse av åtte brettspel_**  (direkte, provoserande, held formelt språk)
2. _Spel som lyskjeglesimulatorar: Formlæretesting på åtte brettspel_
3. _Når dam vart løyst: Formlæreanalyse av åtte brettspel 1993–2024_
4. _Frå Shannon til MuZero: Formlære som minimal teori om brettspelsofistikering_

Anbefaling: **(1)** som hovudtittel; ho seier kva artikkelen gjer utan å forplikte seg til omstridd terminologi.

---

## 2. Ny struktur, 4 sider to-kolonne, seksjon for seksjon

Budsjett: ~3000 ord + 4 figurar + 2 tabellar + kompakt referanseliste.

### Samandrag (150 ord, beheld mdframed-stilen)

Ny vinkling: byrjar med datahistoriepåstanden (dam løyst 1993/2007, Deep Blue 1997, AlphaZero 2017, MuZero 2019), endar med Formlæresynteselikning og BGG-korrelasjon. Orddropp: "eleganse". Bruk: "lyskjeglevolum", "formkompetanse", "omhugsbreidde × stabilitet".

### Seksjon 1: Innleiing (~350 ord)

Tre punkt:

(a) **Datahistoriearken**: Shannon (1950) kvantifiserer sjakkrom til 10^120. Dam vart svak-løyst i 1993, sterkt-løyst i 2007 (Schaeffer et al., _Science_). Deep Blue slo Kasparov 1997. AlphaZero (Silver et al. 2018, _Science_) lærer sjakk, Go og shogi frå null på 24 timar. MuZero (Schrittwieser et al. 2020, _Nature_) gjer det utan spelreglane: han lærer dynamikken sjølv og planleggjer gjennom _in-silico lyskjegleoperasjonar_. Datahistoria viser at spel har vore den reinaste testen for kva kognisjon gjer.

(b) **Men datahistoria fortel oss ikkje kvifor sjakk er meir interessant enn dam.** Ingen algoritme forklarer kvifor eit spel med to trekkmodular (dam) kollapsar innanfor tusen år medan eit spel med seks (sjakk) held i tusen år til. Det er eit designteorispørsmål, ikkje eit AI-spørsmål.

(c) **Formlære (Finne 2026)**: éi likning, tre tradisjonar. Bidraget her er å vise at SG og CK er degenererte spesialtilfelle og at spel er den ideelle testklassen fordi spel _er_ lyskjegleoperasjonar. Over åtte brettspel: ρ_s(n_θ, BGG-vekt) = 0,929.

Stil: unngå em-dash (brukarmemo); bruk semikolon eller punktum.

### Seksjon 2: Relatert arbeid (~300 ord, TØRT)

Tre rørsler:

(a) **Spelkompleksitetsteori** (Shannon 1950; Allis 1994; Van den Herik et al. 2002; Schaeffer et al. 2007). Kvantifiserer, løyser ikkje designspørsmålet.

(b) **Spelkvalitetsmetrikkar**: Browne og Maire (2010, _IEEE TCIAIG_) induktive 57-aksar-lister; Browne (2012) elegance = depth/complexity. Lantz, Isaksen, Jaffe, Nealen, Togelius (2017) formelle djupnemetrikkar. Ingen av desse er avleidd frå eit formelt designteorigrunnlag.

(c) **Formelle designteoriar på spel**: Sicart (2023, DiGRA) klamrar CK-teorien for speldesign men manglar grammatikk og landskap. Piette, Soemers, Stephenson, Browne (2020, ECAI) leverer ludeme-systemet Ludii; kompositoriske reglar utan preferansestruktur. Ingen sameiner dei tre (grammatikk + landskap + lyskjegle) til eitt formelt apparat.

**Posisjonering**: Formlære er den minimale teorien som subsumerer alle tre. Spela er testcasen.

### Seksjon 3: Kva SG, CK, og Ludii kan; og ikkje kan (~500 ord)

Tre underseksjonar, kort kvar:

**3.1 Formgrammatikk**: Definisjon (SG = (S,R,ω)); sjakk har seks modular, tripp-trapp-tresko éin. Grammatikken er nøytral til kvalitet: L(SG)_sjakk og L(SG)_tripp-trapp-tresko er begge vel-definerte. Ludii generaliserer dette til _ludeme_-kompositorar (Piette 2020); same avgrensinga gjeld.

**3.2 CK-teori**: Fire operatorar C→C, C→K, K→K, K→C. Modellerer prosessen. Har ingen metrikk for designets kvalitet (Coatanéa et al. 2010). Sicart (2023) hevdar CK-teorien for speldesign; det som manglar hos Sicart er geometri i C-rommet og preferansestruktur over det realiserte.

**3.3 Lyskjegla**: Fields og Levin (2022, _Entropy_ 24(6):819) definerer den kognitive lyskjegla som "spatio-temporal boundary of events that [a Self] can measure, model, and try to affect" (Levin 2019, _Frontiers Psychol._). Omhug (Doctor et al. 2022) er kor mange aksar agenten faktisk representerer, ikkje kor mange han kan. Ingen av dei tre tradisjonane ovanfor har dette.

**3.4 Rekonstruksjon som degenererte tilfelle** (beheld den gode ein-paragrafs-demonstrasjonen frå noverande seksjon 3.4, men med ludeme-ekvivalens inkludert).

### Seksjon 4: Spel som lyskjegleoperasjonar (NY, ~400 ord)

Dette er den nye seksjonen som gjer artikkelen meir enn ein BGG-korrelasjon.

Hovudpåstand:

> Å spele eit brettspel er å utføre eksplisitte lyskjegleoperasjonar. Når spelaren spør "kva ville motstandaren gjere om eg spelar X?", projiserer ho ei trajektorie av framtidige konfigurasjonar; nøyaktig operasjonen Levin og Fields formaliserer som kognitiv lyskjegle. Same føresjåing-maskineri som Pavlov si hund brukte for å vente mat, formalisert som temporal-difference-læring (Sutton 1988; Sutton og Barto 2018) og nevralt instansiert som dopaminerg prediksjonsfeil (Schultz, Dayan, Montague 1997), er det sjakkspelaren deployer over lengre horisontar og breiare forgreiningar.

Tre konsekvensar:

(a) **Spelsofistikering = lyskjeglevolum**: produktet branching × depth som kompetent spel krev. Tripp-trapp-tresko krev depth 2, b ≤ 9. Go krev depth ≥ 40, b ≈ 250.

(b) **Failure-signaturer** (Csíkszentmihályi 1990): spel med for lite lyskjeglekrav kollapsar i _kjedsemd_; spel med for mykje kollapsar i _angst_ der spelarar fell attende på heuristikkar (Gigerenzer); velfungerande spel sit på flow-diagonalen.

(c) **AI validerer Formlære utan å prøve**: MuZero implementerer bokstaveleg talt ∇_{C(A)} L(c,t): verdinettverket er L, MCTS-utrullingar er lyskjegla, policynettverket er grammatikken. Kognisjonsarkitekturen som slår Go konvergerer med designteorien som forklarer kvifor Go er Go.

Citer her: Silver et al. 2018 _Science_; Schrittwieser et al. 2020 _Nature_; Yoshida, Dolan, Friston 2008 _PLoS CB_ (theory of mind i spel); Csíkszentmihályi 1990.

### Seksjon 5: Empirisk oppsett (~300 ord)

Komprimer dei to noverande tabellane til éi tabelleining med to rader av data (formromsparametrar + omhugsprofil). Dropp brettillustrasjonen (dam vs sjakk); han er dekorativ og tek plass ei reell figur treng.

Definisjonar (kompakt, éin paragraf):
- $n_\theta(x) = |\{i : r_i(x) > \theta\}|$; omhugsbreidde, frå prop 7
- $S(x) = \log_{10}(\Delta t)$; kanaliseringsdjupne, konkurranselevetid
- $\mathcal{D}(x) = n_\theta(x) \cdot S(x)$; lyskjeglevolum-diagnose (NB: _ikkje eleganse_)

Sju seleksjonstrykk (P1–P7) med justert framstilling: nye namn? $P_1$ Djupn, $P_2$ Handterlegheit, $P_3$ Materiell differensiering, $P_4$ Drama, $P_5$ Lærbarheit, $P_6$ Prestige, $P_7$ Remisrate. Behald noverande tal men reforanker på omhug, ikkje eleganse.

### Seksjon 6: Resultat (~250 ord)

Hovudtal: ρ_s($\mathcal{D}$, BGG-vekt) = 0,905 (p < 0,05); ρ_s(n_θ, BGG-vekt) = 0,929 (p < 0,01); ρ_s(n_θ, BGG-vurdering) = 0,976.

Backgammon-avviket står: $\mathcal{D}$ fangar det BGG-brukarar underestimerer (ρ_s-forskjellen er evidens, ikkje problem).

Legg til: korrelasjonane er konsistente med at **lyskjeglevolum** er det BGG-brukarar intuitivt måler når dei ratar "vekt"; ein lyskjegleanalyse er difor ei formalisering av det 400 000 brukarar gjer implisitt.

### Seksjon 7: Falsifisering, avgrensingar, konklusjon (~300 ord komprimert)

Behald dei tre falsifiseringsvilkåra (a, b, c) frå noverande tekst.

Ny konklusjonsvinkling: **Formlære er den minimale teorien som subsumerer SG, CK og ludeme-systema og gjer dei testbare mot datahistoria**. Dam vart løyst i 1993 fordi n_θ = 2. Sjakk held i tusen år fordi n_θ = 6. Go held fordi n_θ = 6 med ny kanalisering. MuZero løyser Go fordi han har bygd opp same lyskjegla som tusen år sjakkspelarar bygde.

Siste setning: _Dam er ikkje enkelt; dam er smalt. Sjakk er ikkje komplekst; sjakk er omhugsrikt._

---

## 3. Fire figurar: spesifikasjon med fallback

Brukar har bede om fire figurar. Gjeve 4-sider-to-kolonne-budsjett er dette stramt; planen er to full-breidde (figure\*) + to kolonne-breidde (figure).

### Fig 1 — Multi-system comparison (full breidde, side 1 eller side 3)

**Type**: tre-panels koordinert figur.

- **Panel (a)**: Scatter av dei åtte spela i log(state-space) × log(game-tree) rom. X = log₁₀(tilstandsrom), Y = log₁₀(speltre). Punktfarge kodar n_θ (rust→teal ramme). Punktstorleik kodar S (log-løysingshorisont). Annoterer: dam (løyst 1993/2007), sjakk (Deep Blue 1997, AlphaZero 2017), Go (AlphaGo 2016, MuZero 2019), Othello (løyst 2023).
- **Panel (b)**: Horisontal tidslinje av løysingar og milepålar: tripp-trapp-tresko (triv.) → Connect Four (1988) → møllle (1993) → dam (1993/2007) → Deep Blue (1997) → Othello (2023) → sjakk/Go (uløyst; MuZero 2019, AlphaZero 2017 som sofistiseringsfronten). Plasser kvar spelikon på riktig år.
- **Panel (c)**: Illustrasjon av kjerneequation ved å vise tre spel-instansar med ulike lyskjegle: tripp-trapp-tresko (smal kjegle, liten SG, flatt L), dam (moderat kjegle), Go (brei kjegle).

**Kjelder**: Tabell 1 i noverande artikkel; nye datofelt frå Wikipedia og dei siterte papera.

**Fallback**: kollaps til berre Panel (a) som kolonne-breidde figur med annotasjoner direkte på punkta.

### Fig 2 — Contour fitness landscape med vacant plateau (kolonne-breidde, side 3)

**Type**: 2D kontourplott av eit leiketøy-landskap L(c,t) over (forgreiningsfaktor b, søkedjupne d). Alle åtte spel plassert som punkt.

- Konturer vist som nivåliner + varm farge-ramp (teal→rust).
- "Vacant plateau" = den flate regionen (låg L) der tripp-trapp-tresko, dam, Connect Four ligg. Merka eksplisitt som _kanaliseringssvikt_: her er det ingenting å navigere, trykka kollapsar.
- Fjella: sjakk, Go, backgammon sit på separate lokale maksima.
- "Uutforska" region markert med stipla omriss: spel som teoretisk kunne eksistert men som ikkje har overlevd fordi ingen designer treftar den regionen.

**Kjelder**: Fiktivt landskap (forklarer det i caption); b- og d-verdiar frå tabell 1.

**Fallback**: 1D "vanskeleg-korridor"-plott med x = n_θ, y = S, punkta som spelikon.

### Fig 3 — Kognitiv lyskjegle og failure signatures (kolonne-breidde, side 4)

**Type**: tre-panels lyskjeglediagram adaptert frå Doctor et al. (2024), med failure-signaturar under kvar kjegle.

- **(a) Smal kjegle (n_θ = 2)**: Agent ser to aksar (handterlegheit + grunnleggjande spelstruktur). Under kjegla: tripp-trapp-tresko, dam. Failure-signaturar: dam konvergerer monotont mot remis; tripp-trapp-tresko er solved av 6-åringar; kjedsemd.
- **(b) Moderat kjegle (n_θ = 5)**: Othello, møllle. Kjegla dekkjer drama og lærbarheit men manglar materiell differensiering.
- **(c) Brei kjegle (n_θ = 6)**: Sjakk, Go, backgammon. Kjegla spenner alle sju trykk-aksar. Stabiliteten følgjer konkurranselevetida.

Under kvar kjegle: ein mikro-sparkline av Elo-utvikling / AI-engine-styrke (for spela som har AI-historie; kvalitativt skildra for dei andre).

**Kjelder**: Gjenbruk `writings/figures/fig-5.44-lyskjegle.png` som mal (den finst allereie frå traktat-arbeidet); adapter med Games-trykk-koding.

**Fallback**: Statisk 3-panel SVG utan Elo-sparkline.

### Fig 4 — CK-teori Design Square (kolonne-breidde, side 2)

**Type**: klassiske CK-firkant (C-rom × K-rom × forward/backward operatorar) med Formlære-oversetjingar innskrivne i kvar celle.

- 2×2 rutenett: rader = C og K; kolonnar = forward og backward.
- Dei fire operatorane C→C, C→K, K→K, K→C i kvar celle med:
  - CK-tradisjonelt namn (partisjon, realisering, deduksjon, konjunksjon)
  - Landskapsoversetjing (frå Table 2 i foundational paper)
  - Spel-døme (trekktrekk i spelet = C→C, sette eit trekk på brettet = C→K, analysere ein posisjon = K→K, oppdage ein ny opning = K→C)

Kort caption: "CK-operatorane er degenererte spesialtilfelle av Formlære-navigering når landskapet fjernast. Spel-kolonna viser korleis dei fire operatorane manifesterer seg konkret."

**Kjelder**: Gjenbruk `writings/figures/fig-5.45-ck.png` som mal; komponer ny versjon i TikZ med spel-døme lagt til.

**Fallback**: Tekst-tabell (bruk booktabs).

---

## 4. Tabellar

Kollapse to tabellar (formrom + omhug) til **éin kompakt felles tabell** med rader for:

- Tilstandsrom (log₁₀), speltre (log₁₀), b, H
- Modulartal
- Løysingsår / Δt
- P_1–P_7 skårar
- n_θ, S, $\mathcal{D}$
- BGG-vekt, BGG-vurdering

Gjer dette med \small + tabular*; 10 rader (éin per spel + header) × ~16 kolonner. Tight, men les; behald berre 2 desimaler.

**Fallback tabell**: behald dei to separate tabellane men flytt sensitivitetsanalysen (tabell 3 i noverande) til appendix-noter eller droppe henne heilt (den er ikkje kritisk for hovudargumentet).

---

## 5. Referansar: 10–15 nye

Noverande bibliografi (14 entries) må utvidast med minst ti:

1. **Sicart, M. (2023).** Beyond the old game design: a new design paradigm in Game Studies through C-K Theory. _DiGRA 2023._
2. **Browne, C. (2012).** Elegance in game design. _IEEE Trans. Comp. Intell. AI in Games_ 4(3): 229–240.
3. **Piette, É., Soemers, D.J.N.J., Stephenson, M., Sironi, C.F., Winands, M.H.M., Browne, C. (2020).** Ludii: The Ludemic General Game System. _ECAI 2020._
4. **Lantz, F., Isaksen, A., Jaffe, A., Nealen, A., Togelius, J. (2017).** Depth in Strategic Games. _AAAI Workshop on What's Next for AI in Games._
5. **Fields, C., Levin, M. (2022).** Competency in Navigating Arbitrary Spaces. _Entropy_ 24(6): 819.
6. **Levin, M. (2019).** The Computational Boundary of a "Self". _Frontiers in Psychology_ 10: 2688.
7. **Silver, D., et al. (2018).** A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. _Science_ 362: 1140–1144.
8. **Schrittwieser, J., et al. (2020).** Mastering Atari, Go, chess and shogi by planning with a learned model. _Nature_ 588: 604–609.
9. **Sutton, R.S. (1988).** Learning to predict by the methods of temporal differences. _Machine Learning_ 3(1): 9–44.
10. **Yoshida, W., Dolan, R.J., Friston, K.J. (2008).** Game Theory of Mind. _PLoS Comput. Biol._ 4(12): e1000254.
11. **Csíkszentmihályi, M. (1990).** _Flow: The Psychology of Optimal Experience._ Harper & Row.
12. **Doctor, T., Wakefield, G., Pavlic, T., Levin, M. (2022).** Biology, Buddhism, and AI: Care as the Driver of Intelligence. _Entropy_ 24(5): 710. (NB: agent flagga 2024-sitatet som tvilsamt; bruk 2022-referansen).

Merk to: referansane (5) og (6) finst allereie i den delte `writings/references/references.bib` (sjå `Levin2022`, `Levin2025`). Bruk `\cite` og sikre at dei vert plukka av artikkelen sin eigen bibitem-blokk, eller migrer til BibLaTeX-integrering.

Fjern / kortar: Van den Herik 2002 (sekundær); behald berre sentrale kjelder for å tene 4-sider-budsjettet.

---

## 6. Venuespesifikasjonar

Eksisterande LaTeX-oppsett: `\documentclass[10pt,twocolumn]{article}` med geometry + tikz + booktabs + mdframed. Dette er generisk; ingen av dei kandidat-venuene tek det direkte.

### Primær kandidat: International Journal of Architectural Computing (SAGE)

- **Lengd**: 4000–6000 ord. Noverande utkast ligg ~3000 ord; plass til utvidinga foreslått over.
- **Format**: Enkelt-kolonne produksjon, SAGE LaTeX-template.
- **Refstil**: SAGE Harvard (author-date).
- **Handling**: Lag ein parallell `check_or_checkers-ijac.tex` som importerer SAGE-class og konverterer bibitem-blokken til natbib/biblatex.
- **URL**: https://journals.sagepub.com/author-instructions/jac

### Sekundær: Design Science (Cambridge, open access)

- **Lengd**: 6000–10000 ord typisk; ingen hard grense.
- **Format**: Enkelt-kolonne; `dsj-class`.
- **Refstil**: Cambridge author-date.
- **Handling**: Alternativt komplett, særleg om artikkelen utvidast til ~8 sider.
- **URL**: https://www.cambridge.org/core/journals/design-science/information/author-instructions

### Tertiær: Nexus Network Journal (Springer)

- **Lengd**: 15–25 sider vanleg; 4-sider-versjonen er for kort for Research. Reframe som _Didactics_ eller _Geometer's Angle_.
- **Format**: Enkelt-kolonne; `sn-jnl.cls`.
- **Handling**: Lag `check_or_checkers-nnj.tex` om redaktøren gjev grøn lampe for kort format; elles ekspander til 10 sider.
- **URL**: https://link.springer.com/journal/4/submission-guidelines

### Tertiær, om reframing til urban morfologi: Environment and Planning B (SAGE)

- **Lengd**: ~8000 ord. Short Communication akseptabelt.
- **Problem**: Spel-fokuset er utanfor tidsskriftet sitt scope (urban/spatial). Ville krevje at artikkelen rammar spel som _diskrete romlege system_ og argumenterer at same analysen gjeld for urban morfologi.
- **Handling**: Ikkje prioriter; bruk som plan B om IJAC avviser.

### Frozen article.cls twocol som preprint

Behald `check_or_checkers.tex` som det er (after revisjon) som preprint-versjon (arXiv/SocArXiv). Kvar venue får sin eigen `check_or_checkers-<venue>.tex` som input den same `body.tex`-hovuddelen.

---

## 7. Revisjonsrekkjefølgje (implementeringsplan)

Rekkefølgje er vald slik at teoretisk omrigging er gjort før figurane, og figurane er på plass før den endelege tekstgjennomgangen:

1. **Seksjon 1 (intro) + samandrag**: skriv om med datahistoriearken og drop "eleganse" frå ramma.
2. **Seksjon 2 (relatert arbeid)**: legg til Sicart, Browne 2012, Piette/Ludii, Lantz.
3. **Seksjon 3 (SG/CK/ludeme/lyskjegle)**: utvid med ludeme og lyskjegle-underseksjonar.
4. **Seksjon 4 (spel som lyskjegleoperasjonar)**: heilt ny seksjon, siter MuZero/AlphaZero/Sutton/Yoshida.
5. **Tabell 1 kollaps**: slå saman formrom og omhug til éi tabell.
6. **Fig 4 (CK Design Square)**: TikZ-rendering av 2×2 med Formlære-mapping.
7. **Fig 1 (multi-system comparison)**: Python/matplotlib, full breidde.
8. **Fig 2 (contour landscape)**: Python/matplotlib, kolonne-breidde.
9. **Fig 3 (lyskjegler + failure signatures)**: TikZ eller gjenbruk av eksisterande `fig-5.44-lyskjegle.png` med annotasjonar.
10. **Seksjon 5–7 (empirisk, resultat, konklusjon)**: omskriv i lys av ny ramme.
11. **Referanseliste**: utvid til 22–24 entries.
12. **Venuespesifikk reformat**: lag `check_or_checkers-ijac.tex` som separat fil.

Estimat: 2–3 arbeidsdagar totalt for full revisjon + figurar; ein ekstra dag for IJAC-reformatering.

---

## 8. Risiko og mothugg

**Risiko 1**: Referansegrunnlaget blir for tungt for ein 4-sider-artikkel. _Mothugg_: bruk kompakt referanse-stil (f.eks. "(Sicart 2023; Browne 2012)") og kutt 2002-Van-den-Herik + anna rein bakgrunnsstoff.

**Risiko 2**: Reviewerar i spelforsking avviser fordi Formlære ikkje er demonstrert å slå Browne sin evolusjonære spelevalueringsalgoritme. _Mothugg_: artikkelen hevdar _minimalitet_ (færre parametrar, fleire subsumeringar), ikkje prediktiv overlegenheit. Lag det eksplisitt i diskusjonen.

**Risiko 3**: Designteorireviewerar kjenner verken AlphaZero eller MuZero og oppfattar AI-seksjonen som kosmetisk. _Mothugg_: legg MuZero-påstanden i seksjon 4 som ei _korroborasjon_ (teoriar konvergerer frå to retningar), ikkje som bevis.

**Risiko 4**: "Lyskjegle" les som fysikkjargon for ikkje-biologi-lesarar. _Mothugg_: ved første bruk, glos (_"kognitiv lyskjegle; den projiserbare horisonten av omhug og handling"_) og knytt til meir kjent "planleggingshorisont" / "forward model" frå RL-litteraturen.

---

## 9. Hva som IKKJE skal endrast

- Kjernelikninga Form = SG(∇_{C(A)} L(c,t)) står.
- 8-spel-utvalet og BGG-data står.
- Sensitivitetsanalysen (tabell 3 i noverande) kan stå som fotnote, men er ikkje kritisk.
- Produktforma $\mathcal{D} = n_\theta \cdot S$ står; berre namnet endrast (frå eleganse til lyskjeglevolum).
- Spearman ρ_s-talene står.
- Falsifiseringsvilkåra (a, b, c) står.

---

## 10. Ope: avgjerder brukar bør ta før implementering

1. **Namn på indeksen**: `lyskjeglevolum $\mathcal{V}$`, `formkompetanse $\mathcal{F}$`, eller berre $\mathcal{D}$ (diagnose)? Anbefaling: **lyskjeglevolum**; det knyttar direkte til Levin og er sjølvforklarande.

2. **Tittel**: 1-4 i lista over. Anbefaling: **_Dam eller sjakk: ein lyskjegleanalyse av åtte brettspel_**.

3. **Målvenue**: IJAC vs Design Science vs NNJ. Anbefaling: **IJAC** først (lengd passar mest direkte; minimum reformatering).

4. **Om figurkvote (4 figurar i 4 sider): aksepter stramt, eller ekspander artikkelen til 6–8 sider og sikt på Design Science?** Anbefaling: **ekspander til 6 sider + IJAC**.

5. **MuZero-påstanden i seksjon 4: ei påstand om konvergens (forsiktig) eller ei sterk påstand om at Formlære er AI-bevist (djerv)?** Anbefaling: **forsiktig**; det er meir truverdig og opnar for ein oppfølgjar-artikkel som pressar djerv-påstanden.
