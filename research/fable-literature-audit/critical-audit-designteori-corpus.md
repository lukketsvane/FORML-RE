# Critical audit of the existing designteori corpus

## Scope

This is a methodological review of the repository's published corpus description,
full-text study and analysis script. It is not a re-analysis of the 1,461 PDFs.
The reported figures below are therefore treated as the repository's reported
outputs, not independently verified empirical facts.

Primary materials:
- `lukketsvane/designteori/gransking/README.md`
- `lukketsvane/designteori/gransking/artikkel.md`
- `lukketsvane/designteori/gransking/data/resultatsamandrag.json`
- `lukketsvane/designteori/gransking/analyse_korpus.py`
- `lukketsvane/designteori/designteori/fulltext.py`
- `lukketsvane/designteori/pdf/manifest.json`

## What is genuinely valuable

The corpus is an unusually useful research infrastructure: it separates a
Nordic work-level frame from a citation graph, indexes a sizeable OA full-text
subset, records PDF hashes and supports page-level extraction. Its report is
also explicit about several limits: the full-text subset is not the whole
population; references are not equivalent to replication; and keyword signals
are not the same thing as a validated codebook.

The current catalogue reports 6,454 works, 1,477 catalogue PDFs and 1,461
full texts extracted into 28,955 pages / 12,431,220 words. Those values should
be versioned with the manifest and extraction date whenever reused.

## Core correction: absence of a string is not absence of a practice

The analysis script searches extracted prose with regular expressions. This
produces high-value *screening indicators*, but a paper can describe a practice
without using the selected vocabulary, and a hit can occur without the practice
being carried out. The direction and magnitude of each error need manual
validation before population-level interpretations.

The most consequential mismatches are:

### P1 — research programme and revision

Reported signals include singleton citations (75.89%) and revision markers in
1.23% of the full-text subset. A singleton citation is not by itself evidence
of weak cumulative knowledge: it depends on corpus boundaries, publication
genres, citation coverage, and the expected distribution of references in a
large heterogeneous field. Revision markers are a narrow lexical proxy; a
paper may correct, qualify or extend an argument without using words such as
“refute” or “falsify”.

**Re-read:** explicit engagement with prior propositions, models, datasets,
methods, replication, correction, criticism, and changes to operational
definitions. Distinguish a citation chain from a chain of evidential
dependence.

### P2 — cumulative knowledge and “semantic amnesia”

The reported 94.13% non-citation rate for later semantically similar pairs
(cosine >= 0.80) is not a direct measure of forgetting. Topic similarity does
not establish that two works address the same claim, use the same unit of
analysis, or compete over the same evidence. Similarity models can also miss
translations, indirect references, book chapters and older or poorly indexed
works.

**Re-read:** identify the actual shared question, construct, population, method
and outcome in each candidate pair. Record whether the later work cites the
earlier one directly, indirectly, through a review, or not at all. Only label
a pair as a plausible missed lineage after human inspection of both works.

### P3 — falsifiability and formal hypotheses

The formal-hypothesis detector looks for forms such as H0/H1, “null hypothesis”,
“testable prediction” and “falsifiable hypothesis”. These are not necessary
conditions for disciplined inquiry. Historical, interpretive, constructive,
practice-led and qualitative design research can be systematic and corrigible
without a formal null-hypothesis test.

**Re-read:** code the kind of claim (descriptive, interpretive, causal,
generative, normative, formal); identify what would count as a counterexample;
and ask whether the method could in principle change the author's conclusion.
Distinguish an explicitly empirical effect claim from an aesthetic or
conceptual contribution.

### P4 — disciplinary import and export

Field-level citation categories can reveal where references flow, but
classifications such as HCI, visual arts, engineering and innovation
management overlap with design. A low share of citations from the natural
sciences does not demonstrate low intellectual value or weak export.

**Re-read:** trace specific concepts, methods, instruments and empirical
results that are reused outside the originating venue. Distinguish citation
counts from substantive uptake, and distinguish disciplinary labels from the
actual research question and method.

### P5 — process methods and effect evaluation

The script searches for process methods (workshops, co-design, probes, RtD)
and a restricted set of controlled-effect phrases. This contrasts a broad
family of qualitative and generative methods with a narrow vocabulary of
experimental evaluation. It risks treating different research purposes as
failed versions of a controlled trial.

**Re-read:** first determine the paper's intended knowledge claim. For a causal
or comparative effect claim, inspect the counterfactual, baseline, outcome,
measurement and failure reporting. For a generative or interpretive claim,
inspect traceability, reflexivity, rival interpretations, transfer conditions
and participant accountability instead.

