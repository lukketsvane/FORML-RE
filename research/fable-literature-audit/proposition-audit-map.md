# Proposition-level literature audit map

This map determines what the first literature-reading rounds must test. It is
not a claim that the propositions are already validated. The exact wording and
status must always be taken from `traktat/tekst/formlaere.tex` on the branch
being reviewed.

| FORMLÆRE locus | Theoretical question to test | Comparison families | Evidence needed before changing the text |
| --- | --- | --- | --- |
| 1, 1.02, 1.11–1.212 | Is form adequately defined as an arrangement/structure of differences, and what is held invariant by the chosen abstraction? | Semper and tektonics; morphology; structuralism; Gestalt; relational ontology; shape representation | Distinguish ontological claims from analytic definitions; examples where same silhouette conceals different structure or function |
| 1.3 and 1.4–1.44 | Are the form space, material/historical partition and epistemic partition distinct and non-redundant? | Shape grammars; C–K theory; possibility spaces; affordance theory; modal and design-space accounts | State exactly which partition is material, historical, epistemic or operational; show non-equivalent boundary cases |
| 2.1–2.21 | Are concurrent selection pressures independently identifiable, and when does an aggregate variable hide trade-offs? | Multi-objective optimisation; ecological psychology; pragmatism; value-sensitive design; socio-technical systems | Operational measures independent of the chosen form; at least one case with conflicting pressures and one where the variable is only a proxy |
| 3.01–3.3 | When is a log-additive landscape mathematically justified, and how should interaction terms be represented? | Statistical mechanics; exponential families; Bayesian models; fitness landscapes; multi-criteria decision analysis | Derive factorisation assumptions; counterexamples with non-separable interactions; compare predictive fit out-of-sample |
| 3.4–4.5 | How do realisations change later constraints, opportunities and path dependence? | Evolutionary theory; niche construction; path dependence; technological transitions; material culture | Separate changed possibilities from changed access/knowledge; trace an actual before/after condition rather than infer change from novelty |
| 5.02–5.114 | What makes a system boundary, agent, goal region, policy and tolerance analytically useful? | Cybernetics; Ashby; autopoiesis; active inference; control theory; distributed cognition | Identify observable system, environment, feedback path, perturbation, goal criterion and policy; compare systems with no regulation |
| 5.21–5.234 | Can axis-specific capacity and joint capacity be distinguished under one shared policy and common disturbance conditions? | Robust control; viability theory; multi-objective control; resource-bounded agency | Test whether a policy holds multiple axes simultaneously; do not combine separate best-case policies into one fictitious capacity |
| 5.7–5.72 | Does the proposed kernel describe a local transition mechanism, and under what conditions does it reduce to existing generative or selection models? | Shape grammars; C–K; Markov decision processes; policy selection; stochastic search | Show a complete transition specification, state space, proposal mechanism, acceptance rule and counterexample; do not call the synthesis a source-derived law |
| 6.6–6.641 | Does the maximum-relative-entropy / Gibbs distribution follow from the stated constraints, and do the Markov-chain conditions ensure invariance and convergence? | Jaynes; statistical mechanics; Metropolis–Hastings; MCMC; maximum entropy | Check support, normalisability, detailed balance, irreducibility, aperiodicity, reversibility and proposal support; separate search from irreversible making |
| 6.673–6.674 | Are the covariance identities correctly derived and are the “held fixed” quantities really fixed under changes in precision or weights? | Exponential-family identities; sensitivity analysis; causal inference; precision weighting | Re-derive independently; test with finite differences and synthetic counterexamples; distinguish local derivatives from finite interventions |
| 7.14–7.1521 | Do prediction, goal and holding horizons capture distinct forms of limitation, and is the proposed failure signature observable? | Control theory; bounded rationality; active inference; resilience; human factors | Give operational definitions, observable outcomes, independent measurement of actual consequences and cases that falsify the signature |
| 7.15 and adjacent meta-theory | Does the meta-theorem follow from prior propositions, and can a rival theory provide a counterexample? | Philosophy of science; Lakatos; Popper; design epistemology; theory comparison | Identify premises, derivation and scope; search actively for existing design theories with both generative and competence/knowledge layers |

## Cross-cutting tests

### 1. Do not collapse three distinct spaces

For every paper, record separately:
- **Ontic/material possibility:** what the world and material laws permit.
- **Historical/operational accessibility:** what the current tools, resources and
  processes can realise.
- **Epistemic status:** what agents know, can conceive, have tested or have
  ruled out.

A single word such as “possible” must not be used to slide between these levels.
C–K theory must be reconstructed in its own terms before comparison with
`(K,C,F)`; the mapping is a FORMLÆRE interpretation, not a neutral identity.

### 2. Separate agent estimate, priority, capacity and outcome

For each empirical or formal source, identify:
- what is sensed or estimated;
- what is valued or weighted;
- what policy is available;
- what the system can jointly hold under the same perturbation;
- what actually happens to each affected party.

A good prediction is not a good outcome. A declared value is not a maintained
constraint. A high score on one axis is not evidence of joint capacity.

### 3. Treat the kernel and distribution as different mathematical objects

The core equation at 5.7 is a proposed local transition/behavioural synthesis.
The distribution at 6.6 is a conditional probability model. The transition
kernel, target distribution and irreversible material history must be analysed
separately. A stationary distribution for a search process is not a law of
historical production.

### 4. Require negative and rival cases

The reading queue must deliberately include sources that:
- build rigorous, cumulative design theory;
- use qualitative or practice-led methods with strong validation;
- report failed, negative or null results;
- treat form, agency, materiality or design knowledge in ways incompatible
  with FORMLÆRE;
- identify concepts the formal model cannot yet represent.

The audit succeeds only if it can change or narrow FORMLÆRE, not merely decorate
its existing argument with more citations.

## Proposed first 100-paper sample

Use the strata in `critical-audit-designteori-corpus.md`, with at least 20%
reserved for potential counterexamples or clearly rival conceptual frameworks.
Within every stratum, balance publication periods and venues. The 100-paper
pilot calibrates the extraction protocol; it is not a basis for field-wide
prevalence estimates.

## Acceptance criterion for a proposition revision

A change is eligible for the manuscript only when:
1. two or more independent works have been checked against the actual PDF pages;
2. at least one work offers a serious qualification, challenge or alternative;
3. the exact premise affected is identified;
4. the mathematical derivation is independently checked where relevant;
5. the revised proposition has a clear status (definition, postulate, consequence,
   observation or illustration);
6. references and notes accurately distinguish source result from FORMLÆRE's
   synthesis; and
7. `make all` completes with synchronized PDF and web source hashes.
