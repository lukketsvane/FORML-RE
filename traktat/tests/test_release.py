"""A release must fail closed when source or committed print files drift."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
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
                         "notes": [], "sources": [{"id": "1"}], "figures": []}
        # These specimens test release identity, not PDF rendering. The real
        # release renderer separately checks PDF destinations and glyphs.
        assets = {"formlaere.pdf": b"committed PDF specimen", "formlaere-latex.zip": b"committed TeX specimen"}
        for name, data in assets.items():
            (self.pdf / name).write_bytes(data)
        self.manifest = {"sourceHash": "current-source",
                         "outputs": {name: hashlib.sha256(data).hexdigest() for name, data in assets.items()},
                         "quality": {"propositions": 1, "notes": 0, "references": 1, "figures": 0}}
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


if __name__ == "__main__":
    unittest.main()
