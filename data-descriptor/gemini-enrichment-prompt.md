# Gemini Vision enrichment prompt

For kvart stolbilete (bguw/), send dette promptet:

```
Analyser dette stolbiletet. Returner KUN eit JSON-objekt med desse felta:

{
  "tal_komponentar": <int, tal på distinkte strukturelle delar: bein, sete, rygg, armlene, sargar, etc.>,
  "har_armlene": <bool>,
  "har_polstring": <bool>,
  "rygg_type": <"open" | "heiltre" | "polstra" | "spiler" | "ingen">,
  "tal_bein": <int>,
  "symmetri": <"bilateral" | "radial" | "asymmetrisk">,
  "synleg_samansetjing": <"tapp-og-hol" | "skruar" | "bøygd" | "sveisa" | "ingen_synleg">,
  "ornament_nivaa": <0-3, 0=ingen, 1=enkel, 2=moderat, 3=rikt dekorert>,
  "struktur_type": <"fire-bein" | "frittberande" | "pidestall" | "bukk" | "samanleggbar" | "stablbar" | "gyngande" | "anna">
}
```

Bruk `gemini-2.5-flash`. Batch med 40 concurrent workers. Lagre som `STOLAR/vision_features.csv`.
