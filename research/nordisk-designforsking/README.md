# Nordisk designforsking, 2000–2026 — open metakartlegging

Reproduserbar **søkjebasert bibliografisk database** for nordisktilknytt designforsking.
Dette prosjektet er ikkje ei gjennomlesing av alle publiserte arbeid, og ikkje ein
statistisk metaanalyse av empiriske effektar. Det er eit dokumentert utgangspunkt
for ein testbar metascience-studie av kumulativitet i designteori.

## Status 2. november 2026

- 31 førehandsspesifiserte OpenAlex-søkjeuttrykk
- 96 gjennomførte søkjesider (inntil fem per uttrykk, høgst 100 treff per side)
- 7 300 unike kandidatar; 3 729 med nordisk forfattartilknyting og relevansterm i tittelen
- 3 571 kandidatpostar skal vurderast manuelt, ikkje teljast som feil eller irrelevante utan kontroll
- Utvidinga vart avbroten av HTTP 429 (API-grense) før alle frasar var gjennomgått til side 5
- 0 fulltekst-PDF-ar lasta ned av dette systemet

**NB:** Tala er ikkje eit anslag på kor mange nordiske designstudiar som finst.
Toppsider sorterte etter OpenAlex-relevans har systematiske skeivskapar.
Inkluderinga er regelbasert og førebels, ikkje fagleg verifisert.

**[Sjå datadashboard med 18 figurar og alle hovudfunn](results/DASHBOARD.md).**

## Datakjelde, søk og utval

Kjelde: https://openalex.org og https://help.openalex.org/api/

1. Perioden er publikasjonsår 2000–2026.
2. «Nordisk» er operasjonalisert som minst éin forfattar med institusjonstilknyting
   i Noreg (NO), Sverige (SE), Danmark (DK), Finland (FI) eller Island (IS).
   Utgjevarland, forfattarnamn og språk blir ikkje brukte som erstatning.
3. Typar: artikkel, bok, bokkapittel, konferanseartikkel og review.
4. Søk i OpenAlex etter frasar som «design theory», «research through design»,
   «design methods», «participatory design», «design history», «design ethics» mfl.
   Full søkjestrategi står som konstantane QUERIES og FILTER i collect.py.
5. Opp til fem søkjesider à 100 rangsorterte treff per uttrykk vart freista.
   Etter det første fullførte uttrekket på to sider per uttrykk stoppa utvidinga
   ved API-grensa. Ein revisjonssporbar logg oppgir søk, treff, faktisk henta
   sider, hentedato og registrerte feil, inkludert HTTP 429.
6. Automatisk førehandsinkludering krev relevant designterm i tittelen.
   Dei andre treffkandidatane står i eiga CSV til manuell revisjon.
7. Deduplisering skjer på OpenAlex-arbeids-ID; DOI-duplikat vert rapportert særskilt.
   Ingen påstand om at alt som er inkludert er faktisk designforsking.
8. OpenAlex-abstrakt vert rekonstruert frå den inverterte indeksen.
   Manglande samandrag er manglande data, ikkje negativ evidens.

Denne avgrensinga kan ikkje reprodusere ei systematisk, fullstendig litteraturkartlegging
utan vidare søk i NVA, DiVA, Aalto, Chalmers, CEPHAD, bibliotek og DOI-kryssjekk.

## Køyre

Python 3.11+. På Windows:

    py -3 -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt
    .venv\Scripts\python collect.py --pages 5
    .venv\Scripts\python analyse.py --min-records 3000
    .venv\Scripts\python nullmodell.py
    .venv\Scripts\python robustheit.py
    .venv\Scripts\python abstraktsignal.py
    .venv\Scripts\python datakvalitet.py
    .venv\Scripts\python audit_sample.py --per-theme 25 --excluded 50
    .venv\Scripts\python database.py --archive
    .venv\Scripts\python siteringslinjer.py
    .venv\Scripts\python lag_vurderingsverktoy.py
    .venv\Scripts\python utvalsprotokoll.py
    .venv\Scripts\python kodingsanalyse.py
    .venv\Scripts\python motprover.py
    .venv\Scripts\python validate.py
    .venv\Scripts\python test_datavitskap.py

