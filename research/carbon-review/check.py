import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = (root / "traktat" / "tekst" / "formlaere.tex").read_text(encoding="utf-8")
alternative = (Path(__file__).parent / "CARBON-ALTERNATIV-IKKJE-PUBLISER.md").read_text(encoding="utf-8")
original = {m.group(1): m.group(2) for m in re.finditer(r"\\begin\{formproposition\}\{([\d.]+)\}\{([datio])\}", source)}
proposals = {m.group(1): m.group(2) for m in re.finditer(r"(?m)^\*\*([1-7](?:\.\d+)*)\*\*\s+\*\[([datio])\]\*", alternative)}
sort = lambda s: tuple(map(int, s.split(".")))
missing = sorted(set(original) - set(proposals), key=sort)
extra = sorted(set(proposals) - set(original), key=sort)
changed = [(n, original[n], proposals[n]) for n in sorted(set(original) & set(proposals), key=sort) if original[n] != proposals[n]]
assert len(original) == 491
assert len(proposals) == 486
assert missing == ["1.2343", "1.2354", "2.202", "2.211", "2.2011", "2.2021", "3.401", "5.7221", "5.72312"]
assert extra == ["2.22", "3.304", "3.305", "3.412"]
assert changed == [("1.2341", "a", "t"), ("5.722", "a", "t"), ("5.724", "t", "d")]
with (Path(__file__).parent / "ADRESSEKART.tsv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
assert len(rows) == len(set(original) | set(proposals))
for row in rows:
    n = row["adresse"]
    assert row["main_type"] == original.get(n, "")
    assert row["carbon_type"] == proposals.get(n, "")
print(f"Verified main={len(original)} Carbon={len(proposals)} missing={len(missing)} extra={len(extra)} types={len(changed)}")
