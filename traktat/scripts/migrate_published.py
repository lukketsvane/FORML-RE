#!/usr/bin/env python3
"""One-time, exact migration of the published edition to explicit source markers.

Historical inputs stay in archive/2026-11-01. Never run this to edit a later
canonical edition. The normal build reads tekst/formlaere.tex. This script is a historical fixture only.
"""
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITE = re.compile(r"\[\[kjelde:\d+(?:,\d+)*\]\]")
NOTE = re.compile(r"\[\[notat:[A-Za-z][A-Za-z0-9_.-]*\]\]")


def utf16_index(text: str, offset: int) -> int:
    encoded = text.encode("utf-16-le")
    if offset < 0 or offset * 2 > len(encoded):
        raise ValueError("Citation offset is outside its paragraph")
    return len(encoded[:offset * 2].decode("utf-16-le"))


def migrate_text(original: str, reviewed: dict) -> str:
    text = original
    seen = set()
    for entry in reviewed["entries"]:
        paragraph = entry["paragraph"]
        if paragraph in seen or text.count(paragraph) != 1:
            raise ValueError("Citation paragraph is missing or ambiguous")
        seen.add(paragraph)
        cursor = 0
        pieces = []
        for span in entry["spans"]:
            start = utf16_index(paragraph, span["start"])
            end = utf16_index(paragraph, span["end"])
            if start < cursor or paragraph[start:end] != span["text"]:
                raise ValueError("Reviewed citation span no longer matches")
            ids = span["sourceIds"]
            if not ids or any(not re.fullmatch(r"\d+", str(value)) for value in ids):
                raise ValueError("Invalid reviewed source identifier")
            pieces.extend([paragraph[cursor:start], "[[kjelde:" + ",".join(ids) + "]]"])
            cursor = end
        pieces.append(paragraph[cursor:])
        text = text.replace(paragraph, "".join(pieces), 1)
    return text


def migrate(root: Path = ROOT, force: bool = False) -> dict:
    archive = root / "archive" / "2026-11-01"
    original = (archive / "formlaere.txt").read_text(encoding="utf-8")
    reviewed = json.loads((archive / "citations.json").read_text(encoding="utf-8"))
    old_catalog = json.loads((archive / "kjelder.json").read_text(encoding="utf-8"))
    placements = json.loads((archive / "placements.json").read_text(encoding="utf-8"))
    text = migrate_text(original, reviewed)
    notes = []
    unused_intro = []
    for index, item in enumerate(old_catalog.get("intro", []), 1):
        anchor = item.get("anchor", "")
        # This reproduces the published reader's selection exactly once. Later
        # editing uses an explicit marker, not the wording of this phrase.
        matching = [part for part in re.split(r"\n\s*\n", original) if anchor and anchor in part and not part.startswith("**")]
        if len(matching) != 1:
            unused_intro.append(item)
            continue
        stable_id = "intro-" + str(index)
        target_paragraph = matching[0]
        migrated_paragraph = migrate_text(target_paragraph, {"entries": [e for e in reviewed["entries"] if e["paragraph"] in target_paragraph]})
        if text.count(migrated_paragraph) != 1:
            raise ValueError("Introduction note placement is ambiguous")
        text = text.replace(migrated_paragraph, migrated_paragraph + "[[notat:" + stable_id + "]]", 1)
        note = {"id": stable_id, "proposition": None, "section": "foreword", "note": item["note"], "sources": item.get("sources", [])}
        if item.get("relation"):
            note["relation"] = item["relation"]
        notes.append(note)
    for item in old_catalog.get("annotations", []):
        note = {"id": "prop-" + item["proposition"].replace(".", "-"), "proposition": item["proposition"], "section": None,
                "note": item["note"], "sources": item.get("sources", [])}
        if item.get("relation"):
            note["relation"] = item["relation"]
        notes.append(note)
    catalog = {"version": 2, "language": old_catalog.get("language", "nn"),
               "provenance": {"text": "tekst/formlaere.txt", "note": old_catalog.get("provenance", {}).get("note", "")},
               "sources": deepcopy(old_catalog["sources"]), "notes": notes}
    figures = {"version": 1, "assets": placements["assets"]}
    edition = {"schemaVersion": 1, "title": "FORMLÆRE", "author": "Iver Raknes Finne", "language": "nn", "excludedSourceIds": ["108"]}
    outputs = {root / "tekst" / "formlaere.txt": text,
               root / "kjelder.json": json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
               root / "figurar.json": json.dumps(figures, ensure_ascii=False, indent=2) + "\n",
               root / "edition.json": json.dumps(edition, ensure_ascii=False, indent=2) + "\n"}
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") != content and not force:
            raise ValueError(f"Refusing to overwrite a changed canonical file: {path}")
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    glossary_path = root / "ordliste.json"
    if not glossary_path.exists():
        glossary_path.write_text(json.dumps({"schemaVersion": 1, "entries": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (archive / "unused-intro-notes.json").write_text(json.dumps({"reason": "Not displayed in the migrated published edition; older introduction wording.", "notes": unused_intro}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"citationGroups": sum(len(e["spans"]) for e in reviewed["entries"]), "notes": len(notes), "sources": len(catalog["sources"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--force", action="store_true", help="replace canonical files with the archived published snapshot")
    args = parser.parse_args()
    print(json.dumps(migrate(args.root, args.force), ensure_ascii=False))
