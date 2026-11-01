"""A release must fail closed when source or committed print files drift."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build


class CommittedReleaseGuard(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.pdf = Path(self.temporary.name)
        self.document = {"sourceHash": "current-source", "props": [{"n": "1"}],
                         "notes": [], "sources": [{"id": "1"}], "figures": [], "glossary": []}
        # These specimens test release identity, not PDF rendering. The real
        # release renderer separately checks PDF destinations and glyphs.
        assets = {"formlaere.pdf": b"committed PDF specimen", "formlaere-latex.zip": b"committed TeX specimen"}
        for name, data in assets.items():
            (self.pdf / name).write_bytes(data)
        self.manifest = {"sourceHash": "current-source",
                         "outputs": {name: hashlib.sha256(data).hexdigest() for name, data in assets.items()},
                         "quality": {"propositions": 1, "notes": 0, "references": 1, "figures": 0, "glossary": 0}}
        self.write_manifest()
        self.patcher = patch.object(build, "PDF", self.pdf)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def write_manifest(self):
        (self.pdf / "release.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_current_complete_release_is_accepted(self):
        self.assertEqual(build.require_fresh_pdf(self.document), self.manifest)

    def test_changed_source_cannot_publish_the_old_pdf(self):
        changed = deepcopy(self.document)
        changed["sourceHash"] = "edited-source"
        with self.assertRaisesRegex(ValueError, "stale"):
            build.require_fresh_pdf(changed)

    def test_replaced_pdf_is_rejected_even_with_a_current_source_hash(self):
        (self.pdf / "formlaere.pdf").write_bytes(b"different PDF")
        with self.assertRaisesRegex(ValueError, "modified"):
            build.require_fresh_pdf(self.document)

    def test_missing_portable_bundle_is_rejected(self):
        (self.pdf / "formlaere-latex.zip").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            build.require_fresh_pdf(self.document)

    def test_truncated_empty_output_manifest_is_rejected(self):
        self.manifest["outputs"] = {}
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "must contain the PDF and portable LaTeX bundle"):
            build.require_fresh_pdf(self.document)

    def test_disagreeing_content_counts_are_rejected(self):
        self.manifest["quality"]["notes"] = 1
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "counts differ"):
            build.require_fresh_pdf(self.document)

    def test_changed_glossary_cannot_reuse_an_edition_without_it(self):
        self.document["glossary"] = [{"id": "form", "term": "Form"}]
        with self.assertRaisesRegex(ValueError, "counts differ"):
            build.require_fresh_pdf(self.document)

    def install_mathematics(self):
        key = "a" * 24
        self.document["mathematics"] = {key: {"tex": "a", "display": False}}
        self.manifest["mathematics"] = {key: {"tex": "a", "display": False,
            "mathml": '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi></math>'}}
        self.write_bound_cache()
        return key

    def write_bound_cache(self, payload=None, name="mathematics.json"):
        bundle = self.pdf / "formlaere-latex.zip"
        with zipfile.ZipFile(bundle, "w") as archive:
            archive.writestr(name, json.dumps(self.manifest["mathematics"]) if payload is None else payload)
        self.manifest["outputs"][bundle.name] = hashlib.sha256(bundle.read_bytes()).hexdigest()
        self.write_manifest()

    def test_manifest_mathml_edit_cannot_change_the_website_with_unchanged_print_files(self):
        key = self.install_mathematics()
        before = deepcopy(self.document)
        original_outputs = deepcopy(self.manifest["outputs"])
        self.manifest["mathematics"][key]["mathml"] = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>WRONG</mi></math>'
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "hash-checked LaTeX bundle"):
            build.require_fresh_pdf(self.document)
        self.assertEqual(self.document, before)
        self.assertEqual(self.manifest["outputs"], original_outputs)

    def test_missing_or_invalid_bound_mathml_cache_is_rejected(self):
        self.install_mathematics()
        for name, payload in [("other.json", "{}"), ("mathematics.json", "not JSON"),
                              ("mathematics.json", b"\xff"), ("mathematics.json", "[]")]:
            with self.subTest(name=name, payload=payload):
                self.write_bound_cache(payload, name)
                with self.assertRaisesRegex(ValueError, "mathematics"):
                    build.require_fresh_pdf(self.document)
        bundle = self.pdf / "formlaere-latex.zip"
        bundle.write_bytes(b"Broken ZIP cache")
        self.manifest["outputs"][bundle.name] = hashlib.sha256(bundle.read_bytes()).hexdigest()
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "mathematics cache.*invalid"):
            build.require_fresh_pdf(self.document)

    def test_invalid_later_mathml_does_not_partly_mutate_the_document(self):
        self.install_mathematics()
        key = "b" * 24
        self.document["mathematics"][key] = {"tex": "b", "display": False}
        self.manifest["mathematics"][key] = {"tex": "b", "display": False, "mathml": "<math"}
        self.write_bound_cache()
        before = deepcopy(self.document)
        with self.assertRaisesRegex(ValueError, "Invalid MathML"):
            build.require_fresh_pdf(self.document)
        self.assertEqual(self.document, before)

    def test_web_uses_only_mathml_for_the_current_canonical_tex(self):
        key = self.install_mathematics()
        with patch("subprocess.run", side_effect=AssertionError("Web publication must not need Pandoc")):
            build.require_fresh_pdf(self.document)
        self.assertIn("mathml", self.document["mathematics"][key])
        self.document["mathematics"][key]["tex"] = "b"
        with self.assertRaisesRegex(ValueError, "Stale mathematics"):
            build.require_fresh_pdf(self.document)


if __name__ == "__main__":
    unittest.main()
