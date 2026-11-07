#!/usr/bin/env python3
"""Førehandsspesifisert og etterprøvbart valbenchmark for Formlære §6.6.

Bruk:
  python choice_benchmark.py --demo
  python choice_benchmark.py --csv choice_sets.csv

VIKTIG: --demo lagar berre SYNTETISKE data. Det er aldri empirisk evidens.
CSV må dokumentere alle registrerte tilgjengelege alternativ *før* utfallet.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from math import exp, fsum, isfinite, log
from pathlib import Path
import random

import numpy as np
from scipy.optimize import minimize, minimize_scalar

REQUIRED = {
    "case_id", "group_id", "split", "option_id", "chosen", "feasible",
    "mu", "e1", "e2", "w1", "w2",
}
SPLITS = ("train", "validation", "test")


@dataclass(frozen=True)
class ChoiceSet:
    case_id: str
    group_id: str
    split: str
    option_ids: tuple[str, ...]
    base: np.ndarray
    deviations: np.ndarray
    agent_weights: np.ndarray
    selected_index: int

    @property
    def phi(self) -> np.ndarray:
        return self.deviations @ self.agent_weights


def _parse_bool(s: str) -> bool:
    if s not in ("0", "1"):
        raise ValueError("chosen og feasible skal vere 0 eller 1")
    return s == "1"


def rows_to_cases(rows: list[dict[str, str]]) -> list[ChoiceSet]:
    if not rows:
        raise ValueError("Mangler dokumenterte alternativ")
    if REQUIRED - set(rows[0]):
        raise ValueError("Kolonnar manglar: " + ", ".join(sorted(REQUIRED - set(rows[0]))))
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["case_id"]].append(row)
    result = []
    group_splits: dict[str, str] = {}
    for case_id, alternatives in grouped.items():
        splits = {r["split"] for r in alternatives}
        groups = {r["group_id"] for r in alternatives}
        if len(splits) != 1 or not splits <= set(SPLITS) or len(groups) != 1:
            raise ValueError(f"Splitt/grupper varierer innan case_id {case_id}")
        split = splits.pop()
        group = groups.pop()
        if group in group_splits and group_splits[group] != split:
            raise ValueError(f"LEKKASJE: group_id {group} i fleire datasplittar")
        group_splits[group] = split
        all_names = [r["option_id"] for r in alternatives]
        if len(set(all_names)) != len(all_names):
            raise ValueError(f"Duplisert alternativ i {case_id}")
        if sum(_parse_bool(r["chosen"]) for r in alternatives) != 1:
            raise ValueError(f"Treng nøyaktig eitt observert val i {case_id}")
        if any(_parse_bool(r["chosen"]) and not _parse_bool(r["feasible"]) for r in alternatives):
            raise ValueError(f"Valt alternativ ligg utanfor D i {case_id}")
        feasible = [r for r in alternatives if _parse_bool(r["feasible"])]
        if len(feasible) < 2:
            raise ValueError(f"For få materiellt/operativt tillatne alternativ i {case_id}")
        try:
            base = np.array([float(r["mu"]) for r in feasible], dtype=float)
            deviations = np.array([[float(r["e1"]), float(r["e2"])] for r in feasible], dtype=float)
            weights = np.array([[float(r["w1"]), float(r["w2"])] for r in feasible], dtype=float)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Ugyldige tal i {case_id}") from exc
        if not (np.all(np.isfinite(base)) and np.all(base > 0)):
            raise ValueError(f"mu må vere endeleg og positiv i {case_id}")
        if not (np.all(np.isfinite(deviations)) and np.all(deviations >= 0)):
            raise ValueError(f"Avvik må vere ikkje-negative endelege tal i {case_id}")
        if not (np.all(np.isfinite(weights)) and np.all(weights >= 0)):
            raise ValueError(f"Prioriteringar må vere ikkje-negative i {case_id}")
        if not np.allclose(weights, weights[0], atol=1e-10, rtol=0):
            raise ValueError(f"Prioriteringar varierer innan same val i {case_id}")
        if not np.isclose(weights[0].sum(), 1, atol=1e-9):
            raise ValueError(f"Prioriteringane må summere til éin i {case_id}")
        chosen_options = [r["option_id"] for r in alternatives if _parse_bool(r["chosen"])]
        names = tuple(r["option_id"] for r in feasible)
        result.append(ChoiceSet(
            case_id=case_id, group_id=group, split=split,
            option_ids=names, base=base / base.sum(), deviations=deviations,
            agent_weights=weights[0], selected_index=names.index(chosen_options[0]),
        ))
    for split in SPLITS:
        if sum(c.split == split for c in result) < 5:
            raise ValueError(f"Minst fem valsett er kravde i {split}")
    return result


def load_cases(csv_path: Path) -> list[ChoiceSet]:
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        return rows_to_cases(list(csv.DictReader(f)))


def probs(case: ChoiceSet, model: str, beta: float = 0.0, theta=None) -> np.ndarray:
    """Alle kandidatar i same valsett får identisk tilgjengeleg informasjon."""
    n = len(case.option_ids)
    if model == "uniform":
        logits = np.zeros(n)
    elif model == "grammar":
        logits = np.log(case.base)
    elif model == "form":
        logits = np.log(case.base) - beta * case.phi
    elif model == "weight_only":
        logits = -beta * case.phi
    elif model == "conditional_logit":
        logits = np.log(case.base) - case.deviations @ np.asarray(theta)
    else:
        raise ValueError("Ukjend modell: " + model)
    logits = logits - logits.max()
    p = np.exp(logits)
    return p / p.sum()


def mean_loss(cases, model, *, beta=0.0, theta=None):
    return fsum(-log(max(probs(c, model, beta, theta)[c.selected_index], 1e-300)) for c in cases) / len(cases)


def fit_beta(train, model):
    r = minimize_scalar(
        lambda b: mean_loss(train, model, beta=float(b)),
        bounds=(0.0, 12.0), method="bounded",
        options={"xatol": 1e-6},
    )
    # At beta=0 the form/proposal model is exactly the grammar model.
    return min([0.0, float(r.x), 12.0], key=lambda x: mean_loss(train, model, beta=x))


def fit_conditional_logit(train, validation):
    """Fri fortegn, men berre treningsdata til parameterestimering.

    Regulariseringsstyrken vert vald på valideringssettet, aldri på test.
    """
    def solve(lam):
        def obj(x):
            return mean_loss(train, "conditional_logit", theta=x) + lam * float(x @ x)
        return minimize(obj, np.zeros(2), method="L-BFGS-B").x
    candidates = [solve(lam) for lam in (0.0, 0.01, 0.1, 1.0)]
    return min(candidates, key=lambda theta: mean_loss(validation, "conditional_logit", theta=theta))


def score_cases(test, model, *, beta=0.0, theta=None):
    total = len(test)
    nll, acc, brier = [], 0, []
    for c in test:
        p = probs(c, model, beta, theta)
        truth = np.zeros(len(p))
        truth[c.selected_index] = 1.0
        nll.append(-log(max(float(p[c.selected_index]), 1e-300)))
        acc += int(int(np.argmax(p)) == c.selected_index)
        brier.append(float(np.sum((p - truth) ** 2)))
    return {
        "mean_log_loss": round(float(np.mean(nll)), 6),
        "top1_accuracy": round(acc / total, 6),
        "multiclass_brier": round(float(np.mean(brier)), 6),
        "per_case_losses": nll,
    }


def bootstrap_difference(loss_a, loss_b, group_ids, *, draws=2000, seed=20261107):
    """B - A; bootsrap av grupper, ikkje tilfeldig oppdeling av same prosjekt.

    Ei gruppe kan innehalde fleire påfølgjande val. Vi resamplar heile
    gruppa og reknar eit tal som er vekta med kor mange val gruppa bidreg.
    """
    values = np.asarray(loss_b, dtype=float) - np.asarray(loss_a, dtype=float)
    if len(values) != len(group_ids):
        raise ValueError("Ulik lengd mellom tap og gruppe-ID-ar")
    group_sums, group_counts = defaultdict(float), defaultdict(int)
    for value, group_id in zip(values, group_ids):
        group_sums[group_id] += float(value)
        group_counts[group_id] += 1
    groups = sorted(group_sums)
    if len(groups) < 2:
        raise ValueError("Minst to uavhengige grupper trengst for bootstrap")
    total = np.array([group_sums[g] for g in groups])
    sizes = np.array([group_counts[g] for g in groups])
    rng = np.random.default_rng(seed)
    samples = rng.integers(0, len(groups), size=(draws, len(groups)))
    distribution = total[samples].sum(axis=1) / sizes[samples].sum(axis=1)
    return {
        "delta_log_loss_B_minus_form": round(float(values.mean()), 6),
        "ci95_cluster_bootstrap": [round(float(x), 6) for x in np.quantile(distribution, [0.025, 0.975])],
        "independent_groups": len(groups),
    }


def benchmark(cases):
    parts = {s: [c for c in cases if c.split == s] for s in SPLITS}
    train, validation, test = (parts[s] for s in SPLITS)
    beta_form = fit_beta(train, "form")
    beta_weight_only = fit_beta(train, "weight_only")
    theta = fit_conditional_logit(train, validation)
    opts = {
        "uniform": {},
        "grammar": {},
        "weight_only": {"beta": beta_weight_only},
        "form": {"beta": beta_form},
        "conditional_logit": {"theta": theta},
    }
    scores = {name: score_cases(test, name, **params) for name, params in opts.items()}
    comparison = {
        name: bootstrap_difference(
            scores["form"]["per_case_losses"], scores[name]["per_case_losses"],
            [c.group_id for c in test],
        )
        for name in scores if name != "form"
    }
    for entry in scores.values():
        entry.pop("per_case_losses")
    return {
        "case_counts": {s: len(parts[s]) for s in SPLITS},
        "fitted_parameters": {
            "form_beta": round(beta_form, 6),
            "weight_only_beta": round(beta_weight_only, 6),
            "conditional_logit_theta": [round(float(v), 6) for v in theta],
        },
        "heldout_test": scores,
        "paired_ci95": comparison,
        "notes": [
            "Prøva føreset at alle alternativ, avvik, grunnvekter og agentvekter vart dokumenterte før valet.",
            "Kven som har autoritet og kva data som er legitime, må etablerast utanfor denne statistiske prøva.",
            "Ei empirisk vinst er ikkje dokumentert før reelle, ubrukte og sporbart daterte data er vurderte.",
        ],
    }


def synthetic_rows(world: str, seed=20261107):
    """Tre eksplisitt syntetiske datagenererande mekanismar.

    form: faktisk val etter Formlæra sine på førehand observerte estimat
    uniform: utfall uavhengig av mu og estimat; uniform kan vinne
    adversarial: ein estimatkoeffisient har motsett forteikn; fri logit kan vinne
    """
    rng = random.Random(seed)
    rows = []
    for i in range(800):
        split = "train" if i < 440 else "validation" if i < 560 else "test"
        mu = [exp(rng.uniform(-1.6, 1.6)) for _ in range(4)]
        e = [(rng.uniform(0, 3), rng.uniform(0, 3)) for _ in range(4)]
        w = (0.7, 0.3)
        if world == "form":
            logits = [log(mu[j]) - 2.2 * (w[0]*e[j][0] + w[1]*e[j][1]) for j in range(4)]
        elif world == "uniform":
            logits = [0.0]*4
        elif world == "adversarial":
            logits = [log(mu[j]) + 2.0*e[j][0] - 1.2*e[j][1] for j in range(4)]
        else:
            raise ValueError(world)
        masses = [exp(z-max(logits)) for z in logits]
        r = rng.random() * sum(masses)
        chosen = 0
        for j, mass in enumerate(masses):
            r -= mass
            if r <= 0:
                chosen = j
                break
        for j in range(4):
            rows.append({
                "case_id": f"{world}-{i:04d}", "group_id": f"{world}-group-{i:04d}",
                "split": split, "option_id": f"option-{j}",
                "chosen": str(int(j == chosen)), "feasible": "1",
                "mu": str(mu[j]), "e1": str(e[j][0]), "e2": str(e[j][1]),
                "w1": str(w[0]), "w2": str(w[1]),
            })
    return rows


def main():
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    x = parser.add_mutually_exclusive_group(required=True)
    x.add_argument("--csv", type=Path)
    x.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        out = {world: benchmark(rows_to_cases(synthetic_rows(world)))
               for world in ("form", "uniform", "adversarial")}
        print("SYNTHETISKE PRØVER. INGEN EMPIRISK EVIDENS.")
    else:
        out = benchmark(load_cases(args.csv))
        print("OBSERVERTE DATA: kontroll av førehandsspesifisering og proveniens krev separat audit.")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
