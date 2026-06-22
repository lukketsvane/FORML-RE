#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teikne-sider.py — genererer heilside-illustrasjonar til GRUNNLAUST med
OpenAI sin biletmodell (gpt-image-2), i den same penn-og-blekk-stilen som
Andreas Töpfer sine teikningar til Armen Avanessian-bøkene.

Arbeidsgang (slik tinginga lyder):
  1.  «last opp» referansebileta  -> dei vert sende med på KVAR kall som
      stilreferanse (images.edit tek ei liste med bilete).
  2.  les boka kapittel for kapittel i lesEREKKEFØLGJA frå grunnlaust.tex,
      strippar LaTeX til rein nynorsk brødtekst.
  3.  del teksten i oppslag på ~2 sider om gongen (--ord styrer mengda).
  4.  for kvart oppslag: bygg ein prompt (fast stilspesifikasjon + teksten
      som brief) og kall  client.images.edit(model="gpt-image-2", image=[refs], ...).
  5.  lagra PNG i  sider/  og før manifest.json.

Køyring er idempotent: ferdige sider vert hoppa over (--paa-nytt tvingar).
--proev viser planen utan å kalle APIet (gratis), og er fullt testbar offline.

  python3 teikne-sider.py --proev                 # vis plan, ingen kall
  python3 teikne-sider.py --berre 00-til-lesaren  # éin fil
  python3 teikne-sider.py --grense 1              # berre fyrste oppslaget
  python3 teikne-sider.py                         # heile boka

Krev:  pip install openai Pillow   og   OPENAI_API_KEY i miljøet.
Referansebilete: legg JPEG/PNG-ane (t.d. IMG_4026.jpeg) i  stil-referansar/.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

HER = Path(__file__).resolve().parent           # grunnlaust/figurar/
SRC = HER.parent / "src"                         # grunnlaust/src/
HOVUD = SRC / "grunnlaust.tex"                   # for lesErekkjefølgja
REF_DIR = HER / "stil-referansar"                # stilreferansane (du fyller han)
UT_DIR = HER / "sider"                           # ferdige sider hamnar her
MANIFEST = UT_DIR / "manifest.json"

# Standardval. gpt-image-2 finst på kontoen; boka er 165x240 mm (ståande ~2:3),
# så portrett er rett — ikkje det 16:9 som code-snutten hadde. Storleiken er
# eit flagg av di gpt-image-2 kan ta fleire mål enn gpt-image-1.
STD_MODELL = "gpt-image-2"
STD_STORLEIK = "2304x3456"      # EI ståande side (portrett ~2:3), under px-budsjettet
STD_KVALITET = "high"
STD_ORD = 850                   # ~eitt oppslag ≈ to boksider tekst
STD_UTSNITT = HER / "utsnitt.txt"   # valfrie kuraterte korte parti (--utsnitt)
STD_REF_FIL = "IMG_4017.jpeg"   # referansefilnamn i utskriven kode (--kode)
GYLDIGE_KVALITETAR = {"low", "medium", "high", "auto"}

