# FORMLÆRE: forskingssløyfa

Arbeid berre på greina `autoresearch/formlaere-designteori-20261115`. Utgangspunktet er den autoritative `traktat/tekst/formlaere.tex` på `main`. Ikkje bland dette med eldre traktatarkiv.

## Målestokk

Ei betre formulering er ikkje eit betre forskingsresultat. Hovudmålet er prediksjonar, forklaringsskilje og motprøver som andre kan gjenta. Ingen agent skal sjølv stadfeste påstandar ved å gje eigne svar høg karakter. Inga endring av `main` utan menneskeleg gjennomgang.

## Kjeldene

- `traktat/tekst/formlaere.tex`: 491 proposisjonar fordelt 118, 27, 20, 16, 145, 112, 53.
- `research/nordisk-designforsking/results/possible_counterexamples_to_non_cumulative_design.csv`: 150 prioriterte siteringspar. Dei manuelle kontrollfelta er ikkje fylte ut. Kandidat er ikkje motbevis, replikasjon eller stadfesting.
- `research/nordisk-designforsking/CODEBOOK.md`: variablane H1–H3, E1–E3 og C1–C5; fulltekst, dokumenterte sidetal og uavhengig dobbeltkoding før publiserbare konklusjonar.
- `lukketsvane/designteori`, `docs/data/korpus.csv`: 6432 bibliografiske registreringar i siste undersøkte eksport. Korpuset er nyttig til leiting og samanlikningar, men ikkje 6432 fulltekstar eller manuelt validerte arbeid.
- PR #20: `research/formlaere-mot-designteori/` har forsøksprotokoll, bevisregister og CAD-instrument. Dette er ein kandidat for selektiv innhenting, ikkje empirisk bevis eller ein PR som skal merge automatisk.
- PR #18 og #21: umerga tekstrevisjonar som må vurderast opp mot den gjeldande kjelda før eventuell cherry-pick.

## Éin runde

1. Frys git-SHA for manuskript, korpus, evalkode og førre hypotese. Vel éin nummerert proposisjon og skriv ei avgrensa påstand.
2. Beskriv minst éi seriøs rivalforklaring eller motmodell. Oppgje kva ulik observasjon dei føreseier, eller kva konkret motdøme som kan felle påstanden.
3. Finn moglege belegg i begge korpus. Kontroller primærkjelda, faktiske avsnitt/sider og utvalsvilkår før du oppgraderer noko frå kandidat. Manglande fulltekst vert ståande som uviss, aldri negativ evidens.
4. Frys metode, utval, baseline, målevariabel og avgjerdsregel før du ser testutfalla. Skil utviklingsmaterialet frå ei uendra utprøvingsmengde; det same materialet kan ikkje både utvikle og validere modellen.
5. Skriv eitt avgrensa forsøkskort i `autoresearch/experiments/` med `claim`, `rival`, `falsifier`, `measurement`, `baseline`, `proposition`, `status`, `evidence`. Bruk berre `open`, `needs-human-review` eller `inconclusive` før uavhengig vurdering.
6. Køyre `python autoresearch/harness.py check --record <fil>` og `python -m unittest discover -s autoresearch -p "test_*.py"`. Logg faktiske data, nullfunn, testskårar og svikt.
7. Forslag til endringar i proposisjonar kjem som ein eigen diff med argument, kjelder og reverserbar test. Berre dersom prøva skil rivalane og resultatet toler kontroll, kan endringa tilrådast. Ingen auto-merge.

Agentrollene kan vere *forslagsstillar*, *kritisk motlesar*, *matematisk kontrollør* og *kjeldelesar*. Dei må byggje på same frosne kjelder, ikkje berre samtykkje med kvarandre.

## Køyrbar avgrensa kontroll

```sh
python autoresearch/harness.py status
python autoresearch/harness.py search "replication"
python autoresearch/harness.py search "participatory design" --designteori /sti/til/designteori/docs/data/korpus.csv
python autoresearch/harness.py check --record autoresearch/experiments/0001-kumulativitet.json
python -m unittest discover -s autoresearch -p "test_*.py"
```

`status` tel proposisjonar, bibliografiske kandidatar og dokumentert fulltekstkontroll og rapporterer kjeldehashar. `search` er berre enkelt tittelordsøk for å finne kandidatar, ikkje semantisk relevans eller validert fagleg bevis. `check` validerer strukturen til forsøkskort, ikkje vitskapleg sanning.

Korpuset i `designteori` skal liggje utanfor dette repoet eller sendast inn som lokal fil. Ikkje kopier private/fulltekst-PDF-ar inn i GitHub.

## Grenser for endringar og kostnad

- Ikkje endre `main`, ikkje merge automatisk, og ikkje slett greiner med unike commits.
- Bruk git fetch og inspiser diff/CI for PR #18, #20 og #21 før selektiv cherry-pick. Ta berre med endringar som ikkje kolliderer med gjeldande manuskript; PR #20 sine data/protokollar er første kandidat.
- Start med éi forskingsrunde om gongen, med eksplisitt modell og API-budsjett. Ikkje køyr fleire autonome forsøk berre fordi eit språkmodell-estimat ser betre ut.
- Det er først ein vitskapleg framgang når ein ekstern prøve eller ny kontrollert utleiing skil teorien frå rivalen.