På Linux/macOS, bytt til .venv/bin/python.
Samlinga kan haldast oppdatert med nye sider; all import er idempotent på OpenAlex-ID
og søkjeuttrykk. Slett ikkje query_log med mindre du medvite ønskjer å gjere ny fullimport.
Merk at OpenAlex har delte gratisbudsjetter og endrar indeksen over tid.

Søkje i databasen:

    .venv\Scripts\python sok.py "form and function" --limit 12

## Mappestruktur

- collect.py — innsamling, de-duplisering, SQLite-tabellar, søkjelogg og FTS5
- analyse.py — deskriptiv analyse, tekstrom, siteringsgraf og figurar
- sok.py — lokalt tekst- og latent semantisk søk
- nullmodell.py — referansestratifisert sensitivitetsanalyse av temalikskap i interne siteringar
- audit_sample.py — reproduserbart, tomt dobbeltkodingsskjema for uavhengig kontroll
- database.py — gzip-pakking og integritetstest ved gjenoppretting
- robustheit.py — stratifisert siteringsnullmodell, robustheitssjekkar, bibliografisk kopling og klyngestabilitet
- abstraktsignal.py — eksplisitte regex-treff om hypotesar, evaluering og replikasjon i samandrag (ikkje dokumenterte metodar)
- datakvalitet.py — duplikat, tidsskjeve referansar, inklusjonsflagg og dekning
- validate.py — dynamiske, verifiserte publiseringskontrollar
- siteringslinjer.py — semantiske siteringspar mot tema-, år- og popularitetsjustert referansemodell
- lag_vurderingsverktoy.py — lagar lokal nettlesar for dobbelkoding av 200 kandidatpar
- utvalsprotokoll.py — trekt 600-postars sannsynsutval frå den **automatiske** inkluderingsramma, med vekter
- kodingsanalyse.py — bereknar berre Kappa og indikatorar etter reell uavhengig manuell koding
- test_datavitskap.py — kontroll av dataintegritet, metadataarkiv og analyseregresjonar
- motprover.py — målretta søk etter moglege motdøme til ikkje-kumulativitet; ingen automatiske stadfestingar
- CODEBOOK.md — uavhengig menneskeleg vurdering av kumulativitet
- data/nordic_design_research.sqlite.gz — komprimert **offentleg metadata-only**-database; programmet gjenopprettar han automatisk
- results/RAPPORT.md — generert rapport; sjå figurar, CSV, JSON
- results/included_publications.csv — førebels tittelinkluderte postar, utan opphavsrettsleg verna samandrag
- results/candidates_for_manual_review.csv — utelatne frå automatisk analyseseleksjon
- results/lsa_vectors.npz — latent semantisk tekstrepresentasjon
- results/SITERINGSLINJER.md — semantisk kontrollerte siteringar og bootstrap
- results/lineage_review_queue.csv — 200 kandidatsiteringar med tittel/DOI for manuell gransking
- results/review.html — lokal, nettlesarbasert blindpar-koding, inga nettverksopplasting
- results/UTVALSPLAN.md — utvalsdesign, 600 postar, 54 strata og inverse utvalsvekter
- results/probability_sample_600_double_coder.csv — fulltekstkodeark for to uavhengige kodarar
- results/CODING_PROGRESS.md — faktisk, førebels tom kodingsstatus; ingen oppdikta funn
- results/MOTPROVER.md — systematisk søk etter kandidatar som kan utfordre hovudhypotesen
- results/possible_counterexamples_to_non_cumulative_design.csv — 150 kandidatsiteringar, enno ikkje verifiserte

## Analyser og kva dei faktisk seier

1. **Deskriptiv bibliometri:** talet på treff per år, kategorisert tema, land,
   publiseringskjelde og globalt OpenAlex-siteringstal. Ikkje estimert feltproduksjon.
2. **Direkte siteringar:** kor mange kjeldearbeid som viser til andre arbeid
   i det *innhenta* utvalet. Kantar ut av databasen vert ikkje rekna som fråvær av referansar.
3. **Krysstematisk nettverk:** referansar mellom temamerkelappar frå søk.
   Siteringsfellesskap er ikkje det same som replikasjonsfellesskap.
4. **Latent semantisk analyse:** TF–IDF + TruncatedSVD (LSA) av tittel +
   tilgjengeleg samandrag, K-means og tekstnærleik. Dette er *ikkje* PDF-fulltekst
   eller ein ekstern språkmodell-embedding.
