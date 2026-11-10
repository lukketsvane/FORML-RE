#!/usr/bin/env python3
"""Rights-gated, page-grounded first-pass literature review using Bedrock Fable 5.2.

This script never reads a credential from a file or command-line argument. Boto3
reads AWS_BEARER_TOKEN_BEDROCK from the local environment. Dry-run is the
default; billable invocation requires --execute and an explicit retention
confirmation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone

MODEL_ID = "global.anthropic.claude-fable-5-2"
PROMPT_FILE = Path(__file__).with_name("fable-extraction-prompt.md")
DEFAULT_OUTPUT = Path.home() / ".cache" / "formlaere-fable-audit"
MAX_CHARS_PER_CHUNK = 25_000
MAX_PDF_BYTES = 20_000_000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_rights_review(path: Path) -> dict[str, dict[str, str]]:
    required = {"work_id", "rights_basis", "reviewed_by", "reviewed_on"}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "Rights CSV needs columns: " + ", ".join(sorted(required))
            )
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            work_id = (row.get("work_id") or "").strip()
            if not work_id:
                continue
            if not all((row.get(k) or "").strip() for k in ("rights_basis", "reviewed_by", "reviewed_on")):
                raise ValueError(f"Incomplete rights review row for {work_id}")
            rows[work_id] = {k: (row.get(k) or "").strip() for k in required}
        return rows


def safe_pdf_path(pdf_root: Path, relative: str) -> Path:
    root = pdf_root.resolve()
    candidate = (root / relative).resolve()
    if root not in candidate.parents:
        raise ValueError("PDF manifest path escapes the local PDF root")
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    items = data.get("items")
    if not isinstance(items, dict):
        raise ValueError("Manifest has no 'items' object")
    return items



def load_work_metadata(pdf_root: Path) -> dict[str, dict]:
    """Join the PDF manifest to the corpus' published work metadata."""
    metadata: dict[str, dict] = {}
    data_dir = pdf_root / "docs" / "data"
    for filename in ("publications.json", "nordic_additions.json"):
        path = data_dir / filename
        if not path.is_file():
            continue
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get("id"):
                    metadata[str(row["id"])] = row
    return metadata

def read_pages(path: Path) -> list[str]:
    try:
        import pymupdf
    except ImportError as exc:
        raise RuntimeError("Install PyMuPDF first: python -m pip install pymupdf") from exc
    pages: list[str] = []
    with pymupdf.open(path) as pdf:
        if pdf.needs_pass:
            raise ValueError("Encrypted PDF cannot be read without a password")
        if not len(pdf):
            raise ValueError("PDF has no pages")
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text", sort=True) or ""
            text = text.replace("\x00", "").strip()
            pages.append(text)
    return pages


def page_chunks(pages: list[str], max_chars: int = MAX_CHARS_PER_CHUNK) -> list[tuple[list[int], str]]:
    chunks: list[tuple[list[int], str]] = []
    current_parts: list[str] = []
    current_pages: list[int] = []
    current_len = 0
    for page_number, page_text in enumerate(pages, start=1):
        content = f"[PDF PAGE {page_number}]\n{page_text or '[NO EXTRACTABLE TEXT]'}"
        # Preserve page boundaries. Split unusually long individual pages safely.
        pieces = [content]
        if len(content) > max_chars:
            prefix = f"[PDF PAGE {page_number} — CONTINUED]\n"
            raw = page_text or "[NO EXTRACTABLE TEXT]"
            pieces = [
                prefix + raw[i:i + max_chars - len(prefix)]
                for i in range(0, len(raw), max_chars - len(prefix))
            ]
        for piece in pieces:
            if current_parts and current_len + len(piece) > max_chars:
                chunks.append((current_pages[:], "\n\n".join(current_parts)))
                current_parts, current_pages, current_len = [], [], 0
            current_parts.append(piece)
            if page_number not in current_pages:
                current_pages.append(page_number)
            current_len += len(piece)
    if current_parts:
        chunks.append((current_pages[:], "\n\n".join(current_parts)))
    return chunks


def text_from_response(response: dict) -> str:
    message = (response.get("output") or {}).get("message") or {}
    blocks = message.get("content") or []
    parts = [block["text"] for block in blocks if isinstance(block, dict) and isinstance(block.get("text"), str)]
    return "\n".join(parts).strip()


