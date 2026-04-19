# STOLAR Research Findings Log

## Statistiske funn (2026-04-12)

### STERKE FUNN

**1. Ornament driv geometri (ikkje berre dekorerer)**
- ornament vs sphaerisitet: ρ = -0.429, p < 0.001
- ornament vs tregleiksratio: ρ = -0.401, p < 0.001
- ornament vs kompleksitet: ρ = -0.245, p = 0.002
- Ornamenterte stolar er MINDRE sfæriske og MINDRE kompakte. Ornament er ikkje dekorasjon; det endrar grunnforma.

**2. Stil ≠ Geometri**
- ARI = 0.028, NMI = 0.088
- Kunsthistoriske stilperiodar har nesten NULL samanheng med geometriske klynger
- LDA: 24.8% accuracy vs 9.1% chance (2.7x). Signal er reelt men svakt
- Stil er ein kulturell etikett, ikkje ein formkategori

**3. Alle mesh-trekk har høgt signifikante tidstrendar**
- Sphaerisitet aukar: ρ = 0.415, p < 10^-48
- Tregleiksratio aukar: ρ = 0.368, p < 10^-37
- Kompleksitet aukar: ρ = 0.174, p < 10^-9
- Fyllgrad aukar: ρ = 0.110, p < 10^-4
- Stolar vert rundare, meir kompakte, meir komplekse og tettare over tid

**4. Formrommet krympar, så ekspanderer**
- 1500-1700: hull = 48.01 (n=187), hull/n = 0.257
- 1700-1800: hull = 43.00 (n=357), hull/n = 0.120
- 1800-1900: hull = 33.07 (n=274), hull/n = 0.121
- 1900-2025: hull = 44.16 (n=310), hull/n = 0.143
- Industriell standardisering krympa rommet; modernismen opna det att

**5. Materialdiversitet ≠ geometrisk diversitet**
- 1600s: 19 mat, geom.div = 0.197
- 1700s: 27 mat, geom.div = 0.164
- 1800s: 31 mat, geom.div = 0.138
- 1900s: 44 mat, geom.div = 0.195
- 1800-talet har FLEST materialar etter 1600 men LÅGASTE formvariasjonen

**6. PCA-aksar**
- PC1 (35.5%): tregleiksratio (+0.66) og sphaerisitet (+0.57) = kompaktheit/runding
- PC2 (24.5%): hylstervolum (+0.73) og kompleksitet (-0.63) = masse vs detalj
- 60% total forklart varians

**7. Korrelasjonsstruktur**
- hogde-volum: r = 0.64
- breidde-djupn: r = 0.78 (stolar har nesten kvadratiske planproporsjonar)
- sphaerisitet-tregleiksratio: r = 0.57
- mesh-trekk er i stor grad uavhengige av katalogdimensjonar (alle |r| < 0.25)

**8. Material driv form (men ikkje kompleksitet)**
- Kruskal-Wallis sphaerisitet: H=53.6, p < 10^-9
- Kruskal-Wallis fyllgrad: H=55.3, p < 10^-9
- Kruskal-Wallis tregleiksratio: H=48.8, p < 10^-8
- Kruskal-Wallis kompleksitet: H=12.3, p=0.09 (ikkje signifikant!)
- Material avgjer kor rund og kompakt ein stol er, men IKKJE kor detaljert

**9. Polstring endrar form**
- Polstra stolar er meir sfæriske: median 0.819 vs 0.802, p < 0.05
- Polstra stolar er meir komplekse: median 5.343 vs 5.220, p < 0.05

**10. Dimensjonskonvergens er ikkje monoton**
- Hogde CV: pre-1700=0.918, 1700s=0.302, 1800s=0.718, post-1900=0.333
- Breidde CV: pre-1700=0.770, 1700s=0.433, 1800s=0.452, post-1900=0.501
- Dramatisk drop til 1700-talet, auking att på 1800-talet, ny stabilisering

**11. Temporalt naboskap er reelt men svakt**
- Same period mean dist: 0.541 vs diff period: 0.538
- Cohen's d = 0.005. Tid forklarar nesten ingenting av formvariasjonen

**12. Sphaerisitet er ekstremt skeivfordelt**
- skewness = -5.39, kurtosis = 54.66
- Dei fleste stolar er runde; lang hale av ikkje-sfæriske
- Hull_volume endå verre: skew = +23.76, kurt = 575

**13. Museum-bias er minimal**
- Barokk: NM sph=0.763 vs VA sph=0.782 (signifikant men liten effekt)
- Rokokko, Nyklassisisme, Historisme: ingen signifikant skilnad

**14. Mest typiske stolar**
- Hepplewhite-stol OK-08490 (1790): nærast sentroiden
- Den "gjennomsnittlege stolen" er ein britisk nyklassisistisk trestol frå seint 1700-tal

**15. Mest uvanle stolar**
- O368671 Barokk-stol (1692): Mahalanobis d=14.3
- O119975 "Pratt" nyklassisist-stol (1790): d=14.0
- Antelope-stol (1951): d=10.6; mest uvanle modernist

### AVANSERTE ANALYSAR (2026-04-12/13)

