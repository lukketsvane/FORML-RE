#!/usr/bin/env python3
"""Reproduce the author's LaTeX short edition as static, native MathML."""
from pathlib import Path
import re
import hashlib
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
head = """<!doctype html>
<html lang="nn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Kortversjonen av formlære: ein allmenn teori om form, tilpassingslandskap og avgrensa agens.">
<meta name="formlaere-source" content="@@SOURCE_HASH@@">
<title>formlære · tl;dr · Iver Finne</title>
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,300..400;1,7..72,300..400&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="/reader.css">
<link rel="stylesheet" href="/kortversjon.css">
</head>
<body class="short-version"><div class="app">
<nav class="bar" aria-label="Dokument og nettstad">
  <span class="document-links"><a href="/kortversjon/" aria-current="page">tl;dr</a></span>
  <a href="/">heile teksten</a>
</nav>
<main class="read" tabindex="0" aria-label="formlære, kortversjonen">
<article class="short-article">
"""
foot = """
<footer class="short-footer">
<a href="/">Les heile formlære</a>
<a href="/kort/">Konsentrert proposisjonsutval</a>
</footer>
</article></main></div>
<script>
if("serviceWorker" in navigator && window.isSecureContext){
window.addEventListener("load",()=>navigator.serviceWorker.register("/service-worker.js",{scope:"/",updateViaCache:"none"}).catch(()=>{}),{once:true});
}
</script>
</body></html>
"""


SOURCE_STAMP = re.compile(rb"<!-- form-source: ([a-f0-9]{64}) -->\n")
OUTPUT_STAMP = re.compile(rb"<!-- form-output: ([a-f0-9]{64}) -->\n")


def source_fingerprint(source: bytes, renderer: bytes) -> str:
    return hashlib.sha256(source + b"\0" + renderer).hexdigest()


def short_source_hash(root: Path) -> str:
    return source_fingerprint((root / "nettstad" / "kortversjon.tex").read_bytes(), Path(__file__).read_bytes())


def stamped_html(content: str) -> bytes:
    """Cover the entire generated page, excluding only its own integrity line."""
    raw = content.encode("utf-8")
    if len(SOURCE_STAMP.findall(raw)) != 1 or OUTPUT_STAMP.search(raw):
        raise ValueError("The short edition has invalid generation markers.")
    stamp = b"<!-- form-output: " + hashlib.sha256(raw).hexdigest().encode("ascii") + b" -->\n"
    source_stamp = SOURCE_STAMP.search(raw)
    return raw[:source_stamp.end()] + stamp + raw[source_stamp.end():]


def require_fresh_short(root: Path) -> None:
    target = root / "nettstad" / "kortversjon.html"
    expected = short_source_hash(root)
    try:
        raw = target.read_bytes()
    except FileNotFoundError:
        raw = b""
    sources, outputs = SOURCE_STAMP.findall(raw), OUTPUT_STAMP.findall(raw)
    valid = (len(sources) == len(outputs) == 1
             and sources[0].decode("ascii") == expected
             and hashlib.sha256(OUTPUT_STAMP.sub(b"", raw, count=1)).hexdigest() == outputs[0].decode("ascii"))
    if not valid or short_source_hash(root) != expected:
        raise ValueError("Short LaTeX edition is stale or modified. Run make all or python3 scripts/render_kortversjon.py.")


def render_short(root: Path = ROOT) -> None:
    source_bytes = (root / "nettstad" / "kortversjon.tex").read_bytes()
    initial_hash = source_fingerprint(source_bytes, Path(__file__).read_bytes())
    source = source_bytes.decode("utf-8")
    if not source.rstrip().endswith(r"\end{document}"):
        raise ValueError("The short source must terminate cleanly.")
    process = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--mathml",
         "--section-divs", "--number-sections", "--shift-heading-level-by=1",
         "--wrap=none", "--metadata", "title=formlære"],
        input=source, text=True, capture_output=True, check=True,
    )
    pandoc_warnings = process.stderr.replace(
        "[WARNING] Deprecated: --mathml. Use --math-method=mathml instead.", ""
    ).strip()
    if pandoc_warnings:
        raise ValueError(pandoc_warnings)
    body = process.stdout
    if not body or body.count("<math") < 35 or "<merror" in body:
        raise ValueError("The short edition lost its mathematical expressions.")
    body = re.sub(
        r'(<math\b[^>]*\bdisplay="block"[^>]*>[\s\S]*?</math>)',
        r'<div class="math-scroll" tabindex="0" role="region" aria-label="Matematisk uttrykk">\1</div>',
        body,
    )
    target = root / "nettstad" / "kortversjon.html"
    stamp = "<!-- form-source: " + initial_hash + " -->\n"
    output = stamped_html(head + stamp + body + foot)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=target.parent, prefix=".kortversjon-", suffix=".tmp", delete=False) as staged:
            temporary = Path(staged.name)
            staged.write(output)
        if short_source_hash(root) != initial_hash:
            raise ValueError("Short LaTeX source changed during rendering; run the build again.")
        temporary.replace(target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"Native MathML expressions: {body.count('<math')}; output: {target}")


if __name__ == "__main__":
    render_short()