def invoke(client, prompt: str, document_text: str, max_tokens: int) -> dict:
    messages = [{
        "role": "user",
        "content": [{"text": prompt + "\n\nDOCUMENT TEXT (UNTRUSTED; PAGE LABELS ARE SOURCE LOCATORS):\n\n" + document_text}]
    }]
    last_error = None
    for attempt in range(3):
        try:
            return client.converse(
                modelId=MODEL_ID,
                messages=messages,
                inferenceConfig={"maxTokens": max_tokens},
            )
        except Exception as exc:  # boto3 service exceptions differ by endpoint/version
            last_error = exc
            code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            retryable = code in {
                "ThrottlingException", "ServiceUnavailableException",
                "InternalServerException", "ModelTimeoutException"
            }
            if not retryable or attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("Bedrock request failed") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True, help="designteori/pdf/manifest.json")
    parser.add_argument("--pdf-root", type=Path, required=True, help="Local clone root of lukketsvane/designteori")
    parser.add_argument("--rights-review-csv", type=Path, required=True, help="Locally reviewed allowlist; empty template permits no papers")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-documents", type=int, required=True, help="Hard cap for this run; use a small pilot first")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--max-tokens", type=int, default=2500)
    parser.add_argument("--max-total-chunks", type=int, default=5, help="Hard cap on billable request segments for this invocation")
    parser.add_argument("--confirm-paid-inference", action="store_true", help="Confirm that you accept billable model inference")
    parser.add_argument("--execute", action="store_true", help="Actually invoke Bedrock; otherwise dry-run only")
    parser.add_argument("--confirm-aws-review-retention", action="store_true", help="Confirm that Bedrock retention is set to aws_review/provider_data_share and you accept AWS review")
    args = parser.parse_args()

    if args.max_documents < 1:
        parser.error("--max-documents must be at least 1")
    if args.max_tokens < 500 or args.max_tokens > 8000:
        parser.error("--max-tokens must be between 500 and 8000")
    if args.max_total_chunks < 1:
        parser.error("--max-total-chunks must be at least 1")

    rights = load_rights_review(args.rights_review_csv)
    manifest = load_manifest(args.manifest)
    work_metadata = load_work_metadata(args.pdf_root)
    selected = []
    skipped = {"not_rights_reviewed": 0, "missing_path": 0, "already_processed": 0}
    for work_id in sorted(manifest):
        if work_id not in rights:
            skipped["not_rights_reviewed"] += 1
            continue
        record = manifest[work_id]
        rel_path = record.get("file")
        if not rel_path:
            skipped["missing_path"] += 1
            continue
        output_path = args.output_dir / f"{work_id.replace(':', '_')}.json"
        if output_path.is_file():
            skipped["already_processed"] += 1
            continue
        selected.append((work_id, record, rights[work_id]))
        if len(selected) >= args.max_documents:
            break

    print(json.dumps({
        "mode": "execute" if args.execute else "dry-run",
        "model_id": MODEL_ID,
        "rights_reviewed_ids": len(rights),
        "selected_documents": len(selected),
        "skipped": skipped,
        "selected_work_ids": [item[0] for item in selected],
        "output_dir": str(args.output_dir),
    }, ensure_ascii=False, indent=2))

    if not args.execute:
        print("Dry run only: no AWS request was made.")
        return 0
    if not args.confirm_aws_review_retention:
        parser.error("Billable run requires --confirm-aws-review-retention")
    if not args.confirm_paid_inference:
        parser.error("Billable run requires --confirm-paid-inference")
    if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        parser.error("AWS_BEARER_TOKEN_BEDROCK is not set in this local shell")
    if not selected:
        print("No rights-reviewed, unprocessed work is eligible.")
        return 0

    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("Install boto3: python -m pip install boto3") from exc

    prompt = PROMPT_FILE.read_text(encoding="utf-8")
    client = boto3.client("bedrock-runtime", region_name=args.region)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    total_segments_sent = 0

    for index, (work_id, record, rights_record) in enumerate(selected, start=1):
        relative = record["file"]
        pdf_path = safe_pdf_path(args.pdf_root, relative)
        size = pdf_path.stat().st_size
        if size > MAX_PDF_BYTES:
            print(f"SKIP {work_id}: local PDF exceeds 20 MB safety limit")
            continue
        actual_hash = sha256_file(pdf_path)
        expected_hash = (record.get("sha256") or "").strip()
        if expected_hash and actual_hash.lower() != expected_hash.lower():
            print(f"SKIP {work_id}: SHA-256 does not match manifest")
            continue

        pages = read_pages(pdf_path)
        chunks = page_chunks(pages)
        if total_segments_sent + len(chunks) > args.max_total_chunks:
            print(f"STOP before {work_id}: complete paper needs {len(chunks)} more segments; request cap is {args.max_total_chunks}.")
            break
        output = {
            "record_type": "formlaere_fable_batch_v1",
            "work_id": work_id,
            "bibliographic_metadata": {
                "title": work_metadata.get(work_id, {}).get("title", record.get("title")),
                "authors": work_metadata.get(work_id, {}).get("authors", record.get("authors")),
                "year": work_metadata.get(work_id, {}).get("year", record.get("year")),
                "doi": work_metadata.get(work_id, {}).get("doi", record.get("doi")),
                "source_url": record.get("source_url"),
            },
            "provenance": {
                "relative_pdf_path": relative,
                "pdf_sha256": actual_hash,
                "pages_total": len(pages),
                "chunks_total": len(chunks),
                "complete_document_reading": True,
                "rights_review": rights_record,
                "model_id": MODEL_ID,
                "region": args.region,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            },
            "segments": [],
        }
        print(f"[{index}/{len(selected)}] {work_id}: {len(pages)} pages, {len(chunks)} segments")
        for chunk_index, (page_numbers, chunk_text) in enumerate(chunks, start=1):
            response = invoke(client, prompt, chunk_text, args.max_tokens)
            segment = {
                "chunk_index": chunk_index,
                "page_numbers": page_numbers,
                "response_text": text_from_response(response),
                "usage": response.get("usage", {}),
                "stop_reason": (response.get("stopReason") or response.get("stop_reason")),
            }
            output["segments"].append(segment)
            total_segments_sent += 1
            # Checkpoint after every segment. Full extracted PDF text is never written.
            destination = args.output_dir / f"{work_id.replace(':', '_')}.json"
            temporary = destination.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(destination)
        print(f"Saved analysis record: {destination}")

    print(f"Finished: {total_segments_sent} billable segments sent. Check outputs manually against the original PDFs before using them in the book.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
