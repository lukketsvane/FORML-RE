# FORMLÆRE: føreord og etterord

Dette er ei sjølvstendig litterær redaksjon med Claude Fable 5.2. Ho køyrer separat frå den ordinære AutoResearch-sløyfa og skal ikkje gjere dei same inngrepa om att.

Les først **heile** `traktat/tekst/formlaere.tex`, inkludert føreordet, lesekoden, alle 491 proposisjonar og den siste lina i 7.34. Les så dei siste rapportane under `traktat/revisjon/litteraer-autoresearch-*.md`. Gjer deg opp ei sjølvstendig meining før du les kva dei tidlegare modellane meinte.

## Arbeidet

**Føreord:** Revider berre teksten mellom `\section{Føreord}` og `\section{Lesekode}`. Gjer argumentet skarpare, mindre førehandsforklarande og mindre sjølvhevdande. Prøv om ansvaret for det forma gjer med andre, og spørsmålet om kva som kan felle læra, kan verke gjennom komposisjonen i staden for å verte proklamert. Behald brodden, men svekk påstandar som den fullstendige traktaten ikkje gjev grunnlag for. Prøv mot tekstens eigen motstand, ikkje mot smak eller tal.

**Etterord:** Skriv eit heilt nytt, litterært etterord etter `\end{formproposition}` til 7.34, med nøyaktig `\section{Etterord}`. Finn ei form som får slutten til å verke attende på byrjinga. Gå lenger enn eit samandrag og unngå å rose verket eller teorien. Den som les, skal stå att med noko som kan prøvast, og noko som har fått endra tyding under lesinga. Behald det opne i «Fjellet er ikkje i kartet. Men den som les kartet, står på fjellet.» om det framleis ber. Fire til åtte konsentrerte avsnitt er høveleg. Dette skal vere prosa, ikkje nye proposisjonar.

Bruk tre ulike motlesingar dersom budsjettet tillet det: ein kompromisslaus litterær lesar, ein filosof som prøver premissane, og ein lesar som ber konsekvensane av ei form. Dei skal fyrst lese uavhengig av kvarandre. Vurder radikale alternativ, men forkast alt som berre forklarer, gjentek eller pyntar. Ei endring treng ikkje verte stor for å verke i heilskapen.

## Strenge grenser

- Endre **berre** `traktat/tekst/formlaere.tex` og den oppgjevne rapportfila.
- Ingen eksisterande proposisjon, proposisjonsadresse, type, rekkjefølgje eller tekst får endrast, heller ikkje 7.34.
- Behald alle matematiske uttrykk, kjeldemarkeringar og notatmarkørar i same rekkjefølgje. Ikkje innfør nye formlar, kjelder eller note-ID-ar i etterordet.
- Hald dei eksisterande seksjonsoverskriftene urørte. Legg berre til den nye `\section{Etterord}` heilt til slutt.
- Ingen endring i testkode, CSS, generert HTML, PDF, byggjesystem eller workflow. Desse vert bygde og validerte etter redaksjonen.
- Nynorsk, «me» der det er naturleg, aldri em dash. Bruk berre LaTeX-syntaks den eksisterande parseren støttar.

## Rapport

Skriv ei kritisk rapportfil på den oppgjevne staden, minst 1200 teikn, med dei fire overskriftene:

### Behaldne
### Forkasta
### Heilskap
### Uvisse

Skildre konkrete endringar og tap, reelt forkasta framlegg, forholdet til heile traktaten og kva som ikkje er avklart. Ikkje framstill litterær dom som empirisk prov. Ikkje opprett PR eller push. Arbeidsflyten flettar automatisk berre etter beståtte kontrollar, og stoppar ved konflikt med parallell revisjon.
