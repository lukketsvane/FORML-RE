import json
import re
import sys
from pathlib import Path
from check import CITATIONS, MATHEMATICS, PROPOSITION

FOREWORD = r"\section{Føreord}"
READING = r"\section{Lesekode}"
AFTERWORD = r"\section{Etterord}"
REQUIRED = ("### Behaldne", "### Forkasta", "### Heilskap", "### Uvisse")


def validate(before, after, report):
    old = before.read_text(encoding="utf-8")
    new = after.read_text(encoding="utf-8")
    notes = report.read_text(encoding="utf-8")
    if old.count(FOREWORD) != 1 or old.count(READING) != 1 or AFTERWORD in old:
        raise ValueError("Unexpected original manuscript structure")
    if new.count(FOREWORD) != 1 or new.count(READING) != 1 or new.count(AFTERWORD) != 1:
        raise ValueError("Foreword, reading code or afterword was lost or duplicated")
    old_prefix, old_other = old.split(FOREWORD, 1)
    old_foreword, old_body = old_other.split(READING, 1)
    new_base, afterword = new.split(AFTERWORD, 1)
    new_prefix, new_other = new_base.split(FOREWORD, 1)
    new_foreword, new_body = new_other.split(READING, 1)
    if new_prefix != old_prefix or new_body.rstrip() != old_body.rstrip():
        raise ValueError("Changes outside the foreword and appended afterword")
    if new_foreword == old_foreword:
        raise ValueError("Foreword was not revised")
    if len(afterword.strip()) < 400 or len(afterword.strip()) > 8000:
        raise ValueError("Afterword must be substantive and concise")
    if re.search(r"\\(?:section|title|begin|end)\b", afterword):
        raise ValueError("Unexpected structure in afterword")
    if MATHEMATICS.findall(new) != MATHEMATICS.findall(old):
        raise ValueError("Mathematics changed")
    if CITATIONS.findall(new) != CITATIONS.findall(old):
        raise ValueError("Citations or notes changed")
    old_props = [match.group(0) for match in PROPOSITION.finditer(old)]
    new_props = [match.group(0) for match in PROPOSITION.finditer(new)]
    if len(old_props) != 491 or old_props != new_props:
        raise ValueError("One of 491 propositions changed")
    if len(notes.strip()) < 1200 or not all(heading in notes for heading in REQUIRED):
        raise ValueError("The editorial report is missing or incomplete")
    print(json.dumps({"propositions": 491, "foreword_changed": True, "afterword_characters": len(afterword.strip()), "mathematics_preserved": True, "citations_preserved": True}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: check_foreword_afterword.py BEFORE_TEX AFTER_TEX REPORT")
    validate(*(Path(path) for path in sys.argv[1:]))
