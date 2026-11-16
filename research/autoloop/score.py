import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "formlaere-mot-designteori"))
from stolar_heldut import prepare, features
from stolar_robusthet import technique_features, category_features
from stolar_designar_holdut import artist_clusters
from candidate import predict

CORPUS_SHA256 = "b552be3f754865854481c6f2ee1d46f604c59a8b70127963f402c6f328dab24e"
FEATURES = ("year", "technique", "origin", "materials")


def score(path, phase="dev"):
    if hashlib.sha256(path.read_bytes()).hexdigest() != CORPUS_SHA256:
        raise ValueError("The STOLAR dataset does not match the frozen checksum")
    data, provenance = prepare(path)
    if provenance["included_objects"] != 1598:
        raise ValueError("The STOLAR sampling frame changed")
    groups = artist_clusters(data)
    indices = np.arange(len(data))
    first = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=20261116)
    dev, held = next(first.split(data, groups=groups))
    if phase == "dev":
        folds = GroupShuffleSplit(n_splits=5, test_size=0.25, random_state=20261117)
        splits = [(dev[tr], dev[te]) for tr, te in folds.split(data.iloc[dev], groups=groups[dev])]
    else:
        splits = [(dev, held)]
    losses, baselines = [], []
    y = data[["log_H_W", "log_W_D", "log_size"]].to_numpy()
    for train_ix, test_ix in splits:
        if set(groups[train_ix]) & set(groups[test_ix]):
            raise AssertionError("Data leakage across creator groups")
        tr, te = data.iloc[train_ix], data.iloc[test_ix]
        f = features(tr, te)
        f["technique"] = technique_features(tr, te)
        f["origin"] = category_features(tr, te, "origin")
        mean, scale = y[train_ix].mean(0), y[train_ix].std(0)
        if (scale <= 0).any():
            raise ValueError("Degenerate target variable")
        y_train = (y[train_ix] - mean) / scale
        y_test = (y[test_ix] - mean) / scale
        base_train = np.column_stack([f[k][0] for k in FEATURES])
        base_test = np.column_stack([f[k][1] for k in FEATURES])
        standard = Ridge(alpha=20.0).fit(base_train, y_train).predict(base_test)
        predicted = np.asarray(predict(f, y_train), dtype=float)
        if predicted.shape != y_test.shape or not np.all(np.isfinite(predicted)):
            raise ValueError("Candidate produced invalid predictions")
        baselines.append(float(np.mean((standard - y_test) ** 2)))
        losses.append(float(np.mean((predicted - y_test) ** 2)))
    return {
        "phase": phase,
        "source_sha256": CORPUS_SHA256,
        "included_objects": provenance["included_objects"],
        "heldout_groups": int(len(set(groups[held]))),
        "folds": len(splits),
        "baseline_mse": sum(baselines) / len(baselines),
        "candidate_mse": sum(losses) / len(losses),
        "wins": sum(a < b for a, b in zip(losses, baselines)),
        "baseline_fold_mse": baselines,
        "candidate_fold_mse": losses,
        "scope": "Observed catalogue geometry only. Not a test of causal agency, choice, or design-theory superiority.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("--phase", choices=("dev", "final"), default="dev")
    arguments = parser.parse_args()
    print(json.dumps(score(arguments.data, arguments.phase), indent=2, sort_keys=True))