# --------------------------------------------------------------------------
# STILSPESIFIKASJON — fast del av kvar prompt. Ordrett etter det fungerande
# eksempelet (kort nynorsk-instruks; teksten følgjer rett etter «etc:»).
# --------------------------------------------------------------------------
STIL = (
    "Lag ei bokside i same ånd som dei vedlagde referansane (Andreas Töpfer; "
    "Reza Negarestani sin Cyclonopedia; Graham Harman sin Quadruple Object). "
    "Tenk, observer, planlegg, så teikn.\n\n"
    "TEIKNESTIL (viktigast): teikna LAUST, raskt og skissaktig, med spontan, handlaga "
    "blekkstrek slik som i referansane. IKKJE detaljert, polert, glatt eller realistisk. "
    "Formene er ABSTRAKTE og konseptuelle, ikkje bokstavlege: gjer omgrepa om til rare, "
    "oppfunne former, diagram og umoglege scenar — IKKJE pene, realistiske avbildingar "
    "av møblar, rom og ting. Ver OVERRASKANDE, dristig og eigenarta — aldri generisk, "
    "dekorativt eller keisamt (bland).\n\n"
    "TEIKNINGANE DOMINERER sida: store, SPEKULATIVE penn-og-blekk-teikningar — "
    "ansiktslause kroppar som rom og kar, figurar inni kuler og strukturar, "
    "gjennomskjeringar og snitt, ting som morfar til andre ting, same figur i fleire "
    "tilstandar, uvanlege perspektiv. Samanhengande svart konturlinje på kvitt papir; "
    "nokre solide svarte flater og stipla hjelpelinjer (som i Cyclonopedia); ingen "
    "farge, ingen gråtone-skugge. Aldri bokstavlege ikon.\n\n"
    "TEKSTEN er forankring, ikkje fyll: set teksten nedanfor som eit MODEST blokk ekte, "
    "leseleg, korrekt stava trykt serif-tekst — typisk éi spalte eller eit avsnitt — og "
    "IKKJE fyll heile sida med tekst; storparten av flata er teikning. Ord for ord, ikkje krot, "
    "ikkje parafrase. Løpande topptekst (tittelen) og sidetal som i referansane. "
    "Handskrift berre på små figur-etikettar, få og små.\n\n"
    "Lat teikninga bere meininga.\n\n"
    "FORMAT: EI EINSKILD STÅANDE SIDE (portrett, om lag 2:3) — IKKJE eit oppslag, "
    "IKKJE to sider, IKKJE liggjande. Éi bokside om gongen, med sidetal. Teksten SKAL "
    "stå på sida som ekte leseleg trykt tekst. Match dei vedlagde referansane tett: "
    "same strekkvalitet, tettleik, komposisjon og handskrift.\n\netc:"
)

# ==========================================================================
# LaTeX -> rein tekst
# ==========================================================================

def _fjern_balansert(s: str, kommando: str) -> str:
    """Fjern  \\kommando[..]{..}  inkludert det balanserte {..}-argumentet."""
    ut = []
    i = 0
    n = len(s)
    nøkkel = "\\" + kommando
    while i < n:
        j = s.find(nøkkel, i)
        if j == -1:
            ut.append(s[i:])
            break
        # sikre at det er heile kommandonamnet (ikkje prefiks av eit lengre)
        k = j + len(nøkkel)
        if k < n and (s[k].isalpha() or s[k] == "*"):
            ut.append(s[i:j + len(nøkkel)])
            i = j + len(nøkkel)
            continue
        ut.append(s[i:j])
        # hopp over valfrie [..]
        while k < n and s[k] in " \t":
            k += 1
        while k < n and s[k] == "[":
            d = 1
            k += 1
            while k < n and d:
                d += {"[": 1, "]": -1}.get(s[k], 0)
                k += 1
            while k < n and s[k] in " \t":
                k += 1
        # hopp over eitt balansert {..}
        if k < n and s[k] == "{":
            d = 1
            k += 1
            while k < n and d:
                d += {"{": 1, "}": -1}.get(s[k], 0)
                k += 1
        i = k
    return "".join(ut)


def _pakk_ut(s: str, kommando: str) -> str:
    """\\kommando{arg} -> arg  (gjenta til ingen att; handterer nøsting)."""
    mønster = re.compile(r"\\" + kommando + r"\*?\s*\{")
    while True:
        m = mønster.search(s)
        if not m:
            return s
        start = m.end() - 1            # peikar på {
        d, k = 1, start + 1
        while k < len(s) and d:
            d += {"{": 1, "}": -1}.get(s[k], 0)
            k += 1
        s = s[:m.start()] + s[start + 1:k - 1] + s[k:]


