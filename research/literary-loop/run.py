import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from validate import ROOT, TEXT, check_worktree

HERE = Path(__file__).resolve().parent
REVIEWS = HERE / "reviews"
STATE = HERE / "state.json"
BRANCH = "literary/formlaere-adversarial-20261116"
MAX_BUDGET = 80
STAGES = {"editor": 8, "philosopher": 4, "poet": 4, "reviser": 5, "final": 3}
READING_RESERVE = 6
SCHEDULE = [
    "Første rørsle: korleis skilnad, objekt, mogleg form og den første avgrensinga tek til å bety noko anna når dei møter handlag, realisering og etisk omsyn seinare.",
    "Andre rørsle: motiv som vender tilbake, måten form gjer motstand, endringa frå registrering og modell til berar, hand og den andre sin motstand. Rytme, nødvendig stillheit, avgrensa gjentaking.",
    "Tredje rørsle: lat siste kapittel kaste eit nytt lys på dei første proposisjonane utan å forklare denne effekten. Slutten må fortene opninga, ikkje gjenta henne som slogan.",
]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def save(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def start():
    REVIEWS.mkdir(parents=True, exist_ok=True)
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("Refusing to run outside the isolated literary branch")
    raw_path = REVIEWS / "01-map.raw.json"
    if not raw_path.is_file():
        raise RuntimeError("The full-treatise reading is not finished")
    mapping = json.loads(raw_path.read_text(encoding="utf-8-sig"))
    if mapping.get("is_error") or not (REVIEWS / "01-map.md").is_file():
        raise RuntimeError("The initial literary map failed")
    if STATE.is_file():
        state = json.loads(STATE.read_text(encoding="utf-8"))
    else:
        state = {
            "schema": 1, "model": "claude-fable-5-2", "ceiling_usd": MAX_BUDGET,
            "reserved_usd": READING_RESERVE,
            "estimated_usd": float(mapping.get("total_cost_usd") or READING_RESERVE),
            "completed_rounds": 0, "accepted_rounds": 0, "consecutive_rejections": 0,
            "runs": [{"stage": "map", "ceiling_usd": READING_RESERVE,
                      "estimated_usd": mapping.get("total_cost_usd")}],
        }
        save(state)
    return state


def call(state, name, prompt, budget, tools, turns=26):
    if state["reserved_usd"] + budget > MAX_BUDGET:
        raise RuntimeError("Literary API budget allocation exhausted")
    state["reserved_usd"] += budget
    run = {"stage": name, "ceiling_usd": budget, "estimated_usd": None}
    state["runs"].append(run)
    save(state)
    cmd = [
        shutil.which("claude") or "claude", "-p", prompt, "--model", "claude-fable-5-2",
        "--effort", "high", "--max-turns", str(turns), "--max-budget-usd", str(budget),
        "--permission-mode", "bypassPermissions", "--tools", tools,
        "--output-format", "json",
    ]
    raw_path = REVIEWS / (name + ".raw.json")
    err_path = REVIEWS / (name + ".stderr.log")
    print("FABLE_START " + name + " max_USD=" + str(budget), flush=True)
    with raw_path.open("w", encoding="utf-8") as out, err_path.open("w", encoding="utf-8") as err:
        result = subprocess.run(cmd, cwd=ROOT, stdout=out, stderr=err, timeout=1500, check=False)
    try:
        data = json.loads(raw_path.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError):
        data = {"is_error": True}
    cost = data.get("total_cost_usd")
    try:
        cost = float(cost)
        if cost < 0:
            cost = budget
    except (ValueError, TypeError):
        cost = budget
    run["estimated_usd"] = cost
    state["estimated_usd"] += cost
    save(state)
    text = data.get("result") or ""
    if not isinstance(text, str):
        text = ""
    (REVIEWS / (name + ".md")).write_text(text, encoding="utf-8")
    print("FABLE_END " + name + " exit=" + str(result.returncode) +
          " est_USD=" + str(round(cost, 4)) + " chars=" + str(len(text)), flush=True)
    if result.returncode or data.get("is_error") is not False or len(text) < 80:
        raise RuntimeError("Fable stage failed: " + name)
    return text


def verdict(text):
    values = re.findall(r"^DOM:\s*(HALD|ENDRE|FORKAST)\s*$", text, flags=re.MULTILINE)
    return values[-1] if values else "FORKAST"


def revert_manuscript():
    git("restore", "--", "traktat/tekst/formlaere.tex")


def save_round(state, round_no, outcome, reason):
    state["completed_rounds"] = round_no
    state["accepted_rounds"] += int(outcome)
    state["consecutive_rejections"] = 0 if outcome else state["consecutive_rejections"] + 1
    save(state)
    log = REVIEWS / (f"{round_no:02d}-decision.md")
    log.write_text(
        f"# Litterær prøverunde {round_no}\n\n"
        f"**Maskinelt redaksjonsutfall:** {'bevart for menneskeleg review' if outcome else 'forkasta'}.\n\n"
        f"{reason}\n\nIngen empirisk validering eller objektiv litteraturskår. "
        "Ingen endring i main.\n", encoding="utf-8"
    )
    staged = ["research/literary-loop/state.json", "research/literary-loop/reviews"]
    if outcome:
        staged.append("traktat/tekst/formlaere.tex")
    git("add", "--", *staged)
    git("diff", "--cached", "--check")
    git("commit", "-m", f"Litterær motprøve {round_no}: " + ("bevar komposisjonsendringar" if outcome else "forkast forslaget"))
    git("push", "origin", "HEAD:" + BRANCH)


def main():
    state = start()
    for number, theme in enumerate(SCHEDULE, start=1):
        if state["completed_rounds"] >= number:
            continue
        if state["consecutive_rejections"] >= 2:
            print("STOP: two consecutive failed literary proposals", flush=True)
            break
        base = git("rev-parse", "HEAD")
        label = f"{number:02d}"
        editor = (
            "Les research/literary-loop/program.md, reviews/01-map.md og heile "
            "traktat/tekst/formlaere.tex. Arbeid litterært, ikkje statistisk. "
            "Tema for denne runden: " + theme + "\n"
            "Du er redaktøren. Gjer 4-16 **små, men kompositorisk vesentlege** "
            "endringar, berre i traktat/tekst/formlaere.tex. Bruk Edit, aldri "
            "andre skrivemåtar. Endringane skal byggje nye samanhengar mellom "
            "ulike delar, ikkje berre gjere setningane glatte. Bevar gåte, trykk, "
            "matematikk, kjeldetilvisingar og alle proposisjonsnummer. "
            "Ikkje skriv utanfor proposisjonane. Det er lov å avstå frå endringar "
            "dersom ingen verkeleg held. Skriv ei kort grunngjeving for kvar "
            "endringa i svaret, med nummer og kor i verket ho får konsekvens."
        )
        try:
            call(state, f"{label}-editor", editor, STAGES["editor"], "Read,Edit,Grep,Glob", 36)
            measurements = check_worktree()
            if not measurements["changed"]:
                revert_manuscript()
                save_round(state, number, False, "Ingen endring med tilstrekkeleg konkret litterær hypotese.")
                continue
            diff = git("diff", "--", "traktat/tekst/formlaere.tex")
            (REVIEWS / f"{label}-diff.patch").write_text(diff + "\n", encoding="utf-8")
            common = (
                "Les heile traktat/tekst/formlaere.tex, kartet i research/literary-loop/reviews/01-map.md, "
                f"og den konkrete diffen research/literary-loop/reviews/{label}-diff.patch. "
                f"Utgangspunktet er commit {base}. Motles det du ser. "
                "Du må samanlikne den gamle ordlyden med den nye og aktivt finne "
                "kva den gamle gjer betre. Ein vakrare setning er ikkje eit framsteg. "
                "Ikkje endre filer. Skriv dokumenterte ja- og neiargument, nøyaktige "
                "proposisjonsnummer, og kva som skjer med komposisjonen frå første til siste del. "
                "Avslutt med nøyaktig ei line: DOM: HALD eller DOM: ENDRE eller DOM: FORKAST."
            )
            philosophy = common + (
                "\nDu er FILOSOFISK MOTLESAR, uavhengig av redaktøren: Finn tapte premiss, "
                "falsk presisjon, tomme paradoks, omgrepsgliding og djupn som gjekk tapt."
            )
            poetry = common + (
                "\nDu er POETISK OG KOMPOSITORISK MOTLESAR, uavhengig: "
                "Prøv rytme, tilbakevending med forskoven tyding, biletlege trykk, "
                "tausheit, negativt rom, grense og slutten si omdanning av byrjinga."
            )
            a = verdict(call(state, f"{label}-philosopher", philosophy, STAGES["philosopher"], "Read,Grep,Glob", 24))
            b = verdict(call(state, f"{label}-poet", poetry, STAGES["poet"], "Read,Grep,Glob", 24))
            if a == "FORKAST" and b == "FORKAST":
                revert_manuscript()
                save_round(state, number, False, "Begge uavhengige lesarar forkasta endringane.")
                continue
            keep = a == "HALD" and b == "HALD"
            if not keep:
                revise = (
                    "Les heile traktaten, research/literary-loop/program.md, "
                    f"reviews/{label}-philosopher.md og reviews/{label}-poet.md. "
                    "Du er ei streng tredje hand. Den førre endringa er framleis "
                    "berre eit forslag. Revider eller gå attende til den originale "
                    "proposisjonsordlyden der kritikken held. Endre berre "
                    "traktat/tekst/formlaere.tex. Det er betre å forkaste ti "
                    "overflatiske forbetringar enn å miste ei nødvendig gåte. "
                    "Bevar dei 491 adressene, all matte, kjelder og heile komposisjonen."
                )
                call(state, f"{label}-reviser", revise, STAGES["reviser"], "Read,Edit,Grep,Glob", 30)
                measurements = check_worktree()
                if measurements["changed"]:
                    (REVIEWS / f"{label}-diff-after-revision.patch").write_text(
                        git("diff", "--", "traktat/tekst/formlaere.tex") + "\n",
                        encoding="utf-8"
                    )
                    final = (
                        "Du er siste, SKEPTISKE litterære motlesar. Les "
                        "traktat/tekst/formlaere.tex, det heilskaplege kartet, dei to "
                        f"motlesingane for runde {number} og reviews/{label}-diff-after-revision.patch. "
                        "Det er ditt oppdrag å avsløre at den reviderte ordlyden "
                        "berre er penare, mindre gåtefull eller logisk dårlegare. "
                        "Du kan ikkje redigere. Vurder heilskapen. Avslutt med "
                        "DOM: HALD, DOM: ENDRE eller DOM: FORKAST på eiga line."
                    )
                    keep = verdict(call(state, f"{label}-final", final, STAGES["final"], "Read,Grep,Glob", 24)) == "HALD"
            if keep:
                measurements = check_worktree()
                save_round(state, number, True, "Endringsnummer: " + ", ".join(measurements["changed"]) +
                           ". Maskinlesarar tilrår å bevare dei, men det står att menneskeleg gjennomgang.")
            else:
                revert_manuscript()
                save_round(state, number, False, "Kompositorisk motprøve gav ikkje tilstrekkeleg haldbart framsteg.")
        except Exception as error:
            revert_manuscript()
            print("STOP_ERROR " + str(error)[:400], flush=True)
            save(state)
            raise
    print("LITERARY_LOOP_FINISHED " + json.dumps({
        "reserved_usd": state["reserved_usd"],
        "estimated_usd": state["estimated_usd"],
        "completed_rounds": state["completed_rounds"],
        "accepted_rounds": state["accepted_rounds"]
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
