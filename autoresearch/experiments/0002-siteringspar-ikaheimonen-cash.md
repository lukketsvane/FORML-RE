# Revisjonsnotat 0002: Ikäheimonen mfl. (2024) → Cash mfl. (2022)

**Dato:** 15. november 2026. **Oppdrag:** issue #27, etterarbeid etter #25 og PR #26.
**Forsøkskort:** [`0002-siteringspar-ikaheimonen-cash.json`](0002-siteringspar-ikaheimonen-cash.json).
**Status:** `needs-human-review`. Éin lesar (Claude Fable 5.2), inga dobbeltkoding, ingen uavhengig kontroll.

## Funn

Siteringa er **bakgrunn med avgrensa omgreps- og metodebruk**. Ikäheimonen mfl. prøver, replikerer, reviderer eller utvidar ikkje noko i Cash mfl. Paret er ikkje eit motdøme til fråværsformuleringa i føreordet, og heller ikkje ei stadfesting av henne.

## Hypotese, rival og skiljeobservasjon

- **H:** Den nyare artikkelen tek ein spesifikk påstand eller tilråding frå den eldre og prøver, replikerer, reviderer eller vidareutviklar han med eige materiale (L3–L7).
- **R1:** Siteringa er bakgrunn, omgrepsbruk eller metodebruk utan prøve (L0–L2). Høg cosine (0,878) og treff på replikasjonsord kjem av at begge er metodenotat om forskingskvalitet.
- **R2:** Den nyare artikkelen utvidar utvalsrammeverket til dataintensiv forsking (L3) utan å prøve det.
- **Skilje:** H krev ein passasje som namngjev ein bestemt påstand hos Cash mfl., rettar data mot han og rapporterer utfall. R2 krev ein passasje som endrar eller legg til noko i dei åtte omsyna. R1 held dersom Cash mfl. berre står som støtte for omgrep, merkelapp eller vidare lesing. Utan fulltekst: uavgjort.

**Ikkje førehandsregistrert.** Formuleringane følgjer oppdragsteksten og kodeboka, men vart skrivne ned i same økt som tekstane vart opna, og kortet vart fullført etter lesinga. Kodane L0–L7 er henta uendra frå `CODEBOOK.md`, tillegg 0.2 C.

**Utval:** formålsretta. Paret er peika ut i oppdraget frå rad 12 i ei kandidatliste som sjølv er sortert etter cosine og ordtreff. Ingen frekvens for feltet kan utleiast.

## Kjelder som faktisk er lesne

