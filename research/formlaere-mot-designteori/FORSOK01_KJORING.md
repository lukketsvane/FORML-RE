# FORSØK 01: verkeleg CAD-motor, uavhengige vurderingar og nye val

*Pilotutgåve 7. november 2026. Knytt til [FORML-RE PR #20](https://github.com/lukketsvane/FORML-RE/pull/20) og [50x50x50 PR #5](https://github.com/lukketsvane/50x50x50.iverfinne.no/pull/5). Ingen menneskeval er registrerte enno.*

## Ferdig instrument

Eksporten i 50x50x50-motoren brukar dei fire aktive typologiane VAFFEL, SKIVE, STRAUM og RIBBE. Han hentar standardparametrar og eksisterande posar, måler objekt og testar harde/mjuke reglar med nettopp den motoren som nettsida nyttar. Han genererer åtte valsett med fire alternativ, dokumentert hash, motorparameterar, måltal og eksakte 3D-lenkjer. Kandidatar med harde modellregelbrot blir ikkje presenterte, men avvisinga blir loggført. Dette er **ikkje** fysisk sertifiserte møblar.

Den separate [HTML-innsamlaren](forsok01.html) lagrar ikkje noko på ein server. Han har tre roller: Vurderar 1 estimerer produksjons- og monteringsavvik, vurderar 2 estimerer bruks- og formavvik, og eit avgjerdspanel får sjå begge vurderingane og ta eit faktisk val. Kvar rolle eksporterer anonymisert JSON med manifest-hash og tidsstempel.

[Valdatakompilatoren](forsok01_samle.py) lagar eit balansert, frosen datasplitt for panel, validerer dei tre kjeldefilene per panel og skriv ei CSV-fil som [valbenchmarken](choice_benchmark.py) kan lese. Kompilatoren avviser svar med feil manifest, manglande rolle, same aktør på tvers av panel, manglande skårar og vurderingar datert etter valet.

## Køyring, utan endring av produksjonssida

1. I ein checkout av 50x50x50 PR #5, køyr:

       npx tsx scripts/formlaere-forsok01.ts > formlaere-kandidatar.json

   Arkiver manifest og kjelde-commit. GitHub Actions-jobben i PR-en er sett opp til å kontrollere hash, kandidatsett og fråvær av fabrikerte utfall.

2. I ein checkout av FORML-RE PR #20, i forskingsmappa:

       python forsok01_samle.py roster /sti/formlaere-kandidatar.json --out panel.csv --panels 12

   Frys roster **før** menneska vurderer kandidatane. Tolv panel krev tre ulike deltakarar per panel dersom ingen person skal delta i fleire train/test-grupper.

3. Opne forsok01.html i ein nettlesar med lokale filer, eller publiser han som ei isolert intern forskingsside. Kvar deltakar lastar inn SAME kandidatmanifest, skriv inn tildelt panelkode og ein pseudonym aktørkode. Vurderarane skal ikkje sjå sluttval. Begge gjev fire skårar frå 0 til 10 per valsett. Avgjerda skal vere fri, ikkje eit automatisert Gibbs-trekk.

4. Avgjerdspanelet lastar inn begge daterte vurderingsfilene og registrerer val under den førehandstildelte innverknadsregelen. Dei tre råfilene skal arkiverast uendra.

5. Etter innsamling legg forsøksleiaren alle anonymiserte svarfiler i ei mappe, og køyrer:

       python forsok01_samle.py compile /sti/formlaere-kandidatar.json panel.csv svar/ --out choices.csv
       python choice_benchmark.py --csv choices.csv

   Den siste kommandoen krev NumPy og SciPy. Rapporter fullførte og manglande panel, usikkerheit og alle rivalmodellar.

## Kva piloten faktisk testar

Dette er ei **avgrensa prøve av seleksjonsleddet**. For kvar generator er det valt eitt kuratert alternativ i kvart sett. Mu = 0,25 er ei uniform vekt i den stratifiserte framvisinga, **ikkje** den naturlege sannsynsfordelinga til grammatikken. Me kan ikkje hevde at generatoren og seleksjonen er identifiserte frå dette åleine.

Valsett kan dele dei same formfamiliane mellom panel. Ein test på nye menneske er ikkje nødvendigvis ein test på nye former. Neste fase må halde både aktørar og formfamiliar utanfor trening.

Tildelte innverknadsvekter er **prosedyrevekt**, ikkje målt faktisk makt. Dersom panelet avvik frå ordninga, er dette eit funn og må ikkje retterast slik at teorien ser rett ut. Tidsstempel frå ein klient kan manipulerast, så ein eventuell publisert studie bør ha eit uavhengig registreringsspor og forsvarleg frivillig samtykke.

Ingen får sitje på ein eksperimentell konstruksjon utan dokumentert fysisk last- og sikkerheitskontroll. Kandidatane frå 50×50×50 oppfyller ikkje automatisk særkrava til det separate Knappen-prosjektet.

**Status:** instrument og kontroller er laga; ingen sjølvstendige menneskelege svar er samla inn, og den fullstendige empiriske overlegenheitspåstanden står open.
