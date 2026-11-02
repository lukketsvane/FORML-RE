# Siteringskjeder 2000–2026: kontroll for tema og sentrale nodar

**Datagrunnlag:** 3729 automatisk tittelinkluderte publikasjonar; 3159 siteringskantar innanfor same avgrensa OpenAlex-utval.

Kjeda er **nyare publikasjon (2020–26) → mellompublikasjon (2010–19) → eldre publikasjon (2000–09)**. Ei kjede er to registrerte referansekantar, ikkje to verifiserte hypotesetestar.

**Observert:** 712 slike kjeder, fordelte på 99 mellomarbeid med minst éi kjede. Dei fem mellomarbeida med flest kjeder ber 286 (40.17 %) av alle kjedene. Dei ti største ber 404 (56.74 %).

## Kontrollar med permuterte mellomarbeid

Nullmodellen held talet på siteringar som kvart mellomarbeid får frå 2020–26 fast. Talet på siteringar mellomarbeidet sjølv har til 2000–09 vert stokke om mellom mellomarbeid innan år eller år+søkjegruppe. Nullmodellen er dermed ein test av kor sterkt **innkomande og utgåande referansetal samvarierer** mellom mellomarbeida, ikkje av sanningsinnhaldet i kjedene.

| Kontroll | Observert | Nullmedian | Nullintervall (2,5–97,5 %) | Monte Carlo-p |
|---|---:|---:|---:|---:|
| Innafor eksakt publikasjonsår | 712 | 226 | 134–378 | 0.0005 |
| Eksakt år og automatisk søkjetema | 712 | 292 | 178–474 | 0.0005 |
| Femårsbolk og søkjetema | 712 | 276 | 169–500 | 0.0005 |
| Utan dei fem største mellomarbeida, år+tema | 426 | 243 | 153–360 | 0.0025 |
| Utan dei ti største mellomarbeida, år+tema | 308 | 203 | 134–303 | 0.0225 |

Resultata er **utforskande** (ikkje førehandsspesifiserte) og nullfordelingane seier berre noko om denne grafen. Søkjerangering, manglande kantar utanfor korpuset, felles forfattarar, artikkeleffektar og temaetikettane sine svakheiter påverkar samanlikninga.

## Største mellomarbeid etter talet på kjeder

- 2012: **Routledge International Handbook of Participatory Design** — 146 kjeder (73 innkomande frå nyare arbeid × 2 referansar til eldre arbeid).
- 2016: **Evolution of design for sustainability: From product design to design for system innovations and transitions** — 40 kjeder (40 innkomande frå nyare arbeid × 1 referansar til eldre arbeid).
- 2017: **Bringing Service Design to manufacturing companies: Integrating PSS and Service Design approaches** — 36 kjeder (9 innkomande frå nyare arbeid × 4 referansar til eldre arbeid).
- 2016: **Participatory design methods in telemedicine research** — 36 kjeder (18 innkomande frå nyare arbeid × 2 referansar til eldre arbeid).
- 2017: **Staging aesthetic disruption through design methods for service innovation** — 28 kjeder (14 innkomande frå nyare arbeid × 2 referansar til eldre arbeid).
- 2016: **Framing Design Thinking: The Concept in Idea and Enactment** — 27 kjeder (27 innkomande frå nyare arbeid × 1 referansar til eldre arbeid).
- 2011: **Action Design Research1** — 25 kjeder (25 innkomande frå nyare arbeid × 1 referansar til eldre arbeid).
- 2013: **Ageing together: Steps towards evolutionary co-design in everyday practices** — 24 kjeder (8 innkomande frå nyare arbeid × 3 referansar til eldre arbeid).
- 2018: **Participatory design for sustainable social change** — 22 kjeder (22 innkomande frå nyare arbeid × 1 referansar til eldre arbeid).
- 2016: **Unpacking the Notion of Participation in Participatory Design** — 20 kjeder (10 innkomande frå nyare arbeid × 2 referansar til eldre arbeid).

## Tolkingsregel

**Høg indirekte tilknyting viser bibliografisk kontinuitet, ikkje empirisk kumulativitet.** Kvar lenkje må lesast i fulltekst og kodast som bakgrunn, metodebruk, vidareutvikling, prøving, replikasjon eller motfunn. Artikkelpar som deler forfattarar bør ikkje teljast som uavhengig replikasjon utan særskild grunngjeving.

Sjå [kjeldekritisk pilot](KJELDEKRITISK_PILOT.md), [gransking av 200 siteringspar](lineage_review_queue.csv) og [all treperiodedata](citation_three_cohort_paths.csv).

**Reproduserbarheit:** Alle råkantane er lagra i `internal_citations.csv`, mellomarbeida i `semantic_clusters.csv`, og tala i `citation_bridge_hub_sensitivity.json`. Permutasjonen nyttar pseudotilfeldig seed `20261102` og 2000 rundar per kontroll.
