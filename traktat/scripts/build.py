#!/usr/bin/env python3
"""Build web, portable LaTeX and the print PDF from one validated document."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from content import load_document, input_manifest

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
PDF = ROOT / "pdf"
DIST = ROOT / "nettstad" / "dist"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def document() -> dict:
    value = load_document(ROOT)
    write_json(BUILD / "document.json", value)
    return value


def counts(doc: dict) -> dict:
    return {"propositions": len(doc["props"]), "notes": len(doc["notes"]),
            "references": len(doc["sources"]), "figures": len(doc["figures"]),
            "glossary": len(doc.get("glossary", []))}


def verify_pdf(path: Path, doc: dict) -> dict:
    from pypdf import PdfReader
    reader = PdfReader(path)
    if doc["sourceHash"] not in str(reader.metadata.get("/Subject", "")):
        raise ValueError("PDF metadata does not identify the current source")
    destinations = set(reader.named_destinations)
    required = ({prop["n"] for prop in doc["props"]}
                | {"notat-" + note["id"] for note in doc["notes"]}
                | {"referanse-" + str(source["id"]) for source in doc["sources"]}
                | {"ord-" + entry["id"] for entry in doc.get("glossary", [])})
    if required - destinations:
        raise ValueError("PDF destinations missing: " + ", ".join(sorted(required - destinations)))
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    if "\ufffd" in extracted:
        raise ValueError("PDF contains replacement characters")
    return {"pages": len(reader.pages), "destinations": len(required), **counts(doc)}


def build_pdf(doc: dict) -> None:
    work = BUILD / "latex"
    work.mkdir(parents=True, exist_ok=True)
    images = work / "illustrations"
    images.mkdir(exist_ok=True)
    for figure in doc["figures"]:
        shutil.copyfile(ROOT / "nettstad" / "illustrations" / figure["file"], images / figure["file"])
    subprocess.run(["python3", str(ROOT / "scripts" / "render_latex.py"),
                    "--document", str(BUILD / "document.json"), "--output", str(work / "formlaere.tex")], check=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH="946684800", FORCE_SOURCE_DATE="1")
    command = ["xelatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "formlaere.tex"]
    for _ in range(2):
        result = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError("XeLaTeX failed:\n" + result.stdout[-6000:] + result.stderr[-1000:])
    log = (work / "formlaere.log").read_text(errors="replace")
    if "Missing character:" in log or "Overfull \\hbox" in log:
        raise ValueError("PDF has missing glyphs or overflowing lines; inspect build/latex/formlaere.log")
    quality = verify_pdf(work / "formlaere.pdf", doc)
    PDF.mkdir(exist_ok=True)
    staged_pdf = PDF / "formlaere.pdf.tmp"
    shutil.copyfile(work / "formlaere.pdf", staged_pdf)
    staged_pdf.replace(PDF / "formlaere.pdf")
    bundle = PDF / "formlaere-latex.zip"
    with zipfile.ZipFile(bundle.with_suffix(".zip.tmp"), "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [work / "formlaere.tex", *sorted(images.glob("*"))]:
            info = zipfile.ZipInfo(path.relative_to(work).as_posix(), date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    bundle.with_suffix(".zip.tmp").replace(bundle)
    manifest = {"schemaVersion": 1, "sourceHash": doc["sourceHash"], "inputs": input_manifest(ROOT),
                "outputs": {"formlaere.pdf": digest(PDF / "formlaere.pdf"), "formlaere-latex.zip": digest(bundle)},
                "quality": quality, "engine": "XeLaTeX"}
    write_json(PDF / "release.json", manifest)
    print(json.dumps({"pdf": str(PDF / "formlaere.pdf"), **quality, "sourceHash": doc["sourceHash"]}, ensure_ascii=False))


def require_fresh_pdf(doc: dict) -> dict:
    path = PDF / "release.json"
    if not path.is_file():
        raise ValueError("Print release is missing. Run make all before publishing.")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("sourceHash") != doc["sourceHash"]:
        raise ValueError("Print release is stale. Run make all; never publish a PDF from another source.")
    if set(manifest.get("outputs", {})) != {"formlaere.pdf", "formlaere-latex.zip"}:
        raise ValueError("Print release must contain the PDF and portable LaTeX bundle")
    for filename, expected in manifest["outputs"].items():
        asset = PDF / filename
        if not asset.is_file() or digest(asset) != expected:
            raise ValueError("Print output is missing or modified: " + filename)
    if {key: manifest["quality"][key] for key in counts(doc)} != counts(doc):
        raise ValueError("Print and web content counts differ")
    return manifest


def build_web(doc: dict) -> None:
    manifest = require_fresh_pdf(doc)
    stage = Path(tempfile.mkdtemp(prefix="web-", dir=BUILD))
    try:
        template = (ROOT / "nettstad" / "reader.html").read_text(encoding="utf-8")
        if template.count("@@SOURCE_HASH@@") != 1:
            raise ValueError("Reader source-hash placeholder is missing or duplicated")
        (stage / "index.html").write_text(template.replace("@@SOURCE_HASH@@", doc["sourceHash"]), encoding="utf-8")
        for name in ("reader.css", "reader.js"):
            shutil.copyfile(ROOT / "nettstad" / name, stage / name)
        data = stage / "traktat"
        data.mkdir()
        write_json(data / "document.json", doc)
        shutil.copyfile(ROOT / "tekst" / "formlaere.txt", data / "formlaere.txt")
        images = data / "illustrations"
        images.mkdir()
        for figure in doc["figures"]:
            shutil.copyfile(ROOT / "nettstad" / "illustrations" / figure["file"], images / figure["file"])
        for filename in manifest["outputs"]:
            shutil.copyfile(PDF / filename, data / filename)
        pwa = ROOT / "nettstad" / "pwa"
        shutil.copyfile(pwa / "manifest.webmanifest", stage / "manifest.webmanifest")
        (stage / "icons").mkdir()
        for icon in pwa.glob("*.png"):
            shutil.copyfile(icon, stage / "icons" / icon.name)
        # Plain static previews preserve legacy paths too. Production redirects are declared below.
        legacy = '<!doctype html><meta charset="utf-8"><script>location.replace("/"+location.search+location.hash)</script><a href="/">FORMLÆRE</a>'
        (stage / "les").mkdir()
        (stage / "les" / "index.html").write_text(legacy)
        for name in ("index.html", "scroll.html"):
            (data / name).write_text(legacy)
        precache = ["/", "/reader.css", "/reader.js", "/manifest.webmanifest", "/traktat/document.json",
                    "/traktat/formlaere.pdf", *["/icons/" + p.name for p in sorted((stage / "icons").glob("*.png"))],
                    *["/traktat/illustrations/" + figure["file"] for figure in doc["figures"]]]
        worker = (pwa / "service-worker.template.js").read_text(encoding="utf-8")
        worker = worker.replace("__SOURCE_HASH__", doc["sourceHash"]).replace("__PRECACHE_ASSETS__", json.dumps(precache))
        (stage / "service-worker.js").write_text(worker, encoding="utf-8")
        files = {p.relative_to(stage).as_posix(): digest(p) for p in sorted(stage.rglob("*")) if p.is_file()}
        write_json(stage / "release.json", {"sourceHash": doc["sourceHash"], "counts": counts(doc), "files": files})
        if DIST.exists():
            shutil.rmtree(DIST)
        stage.replace(DIST)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print(json.dumps({"web": str(DIST), "sourceHash": doc["sourceHash"], **counts(doc)}, ensure_ascii=False))


def check() -> None:
    subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
    subprocess.run(["node", "--check", "nettstad/reader.js"], cwd=ROOT, check=True)
    subprocess.run(["node", "--test", "tests/test_service_worker.mjs", "tests/test_reader.mjs"], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("all", "check", "pdf", "web", "check-generated", "clean"), default="all", nargs="?")
    args = parser.parse_args()
    if args.target == "clean":
        shutil.rmtree(BUILD, ignore_errors=True)
        shutil.rmtree(DIST, ignore_errors=True)
        return
    if args.target == "check":
        check()
        document()
        return
    if args.target == "all":
        check()
    doc = document()
    if args.target in {"all", "pdf"}:
        build_pdf(doc)
    if args.target in {"all", "web"}:
        build_web(doc)
    if args.target == "check-generated":
        require_fresh_pdf(doc)
        print("Print release matches current source, layout and builder.")


if __name__ == "__main__":
    main()