def latex_til_tekst(rå: str) -> str:
    s = rå
    # 1) kommentarar (ikkje \%)
    s = re.sub(r"(?<!\\)%.*", "", s)
    # 2) heile bibliografiske/strukturelle blokker med argument
    for kmd in ("vidarelesing", "laeringsmal", "ovingar", "addcontentsline",
                "markboth", "markright", "label", "index", "includegraphics",
                "graphicspath", "input", "bokfigur", "nocite", "printbibliography",
                "caption", "hypersetup", "addfontfeature", "fontsize",
                "setlength", "vspace", "hspace", "rule", "needspace",
                "definecolor", "textcolor", "colorbox"):
        s = _fjern_balansert(s, kmd)
    # 3) sitatkommandoar -> bort (med argument). Tek vanlege variantar.
    for kmd in ("textcite", "textcites", "parencite", "parencites", "autocite",
                "footcite", "cite", "citeauthor", "citeyear", "supercite"):
        s = _fjern_balansert(s, kmd)
    # 4) overskrifter og utheving -> behald argumentet
    for kmd in ("chapter", "section", "subsection", "subsubsection", "paragraph",
                "emph", "textit", "textbf", "textsc", "textsl", "texttt",
                "underline", "uline", "enquote", "textsuperscript", "MakeLowercase",
                "MakeUppercase", "text", "mbox", "msym", "pic"):
        s = _pakk_ut(s, kmd)
    # 5) miljø: fjern \begin{..}/\end{..}, men la innhaldet stå
    s = re.sub(r"\\begin\{[^}]*\}(\[[^\]]*\])?(\{[^}]*\})?", "", s)
    s = re.sub(r"\\end\{[^}]*\}", "", s)
    # 6) punktlister
    s = re.sub(r"\\item\s*", "\n- ", s)
    # 7) lause makroar utan argument
    s = re.sub(r"\\(par|noindent|clearpage|newpage|nobreak|itshape|upshape|bfseries|"
               r"normalfont|centering|raggedleft|raggedright|small|footnotesize|"
               r"scriptsize|large|Large|LARGE|huge|Huge|normalsize|selectfont|"
               r"vignett|frontmatter|mainmatter|backmatter|null|fill|quad|qquad|"
               r"medskip|bigskip|smallskip|leavevmode|thispagestyle|pagestyle)\b",
               " ", s)
    # 8) teiknerstatningar
    erstatt = {
        r"\\\\": "\n", r"\\,": " ", r"\\;": " ", r"\\:": " ", r"\\ ": " ",
        r"\\&": "&", r"\\%": "%", r"\\#": "#", r"\\_": "_", r"\\\$": "$",
        r"~": " ", r"---": "—", r"--": "–",
        r"``": "“", r"''": "”", r"\\textendash": "–", r"\\textemdash": "—",
        r"\\textperiodcentered": "·", r"\\ldots": "…", r"\\dots": "…",
    }
    for a, b in erstatt.items():
        s = re.sub(a, b, s)
    # 9) rest-makroar (\foo) -> bort
    s = re.sub(r"\\[a-zA-Z@]+\*?", "", s)
    # 10) tomme klammer og opprydding
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ==========================================================================
# Les boka i rett rekkjefølgje og del i oppslag
# ==========================================================================

def lesefiler() -> list[Path]:
    """Filene i \\input-rekkjefølgja frå grunnlaust.tex (brødtekst-delen)."""
    rekkje: list[Path] = []
    if HOVUD.exists():
        for m in re.finditer(r"\\input\{([^}]+)\}", HOVUD.read_text(encoding="utf-8")):
            namn = m.group(1).strip()
            # hald oss til hovudargumentet; hopp over rein backmatter-apparatur
            if namn in ("ordliste",):
                continue
            p = SRC / (namn + ".tex")
            if p.exists():
                rekkje.append(p)
    if not rekkje:   # naudfall: alle nummererte + namngjevne, sortert
        rekkje = sorted(p for p in SRC.glob("*.tex") if p.name != "grunnlaust.tex")
    return rekkje


def avsnitt(tekst: str) -> list[str]:
    return [a.strip() for a in re.split(r"\n\s*\n", tekst) if a.strip()]


def _slug(s: str) -> str:
    s = s.lower()
    for a, b in (("æ", "ae"), ("ø", "o"), ("å", "a"), (" ", "-")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9-]", "", s)
    return re.sub(r"-+", "-", s).strip("-")[:32] or "utsnitt"


