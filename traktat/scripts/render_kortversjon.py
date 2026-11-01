#!/usr/bin/env python3
"""Reproduce the author's LaTeX short edition as static, native MathML."""
from pathlib import Path
import re
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
head = """<!doctype html>
<html lang="nn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Kortversjonen av FORMLÆRE: ein allmenn teori om form, tilpassingslandskap og avgrensa agens.">
<meta name="formlaere-source" content="@@SOURCE_HASH@@">
<title>FORMLÆRE · tl;dr · Iver Finne</title>
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
  <span class="document-links"><a href="/traktat/formlaere.pdf" download="formlære.pdf">formlære.pdf</a>
  <a href="/kortversjon/" aria-current="page">tl;dr</a></span>
  <a href="/">heile teksten</a>
</nav>
<main class="read" tabindex="0" aria-label="FORMLÆRE, kortversjonen">
<article class="short-article">
<header class="short-header">
<p class="short-label">Kortversjon</p>
<p class="short-byline">Iver Finne · Oslo, 2026</p>
</header>
"""
foot = """
<footer class="short-footer">
<a href="/">Les heile FORMLÆRE</a>
<a href="/kort/">Konsentrert proposisjonsutval</a>
<a href="https://iverfinne.no">iverfinne.no</a>
</footer>
</article></main></div>
<script>
if("serviceWorker" in navigator && window.isSecureContext){
window.addEventListener("load",()=>navigator.serviceWorker.register("/service-worker.js",{scope:"/",updateViaCache:"none"}).catch(()=>{}),{once:true});
}
</script>
</body></html>
"""


def short_source_hash(root: Path) -> str:
    source = (root / "nettstad" / "kortversjon.tex").read_bytes()
    return hashlib.sha256(source + b"\0" + Path(__file__).read_bytes()).hexdigest()


def require_fresh_short(root: Path) -> None:
    target = root / "nettstad" / "kortversjon.html"
    expected = "<!-- form-source: " + short_source_hash(root) + " -->"
    if not target.is_file() or expected not in target.read_text(encoding="utf-8"):
        raise ValueError("Short LaTeX edition is stale. Run make all or python3 scripts/render_kortversjon.py.")


def render_short(root: Path = ROOT) -> None:
    source = (root / "nettstad" / "kortversjon.tex").read_text(encoding="utf-8")
    if not source.rstrip().endswith(r"\end{document}"):
        raise ValueError("The short source must terminate cleanly.")
    process = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--mathml",
         "--section-divs", "--number-sections", "--shift-heading-level-by=1",
         "--wrap=none", "--metadata", "title=FORMLÆRE"],
        input=source, text=True, capture_output=True, check=True,
    )
    if process.stderr.strip():
        raise ValueError(process.stderr)
    body = process.stdout
    if not body or body.count("<math") < 35 or "<merror" in body:
        raise ValueError("The short edition lost its mathematical expressions.")
    body = re.sub(
        r'(<math\b[^>]*\bdisplay="block"[^>]*>[\s\S]*?</math>)',
        r'<div class="math-scroll" tabindex="0" role="region" aria-label="Matematisk uttrykk">\1</div>',
        body,
    )
    target = root / "nettstad" / "kortversjon.html"
    stamp = "<!-- form-source: " + short_source_hash(root) + " -->\n"
    target.write_text(head + stamp + body + foot, encoding="utf-8")
    print(f"Native MathML expressions: {body.count('<math')}; output: {target}")


if __name__ == "__main__":
    render_short()