5. **Jensen–Shannon-divergens:** endring i klyngefordeling mellom tidsbolkar,
   ikkje dokumentert framgang eller avgang for disiplinen.
6. **Kvalitetskontroll:** manglande samandrag, DOI-duplikat, proveniens, utvalsskeivskap.
7. **Robustheit:** permutasjon av temamerkelappar innan femårs- og siteringsstrata;
   oppdelte analyser av utvalde designtidsskrift, samandrag og historiske kohortar.
8. **Bibliografisk kopling:** publikasjonpar som viser til fleire av dei same kjeldene;
   ulikt direkte sitering, og ikkje ekvivalent med fagleg prøving.
9. **Ordsignal i samandrag:** strengtreff for hypotesar, prøving, replikasjon og
   konseptuelle arbeid. Dette er søkjesignal, ikkje fagfellevurdert koding.
10. **Stabilitet:** kontroll av kor mykje K-means-klassifikasjonane skiftar med ulike frø.

11. **Semantisk siteringskontinuitet:** 3 159 interne siteringar samanlikna med år-,
    tema- og siteringspopularitetsjusterte alternativ, med eigne resultat utan
    felles forfattarar og der begge samandrag er tilgjengelege.
12. **Verifiserbar fulltekstrevisjon:** 200 målretta siteringspar i eit lokalt
    annotasjonsverktøy, og eit separat stratifisert utval på 600 publikasjonar
    frå den automatisk inkluderte ramma. Alle vurderingsfelt startar blanke.

**Ingen av analysane kan åleine stadfeste at designforskinga ikkje er kumulativ.**
Slutningar om replikasjon og kunnskapsvekst krev manuell koding av konkrete,
falsifiserbare påstandar, vidaretesting og motseiingar i publikasjonar. Sjå CODEBOOK.md.

## Vitskapleg neste steg

- Presiser populasjon og utvalsramme med fleire nordiske register.
- Trekk eit stratifisert sannsynsutval av arbeid og les **fulltekst** med lovleg tilgang.
- Bruk to uavhengige kodarar, rapporter semje/uenigheit og Cohen's kappa.
- Kod hypotesar, prediksjonar, utval, metodar, resultata sine begrensingar,
  replikasjon og eksplisitt teoretisk revisjon etter kodeboka.
- Samanlikn definert kumulativitet med ein referansepopulasjon innan eit anna
  kunnskapsfelt med tilstrekkeleg sjanger- og alderskontroll.
- Først då kan ein teste kor sterkt og kor utbreidd problemet er.

Databasen på CYGNUS har også rekonstruerte OpenAlex-samandrag til intern analyse.
Den offentlege GitHub-arkivfila og CSV-eksportane utelèt desse samandraga og
originale API-payloadar for ikkje å publisere potensielt verna tekst.
Dei publiserte LSA-modellane og resultata er avleidde frå den lokale, rikare databasen;
full nyskaping av tekstanalysen krev at samandraga vert henta på nytt med gjeldande
rettar og API-tilgang. Ikkje redistribuer PDF-fulltekst utan rettar.
Kjeldeidentifikatorar og opphavleg referanse skal bevarast.

## Tidsbruer og eksisterande metascience (kjeldekritisk utviding)

Ei ny kontrollrunde kartlegg **712 indirekte siteringsvegar** frå 2020–26 via
2010–19 til 2000–09. Fem mellomarbeid står for 40,2 % av vegane; det største
er ei handbok, ikkje eit sjølvstendig empirisk replikeringsforsøk.
Sjølv etter år-, tema- og knutepunktkontrollar er dette **bibliografisk
kontinuitet**, ikkje eit mål på prøving eller teoretisk kumulativitet.

- [Siteringsbruer og permutasjonssensitivitet](results/SITERINGSBRUER.md)
- [Rå-ID-ar for 712 kjeder](results/citation_three_cohort_paths.csv)
- [Knutepunkta og graden deira](results/citation_bridge_hubs.csv)
- [Reproduserbar standardbibliotek-Python](citation_three_cohort.py)
- [Kjeldekritisk pilot i utvalde fulltekstar](results/KJELDEKRITISK_PILOT.md)
- [Eksterne systematiske oversyn og replikasjonstaksonomiar](results/EKSTERN_METAVITSKAP.md)
- [Kontroll av korrelasjonar rapporterte ved replikasjon](replication_effect_checks.py)
