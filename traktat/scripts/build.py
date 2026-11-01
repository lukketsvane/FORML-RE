#!/usr/bin/env python3
"""Build web, portable LaTeX and the print PDF from one validated document."""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from content import load_document, input_manifest, manifest_hash
from render_latex import print_figure_path

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


def require_current_source(doc: dict) -> dict[str, str]:
    """Reject a document snapshot if any canonical build input has changed."""
    inputs = input_manifest(ROOT)
    if manifest_hash(inputs) != doc["sourceHash"]:
        raise ValueError("Build inputs changed during the build. Reload the source and run make all.")
    return inputs


def publish_directory(stage: Path, destination: Path) -> None:
    """Install a complete staged release, restoring its predecessor on failure."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    previous = stage.with_name(stage.name + "-previous")
    if previous.exists():
        raise FileExistsError("Release backup already exists: " + str(previous))
    had_previous = destination.exists()
    if had_previous:
        destination.replace(previous)
    try:
        stage.replace(destination)
    except BaseException:
        if had_previous:
            previous.replace(destination)
        raise
    else:
        if had_previous:
            shutil.rmtree(previous, ignore_errors=True)


def document() -> dict:
    from render_kortversjon import require_fresh_short
    require_fresh_short(ROOT)
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
                | {"referanse-" + str(alias) for alias in doc.get("sourceAliases", {})}
                | {"ord-" + entry["id"] for entry in doc.get("glossary", [])})
    if required - destinations:
        raise ValueError("PDF destinations missing: " + ", ".join(sorted(required - destinations)))
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    if "\ufffd" in extracted:
        raise ValueError("PDF contains replacement characters")
    return {"pages": len(reader.pages), "destinations": len(required), **counts(doc)}


def convert_svg(source: Path, destination: Path) -> None:
    """Keep the drawing vector-based and remove converter clock metadata."""
    import cairosvg
    from pypdf import PdfReader, PdfWriter

    converted = cairosvg.svg2pdf(url=str(source), unsafe=False)
    reader = PdfReader(BytesIO(converted))
    if len(reader.pages) != 1 or any(float(edge) <= 0 for edge in
                                     (reader.pages[0].mediabox.width, reader.pages[0].mediabox.height)):
        raise ValueError("SVG did not produce one nonempty PDF page: " + source.name)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.add_metadata({"/Producer": "CairoSVG " + cairosvg.__version__,
                         "/CreationDate": "D:20000101000000Z", "/ModDate": "D:20000101000000Z"})
    writer.write(destination)


def prepare_print_figures(doc: dict, work: Path) -> list[Path]:
    """Rebuild only active print assets, excluding retired or stale figures."""
    images = work / "illustrations"
    if images.exists():
        shutil.rmtree(images)
    images.mkdir(parents=True)
    prepared = {}
    for figure in doc["figures"]:
        source = ROOT / "nettstad" / "illustrations" / figure["file"]
        destination = work / print_figure_path(figure["file"])
        if destination in prepared:
            raise ValueError("Conflicting print figure filename: " + destination.name)
        if source.suffix.lower() == ".svg":
            convert_svg(source, destination)
        else:
            shutil.copyfile(source, destination)
        prepared[destination] = source
    return sorted(prepared)


def prepare_print_layout(work: Path) -> list[Path]:
    """Copy the fixed book cover and licensed fonts without host font lookup."""
    prepared = []
    fonts = work / "fonts"
    if fonts.exists():
        shutil.rmtree(fonts)
    source_fonts = ROOT / "layout" / "fonts"
    if source_fonts.is_dir():
        fonts.mkdir()
        for source in sorted(source_fonts.iterdir()):
            if source.is_file():
                destination = fonts / source.name
                shutil.copyfile(source, destination)
                prepared.append(destination)
    cover = ROOT / "layout" / "cover-stolar.png"
    destination = work / cover.name
    if cover.is_file():
        shutil.copyfile(cover, destination)
        prepared.append(destination)
    elif destination.exists():
        destination.unlink()
    return prepared


def package_latex(work: Path, figures: list[Path], bundle: Path, mathematics: dict | None = None) -> None:
    """Include ready-to-use figures, cover and fonts with their licence."""
    with zipfile.ZipFile(bundle.with_suffix(".zip.tmp"), "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [work / "formlaere.tex", *figures]:
            info = zipfile.ZipInfo(path.relative_to(work).as_posix(), date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
        # Carry the editable manuscript and its shared catalogs with the ready-to-compile edition.
        for name in ("tekst/formlaere.tex", "kjelder.json", "ordliste.json", "figurar.json", "edition.json", "layout/authoring.tex"):
            path = ROOT / name
            if path.is_file():
                info = zipfile.ZipInfo("source/" + name, date_time=(2000, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        if mathematics is not None:
            # The ZIP is hash-checked before publication, binding the web's
            # derived MathML cache to this exact portable print release.
            info = zipfile.ZipInfo("mathematics.json", date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (json.dumps(mathematics, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    bundle.with_suffix(".zip.tmp").replace(bundle)


def build_pdf(doc: dict) -> None:
    require_current_source(doc)
    from latex_source import render_mathml
    render_mathml(doc.get("mathematics", {}))
    write_json(BUILD / "document.json", doc)
    work = BUILD / "latex"
    work.mkdir(parents=True, exist_ok=True)
    figures = prepare_print_figures(doc, work)
    layout_assets = prepare_print_layout(work)
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
    stage = Path(tempfile.mkdtemp(prefix="print-release-", dir=BUILD))
    try:
        shutil.copyfile(work / "formlaere.pdf", stage / "formlaere.pdf")
        bundle = stage / "formlaere-latex.zip"
        package_latex(work, figures + layout_assets, bundle, doc.get("mathematics", {}))
        inputs = require_current_source(doc)
        manifest = {"schemaVersion": 1, "sourceHash": doc["sourceHash"], "inputs": inputs,
                    "outputs": {"formlaere.pdf": digest(stage / "formlaere.pdf"), "formlaere-latex.zip": digest(bundle)},
                    "quality": quality, "engine": "XeLaTeX", "mathematics": doc.get("mathematics", {})}
        write_json(stage / "release.json", manifest)
        require_current_source(doc)
        publish_directory(stage, PDF)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
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
    if "mathematics" in doc:
        from latex_source import validate_mathml
        cached = manifest.get("mathematics", {})
        expected = doc["mathematics"]
        if not isinstance(cached, dict) or set(cached) != set(expected):
            raise ValueError("Print release mathematics differ from the LaTeX manuscript")
        if expected:
            try:
                with zipfile.ZipFile(PDF / "formlaere-latex.zip") as archive:
                    if archive.namelist().count("mathematics.json") != 1:
                        raise ValueError("Portable LaTeX mathematics cache is missing or duplicated")
                    bound_cache = json.loads(archive.read("mathematics.json"))
            except (OSError, zipfile.BadZipFile, KeyError, UnicodeError, json.JSONDecodeError, RuntimeError) as error:
                raise ValueError("Portable LaTeX mathematics cache is missing or invalid") from error
            if not isinstance(bound_cache, dict) or bound_cache != cached:
                raise ValueError("Print release mathematics differ from the hash-checked LaTeX bundle")
        validated = {}
        for key, expression in expected.items():
            saved = cached[key]
            if not isinstance(saved, dict) or any(saved.get(field) != expression[field] for field in ("tex", "display")):
                raise ValueError("Stale mathematics in print release: " + key)
            try:
                validated[key] = validate_mathml(saved.get("mathml", ""))
            except (ET.ParseError, TypeError) as error:
                raise ValueError("Invalid MathML in print release: " + key) from error
        # Do not partly update the document when a later expression is invalid.
        for key, markup in validated.items():
            expected[key]["mathml"] = markup
    return manifest


def build_web(doc: dict) -> None:
    require_current_source(doc)
    manifest = require_fresh_pdf(doc)
    write_json(BUILD / "document.json", doc)
    stage = Path(tempfile.mkdtemp(prefix="web-", dir=BUILD))
    try:
        template = (ROOT / "nettstad" / "reader.html").read_text(encoding="utf-8")
        if template.count("@@SOURCE_HASH@@") != 1:
            raise ValueError("Reader source-hash placeholder is missing or duplicated")
        (stage / "index.html").write_text(template.replace("@@SOURCE_HASH@@", doc["sourceHash"]), encoding="utf-8")
        short_template = (ROOT / "nettstad" / "kort.html").read_text(encoding="utf-8")
        if short_template.count("@@SOURCE_HASH@@") != 1:
            raise ValueError("Short reader source-hash placeholder is missing or duplicated")
        (stage / "kort").mkdir()
        (stage / "kort" / "index.html").write_text(short_template.replace("@@SOURCE_HASH@@", doc["sourceHash"]), encoding="utf-8")
        math_template = (ROOT / "nettstad" / "kortversjon.html").read_text(encoding="utf-8")
        if math_template.count("@@SOURCE_HASH@@") != 1:
            raise ValueError("MathML short reader source hash placeholder missing or duplicated")
        (stage / "kortversjon").mkdir()
        (stage / "kortversjon" / "index.html").write_text(math_template.replace("@@SOURCE_HASH@@", doc["sourceHash"]), encoding="utf-8")
        shutil.copyfile(ROOT / "nettstad" / "kortversjon.css", stage / "kortversjon.css")
        for name in ("reader.css", "reader.js"):
            shutil.copyfile(ROOT / "nettstad" / name, stage / name)
        data = stage / "traktat"
        data.mkdir()
        write_json(data / "document.json", doc)
        shutil.copyfile(ROOT / "tekst" / "formlaere.tex", data / "formlaere.tex")
        images = data / "illustrations"
        images.mkdir()
        for figure in doc["figures"]:
            shutil.copyfile(ROOT / "nettstad" / "illustrations" / figure["file"], images / figure["file"])
        for filename, expected in manifest["outputs"].items():
            shutil.copyfile(PDF / filename, data / filename)
            if digest(data / filename) != expected:
                raise ValueError("Print output changed while staging the website: " + filename)
        pwa = ROOT / "nettstad" / "pwa"
        shutil.copyfile(pwa / "manifest.webmanifest", stage / "manifest.webmanifest")
        (stage / "icons").mkdir()
        for icon in pwa.glob("*.png"):
            shutil.copyfile(icon, stage / "icons" / icon.name)
        # Plain static previews preserve legacy paths too. Production redirects are declared below.
        legacy = '<!doctype html><meta charset="utf-8"><script>location.replace("/"+location.search+location.hash)</script><a href="/">formlære</a>'
        (stage / "les").mkdir()
        (stage / "les" / "index.html").write_text(legacy)
        for name in ("index.html", "scroll.html"):
            (data / name).write_text(legacy)
        precache = ["/", "/kort/", "/kortversjon/", "/kortversjon.css", "/reader.css", "/reader.js", "/manifest.webmanifest", "/traktat/document.json",
                    "/traktat/formlaere.pdf", *["/icons/" + p.name for p in sorted((stage / "icons").glob("*.png"))],
                    *["/traktat/illustrations/" + figure["file"] for figure in doc["figures"]]]
        worker = (pwa / "service-worker.template.js").read_text(encoding="utf-8")
        worker = worker.replace("__SOURCE_HASH__", doc["sourceHash"]).replace("__PRECACHE_ASSETS__", json.dumps(precache))
        (stage / "service-worker.js").write_text(worker, encoding="utf-8")
        files = {p.relative_to(stage).as_posix(): digest(p) for p in sorted(stage.rglob("*")) if p.is_file()}
        write_json(stage / "release.json", {"sourceHash": doc["sourceHash"], "counts": counts(doc), "files": files})
        require_current_source(doc)
        publish_directory(stage, DIST)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print(json.dumps({"web": str(DIST), "sourceHash": doc["sourceHash"], **counts(doc)}, ensure_ascii=False))


def check() -> None:
    subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
    subprocess.run(["node", "--check", "nettstad/reader.js"], cwd=ROOT, check=True)
    subprocess.run(["node", "--test", "tests/test_service_worker.mjs", "tests/test_reader.mjs", "tests/test_kort.mjs"], cwd=ROOT, check=True)


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
    if args.target in {"all", "pdf"}:
        from render_kortversjon import render_short
        render_short(ROOT)
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