| | Nyare | Eldre |
|---|---|---|
| Verk | Ikäheimonen, Li, Yao, Zuo, Aledavood og Hölttä-Otto, *Journal of Engineering Design* 36(12), 2183–2203; på nett 1.9.2024 | Cash, Isaksson, Maier og Summers, *Design Studies* 78 (2022), artikkel 101077, s. 1–21; på nett 2021 |
| DOI | [10.1080/09544828.2024.2396194](https://doi.org/10.1080/09544828.2024.2396194) | [10.1016/j.destud.2021.101077](https://doi.org/10.1016/j.destud.2021.101077) |
| Lesen versjon | Forlagets versjon, nettfyrst, paginert 1–21, CC BY-NC-ND | Forlagssats, trykte sider 1–21, CC BY |
| Henta frå | [Aaltodoc](https://aaltodoc.aalto.fi/handle/123456789/132938) | [Strathprints](https://strathprints.strath.ac.uk/78987/) |
| Omfang | Brødtekst s. 1–17 heilt; referansar berre søkte | Brødtekst s. 1–14 og 17; tabell 4, figurar og referansar ikkje nærlesne |

Sidetala for Ikäheimonen mfl. nedanfor er nettfyrst-sidene i den lesne fila. Heftesidene i parentes er utrekna (n + 2182) og **ikkje** kontrollerte mot hefte-PDF-en; forlagssida gav HTTP 403. SHA-256 for begge filene står i forsøkskortet. Ingen PDF er lagd i repoet.

## Dei tre siteringane

Søk på «Cash» i heile den nyare teksten gjev tre tilvisingar til Cash mfl. (2022), i tillegg til tilvisingar til Cash (2018).

| # | Stad i nyare tekst | Kva som vert sitert | Tilsvarande stad hos Cash mfl. | Kode |
|---|---|---|---|---|
| 1 | s. 2 (2184), innleiing | Dataintensiv designforsking kan bidra til «theory building (e.g. pattern identification) or testing (e.g. prediction)» | s. 2, 3–4 og tabell 1 s. 7. Cash mfl. tilskriv sjølve syklusen til Cash (2020) og Wallace (1971) | L1 omgrepsbruk |
| 2 | s. 5 (2187), kasusbakgrunn | «This case is a combination of purposeful and convenience sampling (Cash et al. 2022)» | s. 10: ikkje-sannsynsutval som «purposive», «quota», «convenience»; omsyn 6 | L2 metodebruk utan prøve |
| 3 | s. 17 (2199), diskusjon | Andre kvalitetsmål «should be considered, including sampling (Cash et al. 2022)» | Verket som heilskap; ingen side eller påstand peika ut | L0 bakgrunn |

Merknader:

- **Sitering 2** er det næraste ein kjem bruk. Typologien set namn på valet av *illustrasjonskasus* for notatet, ikkje på eit deltakarutval i ny datainnsamling. Det er i tråd med tilrådinga hos Cash mfl. om å rapportere skjema eksplisitt (s. 10), men ingenting vert prøvd og typologien vert ikkje endra. Grensa mellom L1 og L2 her er eit skjønn som uavhengige kodarar bør ta.
- **Sitering 3:** leddet om «the link between theory and the intended context» er tilskrive Crilly (2019), ikkje Cash mfl.
- Ingen av dei tre siteringane oppgjev side hos Cash mfl. Kolonnen «tilsvarande stad» er mi lokalisering, ikkje forfattarane si.

## Kvifor ikkje H eller R2

Cash mfl. er sjølv eit forskingsnotat utan eige datagrunnlag. Teksten seier at han ikkje er eit systematisk oversyn (s. 3), at arbeidet «necessarily focused on conceptual development», og at det trengst systematisk oversyn over utvalspraksis, metaanalyse og evaluering av omsyna (s. 14). Det er altså den eldre teksten sjølv som oppgjev kva ei prøve ville vore. Ikäheimonen mfl. gjer ingen av delane: bidraget deira er ein arbeidsflyt frå datavitskap, tilpassa frå CRISP-DM og vist på eit tidlegare kasus (s. 3–4, 7–15). Utval er ikkje tema utanom dei tre setningane over.

## Det falske positive signalet

Kandidatlista flagga paret med `explicit_replication_words=True`. Orda gjeld emnet til den nyare artikkelen (reproduserbarheit som mål) og éi replikasjonsavsikt i kasuset: spørsmål 1 «seeks to replicate and extend findings from earlier physiological studies on facial mimicry» (s. 8). Den avsikta er retta mot ein annan litteratur enn Cash mfl. Notatet rapporterer ikkje utfall for spørsmåla og viser til Salmi, Li og Hölttä-Otto (2023) for metoden (s. 8). Om *den* relasjonen er ein replikasjon, er ikkje undersøkt her.

## Gradering

| Påstand | Grad |
|---|---|
| Den nyare artikkelen siterer den eldre | Fast: Crossref-referanseliste, lesen referanseliste s. 18, tre tilvisingar i teksten |
| Dei tre siteringsstadene og ordlyden | Lesen i forlagets versjon av éin lesar; treng menneskeleg kontroll |
| Klassifikasjon L1 / L2 / L0 | Førebels; grensa L1/L2 for sitering 2 er skjønn |
| Fråvær av L3–L7 mot Cash mfl. | Byggjer på fullstendig lesing av brødteksten og maskinsøk; førebels til dobbeltkoda |
| Heftesidetal 2184, 2187, 2199 | Utrekna, ikkje sett |
| Noko om feltet som heilskap | Ingen grad. Kan ikkje utleiast |

## Ikkje kontrollert

- Inga uavhengig koding. Feltet `reviewer` i kortet er tomt, og kandidat-CSV-en er ikkje endra.
- Cash mfl.: tabell 4 (s. 15–16), figur 1–3 og referanselista.
- Salmi mfl. (2023), Cash (2018) og dei fysiologiske mimikkstudiane.
- Dei 149 andre kandidatpara.
- `lukketsvane/designteori`: berre DOI-oppslag i `korpus.csv` (6432 postar). Den eldre artikkelen finst der, den nyare ikkje.
- Dei 491 proposisjonane er talde strukturelt av `harness.py status`, ikkje vurderte.

## Framlegg til føreordet

Ingen. Prøva krev ikkje revisjon, og ho gjev heller ikkje grunnlag for å skjerpe formuleringa. Eitt formålsretta par med utfall R1 flyttar ikkje påstanden i nokon retning.

## Køyrde kontrollar

Køyrde 15. november 2026 med Python 3.14.4 på `fa49ecc` pluss dei to nye filene:

| Kommando | Utfall |
|---|---|
| `python autoresearch/harness.py check --record autoresearch/experiments/0002-siteringspar-ikaheimonen-cash.json` | Består: `structurally_valid: true`, 5 evidenspostar, proposisjon 7.17 |
| `python -m unittest discover -s autoresearch -p "test_*.py"` | Består: 5 testar, OK |
| `python autoresearch/harness.py status` | 491 proposisjonar, 150 kandidatpar, 0 uavhengige fulltekstvalideringar, 0 stadfesta motdøme (uendra) |

`check` validerer berre strukturen på kortet, ikkje at funna er sanne.

## Mogleg neste runde (ikkje starta)

Dersom forfattaren vil ha ein runde til: vel par der `direct_test_words=True` og der den eldre teksten set fram eit empirisk funn, ikkje eit rammeverk. Eit metodenotat som siterer eit anna metodenotat kan vanskeleg bli noko anna enn L0–L3.
