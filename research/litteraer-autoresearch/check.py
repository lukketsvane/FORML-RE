import json
import re
import sys
from pathlib import Path

PROPOSITION = re.compile(r"\\begin\{formproposition\}\{([^}]+)\}\{([a-z])\}(.*?)\\end\{formproposition\}", re.S)
MATHEMATICS = re.compile(r"\\\[(.*?)\\\]|\\\((.*?)\\\)", re.S)
CITATIONS = re.compile(r"\\(?:kjelder|notat)\{[^}]*\}")
HEADINGS = re.compile(r"\\section\{[^}]*\}")
REQUIRED = ("### Behaldne", "### Forkasta", "### Heilskap", "### Uvisse")


def validate(before, after, report):
    old = before.read_text(encoding="utf-8")
    new = after.read_text(encoding="utf-8")
    notes = report.read_text(encoding="utf-8")
    old_propositions = [(m.group(1), m.group(2)) for m in PROPOSITION.finditer(old)]
    new_propositions = [(m.group(1), m.group(2)) for m in PROPOSITION.finditer(new)]
    if len(old_propositions) != 491 or new_propositions != old_propositions:
        raise ValueError("A proposition number, type or order changed")
    if new.count(r"\begin{formproposition}") != 491 or new.count(r"\end{formproposition}") != 491:
        raise ValueError("A proposition boundary was lost")
    if MATHEMATICS.findall(new) != MATHEMATICS.findall(old):
        raise ValueError("A mathematical expression changed")
    if CITATIONS.findall(new) != CITATIONS.findall(old):
        raise ValueError("A source reference or note changed")
    if HEADINGS.findall(new) != HEADINGS.findall(old):
        raise ValueError("A chapter boundary changed")
    if len(notes.strip()) < 1500 or not all(h in notes for h in REQUIRED):
        raise ValueError("The adversarial literary report is missing or incomplete")
    changed = [
        n for (n, _), a, b in zip(
            old_propositions,
            (m.group(3) for m in PROPOSITION.finditer(old)),
            (m.group(3) for m in PROPOSITION.finditer(new)),
        )
        if a != b
    ]
    print(json.dumps({
        "propositions": 491,
        "revised_propositions": changed,
        "manuscript_changed": old != new,
        "mathematics_preserved": True,
        "citations_preserved": True,
        "report_present": True,
    }, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: check.py ORIGINAL_TEX CANDIDATE_TEX EDITORIAL_REPORT")
    validate(*(Path(path) for path in sys.argv[1:]))
