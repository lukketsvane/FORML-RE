import argparse
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "traktat/tekst/formlaere.tex"
CANDIDATES = ROOT / "research/nordisk-designforsking/results/possible_counterexamples_to_non_cumulative_design.csv"
PROPOSITION = re.compile(r"\\begin\{formproposition\}\{([^}]+)\}\{([^}]+)\}")
EXPECTED = {"1": 118, "2": 27, "3": 20, "4": 16, "5": 145, "6": 112, "7": 53}
TRUE_VALUES = {"true", "1", "yes", "verified"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def propositions():
    source = MANUSCRIPT.read_text(encoding="utf-8")
    found = PROPOSITION.findall(source)
    if len(found) != source.count(r"\begin{formproposition}"):
        raise ValueError("Ukjend eller ufullstendig proposisjonsmarkør")
    ids = [number for number, kind in found]
    if len(ids) != len(set(ids)) or any(kind not in "dat oi".replace(" ", "") for _, kind in found):
        raise ValueError("Dupliserte nummer eller ugyldig statusbokstav")
    counts = dict(collections.Counter(number.split(".")[0] for number in ids))
    if counts != EXPECTED:
        raise ValueError(f"Endra dekningsgrunnlag: {counts}")
    return dict(found)


def candidates():
    with CANDIDATES.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    required = {"citing_id", "cited_id", "citing_title", "cited_title", "citing_doi", "cited_doi", "independent_fulltext_validation", "confirmed_counterexample_to_non_cumulativity"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Kandidatkorpuset manglar obligatoriske kolonnar")
    return rows


def status(designteori=None):
    props = propositions()
    rows = candidates()
    pairs = {(r["citing_id"], r["cited_id"]) for r in rows}
    if len(pairs) != len(rows):
        raise ValueError("Dupliserte siteringspar")
    result = {
        "manuscript_sha256": digest(MANUSCRIPT),
        "propositions": len(props),
        "chapters": dict(collections.Counter(p.split(".")[0] for p in props)),
        "candidate_sha256": digest(CANDIDATES),
        "candidate_citation_pairs": len(rows),
        "independent_fulltext_validations": sum(r["independent_fulltext_validation"].strip().lower() in TRUE_VALUES for r in rows),
        "confirmed_counterexamples": sum(r["confirmed_counterexample_to_non_cumulativity"].strip().lower() in TRUE_VALUES for r in rows),
        "caveat": "Kandidatpar og bibliografiske metadata er ikkje fulltekstprov."
    }
    if designteori:
        with designteori.open(encoding="utf-8-sig", newline="") as file:
            result["designteori_records"] = sum(1 for _ in csv.DictReader(file))
        result["designteori_sha256"] = digest(designteori)
    return result


def words(value):
    return set(re.findall(r"[^\W\d_]{3,}", value.casefold()))


def search(query, designteori=None, limit=8):
    terms = words(query)
    if not terms:
        raise ValueError("Søkjemønsteret må ha eit ord")
    matches = []
    for row in candidates():
        title = row["citing_title"] + " " + row["cited_title"]
        score = len(terms & words(title))
        if score:
            matches.append((score, {
                "source": "nordisk-designforsking/candidate-pair",
                "status": "ikkje_fulltekstverifisert",
                "citing_id": row["citing_id"],
                "cited_id": row["cited_id"],
                "citing_title": row["citing_title"],
                "cited_title": row["cited_title"],
                "citing_doi": row["citing_doi"],
                "cited_doi": row["cited_doi"]
            }))
    if designteori:
        with designteori.open(encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                score = len(terms & words(row["title"]))
                if score:
                    matches.append((score, {
                        "source": "designteori/metadata",
                        "status": row["status"],
                        "id": row["id"],
                        "title": row["title"],
                        "doi": row["doi"],
                        "year": row["year"]
                    }))
    matches.sort(key=lambda entry: (-entry[0], entry[1].get("id", entry[1].get("citing_id", ""))))
    return [record for _, record in matches[:limit]]


def check(record_path):
    record = json.loads(record_path.read_text(encoding="utf-8"))
    required = ("proposition", "claim", "rival", "falsifier", "measurement", "baseline")
    if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required):
        raise ValueError("Forsøket manglar påstand, rival, motprøve, mål eller baseline")
    if record["proposition"] not in propositions():
        raise ValueError("Ukjent proposisjonsnummer")
    if record.get("status") not in ("open", "needs-human-review", "inconclusive"):
        raise ValueError("Ein automatisk kontroll kan ikkje stadfeste eller felle teorien")
    evidence = record.get("evidence")
    if not isinstance(evidence, list):
        raise ValueError("Evidenslista må vere ei liste")
    for item in evidence:
        if not isinstance(item, dict) or not all(item.get(k) for k in ("source_id", "source_url", "page", "status")):
            raise ValueError("Evidens manglar kjelde-ID, URL, side eller status")
        if item["status"] not in ("candidate", "fulltext-read", "human-verified"):
            raise ValueError("Ukjend evidensstatus")
        if item["status"] == "human-verified" and not item.get("reviewer"):
            raise ValueError("Uavhengig kontrollør manglar")
    return {
        "proposition": record["proposition"],
        "evidence_items": len(evidence),
        "structurally_valid": True,
        "caveat": "Dette kontrollerer sporbarheit, ikkje at påstandane er sanne."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "search", "check"))
    parser.add_argument("query", nargs="?")
    parser.add_argument("--designteori", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    if args.command == "status":
        result = status(args.designteori)
    elif args.command == "search":
        if args.query is None:
            parser.error("search treng søkjeord")
        result = search(args.query, args.designteori, args.limit)
    else:
        if args.record is None:
            parser.error("check treng --record")
        result = check(args.record)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
