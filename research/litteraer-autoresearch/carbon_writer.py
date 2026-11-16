import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from decimal import Decimal
from pathlib import Path

def main():
    suggestions = Path(sys.argv[1])
    cost_file = Path(sys.argv[2])
    key = os.getenv("GEMINI_API_KEY")
    suggestions.write_text("", encoding="utf-8")
    cost_file.write_text("0", encoding="utf-8")
    if not key:
        print("Gemini Carbon HIGH: ingen GEMINI_API_KEY, hoppar over utan API-kostnad")
        return

    root = Path("traktat")
    manuscript = (root / "tekst/formlaere.tex").read_text(encoding="utf-8")
    short = (root / "nettstad/kortversjon.tex").read_text(encoding="utf-8")
    prompt = (
        "Du er ein sjølvstendig litterær medredaktør for FORMLÆRE på nynorsk. "
        "Les heile traktaten og den matematiske kortversjonen før du skriv. "
        "Foreslå tre til åtte vesentlege litterære og kompositoriske omskrivingar. "
        "For kvar: oppgje presis proposisjonsadresse eller føreordsstad, kort eksakt førtekst, "
        "ei ny formulering i LaTeX og kvifor ho endrar kva teksten får lesaren til å erfare. "
        "Motprøv dine eigne alternativ, og forkast svakare forslag. "
        "Ingen endring av proposisjonsnummer, type, rekkjefølgje, likningar, kjeldemarkeringar eller notat. "
        "Hald deg til nynorsk, bruk me, ingen em dash. "
        "Sjå føreordet, hovudargumentet og etterordet i samanheng. "
        "Du skal ikkje påstå at dine forslag er betre utan grunngjeving. "
        "Skriv berre konkrete redaksjonelle alternativ, ikkje instruksjonar til verktøy eller arbeidsflyt.\n\n"
        "AUTORITATIV TRAKTAT:\n" + manuscript
        + "\n\nMATEMATISK KORTVERSJON:\n" + short
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingLevel": "HIGH"}, "maxOutputTokens": 16000}
    }
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    if len(payload) > 220000:
        raise SystemExit("Carbon: konteksten er for stor til det budsjetterte eine API-kallet")

    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-4-carbon:generateContent",
        data=payload,
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"Carbon: API avviste kallet (HTTP {error.code})") from error

    usage = result.get("usageMetadata") or {}
    if "promptTokenCount" not in usage or "totalTokenCount" not in usage:
        raise SystemExit("Carbon: manglande tokenrekneskap; kan ikkje stadfeste budsjettet")
    input_tokens = int(usage["promptTokenCount"])
    output_tokens = max(
        int(usage["totalTokenCount"]) - input_tokens,
        int(usage.get("candidatesTokenCount", 0)) + int(usage.get("thoughtsTokenCount", 0))
    )
    rate_in, rate_out = (Decimal("2"), Decimal("10")) if date.today() < date(2026, 12, 1) else (Decimal("4"), Decimal("20"))
    estimated = (Decimal(input_tokens) * rate_in + Decimal(output_tokens) * rate_out) / Decimal(1000000)
    cost_file.write_text(str(estimated), encoding="utf-8")
    print(f"Gemini Carbon HIGH: {input_tokens} inn, {output_tokens} ut/tenking, estimert {estimated} USD")
    if estimated > Decimal(os.environ["CARBON_MAX_USD"]):
        raise SystemExit("Carbon: estimert kostnad over reservert grense, stoppar vidare modellbruk")

    parts = ((result.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
    prose = "\n".join(part["text"] for part in parts if "text" in part and not part.get("thought"))
    if not prose.strip():
        raise SystemExit("Carbon: ingen redaksjonell tekst vart returnert")
    suggestions.write_text("# Uavhengige forslag frå Gemini 4 Carbon, HIGH\n\n" + prose, encoding="utf-8")

if __name__ == "__main__":
    main()