@dataclass
class Oppslag:
    nr: int
    kjelde: str                 # filnamn-stamme, t.d. "06-bauhaus"
    tittel: str                 # fyrste overskrift i biten
    tekst: str
    ord: int = 0
    prefiks: str = "side"       # filnamnprefiks ("side" / "utsnitt")
    bilete: str = ""            # utfilnamn

    def stamme(self) -> str:
        return f"{self.prefiks}-{self.nr:02d}-{self.kjelde}"


def del_i_oppslag(filer: list[Path], mål_ord: int) -> list[Oppslag]:
    """Grådig oppdeling: samle avsnitt til ~mål_ord per oppslag; ny fil => nytt
    oppslag. Ein for liten hale (< mål_ord/4) blir slegen inn i førre oppslag,
    så vi slepp einslege restsider."""
    min_hale = max(250, mål_ord // 3)
    oppslag: list[Oppslag] = []
    nr = 0
    for f in filer:
        rein = latex_til_tekst(f.read_text(encoding="utf-8"))
        if not rein:
            continue
        fyrste = rein.splitlines()[0].strip() if rein.splitlines() else f.stem
        bitar: list[str] = []
        bunke: list[str] = []
        bunke_ord = 0
        for a in avsnitt(rein):
            ao = len(a.split())
            if bunke and bunke_ord + ao > mål_ord:
                bitar.append("\n\n".join(bunke))
                bunke, bunke_ord = [], 0
            bunke.append(a)
            bunke_ord += ao
        if bunke:
            bitar.append("\n\n".join(bunke))
        if len(bitar) >= 2 and len(bitar[-1].split()) < min_hale:
            bitar[-2] = bitar[-2] + "\n\n" + bitar[-1]
            bitar.pop()
        for b in bitar:
            nr += 1
            oppslag.append(Oppslag(nr, f.stem, fyrste, b, len(b.split())))
    return oppslag


def les_utsnitt(sti: Path) -> list[Oppslag]:
    """Kuraterte korte parti. Blokker skilde med ein linje '==='; valfri
    fyrste linje '@ etikett' gjev kjelde/tittel. Føretrekt arbeidsmåte:
    eitt sterkt, kort utsnitt -> éi teikning som tek over sida."""
    rå = sti.read_text(encoding="utf-8")
    oppslag: list[Oppslag] = []
    nr = 0
    for blokk in re.split(r"(?m)^===+\s*$", rå):
        # fjern kommentar- og tomlinjer FYRST, så «@»-etiketten blir funnen
        linjer = [l for l in blokk.splitlines() if not l.lstrip().startswith("#")]
        while linjer and not linjer[0].strip():
            linjer.pop(0)
        while linjer and not linjer[-1].strip():
            linjer.pop()
        if not linjer:
            continue
        etikett = ""
        if linjer[0].lstrip().startswith("@"):
            etikett = linjer[0].lstrip()[1:].strip()
            linjer = linjer[1:]
        kropp = "\n".join(linjer).strip()
        if not kropp:
            continue
        nr += 1
        tittel = etikett or kropp.split(".")[0][:48]
        oppslag.append(Oppslag(nr, _slug(tittel), tittel, kropp,
                               len(kropp.split()), prefiks="utsnitt"))
    return oppslag


# ==========================================================================
# Prompt + API
# ==========================================================================

def bygg_prompt(o: Oppslag) -> str:
    # Den fungerande forma: instruks + «etc:» + bokteksten for oppslaget.
    return f"{STIL} {o.tekst}"


def referansebilete() -> list[Path]:
    if not REF_DIR.exists():
        return []
    er = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted(p for p in REF_DIR.iterdir() if p.suffix.lower() in er)


def lag_klient():
    from openai import OpenAI
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("FEIL: OPENAI_API_KEY er ikkje sett i miljøet.")
    return OpenAI()


def kall_med_backoff(klient, **kw):
    """images.edit med eksponentiell backoff på forbigåande feil."""
    from openai import APIError, APIConnectionError, RateLimitError
    forseinking = 2.0
    siste = None
    for forsok in range(5):
        opne = [open(p, "rb") for p in kw["_refs"]]
        try:
            argv = {k: v for k, v in kw.items() if not k.startswith("_")}
            return klient.images.edit(image=opne, **argv)
        except (APIConnectionError, RateLimitError) as e:
            siste = e
            if forsok == 4:
                break
            time.sleep(forseinking)
            forseinking *= 2
        except APIError as e:
            # 5xx er forbigåande; 4xx er reell (feil parameter osv.) -> stogg
            status = getattr(e, "status_code", None)
            if status and 500 <= status < 600 and forsok < 4:
                siste = e
                time.sleep(forseinking)
                forseinking *= 2
                continue
            raise
        finally:
            for fh in opne:
                fh.close()
    raise siste if siste else RuntimeError("ukjend feil i kall_med_backoff")


def lagra_svar(svar, ut: Path) -> dict:
    d = svar.data[0]
    if getattr(d, "b64_json", None):
        ut.write_bytes(base64.b64decode(d.b64_json))
    elif getattr(d, "url", None):
        import urllib.request
        urllib.request.urlretrieve(d.url, ut)
    else:
        raise RuntimeError("svaret hadde verken b64_json eller url")
    bruk = getattr(svar, "usage", None)
    return {"usage": bruk.model_dump() if hasattr(bruk, "model_dump") else None}


def les_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"sider": {}}


