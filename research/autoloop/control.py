import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STATE = HERE / "state.json"
CANDIDATE = HERE / "candidate.py"
REFERENCE = HERE / "reference.py"
BUDGET = 80.0
PER_RUN = 8.0
MAX_RUNS = 10
MAX_NO_GAIN = 2


def read_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def write_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def complete(state):
    return (
        state["attempts"] >= MAX_RUNS
        or state["reserved_usd"] + PER_RUN > BUDGET
        or state["estimated_usd"] + PER_RUN > BUDGET
        or state["no_gain"] >= MAX_NO_GAIN
    )


def reserve():
    state = read_state()
    if state["complete"] or complete(state):
        print("READY=0")
        return
    state["attempts"] += 1
    state["reserved_usd"] += PER_RUN
    state["last_run_id"] = os.environ.get("GITHUB_RUN_ID", "local")
    write_state(state)
    print("READY=1")


def candidate_is_safe():
    source = CANDIDATE.read_text(encoding="utf-8")
    if len(source.encode("utf-8")) > 16000:
        raise ValueError("Candidate code too large")
    tree = ast.parse(source)
    imports = {"numpy", "sklearn", "scipy", "math", "typing", "functools", "itertools", "collections"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if not all(alias.name.split(".")[0] in imports for alias in node.names):
                raise ValueError("Candidate imports outside scientific allowlist")
        if isinstance(node, ast.ImportFrom):
            if not node.module or node.module.split(".")[0] not in imports:
                raise ValueError("Candidate imports outside scientific allowlist")
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            raise ValueError("Global state not allowed")
        if isinstance(node, ast.Call):
            target = node.func
            name = target.id if isinstance(target, ast.Name) else target.attr if isinstance(target, ast.Attribute) else ""
            if name in {
                "open", "exec", "eval", "compile", "__import__", "getattr", "setattr",
                "globals", "locals", "vars", "system", "popen", "run", "read_text",
                "read_bytes", "load", "save", "dump", "urlopen", "request",
            }:
                raise ValueError("Candidate attempts external or reflective operations")
    if not any(isinstance(node, ast.FunctionDef) and node.name == "predict" for node in tree.body):
        raise ValueError("Candidate must expose predict(features, y_train)")


def tested():
    command = [sys.executable, "-m", "unittest", "discover", "-s", "research/formlaere-mot-designteori", "-p", "test_*.py"]
    finished = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=240)
    if finished.returncode:
        raise ValueError("Pre-existing research tests failed: " + (finished.stderr or "")[-1200:])


def finish(data_path, result_path, approved_state_path):
    approved = json.loads(approved_state_path.read_text(encoding="utf-8"))
    if read_state() != approved:
        raise ValueError("Budget state changed after reservation")
    state = approved
    actual = None
    reported_success = False
    if result_path.is_file():
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
            actual = float(result["total_cost_usd"])
            reported_success = result.get("is_error") is False
        except (ValueError, KeyError, TypeError):
            pass
    state["estimated_usd"] += actual if actual is not None and actual >= 0 else PER_RUN
    run_id = str(state["last_run_id"])
    summary = {
        "run_id": run_id, "reserved_usd": state["reserved_usd"],
        "estimated_usd": state["estimated_usd"], "accepted": False,
    }
    changed = set(subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines())
    permitted = {"research/autoloop/candidate.py", "research/autoloop/state.json"}
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
    ).splitlines()
    if reported_success and changed == permitted and not untracked:
        try:
            candidate_is_safe()
            from score import score
            measurements = score(data_path, "dev")
            summary["dev"] = measurements
            before = min(measurements["baseline_mse"], state["best_mse"])
            if measurements["candidate_mse"] <= before - 0.005 and measurements["wins"] >= 4:
                tested()
                state["best_mse"] = measurements["candidate_mse"]
                state["accepted"] += 1
                state["no_gain"] = 0
                summary["accepted"] = True
                summary["reason"] = "Frozen validation MSE improved against baseline and best previous model"
            else:
                summary["reason"] = "No sufficient improvement on frozen validation folds"
        except Exception as exc:
            summary["reason"] = "Rejected: " + str(exc)[:450]
    else:
        summary["reason"] = "Model failed or modified non-candidate files"
    if not summary["accepted"]:
        subprocess.run(["git", "restore", "--", "research/autoloop/candidate.py"], cwd=ROOT, check=True)
        state["no_gain"] += 1
    state["complete"] = complete(state)
    if state["complete"]:
        from score import score
        final = score(data_path, "final")
        summary["sealed_final"] = final
        if final["candidate_mse"] >= final["baseline_mse"]:
            shutil.copyfile(REFERENCE, CANDIDATE)
            summary["final_verdict"] = "No improvement on untouched groups; original baseline restored"
            state["best_mse"] = state["initial_mse"]
        else:
            summary["final_verdict"] = "Improved held-out MSE; observational prediction only"
    write_state(state)
    history = HERE / "history"
    history.mkdir(exist_ok=True)
    (history / (str(state["attempts"]).zfill(2) + ".json")).write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: summary[k] for k in ("run_id", "accepted", "reason")}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "reserve":
        reserve()
    elif len(sys.argv) == 5 and sys.argv[1] == "finish":
        finish(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        raise SystemExit("Usage: control.py reserve | finish DATA RESULT RESERVED_STATE")
