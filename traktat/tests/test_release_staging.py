"""Failures and source edits must leave the previous complete release usable."""
from __future__ import annotations

from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
from content import CANONICAL, source_hash


class ReleaseStaging(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.build = self.root / "build"
        self.build.mkdir()
        self.pdf = self.root / "pdf"
        self.pdf.mkdir()
        self.site = self.root / "nettstad"
        self.site.mkdir()
        self.dist = self.site / "dist"
        self.dist.mkdir()
        for name in (*CANONICAL, "vercel.json", "requirements-build.txt"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{"assets": []}' if name == "figurar.json" else "Original source.")
        for name in ("reader.html", "kort.html", "kortversjon.html"):
            (self.site / name).write_text("<!doctype html>@@SOURCE_HASH@@")
        for name in ("reader.css", "reader.js", "kortversjon.css"):
            (self.site / name).write_text("Reader asset.")
        pwa = self.site / "pwa"
        pwa.mkdir()
        (pwa / "manifest.webmanifest").write_text("{}")
        (pwa / "service-worker.template.js").write_text("__SOURCE_HASH__ __PRECACHE_ASSETS__")
        self.doc = {"sourceHash": source_hash(self.root), "props": [{"n": "1"}],
                    "notes": [], "sources": [{"id": "1"}], "figures": [], "glossary": [], "mathematics": {}}
        self.quality = {"pages": 1, "destinations": 1, **build.counts(self.doc)}
        outputs = {"formlaere.pdf": b"Previous PDF.", "formlaere-latex.zip": b"Previous bundle."}
        for name, data in outputs.items():
            (self.pdf / name).write_bytes(data)
        (self.pdf / "release.json").write_text(json.dumps({
            "sourceHash": self.doc["sourceHash"], "quality": self.quality, "mathematics": {},
            "outputs": {name: hashlib.sha256(data).hexdigest() for name, data in outputs.items()},
        }))
        (self.dist / "index.html").write_text("Previous website.")
        self.previous_pdf = self.files(self.pdf)
        self.previous_web = self.files(self.dist)
        stack = ExitStack()
        self.addCleanup(stack.close)
        for name, value in (("ROOT", self.root), ("BUILD", self.build), ("PDF", self.pdf), ("DIST", self.dist)):
            stack.enter_context(patch.object(build, name, value))
        stack.enter_context(patch("latex_source.render_mathml"))
        stack.enter_context(patch.object(build, "verify_pdf", return_value=self.quality))
        stack.enter_context(patch.object(build.subprocess, "run", side_effect=self.compile))

    @staticmethod
    def files(directory):
        return {path.relative_to(directory).as_posix(): path.read_bytes()
                for path in directory.rglob("*") if path.is_file()}

    def compile(self, command, *, cwd=None, **kwargs):
        work = Path(cwd) if cwd else self.build / "latex"
        if command[0] == "python3":
            (work / "formlaere.tex").write_text("Generated LaTeX.")
        else:
            (work / "formlaere.pdf").write_bytes(b"New complete PDF.")
            (work / "formlaere.log").write_text("Clean compilation.")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    def change_source(self):
        (self.root / "tekst/formlaere.tex").write_text("Edited while the edition was building.")

    def test_failed_bundle_preserves_all_previous_print_files(self):
        def fail_bundle(work, figures, bundle):
            bundle.with_suffix(".zip.tmp").write_bytes(b"Partial ZIP.")
            raise OSError("Bundle storage failed")
        with patch.object(build, "package_latex", side_effect=fail_bundle):
            with self.assertRaisesRegex(OSError, "Bundle storage failed"):
                build.build_pdf(self.doc)
        self.assertEqual(self.files(self.pdf), self.previous_pdf)
        self.assertFalse(list(self.build.glob("print-release-*")))

    def test_complete_print_release_replaces_the_old_files_together(self):
        build.build_pdf(self.doc)
        self.assertEqual((self.pdf / "formlaere.pdf").read_bytes(), b"New complete PDF.")
        manifest = json.loads((self.pdf / "release.json").read_text())
        for name, expected in manifest["outputs"].items():
            self.assertEqual(hashlib.sha256((self.pdf / name).read_bytes()).hexdigest(), expected)
        self.assertEqual(build.require_fresh_pdf(self.doc), manifest)
        self.assertFalse(list(self.build.glob("print-release-*")))

    def failed_install(self, destination):
        replace = Path.replace
        def fail_new_stage(path, target):
            if Path(target) == destination:
                if path.parent == self.build and not path.name.endswith("-previous"):
                    raise OSError("Release install failed")
            return replace(path, target)
        return patch.object(Path, "replace", fail_new_stage)

    def test_failed_print_install_restores_previous_release(self):
        with self.failed_install(self.pdf):
            with self.assertRaisesRegex(OSError, "Release install failed"):
                build.build_pdf(self.doc)
        self.assertEqual(self.files(self.pdf), self.previous_pdf)
        self.assertFalse(list(self.build.glob("print-release-*")))

    def test_changed_inputs_before_build_are_rejected_without_touching_output(self):
        self.change_source()
        for operation in (build.build_pdf, build.build_web):
            with self.subTest(operation=operation.__name__):
                with self.assertRaisesRegex(ValueError, "inputs changed"):
                    operation(self.doc)
        self.assertEqual(self.files(self.pdf), self.previous_pdf)
        self.assertEqual(self.files(self.dist), self.previous_web)

    def test_source_edit_during_packaging_cannot_publish_a_mixed_print_edition(self):
        package = build.package_latex
        def edit_after_packaging(*args):
            package(*args)
            self.change_source()
        with patch.object(build, "package_latex", side_effect=edit_after_packaging):
            with self.assertRaisesRegex(ValueError, "inputs changed"):
                build.build_pdf(self.doc)
        self.assertEqual(self.files(self.pdf), self.previous_pdf)

    def test_source_edit_during_web_copy_keeps_previous_website(self):
        copy = build.shutil.copyfile
        def edit_after_copy(source, destination, **kwargs):
            result = copy(source, destination, **kwargs)
            if Path(source) == self.root / "tekst/formlaere.tex":
                self.change_source()
            return result
        with patch.object(build.shutil, "copyfile", side_effect=edit_after_copy):
            with self.assertRaisesRegex(ValueError, "inputs changed"):
                build.build_web(self.doc)
        self.assertEqual(self.files(self.dist), self.previous_web)
        self.assertFalse(list(self.build.glob("web-*")))

    def test_failed_web_install_restores_previous_website(self):
        with self.failed_install(self.dist):
            with self.assertRaisesRegex(OSError, "Release install failed"):
                build.build_web(self.doc)
        self.assertEqual(self.files(self.dist), self.previous_web)
        self.assertFalse(list(self.build.glob("web-*")))

    def test_successful_web_install_replaces_the_previous_website(self):
        build.build_web(self.doc)
        self.assertNotIn("Previous website.", (self.dist / "index.html").read_text())
        self.assertEqual((self.dist / "traktat/formlaere.pdf").read_bytes(), (self.pdf / "formlaere.pdf").read_bytes())
        self.assertEqual((self.dist / "traktat/formlaere.tex").read_bytes(), (self.root / "tekst/formlaere.tex").read_bytes())
        self.assertFalse(list(self.build.glob("web-*")))

    def test_modified_pdf_during_copy_cannot_enter_the_website(self):
        copy = build.shutil.copyfile
        def change_print_before_copy(source, destination, **kwargs):
            if Path(source) == self.pdf / "formlaere.pdf":
                Path(source).write_bytes(b"Changed after release validation.")
            return copy(source, destination, **kwargs)
        with patch.object(build.shutil, "copyfile", side_effect=change_print_before_copy):
            with self.assertRaisesRegex(ValueError, "Print output changed"):
                build.build_web(self.doc)
        self.assertEqual(self.files(self.dist), self.previous_web)


if __name__ == "__main__":
    unittest.main()