**16. DISPARITY THROUGH TIME (DTT)**
- Sum of variances per 50-årsperiode:
  - 1525: 4.89 (n=9, høg men lite utval)
  - 1675: 8.42 (n=130, TOPP; barokken hadde storst formvariasjon)
  - 1775: 3.62 (n=252, BOTN; nyklassisismen var mest einsarta)
  - 1875: 2.73 (n=162, minste variasjon nokosinne med godt utval)
  - 1975: 5.15 (n=190, AUKING; postmodernismen opna formrommet att)
- Mean pairwise dist: synk frå 3.08 (1525) til 2.07 (1875), stig att til 2.72 (1975)
- FORTELJINGA: formrommet krympa monotont frå 1500 til 1875 (industrialisering+standardisering), så ekspanderte det att med modernismen

**17. PERMANOVA (stil vs geometri)**
- F = 7.80, R2 = 0.072, p = 0.001 (999 permutasjonar)
- Stil forklarar berre 7.2% av geometrisk varians; 92.8% er innanfor stilar
- SIGNIFIKANT men SVAK effekt: stilar ER geometrisk ulike, men skilnadene er små relativt til variasjonen innanfor kvar stil
- Mest spreidd stil: Postmodernisme (disp=1.989); minst spreidd: Empire (disp=1.181)

**18. RANDOM FOREST STILKLASSIFISERING**
- 5-fold accuracy: 36.6% (sjanse=8.3%, lift=4.4x)
- Hogde er det VIKTIGASTE trekket (0.152); alle mesh-trekk er nesten like viktige (0.11-0.13)
- Best klassifiserte stilar: Barokk (61%), Nyklassisisme (60%), Empire (45%)
- Verst: Samtidsdesign (8%), Viktorianisme (13%), Renessanse (15%)
- INNSIKT: nokre stilar har distinkt geometri (Barokk, Nyklassisisme) medan andre er formelt udefinerte

**19. SIMILARITY NETWORK + LOUVAIN COMMUNITIES**
- 1290 noder, 8767 kantar (k=10 NN)
- 12 communities funne; modularity = 0.79 (høg; nettverket har klar struktur)
- ARI vs stilperiodar: 0.037 (nesten null samanheng)
- NMI vs stilperiodar: 0.149 (svakt signal)
- Communities grupperer etter GEOMETRI, ikkje STIL: C0 er "sfæriske stolar" (sph=0.836), C3 er "kantete stolar" (sph=0.741)
- Kvar community blandar fleire stilperiodar; ingen community er dominert av éin stil

**20. STILTRAJETORIAR GJENNOM MORFOROM**
- Storste sentroidskift: Art Deco (1.236), Barokk (1.084), Renessanse (0.963)
- Minste skift: Funksjonalisme (0.099); funksjonalismen er den mest geometrisk stabile stilen
- Dispersjonsendring: Renessanse krympar (ratio=0.62), Rokokko krympar (0.60), Postmodernisme krympar (0.59)
- Empire og Art Deco ekspanderer (ratio 1.17, 1.19)
- Kronologisk centroid: klar drift langs PC1 frå negativ (pre-1750) til positiv (post-1900); stolar vert meir kompakte

**21a. KOLMOGOROV COMPRESSION (FULLFØRT)**
- Kompresjonsratio (gzip): mean = 0.366, std = 0.007, range 0.333-0.380
- Kompresjon vs sphaerisitet: ρ = 0.410, p < 10^-9 (rundare = vanskelegare å komprimere)
- Kompresjon vs mesh-kompleksitet: ρ = 0.176, p = 0.013
- Kompresjon vs årstal: ρ = 0.144, p = 0.042
- Per-stil: nesten identisk (0.364-0.367); Kolmogorov skil ikkje mellom stilar
- TOLKING: Informasjonsteoretisk kompleksitet fangar overflategeometri (kurvatur) men ikkje kulturell stil

**21b. FILSTORLEIK SOM KOMPLEKSITETSPROXY**
- GLB-filstorleik: mean=10.6 MB, median=9.3 MB, range 2.3-77.0 MB
- Filstorleik vs sphaerisitet: ρ = 0.634, p < 10^-146 (STERKT!)
- Filstorleik vs kompleksitet: ρ = 0.128, p < 10^-6
- Filstorleik vs årstal: ρ = 0.177, p < 10^-10
- Rundare stolar har storare filer; dette er overraskande
- Modernisme har storaste filer (13.8 MB median vs 8.7-9.7 MB for andre)
- TOLKING: Hunyuan3D-2 genererer meir detaljerte meshar for rundare former fordi dei har meir overflate å fange

**22. IMAGEPLOT**
- 293 stolar plotta som sine eigne bilete i kompleksitet x sphaerisitet-rommet
- Visuelt slåande; du kan sjå korleis formtypar klyngjer seg

### SVAKE / IKKJE-FUNN

- Komponenttal vs mesh-trekk: ingen signifikante korrelasjonar (alle p > 0.07)
- Fire-bein vs andre strukturtypar: ingen signifikant skilnad i sphaerisitet eller tregleiksratio
- Gylne snitt: mean H:W = 1.548, signifikant UNDER phi (p < 0.001). IKKJE gylne snitt.
