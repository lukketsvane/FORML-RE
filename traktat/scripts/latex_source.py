"""A deliberately small, validated LaTeX authoring language for both editions.

The manuscript is a real TeX fragment: headings, proposition environments,
formatting, explicit citation commands, and native mathematics. Unknown prose
commands fail rather than silently disappearing from one output.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import xml.etree.ElementTree as ET

MATH_TOKEN = re.compile(r"⟦math:([a-f0-9]{24})⟧")
BEGIN = re.compile(r"\\begin\{formproposition\}\{([1-9]\d*(?:\.\d+)*)\}\{([datio])\}")
ESCAPES = {"%": "%", "&": "&", "#": "#", "_": "_", "$": "$", "{": "{", "}": "}"}


def group(text: str, start: int) -> tuple[str, int]:
    if start >= len(text) or text[start] != "{":
        raise ValueError("Expected a LaTeX argument")
    depth, index = 1, start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    raise ValueError("Unclosed LaTeX argument")


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*(?:\n|$)", "", text).replace("\r\n", "\n").replace("\r", "\n")


def inline(text: str, math: dict) -> str:
    result, index = [], 0
    while index < len(text):
        if text.startswith((r"\(", r"\["), index):
            display = text[index + 1] == "["
            closing = r"\]" if display else r"\)"
            end = text.find(closing, index + 2)
            if end < 0:
                raise ValueError("Unclosed LaTeX mathematics")
            value = text[index + 2:end].strip()
            if not value:
                raise ValueError("Empty LaTeX mathematics")
            # TeX cannot execute arbitrary I/O or macros from the manuscript.
            allowed = {"frac", "dfrac", "tfrac", "sqrt", "text", "mathrm", "mathit", "mathbf", "mathbb", "mathcal", "mathsf", "operatorname", "hat", "widehat", "bar", "overline", "underline", "vec", "tilde", "widetilde", "left", "right", "big", "Big", "bigl", "bigr", "Bigl", "Bigr", "lvert", "rvert", "lVert", "rVert", "vert", "Vert", "langle", "rangle", "lbrace", "rbrace", "sum", "prod", "int", "iint", "oint", "lim", "min", "max", "inf", "sup", "log", "ln", "exp", "sin", "cos", "tan", "det", "dim", "arg", "Pr", "partial", "nabla", "infty", "in", "notin", "ni", "subset", "subseteq", "supset", "supseteq", "cup", "cap", "bigcup", "bigcap", "setminus", "emptyset", "varnothing", "forall", "exists", "neg", "land", "lor", "wedge", "vee", "implies", "iff", "Rightarrow", "Leftrightarrow", "rightarrow", "leftarrow", "to", "mapsto", "longrightarrow", "leftrightarrow", "le", "leq", "ge", "geq", "ne", "neq", "equiv", "sim", "simeq", "approx", "propto", "times", "cdot", "pm", "mp", "circ", "otimes", "oplus", "ldots", "cdots", "vdots", "ddots", "quad", "qquad", "limits", "nolimits", "underbrace", "overbrace", "overset", "underset", "substack", "begin", "end", "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "varpi", "rho", "varrho", "sigma", "varsigma", "tau", "upsilon", "phi", "varphi", "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega"}
            for command in re.findall(r"\\([A-Za-z]+)", value):
                if command not in allowed:
                    raise ValueError("Unsupported LaTeX math command: \\" + command)
            for environment in re.findall(r"\\(?:begin|end)\{([^}]+)\}", value):
                if environment not in {"aligned", "gathered", "cases", "matrix", "pmatrix", "bmatrix"}:
                    raise ValueError("Unsupported math environment: " + environment)
            key = hashlib.sha256((str(display) + value).encode()).hexdigest()[:24]
            math[key] = {"tex": value, "display": display}
            result.append("⟦math:" + key + "⟧")
            index = end + 2
            continue
        char = text[index]
        if char != "\\":
            if char in "{}$&#_^":
                raise ValueError("Unescaped TeX character outside mathematics: " + char)
            result.append(" " if char == "\n" else char)
            index += 1
            continue
        if index + 1 < len(text) and text[index + 1] in ESCAPES:
            result.append(ESCAPES[text[index + 1]])
            index += 2
            continue
        match = re.match(r"\\([A-Za-z]+)", text[index:])
        if not match:
            raise ValueError("Unsupported LaTeX escape near " + text[index:index + 30])
        command = match[1]
        index += len(match[0])
        value, index = group(text, index)
        if command in {"emph", "textit", "textbf"}:
            marker = "**" if command == "textbf" else "*"
            result.append(marker + inline(value, math) + marker)
        elif command == "kjelder":
            if not re.fullmatch(r"\d+(?:,\d+)*", value):
                raise ValueError("Malformed source marker in \\kjelder")
            result.append("[[kjelde:" + value + "]]")
        elif command == "notat":
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", value):
                raise ValueError("Malformed note marker in \\notat")
            result.append("[[notat:" + value + "]]")
        elif command == "textbackslash" and not value:
            result.append("\\")
        elif command == "textasciitilde" and not value:
            result.append("~")
        elif command == "textasciicircum" and not value:
            result.append("^")
        elif command == "newline" and not value:
            result.append("\n")
        else:
            raise ValueError("Unsupported LaTeX prose command: \\" + command)
    return "".join(result)


def parse_latex(source: str) -> tuple[list[dict], list[dict], dict]:
    source = strip_comments(source).strip()
    tokens, props, math = [], [], {}
    cursor = 0
    structural = re.compile(r"\\(?:title\{|section\{|begin\{formproposition\}|end\{formproposition\})")
    while cursor < len(source):
        if source[cursor].isspace():
            cursor += 1
            continue
        if source.startswith((r"\title{", r"\section{"), cursor):
            title = source.startswith(r"\title{", cursor)
            content, cursor = group(source, cursor + (6 if title else 8))
            tokens.append({"kind": "title" if title else "heading", "text": inline(content, math)})
        elif source.startswith(r"\begin{formproposition}", cursor):
            match = BEGIN.match(source, cursor)
            if not match:
                raise ValueError("Malformed proposition environment")
            end = source.find(r"\end{formproposition}", match.end())
            if end < 0:
                raise ValueError("Unclosed proposition " + match[1])
            body = source[match.end():end].strip()
            if structural.search(body):
                raise ValueError("Nested manuscript structure in proposition " + match[1])
            paragraphs = [inline(p.strip(), math) for p in re.split(r"\n\s*\n", body) if p.strip()]
            prop = {"kind": "prop", "n": match[1], "status": match[2], "paragraphs": paragraphs, "notes": []}
            tokens.append(prop)
            props.append(prop)
            cursor = end + len(r"\end{formproposition}")
        else:
            next_structure = structural.search(source, cursor)
            end = next_structure.start() if next_structure else len(source)
            if end == cursor:
                raise ValueError("Unexpected manuscript structure")
            for paragraph in re.split(r"\n\s*\n", source[cursor:end].strip()):
                if paragraph.strip():
                    tokens.append({"kind": "paragraph", "text": inline(paragraph.strip(), math)})
            cursor = end
    return tokens, props, math


def render_mathml(math: dict) -> None:
    """One Pandoc process for all expressions; output is validated before HTML use."""
    if not math:
        return
    keys = sorted(math)
    content = "\n\n".join((r"\[" if math[key]["display"] else r"\(") + math[key]["tex"] + (r"\]" if math[key]["display"] else r"\)") for key in keys)
    result = subprocess.run(["pandoc", "--from=latex", "--to=html5", "--mathml"], input=content, capture_output=True, text=True, check=True)
    if result.stderr.strip():
        raise ValueError("LaTeX mathematics cannot be rendered consistently: " + result.stderr.strip())
    expressions = re.findall(r"<math\b[\s\S]*?</math>", result.stdout)
    if len(expressions) != len(keys):
        raise ValueError("MathML expression count differs from the LaTeX source")
    for key, markup in zip(keys, expressions):
        math[key]["mathml"] = validate_mathml(markup)


def validate_mathml(markup: str) -> str:
    # Pandoc encodes aligned equations with harmless CSS on table cells.
    # Normalize it to the corresponding native MathML attribute.
    markup = re.sub(r'(<mtd\b[^>]*?) style="text-align:\s*(left|right|center);?"',
                    lambda match: match[1] if 'columnalign=' in match[1] else match[1] + ' columnalign="' + match[2] + '"', markup)
    root = ET.fromstring(markup)
    if root.tag != "{http://www.w3.org/1998/Math/MathML}math":
        raise ValueError("Expected MathML root")
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == "merror":
            raise ValueError("MathML contains an error")
        if not element.tag.startswith("{http://www.w3.org/1998/Math/MathML}"):
            raise ValueError("Unexpected non-MathML output")
        for attribute in element.attrib:
            if attribute.lower().startswith("on") or attribute in {"href", "src", "style"}:
                raise ValueError("Unsafe MathML attribute")
    return markup



def legacy_inline_to_latex(text: str) -> str:
    """One-way migration helper; never consulted by the active build."""
    from render_latex import literal
    pattern = re.compile(r"(\[\[kjelde:\d+(?:,\d+)*\]\]|\[\[notat:[A-Za-z][A-Za-z0-9_.-]*\]\]|\*\*[^*]+\*\*|\*[^*]+\*)")
    result = []
    for part in pattern.split(text):
        if part.startswith("[[kjelde:"):
            result.append(r"\kjelder{" + part[9:-2] + "}")
        elif part.startswith("[[notat:"):
            result.append(r"\notat{" + part[8:-2] + "}")
        elif part.startswith("**") and part.endswith("**"):
            result.append(r"\textbf{" + legacy_inline_to_latex(part[2:-2]) + "}")
        elif part.startswith("*") and part.endswith("*"):
            result.append(r"\emph{" + legacy_inline_to_latex(part[1:-1]) + "}")
        else:
            converted = literal(part)
            cursor = 0
            while True:
                index = converted.find(r"\ensuremath{", cursor)
                if index < 0:
                    result.append(converted[cursor:])
                    break
                result.append(converted[cursor:index])
                value, cursor = group(converted, index + len(r"\ensuremath"))
                result.append(r"\(" + value + r"\)")
    return "".join(result)


def migrate_to_latex(source: str) -> str:
    from content import parse_source
    tokens, _ = parse_source(source)
    output = ["% Canonical manuscript for the website and PDF. Edit this file.", "% TeX fragment: compile through the edition builder (make all)."]
    for token in tokens:
        if token["kind"] in {"title", "heading"}:
            output.append((r"\title{" if token["kind"] == "title" else r"\section{") + legacy_inline_to_latex(token["text"]) + "}")
        elif token["kind"] == "paragraph":
            output.append(legacy_inline_to_latex(token["text"]))
        else:
            body = "\n\n".join(legacy_inline_to_latex(p) for p in token["paragraphs"])
            output.append(r"\begin{formproposition}{" + token["n"] + "}{" + token["status"] + "}\n" + body + "\n" + r"\end{formproposition}")
    return "\n\n".join(output) + "\n"
