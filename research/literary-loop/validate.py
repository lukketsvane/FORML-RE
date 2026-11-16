import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / "traktat/tekst/formlaere.tex"
PATTERN = re.compile(r"\\begin\{formproposition\}\{([^}]*)\}\{([^}]*)\}([\s\S]*?)\\end\{formproposition\}")
MATH = re.compile(r"\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\]")
CITES = re.compile(r"\\kjelder\{[^}]*\}")


def parse(data):
    return [(m.group(1), m.group(2), m.group(3)) for m in PATTERN.finditer(data)]


def check(before, after, max_changed=20):
    a = parse(before)
    b = parse(after)
    if len(a) != 491 or [(x, y) for x, y, _ in a] != [(x, y) for x, y, _ in b]:
        raise ValueError("491 proposition identifiers, types or order changed")
    skeleton = lambda t: PATTERN.sub(lambda m: "<PROP:" + m.group(1) + ">", t)
    if skeleton(before) != skeleton(after):
        raise ValueError("Preamble, chapter headings, or text outside propositions changed")
    changed = []
    growth = 0
    for (label, _, old), (_, _, new) in zip(a, b):
        if MATH.findall(old) != MATH.findall(new):
            raise ValueError("Mathematics altered at " + label)
        if CITES.findall(old) != CITES.findall(new):
            raise ValueError("Citations altered at " + label)
        if new != old:
            changed.append(label)
            growth += len(new) - len(old)
            if len(new) > max(2 * len(old), len(old) + 200):
                raise ValueError("Proposition expanded too far: " + label)
            if "—" in new and "—" not in old:
                raise ValueError("Unexpected em dash: " + label)
    if len(changed) > max_changed:
        raise ValueError("More than " + str(max_changed) + " propositions changed")
    if growth > 2200:
        raise ValueError("Excessive overall verbosity")
    return {"changed": changed, "count": len(changed), "net_characters": growth}


def check_worktree():
    text = TEXT.read_text(encoding="utf-8")
    baseline = subprocess.check_output(["git", "show", "HEAD:traktat/tekst/formlaere.tex"], cwd=ROOT).decode("utf-8")
    result = check(baseline, text)
    tracked = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    if any(path != "traktat/tekst/formlaere.tex" for path in tracked):
        raise ValueError("Unexpected tracked file modified: " + str(tracked))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


if __name__ == "__main__":
    try:
        check_worktree()
    except ValueError as exc:
        print("REJECTED: " + str(exc), file=sys.stderr)
        sys.exit(1)
