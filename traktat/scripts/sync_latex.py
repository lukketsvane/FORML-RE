#!/usr/bin/env python3
"""Generate the current LaTeX edition from the same text used by the reader.

No bibliographic numbers are inferred from prose: [[kjelde:...]] is the only
citation syntax. Mathematical exponents remain mathematical exponents.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PROP = re.compile(r"^\*\*(\d+(?:\.\d+)*)([datio])\*\*\s+(.*)$")
CITE = re.compile(r"\[\[kjelde:([\d, ]+)\]\]")


def literal(text: str) -> str:
    """Escape prose while preserving visible mathematical signs."""
    result = []
    index = 0
    while index < len(text):
        ch = text[index]
        if ch == "Λ" and index + 1 < len(text) and text[index + 1] == "̂":
            result.append(r"\ensuremath{\hat{\Lambda}}")
            index += 2
            continue
        if ch == "_":
            match = re.match(r"_\{([^}]+)\}|_([A-Za-z0-9]+)", text[index:])
            if match:
                result.append(r"\textsubscript{" + literal(match[1] or match[2]) + "}")
                index += len(match[0])
                continue
        if ch in "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺":
            match = re.match(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+", text[index:])[0]
            normal = match.translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+"))
            result.append(r"\textsuperscript{" + normal + "}")
            index += len(match)
            continue
        if ch in "αβΓΔδεθκΛλμπρτΦωΠΣνσ∅∇∥≡⊙∈∉⊆∪∖≤≥≈∼∞∑→↔−′″𝕄𝒫𝟙ᵣ₀₁":
            # Latin Modern Math has these signs, including double-struck letters.
            result.append(r"\ensuremath{" + ch + "}")
        elif ch == "\\":
            result.append(r"\ensuremath{\setminus}")
        else:
            result.append({"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                           "_": r"\_", "{": r"\{", "}": r"\}",
                           "^": r"\textasciicircum{}", "~": r"\textasciitilde{}"}.get(ch, ch))
        index += 1
    return "".join(result)


def rich(text: str) -> str:
    parts = re.split(r"(\[\[kjelde:[\d, ]+\]\]|\[\[notat:[^\]]+\]\]|\*\*[^*]+\*\*|\*[^*]+\*)", text)
    result = []
    for part in parts:
        match = CITE.fullmatch(part)
        if match:
            result.append(r"\kjelde{" + re.sub(r"\s", "", match[1]) + "}")
        elif part.startswith("[[notat:"):
            target, anchor = part[8:-2].split("|", 1)
            result.append(r"\hyperlink{kjeldenotat-" + target + "}{" + rich(anchor) + "}")
        elif part.startswith("**") and part.endswith("**"):
            result.append(r"\textbf{" + rich(part[2:-2]) + "}")
        elif part.startswith("*") and part.endswith("*"):
            result.append(r"\textit{" + rich(part[1:-1]) + "}")
        else:
            result.append(literal(part))
    return "".join(result)


def formula(text: str) -> str:
    text = text.replace("\\", r"\setminus ").replace("Λ̂", r"\hat{Λ}")
    text = re.sub(r"_([A-Za-z0-9]+)", r"_{\1}", text)
    text = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+", lambda m: "^{" + m[0].translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")) + "}", text)
    text = text.replace("exp(", r"\exp(").replace("min{", r"\min\{")
    text = text.replace("{A_{i}}", r"\{A_{i}\}")
    text = text.replace("log₁₀", r"\log_{10}")
    return text


def paragraph(text: str) -> str:
    if text.startswith("Form = SG(") and " · " in text:
        equation, caption = text.split(" · ", 1)
        return r"\formel{" + formula(equation).replace("Form", r"\mathrm{Form}") + "}" + r"{\small " + rich(caption) + "}"
    if text.startswith("P(x |") and " · " in text:
        equation, caption = text.split(" · ", 1)
        left, right = equation.split(" = ", 1)
        return (r"\formel{\begin{aligned}" + formula(left) + r"={}&\\ &"
                + formula(right) + r"\end{aligned}}" + r"{\small " + rich(caption) + "}")
    if text.startswith(("P(x_k |", "μ_SG(x) q(", "ν(A; G) =")):
        return r"\formel{" + formula(text.rstrip(",.")) + "}"
    if text.startswith("min{1, e^{"):
        equation, explanation = text.split(", der ", 1)
        equation = formula(equation).replace("}}", r"}\}")
        return r"\formel{" + equation + "}" + "der " + r"\(" + formula(explanation) + r"\)"
    # Keep line-based operator tables legible without introducing layout tables
    # into the shared prose source.
    return "\\\\\n".join(rich(line) for line in text.splitlines())


def parse(text: str):
    introduction = []
    propositions = []
    active = None
    section = ""
    buffer = []

    def flush():
        nonlocal buffer
        value = "\n".join(buffer).strip()
        buffer = []
        if not value:
            return
        if active is not None:
            active["paragraphs"].append(value)
        elif section == "Føreord":
            introduction.append(value)

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            section = line[3:].strip()
            continue
        match = PROP.match(line)
        if match:
            flush()
            active = {"number": match[1], "status": match[2], "paragraphs": []}
            propositions.append(active)
            buffer.append(match[3])
        elif not line.strip():
            flush()
        elif not line.startswith("# "):
            buffer.append(line)
    flush()
    if len(propositions) != 375 or propositions[-1]["number"] != "7.4":
        raise ValueError("Expected the complete current edition (375 propositions, ending at 7.4)")
    return introduction, propositions


def generate(text_path: Path, catalog_path: Path) -> None:
    text = text_path.read_text()
    catalog = json.loads(catalog_path.read_text())
    sources = {str(source["id"]): source for source in catalog["sources"]}
    used = {number.strip() for group in CITE.findall(text) for number in group.split(",")}
    if used - sources.keys():
        raise ValueError(f"Unknown source references: {used - sources.keys()}")
    introduction, propositions = parse(text)

    def annotate(paragraphs, annotations):
        paragraphs = list(paragraphs)
        for target, annotation in annotations:
            anchor = annotation.get("anchor", "")
            if not anchor:
                continue
            for index, value in enumerate(paragraphs):
                match = re.search(re.escape(anchor), value, re.IGNORECASE)
                if match:
                    paragraphs[index] = value[:match.start()] + "[[notat:" + target + "|" + match[0] + "]]" + value[match.end():]
                    break
            else:
                raise ValueError(f"Source-note anchor not found: {target}: {anchor}")
        return paragraphs

    introduction = annotate(introduction, [(f"intro-{index}", item) for index, item in enumerate(catalog.get("intro", []), 1)])
    intro = [r"% Generated by traktat/scripts/sync_latex.py. Edit traktat/tekst/formlaere.txt.",
             r"\silentchapter{Føreord}{føreord}", r"\begin{widebody}", r"\begin{foreordbody}"]
    intro += [paragraph(value) + "\n" for value in introduction]
    intro += [r"\end{foreordbody}", r"\end{widebody}", ""]
    (SRC / "forord.tex").write_text("\n".join(intro))
    output = [r"% Generated by traktat/scripts/sync_latex.py. Edit traktat/tekst/formlaere.txt.",
              r"\silentchapter{Proposisjonar}{proposisjonar}",
              r"\begin{widebody}\footnotesize",
              r"d = definisjon · a = postulat/hypotese · t = modellvilkårsvis følgje · o = observasjon · i = illustrasjon. Desimalnummera viser logiske underordningar, ikkje berre kapittelrekkjefølgje.",
              r"\end{widebody}", r"\vspace{6mm}", ""]
    for prop in propositions:
        command = "mainprop" if "." not in prop["number"] else "prop"
        annotations = [(prop["number"], item) for item in catalog.get("annotations", []) if str(item["proposition"]) == prop["number"]]
        values = annotate(prop["paragraphs"], annotations)
        body = "\n\n".join(paragraph(value) for value in values)
        output += [rf"\{command}{{{prop['number']}}}{{{prop['status']}}}{{{body}}}", ""]
        figures = {
            "1.4": ("scan-20261031-p11-busette-opne-forbodne.png", "Busette, opne og forbodne regionar"),
            "1.54": ("scan-20261031-p13-c-k-operator-tabell-og-rorsle.png", "C–K-operasjonane"),
            "2.212": ("scan-20261031-p16-royrstol-utvikling.png", "Frå sykkelramme til røyrstol"),
            "5.125": ("scan-20261031-p21-agentrang.png", "Agens frå termostat til designar"),
            "6.66": ("scan-20261031-p35-d-modell-diagram.png", "Formrom, grammatikk, landskap og agentar"),
            "7.142": ("scan-20261031-p41-sommarfugl-livslop.png", "Larve, puppe og sommarfugl"),
        }
        if prop["number"] in figures:
            filename, caption = figures[prop["number"]]
            if (ROOT / "nettstad" / "illustrations" / filename).exists():
                output += [r"\begin{figure}[htbp]\centering", r"\includegraphics[width=\linewidth]{" + filename + "}",
                           r"\caption{" + literal(caption) + "}", r"\end{figure}", ""]
    (SRC / "proposisjonar.tex").write_text("\n".join(output))
    bibliography = [r"% Generated from traktat/kjelder.json.",
                    r"\silentchapter{Referansar}{referansar}", r"\begin{widebody}"]
    for source in catalog["sources"]:
        number = str(source["id"])
        citation = literal(source["citation"])
        if source.get("url"):
            url = source["url"].replace("%", r"\%").replace("#", r"\#")
            citation = r"\href{" + url + "}{" + citation + "}"
        bibliography.append(r"\refentry{\hypertarget{kjelde-" + number + "}{}[" + number + "] " + citation + "}")
    bibliography += [r"\end{widebody}", ""]
    (SRC / "referansar.tex").write_text("\n".join(bibliography))
    notes = [r"% Generated from traktat/kjelder.json.",
             r"\silentchapter{Kjeldenotar}{kjeldenotar}", r"\begin{widebody}\small",
             "Kjeldetala viser til verk som teksten byggjer på eller vidarefører. Ein kjeldereferanse er ikkje i seg sjølv eit prov for proposisjonen. Tekstlege parallellar er merkte som slike.\n"]
    for index, annotation in enumerate(catalog.get("intro", []), 1):
        labels = ",".join(str(value) for value in annotation.get("sources", []))
        notes.append(r"\noindent\hypertarget{kjeldenotat-intro-" + str(index) + r"}{}\textbf{Føreord: " + literal(annotation["anchor"]) + "} " + literal(annotation["note"]) + r"\kjelde{" + labels + r"}\par\medskip")
    for annotation in catalog.get("annotations", []):
        number = str(annotation["proposition"])
        labels = ",".join(str(value) for value in annotation.get("sources", []))
        note = annotation.get("note", "")
        relation = annotation.get("relation", "Kjeldegrunnlag")
        notes.append(r"\noindent\hypertarget{kjeldenotat-" + number + r"}{}\textbf{" + literal(number) + "} " + literal(relation) + ": " + literal(note) + (r"\kjelde{" + labels + "}" if labels else "") + r"\par\medskip")
    notes += [r"\end{widebody}", ""]
    (SRC / "kjeldenotar.tex").write_text("\n".join(notes))
    print(f"Generated LaTeX: {len(propositions)} propositions, {len(sources)} references, {len(used)} cited sources.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, default=ROOT / "tekst" / "formlaere.txt")
    parser.add_argument("--catalog", type=Path, default=ROOT / "kjelder.json")
    args = parser.parse_args()
    generate(args.text, args.catalog)
