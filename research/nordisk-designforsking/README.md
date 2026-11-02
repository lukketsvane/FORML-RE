# Nordisk designforsking, 2000–2026 — open metakartlegging

Reproduserbar **søkjebasert bibliografisk database** for nordisktilknytt designforsking.
Dette prosjektet er ikkje ei gjennomlesing av alle publiserte arbeid, og ikkje ein
statistisk metaanalyse av empiriske effektar. Det er eit dokumentert utgangspunkt
for ein testbar metascience-studie av kumulativitet i designteori.

## Status 2. november 2026

- 31 førehandsspesifiserte OpenAlex-søkjeuttrykk
- 60 gjennomførte søkjesider (maks 100 treff per side, maks to sider per uttrykk)
- 4 869 unike kandidatar; 2 889 med nordisk forfattartilknyting og relevansterm i tittelen
- 1 980 kandidatpostar skal vurderast manuelt, ikkje teljast som feil eller irrelevante utan kontroll
- 0 fulltekst-PDF-ar lasta ned av dette systemet

**NB:** Tala er ikkje eit anslag på kor mange nordiske designstudiar som finst.
Toppsider sorterte etter OpenAlex-relevans har systematiske skeivskapar.
Inkluderinga er regelbasert og førebels, ikkje fagleg verifisert.

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
5. Maksimalt 200 rangsorterte resultat per uttrykk. Det vert laga ein
   revisjonssporbar logg med forespurnad, søketreff, side, hentedato og eventuelle feil.
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
    .venv\Scripts\python collect.py --pages 2
    .venv\Scripts\python analyse.py --min-records 2001
    .venv\Scripts\python nullmodell.py
    .venv\Scripts\python audit_sample.py
    .venv\Scripts\python database.py --archive

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
- CODEBOOK.md — uavhengig menneskeleg vurdering av kumulativitet
- data/nordic_design_research.sqlite.gz — komprimert **offentleg metadata-only**-database; programmet gjenopprettar han automatisk
- results/RAPPORT.md — generert rapport; sjå figurar, CSV, JSON
- results/included_publications.csv — førebels tittelinkluderte postar, utan opphavsrettsleg verna samandrag
- results/candidates_for_manual_review.csv — utelatne frå automatisk analyseseleksjon
- results/lsa_vectors.npz — latent semantisk tekstrepresentasjon

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
