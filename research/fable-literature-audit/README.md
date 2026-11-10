# FORMLÆRE — Fable literature audit

Status: research branch; no changes to the published edition.

This workstream uses the separate public corpus repository
[`lukketsvane/designteori`](https://github.com/lukketsvane/designteori) as a
source-discovery and full-text corpus. All changes to the book, its PDF and its
reader remain in [`lukketsvane/FORML-RE`](https://github.com/lukketsvane/FORML-RE).

## Why this audit exists

The corpus repository reports 6,454 Nordic design-research works, 1,477
catalogued PDFs, and a full-text subset of 1,461 PDFs (28,955 pages and
12,431,220 extracted words). These figures describe the repository's current
catalogue and extraction, not a verified census of all design theory.

Its quantitative paper, *Fragmentert ad-hokkrati og epistemisk lukking*,
reports patterns in citations, methods, ethics language and measurement.
Many of those indicators are keyword/regular-expression detections. They are
useful for finding papers and candidate passages, but a missing keyword is not
proof that a method, ethical review, negative result or correction was absent.
The companion critique in this directory identifies where claims need
re-reading and recalibration before they can support FORMLÆRE.

## Research protocol

1. **Inventory and provenance.** Retain the corpus work ID, title, authors,
   year, DOI, repository PDF path, SHA-256, source URL and rights evidence.
2. **Rights gate.** A public PDF URL or an empty licence field is not treated as
   blanket permission. Only process works listed in a locally maintained
   rights-review CSV with an explicit basis for the proposed research use.
3. **Page-grounded reading.** Extract each page with a stable printed/extracted
   page index. Every claim, counterexample and interpretation must point to
   page numbers. Do not store or republish full PDF text.
4. **Structured first-pass analysis.** The model separates empirical,
   interpretive, normative and formal claims; identifies methods and limitations;
   records evidence against as well as in favour of each claim; and maps
   candidate relations to FORMLÆRE propositions without changing them.
5. **Human verification.** A researcher checks each cited passage against the
   PDF, corrects page offsets and independently judges the relation to the
   proposition. Model output is a reading aid, not evidence by itself.
6. **Synthesis.** Only after individual records have been verified may we
   compare traditions, identify repeated problems, propose revisions or add
   bibliography entries.
7. **Edition release.** Changes to the book are made in the canonical LaTeX
   source and shared catalogues. Run `make all` in `traktat/` and commit the
   matching PDF, portable LaTeX bundle and release manifest. Never edit the
   generated PDF or website independently.

## Fable 5.2 invocation and data handling

The batch reader in this directory is a local research utility. It reads
`AWS_BEARER_TOKEN_BEDROCK` from the environment; it never contains or asks for
a key in a prompt, file, command-line argument or Git commit.

**Do not use a credential pasted into chat or any other exposed credential.**
Revoke it and create a fresh, least-privilege credential locally. Fable 5.2
requires the Bedrock retention mode `aws_review`: AWS retains inputs and
outputs inside its boundary for human review. Do not send confidential,
personal, sensitive or unpublished material through this workflow. Keep the
first run small, sequential and rights-cleared. AWS bills model usage; the
script has no price guarantee and must not be treated as a free batch job.

The model identifier defaults to `global.anthropic.claude-fable-5-2`.
Set the account/project retention mode through the AWS Bedrock data-retention
control plane before invocation. The script's explicit confirmation flag is a
second guard, not a substitute for configuring or understanding that setting.

## First run

Clone `lukketsvane/designteori` locally so its PDFs and manifest are available.
Install the local dependencies:

```sh
python -m pip install boto3 pymupdf
```

Create a local rights-review CSV with the columns
`work_id,rights_basis,reviewed_by,reviewed_on`. Add only works for which the
right to process the full text for this research has actually been checked.
Do not commit this file if it contains private notes.

A dry run does not call AWS:

```sh
python batch_reader.py \
  --manifest /path/to/designteori/pdf/manifest.json \
  --pdf-root /path/to/designteori \
  --rights-review-csv /path/to/rights-review.csv \
  --max-documents 3
```

A billable run requires all of the following: a fresh credential in the local
environment, a rights-reviewed work list, a small explicit document limit,
`--execute`, and `--confirm-aws-review-retention`:

```sh
export AWS_BEARER_TOKEN_BEDROCK='set-this-locally; never paste it into chat'
python batch_reader.py \
  --manifest /path/to/designteori/pdf/manifest.json \
  --pdf-root /path/to/designteori \
  --rights-review-csv /path/to/rights-review.csv \
  --max-documents 3 \
  --execute \
  --confirm-aws-review-retention
```

Outputs go to a local cache directory (by default
`~/.cache/formlaere-fable-audit`), not into the public repository. Each
document is split into page-labelled text segments. The script stores the
structured model response, model identifier, PDF hash and token usage; it does
not store the extracted full text in its output records.

## Limits and interpretation

- The current PDF corpus is an availability-selected subset; full-text absence
  is not evidence of non-publication or non-existence.
- OCR quality, layout extraction, tables, diagrams and missing pages must be
  checked. A text-only first pass cannot evaluate visual form or a diagram
  reliably.
- Search terms and embedding similarity are candidate-generation tools, not
  proof of intellectual continuity or discontinuity.
- Do not infer absence of ethics approval, informed consent, preregistration,
  replication, peer review, negative findings or measurement validation from
  absence of a keyword.
- Do not frame FORMLÆRE as the inevitable completion of prior schools. Record
  genuine counterexamples, rival explanations, incompatible premises and
  concepts the tractate cannot absorb without changing its own commitments.
