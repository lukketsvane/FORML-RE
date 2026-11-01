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
from latex_source import migrate_to_latex
from migrate_published import migrate, migrate_text, utf16_index


def historical_fixture(root: Path) -> None:
    """An immutable migration specimen, independent of future author edits."""
    shutil.copy2(ROOT / "vercel.json", root / "vercel.json")
    shutil.copy2(ROOT / "requirements-build.txt", root / "requirements-build.txt")
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
    legacy = root / "tekst" / "formlaere.txt"
    (root / "tekst" / "formlaere.tex").write_text(migrate_to_latex(legacy.read_text()), encoding="utf-8")
    # The migration specimen predates the editorial glossary. Its independent
    # empty catalog keeps future glossary revisions out of historical tests.
    (root / "ordliste.json").write_text(json.dumps({"schemaVersion": 1, "entries": []}) + "\n", encoding="utf-8")


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
        (self.root / "tekst" / "formlaere.tex").write_text(migrate_to_latex(text), encoding="utf-8")

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
        source = self.root / "tekst" / "formlaere.tex"
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
        self.write_source(source.read_text() + "\n**8d**  Ei ny utsegn.\n")
        document = load_document(self.root)
        self.assertEqual(len(document["props"]), 376)


class GlossaryValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        historical_fixture(self.root)
        self.entries = [{"id": "form", "term": "Form", "definition": "Ei ordning av skilnader.", "propositions": ["1"]},
                        {"id": "formrom", "term": "Formrom", "symbol": "𝕄", "definition": "Mengda av alle moglege konfigurasjonar i ein klasse.", "propositions": ["1.31"]}]
        self.write_glossary()

    def tearDown(self):
        self.temp.cleanup()

    def write_glossary(self):
        (self.root / "ordliste.json").write_text(json.dumps({"schemaVersion": 1, "entries": self.entries}, ensure_ascii=False), encoding="utf-8")

    def test_one_glossary_source_reaches_the_document_and_edition_hash(self):
        before = load_document(self.root)
        self.assertEqual(before["glossary"], self.entries)
        self.entries[0]["definition"] = "Ei ordning av skilnader mellom delar."
        self.write_glossary()
        after = load_document(self.root)
        self.assertEqual(after["glossary"][0]["definition"], self.entries[0]["definition"])
        self.assertEqual(before["props"], after["props"])
        self.assertNotEqual(before["sourceHash"], after["sourceHash"])

    def test_duplicate_or_unstable_glossary_ids_are_rejected(self):
        self.entries[1]["id"] = "form"
        self.write_glossary()
        with self.assertRaisesRegex(ValueError, "Duplicate glossary identifier"):
            load_document(self.root)
        self.entries[1]["id"] = "form rom"
        self.write_glossary()
        with self.assertRaisesRegex(ValueError, "Invalid glossary identifier"):
            load_document(self.root)

    def test_untraceable_or_duplicate_proposition_targets_are_rejected(self):
        for targets in ([], ["99.99"], ["1", "1"]):
            with self.subTest(targets=targets):
                self.entries[0]["propositions"] = targets
                self.write_glossary()
                with self.assertRaisesRegex(ValueError, "glossary proposition target"):
                    load_document(self.root)

    def test_empty_definitions_terms_and_symbols_are_rejected(self):
        for field in ("definition", "term", "symbol"):
            with self.subTest(field=field):
                original = deepcopy(self.entries)
                self.entries[0][field] = " "
                self.write_glossary()
                with self.assertRaisesRegex(ValueError, "Empty glossary " + field):
                    load_document(self.root)
                self.entries = original

    def test_unsupported_glossary_schema_is_rejected(self):
        (self.root / "ordliste.json").write_text(json.dumps({"schemaVersion": 2, "entries": self.entries}))
        with self.assertRaisesRegex(ValueError, "glossary schema"):
            load_document(self.root)

    def test_unknown_or_duplicate_glossary_sources_are_rejected(self):
        for ids, error in [(["9999"], "Unknown"), (["1", "1"], "Duplicate")]:
            with self.subTest(sources=ids):
                self.entries[0]["sources"] = ids
                self.write_glossary()
                with self.assertRaisesRegex(ValueError, error + " glossary source"):
                    load_document(self.root)

    def test_glossary_sources_share_the_existing_bibliography(self):
        self.entries[0]["sources"] = ["1"]
        self.write_glossary()
        doc = load_document(self.root)
        self.assertEqual(doc["glossary"][0]["sources"], ["1"])

    def test_cross_field_context_is_shared_and_validated(self):
        self.entries[0].update(fields=["Biologi", "Reguleringsteknikk"], connection="Teksten samanliknar to faglege bruksmåtar.")
        self.write_glossary()
        doc = load_document(self.root)
        self.assertEqual(doc["glossary"][0]["fields"], self.entries[0]["fields"])
        self.assertEqual(doc["glossary"][0]["connection"], self.entries[0]["connection"])
        for fields in ([], ["Biologi", "Biologi"], [""]):
            self.entries[0]["fields"] = fields
            self.write_glossary()
            with self.assertRaisesRegex(ValueError, "Invalid glossary fields"):
                load_document(self.root)
        self.entries[0]["fields"] = ["Biologi"]
        self.entries[0]["connection"] = " "
        self.write_glossary()
        with self.assertRaisesRegex(ValueError, "Empty glossary connection"):
            load_document(self.root)


class ActiveReferenceIntegrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        historical_fixture(self.root)
        (self.root / "tekst/formlaere.txt").write_text("# FORMLÆRE\n\n## Føreord\n\nFøreord.\n\n## Lesekode\n\nKode.\n\n**1d** Form.[[kjelde:1]]\n", encoding="utf-8")
        (self.root / "tekst/formlaere.tex").write_text(migrate_to_latex((self.root / "tekst/formlaere.txt").read_text()), encoding="utf-8")
        self.catalog = {"sources": [{"id": "1", "citation": "Ei brukt kjelde."}], "notes": [], "aliases": {"9001": "1"}}
        (self.root / "figurar.json").write_text(json.dumps({"assets": []}))
        edition_path = self.root / "edition.json"
        edition = json.loads(edition_path.read_text())
        edition["requireReferencedSources"] = True
        edition_path.write_text(json.dumps(edition))
        self.write_catalog()

    def write_catalog(self):
        (self.root / "kjelder.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    def test_alias_preserves_a_retired_id_without_a_duplicate_entry(self):
        document = load_document(self.root)
        self.assertEqual(document["sourceAliases"], {"9001": "1"})
        self.assertEqual([source["id"] for source in document["sources"]], ["1"])

    def test_alias_must_point_directly_to_an_active_source(self):
        self.catalog["aliases"] = {"9001": "9002"}
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "Invalid source alias"):
            load_document(self.root)

    def test_unused_active_reference_is_rejected(self):
        self.catalog["sources"].append({"id": "2", "citation": "Ei ukopla kjelde."})
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "Unreferenced active sources: 2"):
            load_document(self.root)


if __name__ == "__main__":
    unittest.main()
