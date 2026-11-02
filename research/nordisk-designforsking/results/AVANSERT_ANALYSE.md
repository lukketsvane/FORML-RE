# Avansert data science: robustheit, sitering og bibliografisk kopling

Generert: 2026-11-02T17:10:44.872597+00:00

Utval: 3729 automatisk tittelinkluderte postar. Ikkje representativt for all designforsking.

## Sensitivitetsanalysar
| Utval | Publikasjonar | Interne siteringar | Del same tema | Nullmedian |
|---|---:|---:|---:|---:|
| all_auto_included | 3729 | 3159 | 49.8 % | 21.1 % |
| curated_design_venues | 382 | 373 | 43.4 % | 18.8 % |
| works_with_abstract | 2922 | 2054 | 49.0 % | 20.4 % |
| original_top200 | 2889 | 2389 | 50.6 % | 18.8 % |
| since_2010 | 3354 | 2646 | 49.7 % | 20.4 % |
| before_2015 | 1005 | 331 | 57.4 % | 24.5 % |

Permutasjonsnullmodellen held siteringskantar faste og stokkar om på temamerkelappar innan femårs- og siteringspopularitetsstrata. Kode og eksakte tal er i robustness.json.

## Bibliografisk kopling
- 126356 referansetilvisingar til 89009 ulike arbeid.
- 16916 publikasjonpar deler minst tre av dei bevarte referansane.
- 1022 par deler minst fire og har Jaccard 0,12 eller meir.
Bibliografisk kopling viser felles kunnskapsgrunnlag, ikkje replikasjon eller kumulativ teorianalyse.

## Sensitivitet for søkjerangering
            selection  works  abstract_coverage  core_venue_fraction  median_citations  median_publication_year
expanded_ranked_pages    840           0.830952             0.064286               6.0                   2020.0
      initial_top_200   2889           0.769817             0.113534               7.0                   2019.0

## Klyngestabilitet
Median justert Rand-indeks over åtte initialiseringar: 0.552.

## Konklusjon
Dette er robustheits- og strukturmålingar for eit ufullstendig metadatakorpus. Manglande kumulativitet er framleis ei hypotese som krev uavhengig fulltekstkoding av prøvbare påstandar, replikerte resultat og eksplisitt teorirevisjon. Den utvida API-innsamlinga stoppa ved rategrense, ikkje ved uttømmande dekning.
