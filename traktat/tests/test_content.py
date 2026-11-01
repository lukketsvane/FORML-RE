"""Migration and shared-build invariants; no renderer implementation snapshots."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from content import CITE, NOTE, load_document, parse_source, source_hash, validate_document
from migrate_published import migrate, migrate_text, utf16_index


def historical_fixture(root: Path) -> None:
    """An immutable migration specimen, independent of future author edits."""
    shutil.copy2(ROOT / "vercel.json", root / "vercel.json")
    archive = root / "archive" / "2026-11-01"
    archive.mkdir(parents=True)
    original_archive = ROOT / "archive" / "2026-11-01"
    for name in ("formlaere.txt", "citations.json", "kjelder.json", "placements.json"):
        shutil.copy2(original_archive / name, archive / name)
    assets = root / "nettstad" / "illustrations"
    assets.mkdir(parents=True)
    for item in json.loads((archive / "placements.json").read_text())["assets"]:
        # These tests validate source/target/hash semantics, not image decoding.
        # Real image rendering is checked by the release renderer.
        (assets / item["file"]).write_bytes(b"migration fixture asset")
    migrate(root)


class PublishedMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = ROOT / "archive" / "2026-11-01"
        cls.original = (cls.archive / "formlaere.txt").read_text(encoding="utf-8")
        cls.reviewed = json.loads((cls.archive / "citations.json").read_text(encoding="utf-8"))
        cls.temp = tempfile.TemporaryDirectory()
        cls.fixture_root = Path(cls.temp.name)
        historical_fixture(cls.fixture_root)
        cls.canonical = (cls.fixture_root / "tekst" / "formlaere.txt").read_text(encoding="utf-8")
        cls.doc = load_document(cls.fixture_root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_exact_non_citation_prose_statuses_and_addresses_are_preserved(self):
        migrated = migrate_text(self.original, self.reviewed)
        # The only additional metadata is explicit placement for the one note
        # already displayed in the published introduction.
        self.assertEqual(NOTE.sub("", self.canonical), migrated)
        expected_visible = self.original
        for entry in self.reviewed["entries"]:
            paragraph = entry["paragraph"]
            without_sources = paragraph
            for span in reversed(entry["spans"]):
                start = utf16_index(paragraph, span["start"])
                end = utf16_index(paragraph, span["end"])
                without_sources = without_sources[:start] + without_sources[end:]
            expected_visible = expected_visible.replace(paragraph, without_sources, 1)
        self.assertEqual(CITE.sub("", NOTE.sub("", self.canonical)), expected_visible)
        old_tokens, old_props = parse_source(self.original)
        new_tokens, new_props = parse_source(self.canonical)
        self.assertEqual([(p["n"], p["status"]) for p in old_props], [(p["n"], p["status"]) for p in new_props])
        self.assertEqual(len(old_props), 375)
        self.assertEqual(len(new_props), 375)
        self.assertEqual([t["kind"] for t in old_tokens], [t["kind"] for t in new_tokens])

    def test_all_reviewed_citations_migrated_once_and_math_survives(self):
        expected = sum(len(entry["spans"]) for entry in self.reviewed["entries"])
        self.assertEqual(expected, 69)
        self.assertEqual(len(CITE.findall(self.canonical)), expected)
        self.assertIn("10⁷", self.canonical)
        self.assertIn("Z⁻¹", self.canonical)
        for entry in self.reviewed["entries"]:
            for span in entry["spans"]:
                self.assertTrue(set(span["sourceIds"]) <= {source["id"] for source in self.doc["sources"]})

    def test_complete_published_notes_and_figures(self):
        self.assertEqual((len(self.doc["props"]), len(self.doc["notes"]), len(self.doc["sources"]), len(self.doc["figures"])), (375, 41, 108, 6))
        self.assertEqual(sum(note["section"] == "foreword" for note in self.doc["notes"]), 1)
        self.assertEqual(len(NOTE.findall(self.canonical)), 1)
        self.assertNotIn("108", {source["id"] for source in self.doc["sources"]})
        self.assertEqual(next(figure["file"] for figure in self.doc["figures"] if figure["after"] == "6.66"), "model-overview-20261101.jpg")

    def test_migration_rejects_changed_reviewed_span(self):
        review = deepcopy(self.reviewed)
        review["entries"][0]["spans"][0]["text"] = "not the source mark"
        with self.assertRaisesRegex(ValueError, "span"):
            migrate_text(self.original, review)


class SharedSourceValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        historical_fixture(self.root)
        self.doc = load_document(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def write_source(self, text):
        (self.root / "tekst" / "formlaere.txt").write_text(text, encoding="utf-8")

    def test_unknown_citation_fails_instead_of_silent_missing_link(self):
        text = (self.root / "tekst" / "formlaere.txt").read_text()
        self.write_source(text.replace("[[kjelde:15]]", "[[kjelde:9999]]", 1))
        with self.assertRaisesRegex(ValueError, "Unknown cited"):
            load_document(self.root)

    def test_malformed_citation_is_rejected(self):
        text = (self.root / "tekst" / "formlaere.txt").read_text()
        self.write_source(text.replace("[[kjelde:15]]", "[[kjelde:1, 5]]", 1))
        with self.assertRaisesRegex(ValueError, "malformed"):
            load_document(self.root)

    def test_unknown_note_marker_is_rejected(self):
        text = (self.root / "tekst" / "formlaere.txt").read_text()
        self.write_source(text.replace("[[notat:intro-1]]", "[[notat:missing]]", 1))
        with self.assertRaisesRegex(ValueError, "Unknown note"):
            load_document(self.root)

    def test_duplicate_and_unordered_propositions_are_rejected(self):
        doc = deepcopy(self.doc)
        doc["props"][1]["n"] = "1"
        for token in doc["tokens"]:
            if token.get("n") == "1.01":
                token["n"] = "1"
        with self.assertRaisesRegex(ValueError, "Duplicate proposition"):
            validate_document(doc, self.root)
        doc = deepcopy(self.doc)
        doc["props"][1], doc["props"][2] = doc["props"][2], doc["props"][1]
        with self.assertRaisesRegex(ValueError, "order"):
            validate_document(doc, self.root)

    def test_missing_asset_stops_build(self):
        (self.root / "nettstad" / "illustrations" / self.doc["figures"][0]["file"]).unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            load_document(self.root)

    def test_unknown_note_target_and_duplicate_source_are_rejected(self):
        doc = deepcopy(self.doc)
        doc["notes"][1]["proposition"] = "99.9"
        with self.assertRaisesRegex(ValueError, "target"):
            validate_document(doc, self.root)
        doc = deepcopy(self.doc)
        doc["sources"].append(deepcopy(doc["sources"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate source"):
            validate_document(doc, self.root)

    def test_section_note_cannot_move_to_reading_code(self):
        text = (self.root / "tekst" / "formlaere.txt").read_text()
        self.write_source(text.replace("[[notat:intro-1]]", "", 1).replace("## Lesekode", "## Lesekode\nFlytta note.[[notat:intro-1]]\n", 1))
        with self.assertRaisesRegex(ValueError, "outside its target"):
            load_document(self.root)

    def test_hash_is_deterministic_and_changes_with_text_asset_and_layout(self):
        initial = source_hash(self.root)
        self.assertEqual(initial, source_hash(self.root))
        source = self.root / "tekst" / "formlaere.txt"
        source.write_text(source.read_text() + "\n")
        changed_text = source_hash(self.root)
        self.assertNotEqual(initial, changed_text)
        image = self.root / "nettstad" / "illustrations" / self.doc["figures"][0]["file"]
        image.write_bytes(image.read_bytes() + b"test")
        changed_asset = source_hash(self.root)
        self.assertNotEqual(changed_text, changed_asset)
        stylesheet = self.root / "nettstad" / "reader.css"
        stylesheet.write_text("html{color:black}")
        self.assertNotEqual(changed_asset, source_hash(self.root))

    def test_runtime_count_is_not_hardcoded_to_migration_count(self):
        # An added, correctly ordered, uncited proposition is valid without
        # changing generator constants or edition metadata.
        source = self.root / "tekst" / "formlaere.txt"
        source.write_text(source.read_text() + "\n**8d**  Ei ny utsegn.\n")
        document = load_document(self.root)
        self.assertEqual(len(document["props"]), 376)


if __name__ == "__main__":
    unittest.main()