def skriv_manifest(m: dict) -> None:
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


# ==========================================================================
# Hovudprogram
# ==========================================================================

def main() -> None:
    global REF_DIR, UT_DIR, MANIFEST
    ap = argparse.ArgumentParser(description="Teikn GRUNNLAUST-sider med gpt-image-2.")
    ap.add_argument("--proev", action="store_true", help="vis plan, ingen API-kall")
    ap.add_argument("--kode", action="store_true",
                    help="skriv ut ferdige images.edits-kall til å lime inn sjølv (ingen API-kall)")
    ap.add_argument("--paa-nytt", action="store_true", help="lag om sider som finst frå før")
    ap.add_argument("--utsnitt", nargs="?", const=str(STD_UTSNITT), default=None,
                    metavar="FIL", help=f"valfritt: kuraterte korte parti ({STD_UTSNITT.name}) "
                    "i staden for oppslag frå heile boka")
    ap.add_argument("--ref-fil", default=STD_REF_FIL,
                    help=f"referansefilnamn i utskriven kode (std {STD_REF_FIL})")
    ap.add_argument("--maks-refs", type=int, default=5,
                    help="maks tal stilreferansar sende med per kall (std 5)")
    ap.add_argument("--berre", metavar="STAMME", help="berre denne kjeldefila (t.d. 06-bauhaus)")
    ap.add_argument("--grense", type=int, default=0, help="maks tal oppslag å lage (0 = alle)")
    ap.add_argument("--fraa", type=int, default=1, help="start ved oppslag nr N")
    ap.add_argument("--ord", type=int, default=STD_ORD, help=f"mål-ord per oppslag (std {STD_ORD})")
    ap.add_argument("--modell", default=STD_MODELL, help=f"biletmodell (std {STD_MODELL})")
    ap.add_argument("--storleik", default=STD_STORLEIK, help=f"px, t.d. 1024x1536 (std {STD_STORLEIK})")
    ap.add_argument("--kvalitet", default=STD_KVALITET, choices=sorted(GYLDIGE_KVALITETAR))
    ap.add_argument("--input-fidelity", dest="fidelity", default=None,
                    choices=["low", "high"], help="kor tett outputen held seg til referansane")
    ap.add_argument("--refs", default=str(REF_DIR), help="mappe med stilreferansar")
    ap.add_argument("--ut", default=str(UT_DIR), help="utmappe for sider")
    args = ap.parse_args()

    REF_DIR = Path(args.refs)
    UT_DIR = Path(args.ut)
    MANIFEST = UT_DIR / "manifest.json"

    # Standard: oppslag frå heile boka i lesErekkjefølgje. --utsnitt for kurert.
    if args.utsnitt:
        sti = Path(args.utsnitt)
        if not sti.exists():
            sys.exit(f"fann ikkje utsnitt-fila {sti}")
        oppslag = les_utsnitt(sti)
        print(f"modus:         kuraterte utsnitt ({sti.name})")
    else:
        filer = lesefiler()
        if args.berre:
            filer = [f for f in filer if f.stem == args.berre]
            if not filer:
                sys.exit(f"fann inga kjeldefil med stamme '{args.berre}'")
        oppslag = del_i_oppslag(filer, args.ord)
        print(f"modus:         oppslag frå boka (~{args.ord} ord/oppslag)")
    oppslag = [o for o in oppslag if o.nr >= args.fraa]
    if args.grense:
        oppslag = oppslag[: args.grense]

    refs = referansebilete()[: args.maks_refs]
    print(f"teikningar:    {len(oppslag)}")
    print(f"referansar:    {len(refs)} i {REF_DIR}")
    print(f"modell:        {args.modell}   storleik {args.storleik}   kvalitet {args.kvalitet}")
    print(f"utmappe:       {UT_DIR}\n")

    if args.proev:
        for o in oppslag:
            merke = "•" if not (UT_DIR / f"{o.stamme()}.png").exists() else "✓"
            print(f"  {merke} {o.nr:>2}. {o.stamme():<34} {o.ord:>4} ord   «{o.tittel[:46]}»")
        print(f"\n[--proev] {len(oppslag)} oppslag planlagt — ingen kall gjort.")
        if oppslag:
            o0 = oppslag[0]
            print("\n— promptdøme (fyrste oppslag), avkorta —")
            p = bygg_prompt(o0)
            print(p[:1200] + ("…" if len(p) > 1200 else ""))
        return

    if args.kode:
        # Skriv ut ferdige kall til å lime inn sjølv (matchar det fungerande eksempelet).
        for o in oppslag:
            print(f"\n# ===== {o.nr}. {o.tittel} ({o.ord} ord) =====")
            print("from openai import OpenAI")
            print("client = OpenAI()\n")
            print("response = client.images.edits(")
            print(f'  image=open("{args.ref_fil}", "rb"),')
            print(f'  prompt="""{bygg_prompt(o)}""",')
            print(f'  model="{args.modell}",')
            print("  n=1,")
            print(f'  size="{args.storleik}",')
            print(f'  quality="{args.kvalitet}",')
            print('  background="auto",')
            print('  moderation="auto",')
            print(")")
        return

    if not refs:
        sys.exit(f"FEIL: ingen referansebilete i {REF_DIR}. Legg JPEG/PNG-ane "
                 f"(t.d. IMG_4026.jpeg) der, og køyr på nytt. (Sjå README.)")

    UT_DIR.mkdir(parents=True, exist_ok=True)
    klient = lag_klient()
    manifest = les_manifest()

    laga = 0
    feila = 0
    for o in oppslag:
        ut = UT_DIR / f"{o.stamme()}.png"
        if ut.exists() and not args.paa_nytt:
            print(f"  ✓ hoppar over {ut.name} (finst)")
            continue
        prompt = bygg_prompt(o)
        kw = dict(model=args.modell, prompt=prompt, n=1, size=args.storleik,
                  quality=args.kvalitet, background="auto", _refs=refs)
        if args.fidelity:
            kw["input_fidelity"] = args.fidelity
        print(f"  → lagar {ut.name}  ({o.ord} ord, {len(refs)} refs) …", flush=True)
        t0 = time.time()
        try:
            svar = kall_med_backoff(klient, **kw)
            meta = lagra_svar(svar, ut)
        except Exception as e:                      # hald fram batchen om eitt oppslag feilar
            feila += 1
            print(f"    ✗ FEILA: {type(e).__name__}: {str(e)[:160]}", flush=True)
            continue
        dt = time.time() - t0
        manifest["sider"][o.stamme()] = {
            "nr": o.nr, "kjelde": o.kjelde, "tittel": o.tittel, "ord": o.ord,
            "modell": args.modell, "storleik": args.storleik, "kvalitet": args.kvalitet,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:12],
            "refs": [p.name for p in refs], "sekund": round(dt, 1), **meta,
        }
        skriv_manifest(manifest)
        laga += 1
        print(f"    ferdig på {dt:.1f}s")

    print(f"\nferdig: {laga} nye sider i {UT_DIR}" + (f"  ({feila} feila)" if feila else ""))


if __name__ == "__main__":
    main()
