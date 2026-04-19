# Formskrift-atlaset

Eit visuelt atlas og formelt notasjonssystem som følgjer **FORMLÆRE** av Iver Raknes Finne. Atlaset samanstiller traktaten sine proposisjonar grafisk, viser at rammeverket gjeld på tvers av sytten substratnivå, og introduserer **formskrifta**, ei piktografisk notasjon bygd på Unicode-glyfar.

## Struktur

```
formskrift-atlas/
├── README.md
├── Makefile
├── tex/            # LaTeX-kjelder
└── pdf/            # Kompilerte PDF-ar
```

## Innhald

### Atlaset (15 sider samla)

1. **forside.tex** og **notasjon.tex** — forside og komponentkart
2. **pg-seksjon-1.tex** til **pg-seksjon-8.tex** — åtte proposisjonsgrafar, éin per seksjon i traktaten
3. **skalahierarki.tex** — dei sytten kognitive lyskjeglene frå kvark til sivilisasjon
4. **formskrift-einside.tex** — alfabet, kompositorreglar og kjerne-likninga på éi side
5. **formskrift-bevis-einside.tex** — sytten formelle bevis på éi side

### Lengre variantar (for eigenstudium eller distribusjon)

- **formskrift-unicode.tex** — seks-sides versjon med alle bevis og diskusjon
- **formskrift-artikkel.tex** — ti-sides akademisk framstilling av notasjonen

## Typografiske val

- **Font**: TeX Gyre Pagella (hovudtekst) + Symbola (Unicode-glyfar)
- **Kompilator**: XeLaTeX (krev Unicode-støtte)
- **Papirformat**: A4
- **Språk**: Nynorsk

## Kompilering

Du treng XeLaTeX og Symbola-fonten. På Linux/macOS:

```bash
# Installer Symbola-fonten (Ubuntu/Debian)
sudo apt-get install fonts-symbola

# Kompiler alt
make

# Eller enkelteringar
make atlas          # Set saman til ein PDF
make formskrift     # Berre formskrift-sidene
```

På Windows med MiKTeX eller TeX Live må Symbola installerast separat. Sjå [unifoundry.com/symbola](https://unifoundry.com/symbola.html).

## Designprinsipp

Formskrifta følgjer fem reglar:

1. **Linevekt** er 0.4 pt gjennomgåande (utanfor Symbola)
2. **Glyfar** kjem frå Unicode, ikkje teikna
3. **Fyllregel**: strukturelt aktive element er fylte, passive rom er opne
4. **Komposisjon**: sekstan glyfar bygd frå sju primitivar gjennom åtte reglar
5. **Semantikk**: kvar glyf har éin kanonisk tyding

## Sentrale omgrep og glyfar

| Glyf | Omgrep |
|------|--------|
| ▲ | agent |
| (▲) | designar |
| ● | form |
| ⬢ | formgrammatikk |
| □ | formrom |
| ◇ | kognitiv lyskjegle |
| ☉ | omhug |
| ◐ | partisjon |
| ↘ | seleksjonstrykk |
| ∿ | tilpassingslandskap |
| ▽ | substrat |
| ⬟ | transformasjon |

Kjerne-likninga: **● = ⬢(∇∿) ∩ ◇**

Forma er grammatikkens respons på landskapets gradient, projisert på agenten si lyskjegle.

## Lisens

Arbeidet er del av ei doktoravhandling ved Arkitektur- og designhøgskolen i Oslo.
