#!/usr/bin/env python3
"""Shared source parser and validation for web, LaTeX and PDF.

The five canonical files are editable content. Neither renderer may infer
citations from ordinary numbers or maintain a separate glossary.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

PROP = re.compile(r"^\*\*(\d+(?:\.\d+)*)([datio])\*\*\s+(.*)$")
CITE = re.compile(r"\[\[kjelde:(\d+(?:,\d+)*)\]\]")
NOTE = re.compile(r"\[\[notat:([A-Za-z][A-Za-z0-9_.-]*)\]\]")
NUMBER = re.compile(r"[1-9]\d*(?:\.\d+)*")
NOTE_ID = re.compile(r"[A-Za-z][A-Za-z0-9_.-]*")
GLOSSARY_ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
CANONICAL = ("tekst/formlaere.tex", "kjelder.json", "figurar.json", "edition.json", "ordliste.json")


def parse_source(source: str) -> tuple[list[dict], list[dict]]:
    tokens, props, buffer = [], [], []
    active = None

    def flush() -> None:
        value = "\n".join(buffer).strip()
        buffer.clear()
        if not value:
            return
        if active is not None:
            active["paragraphs"].append(value)
        else:
            tokens.append({"kind": "paragraph", "text": value})

    for line in source.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if line.startswith("## ") or line.startswith("# "):
            flush()
            active = None
            tokens.append({"kind": "heading" if line.startswith("## ") else "title", "text": line[3 if line.startswith("## ") else 2:].strip()})
            continue
        match = PROP.match(line)
        if match:
            flush()
            active = {"kind": "prop", "n": match[1], "status": match[2], "paragraphs": [], "notes": []}
            tokens.append(active)
            props.append(active)
            if match[3]:
                buffer.append(match[3])
        elif not line.strip():
            flush()
        else:
            if line.startswith("**") and re.match(r"^\*\*\d", line):
                raise ValueError("Malformed proposition heading: " + line[:60])
            buffer.append(line)
    flush()
    return tokens, props


def marker_ids(text: str) -> tuple[list[str], list[str]]:
    citation_ids = [value for group in CITE.findall(text) for value in group.split(",")]
    note_ids = NOTE.findall(text)
    residue = NOTE.sub("", CITE.sub("", text))
    if "[[" in residue or "]]" in residue:
        raise ValueError("Unknown or malformed source marker")
    for group in CITE.findall(text):
        values = group.split(",")
        if len(values) != len(set(values)):
            raise ValueError("Duplicate source ID in citation group")
    return citation_ids, note_ids


def _number_key(number: str) -> tuple[int, str]:
    first, *rest = number.split(".")
    # The digits after the decimal form a logical address, not an integer:
    # 1.0111 precedes 1.012. Keep chapter numbers numerically ordered.
    return int(first), ".".join(rest)


def input_manifest(root: Path) -> dict[str, str]:
    root = root.resolve()
    paths = {root / name for name in (*CANONICAL, "vercel.json", "requirements-build.txt")}
    for folder in ("scripts", "layout", "nettstad"):
        directory = root / folder
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if any(part in {"__pycache__", "dist", "build", "tmp", ".git", "node_modules"} for part in relative.parts):
                continue
            if path.suffix in {".pyc", ".pyo", ".log", ".aux", ".pdf", ".tex~"} or path.name.startswith("."):
                continue
            paths.add(path)
    figure_path = root / "figurar.json"
    if figure_path.exists():
        figures = json.loads(figure_path.read_text(encoding="utf-8"))
        for figure in figures.get("assets", []):
            paths.add(root / "nettstad" / "illustrations" / figure["file"])
    result = {}
    for path in sorted(paths, key=lambda value: value.relative_to(root).as_posix()):
        if not path.is_file():
            raise ValueError(f"Build input is missing: {path.relative_to(root)}")
        result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def manifest_hash(manifest: dict[str, str]) -> str:
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_hash(root: Path) -> str:
    return manifest_hash(input_manifest(root))


def load_document(root: Path) -> dict:
    root = root.resolve()
    # A model may only carry the fingerprint of the files it actually read.
    # Reject edits during parsing instead of labelling an old AST as current.
    initial_hash = source_hash(root)
    source = (root / "tekst" / "formlaere.tex").read_text(encoding="utf-8")
    catalog = json.loads((root / "kjelder.json").read_text(encoding="utf-8"))
    figures = json.loads((root / "figurar.json").read_text(encoding="utf-8"))
    edition = json.loads((root / "edition.json").read_text(encoding="utf-8"))
    glossary = json.loads((root / "ordliste.json").read_text(encoding="utf-8"))
    if not isinstance(glossary, dict) or glossary.get("schemaVersion") != 1 or not isinstance(glossary.get("entries"), list):
        raise ValueError("Unsupported glossary schema")
    from latex_source import parse_latex
    tokens, props, mathematics = parse_latex(source)
    prop_order = {prop["n"]: index for index, prop in enumerate(props)}
    raw_notes = deepcopy(catalog.get("notes", []))
    ordered_notes = sorted(enumerate(raw_notes), key=lambda pair: (-1 if pair[1].get("section") == "foreword" else prop_order.get(pair[1].get("proposition"), len(props)), pair[0]))
    notes = []
    for _, item in ordered_notes:
        item.setdefault("proposition", None)
        item.setdefault("section", None)
        item["number"] = len(notes) + 1
        notes.append(item)
    note_by_id = {note["id"]: note for note in notes}
    explicit_note_occurrences = []
    for token in tokens:
        texts = token.get("paragraphs", []) if token["kind"] == "prop" else [token.get("text", "")]
        clean = []
        placements = []
        for text in texts:
            marker_ids(text)  # Validate before stripping placement metadata.
            placements.extend(NOTE.findall(text))
            clean.append(NOTE.sub("", text))
        if token["kind"] == "prop":
            token["paragraphs"] = clean
            implicit = [note["id"] for note in notes if note.get("proposition") == token["n"]]
            token["notes"] = list(dict.fromkeys(placements + implicit))
        else:
            token["text"] = clean[0]
            if placements:
                token["notes"] = placements
        explicit_note_occurrences.extend(placements)
    sources = deepcopy(catalog["sources"])
    for number, item in enumerate(sources, 1):
        # IDs and destinations survive editorial deletions; visible numbers
        # follow the active bibliography without leaving gaps.
        item["number"] = number
    document = {"schemaVersion": 1, "sourceHash": initial_hash, "title": edition["title"], "author": edition["author"],
                "tokens": tokens, "props": props, "sources": sources, "notes": notes,
                "figures": deepcopy(figures["assets"]), "glossary": deepcopy(glossary["entries"]),
                "sourceAliases": deepcopy(catalog.get("aliases", {})), "mathematics": mathematics}
    # Placement markers are only used for section notes. Proposition notes
    # already have a stable target and must not acquire duplicate placements.
    for note_id in explicit_note_occurrences:
        if note_id not in note_by_id:
            raise ValueError("Unknown note marker: " + note_id)
        if note_by_id[note_id].get("proposition"):
            raise ValueError("Use the catalog proposition target for note " + note_id)
    validate_document(document, root)
    if source_hash(root) != initial_hash:
        raise ValueError("Source changed while loading the document; run the build again.")
    return document


def validate_document(document: dict, root: Path) -> None:
    if document.get("schemaVersion") != 1:
        raise ValueError("Unsupported document schema")
    props = document.get("props", [])
    if not props:
        raise ValueError("The document contains no propositions")
    numbers = [prop.get("n", "") for prop in props]
    if any(not NUMBER.fullmatch(number) for number in numbers):
        raise ValueError("Invalid proposition identifier")
    if len(set(numbers)) != len(numbers):
        raise ValueError("Duplicate proposition identifiers")
    if numbers != sorted(numbers, key=_number_key):
        raise ValueError("Propositions are not in logical address order")
    if any(prop.get("status") not in {"d", "a", "t", "i", "o"} or not prop.get("paragraphs") for prop in props):
        raise ValueError("Invalid proposition status or empty proposition")
    token_props = [token for token in document.get("tokens", []) if token.get("kind") == "prop"]
    if token_props != props:
        raise ValueError("Proposition list and document stream disagree")
    headings = [token.get("text") for token in document["tokens"] if token.get("kind") == "heading"]
    if headings.count("Føreord") != 1 or headings.count("Lesekode") != 1:
        raise ValueError("The shared foreword or reading code is missing or duplicated")
    glossary = document.get("glossary")
    if not isinstance(glossary, list):
        raise ValueError("The shared glossary must be a list")
    glossary_ids = set()
    glossary_source_ids = {str(source.get("id", "")) for source in document.get("sources", [])}
    for entry in glossary:
        if not isinstance(entry, dict):
            raise ValueError("Invalid glossary entry")
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not GLOSSARY_ID.fullmatch(entry_id):
            raise ValueError("Invalid glossary identifier")
        if entry_id in glossary_ids:
            raise ValueError("Duplicate glossary identifier")
        glossary_ids.add(entry_id)
        for field in ("term", "definition"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError("Empty glossary " + field)
            if "[[" in entry[field] or "]]" in entry[field]:
                raise ValueError("Glossary text must use proposition targets, not source markers")
        if "symbol" in entry and (not isinstance(entry["symbol"], str) or not entry["symbol"].strip()):
            raise ValueError("Empty glossary symbol")
        if "fields" in entry:
            fields = entry["fields"]
            if not isinstance(fields, list) or not fields or any(not isinstance(field, str) or not field.strip() for field in fields) or len(fields) != len(set(fields)):
                raise ValueError("Invalid glossary fields")
        if "connection" in entry and (not isinstance(entry["connection"], str) or not entry["connection"].strip()):
            raise ValueError("Empty glossary connection")
        targets = entry.get("propositions")
        if not isinstance(targets, list) or not targets or any(not isinstance(target, str) or target not in numbers for target in targets):
            raise ValueError("Invalid glossary proposition target")
        if len(targets) != len(set(targets)):
            raise ValueError("Duplicate glossary proposition target")
        cited_sources = entry.get("sources", [])
        if not isinstance(cited_sources, list) or any(not isinstance(source, str) or source not in glossary_source_ids for source in cited_sources):
            raise ValueError("Unknown glossary source identifier")
        if len(cited_sources) != len(set(cited_sources)):
            raise ValueError("Duplicate glossary source identifier")
    sources = document.get("sources", [])
    ids = [str(source.get("id", "")) for source in sources]
    if not sources or any(not re.fullmatch(r"\d+", value) for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Invalid or duplicate source identifier")
    if any(not source.get("citation", "").strip() for source in sources):
        raise ValueError("Source citation is empty")
    if ([source.get("number") for source in sources] != list(range(1, len(sources) + 1))
            or any(type(source.get("number")) is not int for source in sources)):
        raise ValueError("Source display numbers are not consecutive")
    excluded = set(json.loads((root / "edition.json").read_text(encoding="utf-8")).get("excludedSourceIds", []))
    if excluded.intersection(ids):
        raise ValueError("An excluded source identifier is present")
    source_ids = set(ids)
    aliases = document.get("sourceAliases", {})
    if not isinstance(aliases, dict) or any(not isinstance(alias, str) or not isinstance(target, str) or not re.fullmatch(r"\d+", alias) or alias in source_ids or target not in source_ids for alias, target in aliases.items()):
        raise ValueError("Invalid source alias")
    note_ids = [note.get("id", "") for note in document.get("notes", [])]
    if len(note_ids) != len(set(note_ids)) or any(not NOTE_ID.fullmatch(value) for value in note_ids):
        raise ValueError("Invalid or duplicate note identifier")
    expected_note_numbers = list(range(1, len(note_ids) + 1))
    if [note.get("number") for note in document["notes"]] != expected_note_numbers:
        raise ValueError("Note display numbers are not consecutive")
    attached = []
    note_locations = {}
    section = None
    for token in document["tokens"]:
        if token["kind"] == "heading":
            section = {"Føreord": "foreword", "Lesekode": "reading-code"}.get(token.get("text"), token.get("text"))
        for text in token.get("paragraphs", []) if token["kind"] == "prop" else [token.get("text", "")]:
            citation_ids, residual_notes = marker_ids(text)
            if residual_notes:
                raise ValueError("Unresolved note placement metadata")
            if set(citation_ids) - source_ids:
                raise ValueError("Unknown cited source identifier")
        attached.extend(token.get("notes", []))
        for note_id in token.get("notes", []):
            note_locations[note_id] = (token["kind"], section)
    if sorted(attached) != sorted(note_ids):
        raise ValueError("Each note must have exactly one placement")
    for note in document["notes"]:
        if not note.get("note", "").strip() or set(note.get("sources", [])) - source_ids:
            raise ValueError("Empty note or unknown note source")
        proposition, section = note.get("proposition"), note.get("section")
        if proposition:
            if proposition not in numbers or section is not None:
                raise ValueError("Invalid note proposition target")
            prop = props[numbers.index(proposition)]
            if note["id"] not in prop.get("notes", []):
                raise ValueError("Note is attached to the wrong proposition")
        elif section != "foreword":
            raise ValueError("Invalid note section target")
        elif note_locations.get(note["id"]) != ("paragraph", "foreword"):
            raise ValueError("Section note is placed outside its target section")
    for figure in document.get("figures", []):
        if figure.get("after") not in numbers:
            raise ValueError("Figure proposition target does not exist")
        filename = figure.get("file", "")
        if not filename or Path(filename).name != filename or not figure.get("alt", "").strip():
            raise ValueError("Invalid figure metadata")
        if not (root / "nettstad" / "illustrations" / filename).is_file():
            raise ValueError("Figure asset is missing: " + filename)
    figure_names = [figure["file"] for figure in document.get("figures", [])]
    if len(figure_names) != len(set(figure_names)):
        raise ValueError("Duplicate figure placement")
    edition = json.loads((root / "edition.json").read_text(encoding="utf-8"))
    if edition.get("requireReferencedSources"):
        used = {value for token in document["tokens"]
                for text in (token.get("paragraphs", []) if token["kind"] == "prop" else [token.get("text", "")])
                for group in CITE.findall(text) for value in group.split(",")}
        used.update(value for note in document["notes"] for value in note.get("sources", []))
        used.update(value for entry in glossary for value in entry.get("sources", []))
        if source_ids - used:
            raise ValueError("Unreferenced active sources: " + ", ".join(sorted(source_ids - used, key=int)))
