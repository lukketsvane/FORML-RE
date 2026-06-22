#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teikne-formetaten.py — FORMETATEN-sider: full tekst + spekulative teikningar."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("ts", "teikne-sider.py")
ts = importlib.util.module_from_spec(spec); sys.modules["ts"] = ts
spec.loader.exec_module(ts)
ts.STIL = 'Lag ei boksside i same penn-og-blekk-ånd som dei vedlagde referansane (Andreas Töpfer; Negarestani sin Cyclonopedia; Harman sin Quadruple Object) — spekulative, oppfinnsame svartkvit-teikningar. Teikna LAUST, raskt og skissaktig — IKKJE detaljert, polert eller realistisk. ABSTRAKT og konseptuelt, ikkje bokstavleg: rare oppfunne former, ikkje pene avbildingar av ting. Overraskande og dristig, aldri keisamt (bland). Match referansane TETT: same strekkvalitet, tettleik og komposisjon.\n\nVIKTIG: ALL teksten nedanfor skal stå på sida, sett som EKTE, LESELEG, korrekt stava trykt serif-tekst — heile teksten, ord for ord, i same rekkjefølgje, med sidetal. Ikkje kutt, ikkje parafraser, ikkje krot. Dette er ei forteljing (norsk bokmål) frå etaten FORMETATEN.\n\nSaman med teksten: spekulative teikningar som illustrerer scenene — ansiktslause tenestemenn, ein leirklump (Klumpen) i ein plastpose, ein stol som svevar ein centimeter over golvet, takdrypp i ei bøtte, Omnen (omn som godkjenner form), ein 400 år gammal polystyrenkopp med leppestift, ein mandelforma urgammal stein, marsipangrisar. Samanhengande svart konturlinje på kvitt papir, nokre solide svarte flater; ingen farge. Ansiktslause kroppar med vekt og volum.\n\nFORMAT: EI EINSKILD STÅANDE SIDE (portrett, om lag 2:3) — IKKJE eit oppslag, IKKJE to sider, IKKJE liggjande. Éi bokside om gongen, med sidetal.\n\netc:'
sys.argv = ["teikne-formetaten", "--utsnitt", "formetaten-sider.txt", "--ut", "sider-formetaten-portrett", "--maks-refs", "5", "--storleik", "2304x3456"] + sys.argv[1:]
ts.main()
