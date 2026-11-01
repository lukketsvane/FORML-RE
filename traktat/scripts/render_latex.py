#!/usr/bin/env python3
"""Render the validated shared document AST into the A4 XeLaTeX edition.

python scripts/render_latex.py --document build/document.json \
    --output build/latex/formlaere.tex
Then, from build/latex/: xelatex -interaction=nonstopmode -halt-on-error
formlaere.tex (twice for destinations and page references).
The source AST owns content; layout/print.tex owns presentation.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CITATION = re.compile(r"\[\[kjelde:(\d+(?:,\d+)*)\]\]")
MARKUP = re.compile(r"(\[\[kjelde:\d+(?:,\d+)*\]\]|\*\*[^*]+\*\*|\*[^*]+\*)")
XREF = re.compile(r"\((\s*\d+(?:\.\d+)*(?:\s*[,;–—−-]\s*\d+(?:\.\d+)*)*\s*)\)")
SUPERSCRIPT = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+"))
SUBSCRIPT = dict(zip("₀₁₂₃₄₅₆₇₈₉₋₊₌₍₎ᵣ", "0123456789-+=()r"))
ESCAPE = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "^": r"\textasciicircum{}", "~": r"\textasciitilde{}"}


def tex_escape(text: str) -> str:
    return "".join(ESCAPE.get(char, char) for char in text)


def print_figure_path(filename: str) -> Path:
    """XeLaTeX consumes the derived PDF; the web keeps the canonical SVG."""
    asset = Path("illustrations") / filename
    return asset.with_suffix(".pdf") if asset.suffix.lower() == ".svg" else asset


def target(value: object) -> str:
    value = str(value)
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", value):
        raise ValueError(f"Unsafe destination ID: {value!r}")
    return value


def math_character(char: str) -> bool:
    number = ord(char)
    return (unicodedata.category(char) == "Sm" or 0x0370 <= number <= 0x03FF
            or 0x1D400 <= number <= 0x1D7FF or char in "∖′″𝕄𝒫𝟙")


def group(text: str, start: int) -> tuple[str, int]:
    """Read a balanced group, retaining nested delimiters for the inner parser."""
    if text[start] != "{":
        raise ValueError("Expected a script group")
    depth = 1
    for end in range(start + 1, len(text)):
        if text[end] == "{":
            depth += 1
        elif text[end] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:end], end + 1
    raise ValueError(f"Unclosed mathematical script in {text!r}")


def math_fragment(text: str) -> str:
    """Scripts contain notation, not prose; never normalize mathematical alphabets."""
    result = []
    index = 0
    while index < len(text):
        atom, end = math_atom(text, index, force=True)
        if end > index:
            result.append(atom)
            index = end
        else:
            char = text[index]
            result.append({"{": r"\{", "}": r"\}", "\\": r"\setminus ", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$", "~": r"\sim "}.get(char, char))
            index += 1
    return "".join(result)


def script(text: str, start: int) -> tuple[str, int]:
    if text[start] == "{":
        value, end = group(text, start)
    else:
        match = re.match(r"[A-Za-z0-9]+", text[start:])
        value = match[0] if match else text[start]
        end = start + len(value)
    if re.fullmatch(r"[A-Za-z]{2,}", value):
        return r"\mathrm{" + value + "}", end
    return math_fragment(value), end


def math_atom(text: str, start: int, force: bool = False) -> tuple[str, int]:
    char = text[start]
    if math_character(char):
        base, end = char, start + 1
    elif char.isascii() and char.isalnum():
        match = re.match(r"[A-Za-z0-9]+", text[start:])
        base, end = match[0], start + len(match[0])
        if not force and (end == len(text) or text[end] not in "_^̂" and text[end] not in SUPERSCRIPT and text[end] not in SUBSCRIPT):
            return "", start
        if len(base) > 1 and base.isalpha():
            base = r"\mathrm{" + base + "}"
    else:
        return "", start
    if end < len(text) and text[end] == "̂":
        base = r"\hat{" + base + "}"
        end += 1
    while end < len(text):
        char = text[end]
        if char in "_^" and end + 1 < len(text):
            value, end = script(text, end + 1)
            base += char + "{" + value + "}"
        elif char in SUPERSCRIPT or char in SUBSCRIPT:
            mapping, operator = (SUPERSCRIPT, "^") if char in SUPERSCRIPT else (SUBSCRIPT, "_")
            value = ""
            while end < len(text) and text[end] in mapping:
                value += mapping[text[end]]
                end += 1
            base += operator + "{" + value + "}"
        else:
            break
    return base, end


def literal(text: str) -> str:
    result = []
    index = 0
    while index < len(text):
        if text[index] == "\n":
            result.append(r"\newline{}")
            index += 1
            continue
        atom, end = math_atom(text, index)
        if end > index:
            result.append(r"\ensuremath{" + atom + "}")
            index = end
        else:
            char = text[index]
            # These occur as set difference in the shared plain-text notation.
            result.append(r"\ensuremath{\setminus}" if char == "\\" else tex_escape(char))
            index += 1
    return "".join(result)


class Renderer:
    def __init__(self, document: dict):
        if document.get("schemaVersion") != 1:
            raise ValueError("Unsupported document schema")
        self.document = document
        self.sources = {str(item["id"]): item for item in document["sources"]}
        self.notes = {str(item["id"]): item for item in document["notes"]}
        self.numbers = {str(item["n"]) for item in document["props"]}

    def source_links(self, ids: list[str]) -> str:
        result = []
        for value in ids:
            value = str(value)
            if value not in self.sources:
                raise ValueError(f"Unknown source: {value}")
            result.append(r"\hyperlink{referanse-" + target(value) + "}{" + tex_escape(value) + "}")
        return ", ".join(result)

    def note_links(self, ids: list[str]) -> str:
        links = []
        for value in ids:
            value = str(value)
            if value not in self.notes:
                raise ValueError(f"Unknown note: {value}")
            note = self.notes[value]
            links.append(r"\noteref{\hyperlink{notat-" + target(value) + "}{n" + tex_escape(str(note["number"])) + "}}")
        return "".join(links)

    def prose(self, text: str) -> str:
        def xrefs(value: str) -> str:
            from latex_source import MATH_TOKEN
            if MATH_TOKEN.search(value):
                parts, cursor = [], 0
                for match in MATH_TOKEN.finditer(value):
                    parts.append(xrefs(value[cursor:match.start()]))
                    expression = self.document.get("mathematics", {}).get(match[1])
                    if expression is None:
                        raise ValueError("Missing native mathematics: " + match[1])
                    parts.append((r"\[" if expression["display"] else r"\(") + expression["tex"] + (r"\]" if expression["display"] else r"\)"))
                    cursor = match.end()
                parts.append(xrefs(value[cursor:]))
                return "".join(parts)
            result, cursor = [], 0
            for match in XREF.finditer(value):
                result.append(literal(value[cursor:match.start()] + "("))
                inner, last = [], 0
                for number in re.finditer(r"\d+(?:\.\d+)*", match[1]):
                    inner.append(literal(match[1][last:number.start()]))
                    n = number[0]
                    inner.append(r"\hyperlink{" + target(n) + "}{" + n + "}" if n in self.numbers else literal(n))
                    last = number.end()
                inner.append(literal(match[1][last:] + ")"))
                result.append("".join(inner))
                cursor = match.end()
            result.append(literal(value[cursor:]))
            return "".join(result)

        result = []
        for part in MARKUP.split(text):
            citation = CITATION.fullmatch(part)
            if citation:
                result.append(r"\sourceref{" + self.source_links(citation[1].split(",")) + "}")
            elif part.startswith("**") and part.endswith("**"):
                result.append(r"\textbf{" + self.prose(part[2:-2]) + "}")
            elif part.startswith("*") and part.endswith("*"):
                result.append(r"\textit{" + self.prose(part[1:-1]) + "}")
            else:
                result.append(xrefs(part))
        return "".join(result)

    def content(self) -> str:
        output = []
        tokens = self.document["tokens"]
        start = next((i for i, t in enumerate(tokens) if t["kind"] == "heading" and t.get("text") == "Føreord"), 0)
        figures: dict[str, list[dict]] = {}
        for figure in self.document["figures"]:
            figures.setdefault(str(figure["after"]), []).append(figure)
        for token in tokens[start:]:
            kind = token["kind"]
            if kind == "title":
                continue
            if kind == "heading":
                slug = re.sub(r"[^a-z0-9æøå]+", "-", token["text"].lower()).strip("-")
                # Hyperref destinations may be Unicode; proposition/note IDs remain strict.
                style = "[1]" if token["text"] in {"Føreord", "Lesekode"} else ""
                output.append(r"\sectionlabel" + style + "{del-" + slug + "}{" + tex_escape(token["text"]) + "}")
            elif kind == "paragraph":
                output.append(self.prose(token["text"]) + self.note_links(token.get("notes", [])) + r"\par\vspace{8pt}")
            elif kind == "prop":
                n = str(token["n"])
                depth = len(n.partition(".")[2]) if "." in n else 0
                spacing = [13.2, 9.36, 5.76, 4.08, 2.88][min(depth, 4)]
                output.append(r"\begin{proposition}{" + target(n) + "}{" + tex_escape(token["status"]) + "}{" + str(spacing) + "}")
                paragraphs = token["paragraphs"]
                for i, paragraph in enumerate(paragraphs):
                    if i:
                        output.append(r"\bodyparagraph")
                    output.append((r"\hypertarget{" + target(n) + "}{}" if i == 0 else "") + self.prose(paragraph))
                output.append(self.note_links(token.get("notes", [])))
                output.append(r"\end{proposition}")
                for figure in figures.get(n, []):
                    asset = ROOT / "nettstad" / "illustrations" / figure["file"]
                    if not asset.is_file():
                        raise FileNotFoundError(f"Missing illustration: {asset}")
                    portable_asset = print_figure_path(figure["file"])
                    output.append(r"\bookfigure{" + portable_asset.as_posix() + "}{" + tex_escape(figure["alt"]) + "}")

        glossary = self.document.get("glossary", [])
        if glossary:
            output.append(r"\clearpage\sectionlabel{ordliste}{Ordliste}")
            for entry in glossary:
                output.append(r"\begin{referenceentry}[2]{ord-" + target(entry["id"]) + "}{}")
                heading = r"\textbf{" + self.prose(entry["term"]) + "}"
                if entry.get("symbol"):
                    heading += r"\quad " + self.prose(entry["symbol"])
                output.append(heading + r"\par\nobreak\vspace{2pt}\nobreak")
                if entry.get("fields"):
                    output.append(r"\entrymeta{" + tex_escape(" · ".join(entry["fields"])) + "}")
                output.append(self.prose(entry["definition"]))
                if entry.get("connection"):
                    output.append(r"\par\nobreak\vspace{3pt}\nobreak\textit{I teksten:} " + self.prose(entry["connection"]))
                links = []
                for proposition in entry.get("propositions", []):
                    proposition = str(proposition)
                    if proposition not in self.numbers:
                        raise ValueError(f"Unknown glossary proposition: {proposition}")
                    links.append(r"\hyperlink{" + target(proposition) + "}{" + proposition + "}")
                metadata = [", ".join(links)] if links else []
                if entry.get("sources"):
                    metadata.append("Kjelder: " + self.source_links(entry["sources"]))
                if metadata:
                    output.append(r"\entrylinks{" + " · ".join(metadata) + "}")
                output.append(r"\end{referenceentry}")

        for title, items in [("Notat", self.document["notes"]), ("Referansar", self.document["sources"])]:
            output.append(r"\clearpage\sectionlabel{" + ("notat" if title == "Notat" else "referansar") + "}{" + title + "}")
            for item in items:
                if title == "Notat":
                    destination, label = "notat-" + target(item["id"]), "n" + str(item["number"])
                    output.append(r"\begin{referenceentry}{" + destination + "}{" + tex_escape(label) + "}")
                    proposition = item.get("proposition")
                    back = r"\hyperlink{" + (target(proposition) if proposition else "del-føreord") + "}{" + (str(proposition) if proposition else "Føreord") + "}"
                    metadata = back + (" · " + tex_escape(item["relation"]) if item.get("relation") else "")
                    output.append(r"\entrymeta{" + metadata + "}")
                    output.append(self.prose(item["note"]))
                    if item.get("sources"):
                        output.append(r"\entrylinks{[" + self.source_links(item["sources"]) + "]}")
                else:
                    output.append(r"\begin{referenceentry}{referanse-" + target(item["id"]) + "}{" + tex_escape(str(item["id"])) + "}")
                    for alias, canonical in self.document.get("sourceAliases", {}).items():
                        if str(canonical) == str(item["id"]):
                            output.append(r"\hypertarget{referanse-" + target(alias) + "}{}")
                    output.append(literal(item["citation"]))
                    url = item.get("url") or ("https://doi.org/" + item["doi"] if item.get("doi") else None)
                    if url and re.match(r"^https?://", url):
                        safe_url = quote(url, safe=":/?&=%#@+;,$-_.!~*'()")
                        safe_url = safe_url.replace("%", r"\%").replace("#", r"\#").replace("&", r"\&")
                        label = "DOI: " + item["doi"] if item.get("doi") else "Opne kjelda"
                        output.append(r"\entrylinks{\href{" + safe_url + "}{" + tex_escape(label) + "}}")
                output.append(r"\end{referenceentry}")
        return "\n".join(output)

    def render(self) -> str:
        template = (ROOT / "layout" / "print.tex").read_text(encoding="utf-8")
        values = {"TITLE": tex_escape(self.document["title"]), "AUTHOR": tex_escape(self.document["author"]), "SOURCE_HASH": target(self.document["sourceHash"]), "CONTENT": self.content()}
        for key, value in values.items():
            template = template.replace("%%" + key + "%%", value)
        return "% Generated from the shared document AST. Do not edit.\n" + template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document", type=Path, default=ROOT / "build" / "document.json")
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "latex" / "formlaere.tex")
    args = parser.parse_args()
    document = json.loads(args.document.read_text(encoding="utf-8"))
    tex = Renderer(document).render()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tex, encoding="utf-8")
    print(json.dumps({"output": str(args.output), "propositions": len(document["props"]), "glossary": len(document.get("glossary", [])), "notes": len(document["notes"]), "sources": len(document["sources"]), "figures": len(document["figures"]), "sourceHash": document["sourceHash"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
