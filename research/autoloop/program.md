# FORMLÆRE AutoResearch: reell morfologisk prøve

**Mål:** Finn ein modell som føreseier stolars geometri betre enn ein fast referanse på ikkje-brukte objekt. Lågare normalisert MSE er betre.

Dette gjeld **observerte katalogmål**, ikkje kva designarar valde eller kvifor forma vart realisert. Ingen positiv skår her åleine stadfestar FORMLÆRE sin agentmodell eller at designteorien er overlegen konkurrentar.

## Frosen evaluering

- Kjelde: `lukketsvane/stolar-db/STOLAR/api.json`, commit `f9a87f52cb8e6e51e6ee12e1e2f9005bb489cf51`, SHA-256 `b552be3f754865854481c6f2ee1d46f604c59a8b70127963f402c6f328dab24e`.
- Etter dei publiserte inklusjonskriteria vert 1 598 museumspostar brukte, med gruppevis skilje mellom treningsobjekt og halde-ute objekt.
- Grupper av same skapar eller identiske målefamiliar får ikkje lekke over skiljet.
- Fast referanse: ridge med `year`, `technique`, `origin`, `materials` og alpha 20.
- Måltal: gjennomsnittleg normalisert MSE for log(H/W), log(W/D), log geometrisk storleik.
- Frosen utviklingsskår: 5 gruppevise splittar, baseline **0,9169902054**.
- Frosen sluttprøve: 20 % av ubrukte grupper, **skal ikkje målast før heile sløyfa stoppar**.
- For å ta vare på ei endring må ho redusere MSE med minst 0,005 mot både referansen og tidlegare beste kandidat, og slå referansen i minst 4 av 5 splittar. Alle 55 eksisterande forskingstestar må dessutan bestå.
- Ingen endring i målkode, datasplitt, grunnlagsfil, evals, kontrollar eller kjelder er tillaten. Modellen kan berre endre `candidate.py`.

## Kvar runde

1. Claude Fable 5.2 skal leggje fram ein ny, enkel hypotese om kva informasjon eller transformasjon som kan føreseie kataloggeometri betre.
2. Les førre resultat i `research/autoloop/history/` om dei finst. Ikkje gjenta ei tidlegare forkasta løysing utan ei ny grunngjeving. Endre berre `research/autoloop/candidate.py`, funksjonen `predict(features, y_train)`.
3. Bruk berre eigenskapane frå dei fire frosne matrisene `features`. Ikkje les rådata, skjulte testmål eller andre filer frå kandidatfunksjonen. Ikkje bruk objekt-ID, namn, målvariablane eller framtidige etikettar til prediksjon.
4. Prøv kandidatten mot fast utviklingsskår. Tek sløyfa ikkje steget framover, gjenopprett førre versjon automatisk.
5. Registrer faktiske resultat og kostnad, også negative. Etter to mislukka rundar på rad stoppar forsøket automatisk.
6. Når sløyfa stoppar, køyr den forsegla sluttprøva berre éin gong. Slår kandidaten ikkje referansen på ubrukte grupper, går me tilbake til referansen.

## Kostnad og sikkerheit

Høgst 10 modellkall à førehandsreservert 8 USD: **80 USD** automatisk reservert av dei 100 USD brukaren har sett av. Dei resterande 20 USD er buffer for ikkje nøyaktig kostnadsavgrensing og mogleg seinare validering. Eitt modellkall kan ha ulik reell fakturering. `total_cost_usd` er modellklienten sitt estimat, ikkje bekrefta rekning frå Anthropic. Dette oppsettet garanterer ikkje ei absolutt konto-/organisasjonsgrense.

Inga menneskeleg gjennomlesing er kravd for å godta rein, numerisk målebar framgang i **forskingskode**. Teoretiske slutningar, kjeldepåstandar og manuskript skal ikkje automatisk endrast av dette forsøket.

Agenten får ingen Bash- eller nettverkstilgang via Claude-verktøyet; testkøyraren utfører den låste evalueringa. Berre kandidatkoden vert akseptert automatisk. Ingen ekstra GitHub-greiner per runde.

Dette er ein avgrensa reproduksjon av prinsippet i <https://github.com/karpathy/autoresearch>: målbar, frosen eval; éi endring; mål; godta eller forkast; loggfør.