### P6 — post-hoc legitimation of mandates

The mandate detector includes broad phrases such as “public sector”,
“municipality”, “digital transformation”, “sustainability transition” and
“industry partner”. These identify context, not necessarily a pre-decided
mandate. The challenge detector uses a small set of specific phrases, so zero
matches cannot establish that no researcher questioned a mandate.

**Re-read:** distinguish (1) a sponsor or funding relationship, (2) a
pre-existing decision, (3) the researcher's actual discretion, (4) the
possibility of changing or stopping the project, and (5) what the final report
recommended. Do not infer capture or legitimation from context alone.

### P7 — doctoral continuity

Citation databases often under-index theses and their bibliographies. A
doctoral author's absence from one defined corpus after graduation is not
proof of leaving research: they may publish under variant names, in other
fields, books, reports or non-Nordic venues.

**Re-read:** verify author identity cautiously, broaden output types and
repositories, define observation time, and separate research continuity from
formal academic employment.

### P8 — closed publication and peer review

Same-institution citations, author overlap, conference proceedings and
regional venues do not establish peer-review quality or editorial capture.
Some conferences have rigorous external double-blind review; some journals do
not. Citation reciprocity is a network signal, not proof of collusion.

**Re-read:** collect venue-specific review policies, editorial boards,
reviewer independence where public, acceptance/selectivity evidence and
conflicts. Keep these distinct from citation graph measures.

### P9 — research ethics

The reported 91.77% is a rate of *no detected approval wording*, not a
verified rate of absent ethics approval. The search includes broad
participant terms and may miss translated or institution-specific names.
Ethical requirements vary by country, year, study type and whether a work
handles personal or sensitive data. Sikt/NSD, REK and university ethics
committees are not interchangeable bodies.

**Re-read:** classify the participant/data context first; identify the legal
and institutional rule in force at the time; search methods, acknowledgements,
supplementary files and data statements; and use three states: documented,
not found in available text, or verified not required / verified absent.
Never label a paper non-compliant on a keyword miss.

### P10 — measurement and validation

A lack of Cronbach's alpha, SUS, ICC or a named scale is not absence of
rigorous assessment. Qualitative reliability, design critique, ethnographic
validity, triangulation, audit trails, member checking and material testing
may be appropriate depending on the question.

**Re-read:** evaluate the fit between claim and warrant. Code measurement
validity, procedural transparency, inter-coder reliability, triangulation,
replicability, material/performance testing, reflexivity and transferability
as distinct forms rather than one universal psychometric criterion.

## Consequence for FORMLÆRE

The defensible contribution is not “design theory has no theory”. Existing
Nordic work includes substantial traditions in design epistemology,
generative grammar, C–K theory, systems-oriented design, participatory design,
research through design, soma design, design history, aesthetics and
ecological/material design.

The sharper research question is whether and how these traditions can be
compared at the level of:
1. what is treated as a possible form;
2. how alternatives are generated and represented;
3. which constraints and values select among them;
4. what agents know, can attend to and can do;
5. how an artefact or intervention changes its material and social conditions;
6. what kind of evidence can correct the theory;
7. who has standing to contest the declared goal and who bears the consequences.

That is where FORMLÆRE can offer a formal architecture without claiming to
subsume every existing approach. Each tradition must be represented in terms
it would recognise, including real disagreements that cannot be translated
without remainder.

## Priority reading strata

The first 100-paper pilot should be stratified, not simply the most cited:
- 20 foundational or theory-building works (design theory, design epistemology,
  form/function, generative systems);
- 20 formal/generative works (shape grammars, C–K, computational design);
- 15 systems, complexity and cybernetics works;
- 15 practice-led / RtD / participatory / co-design works;
- 10 aesthetic, material and historical works;
- 10 ecological, more-than-human and care-oriented works;
- 10 explicitly critical, negative, replication, evaluation or counterexample
  candidates.

Within each stratum, include a mixture of older and recent works, core and
boundary venues, Nordic and international comparison works, and papers that
seem to challenge rather than support FORMLÆRE.

## Minimum standard before revising propositions

No proposition should be rewritten based on a model-generated abstract alone.
A proposed change must include:
- current proposition ID and exact scope;
- at least two independently verified source passages, preferably from
  competing traditions;
- page-specific evidence for and against;
- a note on what the source does *not* establish;
- the smallest textual change that resolves the issue;
- updated citations and a successful full edition build.
