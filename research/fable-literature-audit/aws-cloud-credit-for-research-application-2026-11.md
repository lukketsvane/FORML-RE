# AWS Cloud Credit for Research — application preparation

**Status:** Prepared for submission; not submitted yet. The official form requires a saved AWS Pricing Calculator share URL. No such URL has been generated, and a generic calculator homepage is not a valid substitute.

## Eligibility and application route

- Applicant category: enrolled graduate / master's student
- Institution: Oslo School of Architecture and Design (AHO), Norway
- Institutional email for application: use the applicant's AHO-issued student address (not reproduced in this public research file)
- AWS account to receive credit: `092509667825`
- Student award ceiling: USD 5,000
- Project type: finite proof-of-concept / benchmark and development of a repeatable, shareable research tool
- Application amount requested: USD 5,000 (maximum student request; award may be lower)
- Research location: Norway
- No faculty endorsement, supervisor, AHO institutional sponsorship, or formal research-group membership is claimed.

AWS's current FAQ defines graduate, post-graduate and PhD students enrolled at accredited research institutions as eligible applicants, says the programme is global outside the Greater China region, and requests an official institution-issued email plus AWS account ID. Student proposals may request up to USD 5,000.
AWS programme: https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/
FAQ: https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/faqs/

## Application form values (working draft)

- First name: Iver
- Last name: Raknes Finne
- Institution: The Oslo School of Architecture and Design (AHO)
- Country/region: Norway
- Industry: Education
- Research-group website: leave blank; no formal research group is being claimed
- AWS account number: `092509667825`
- Area of study: Industrial design; design theory; systems-oriented design; human–AI interaction
- Intended purpose: A finite, reproducible benchmark of AI-assisted design-theory literature analysis, focusing on evidence traceability, citation accuracy, uncertainty, human review and controllability.
- AWS Public Datasets: None. The project will use only public or appropriately licensed scholarly publications and associated bibliographic metadata; it does not depend on an AWS Public Dataset.
- AWS services requested: Amazon Bedrock (explicitly request eligibility for Claude Fable 5.2 inference and other required Bedrock inference); Amazon S3; AWS Lambda; AWS Step Functions; Amazon DynamoDB; Amazon CloudWatch. AWS should confirm Bedrock service eligibility for the awarded credit.
- Credit amount: USD 5,000
- Form context: personal academic research interests (not a business operating-cost request)

The official AWS form's research-group website field does not appear marked required in its current published field list. No fictitious group URL is supplied.

## Proposal description (form-ready)

**Project title: Reproducible Benchmark for Human-Supervised AI Analysis of Design-Theory Literature**

This is a finite six-month graduate research project undertaken by an enrolled master's student at the Oslo School of Architecture and Design (AHO). It will develop and evaluate a reproducible, human-supervised workflow for analysing scholarly literature in design theory and systems-oriented design.

The research problem is that AI-assisted literature analysis can produce plausible summaries while obscuring source provenance, conflating claims, omitting counter-evidence or generating citations that do not support the stated conclusion. The project will test whether a structured workflow can make model-assisted analysis more traceable, auditable and controllable by a human researcher.

The project has five work packages:

1. **Protocol and source register (month 1):** Define a bounded corpus of up to 1,222 bibliographic records. Full-text processing will be limited to publications that are publicly available or whose licence/access terms permit the intended use. Register source identifiers, licences, document hashes and page-level provenance. No private, personal or confidential material will be used.
2. **Cloud workflow prototype (months 1–2):** Build a repeatable pipeline using Amazon Bedrock for model inference, S3 for permitted source material and structured outputs, Lambda and Step Functions for bounded orchestration, DynamoDB for run metadata, and CloudWatch for logging and cost monitoring. The workflow will preserve human approval gates and strict per-run limits.
3. **Controlled benchmark (months 2–4):** Evaluate structured extraction, proposition/evidence mapping and cross-document synthesis. Compare prompt and workflow conditions, including repeat runs and a baseline configuration. Record token usage, latency, failures, evidence coverage, citation/page accuracy and disagreement with human-verified reference annotations. Claude Fable 5.2 is a requested Bedrock model for this benchmark; no claim is made that its account entitlement is already approved.
4. **Human verification and analysis (months 4–5):** Independently review sampled outputs against the cited source pages. Measure traceability, unsupported claims, omissions, uncertainty reporting and the amount of human correction required. Exclude any source that cannot be used lawfully.
5. **Public release (month 6):** Publish the reproducible pipeline, evaluation protocol, schemas, synthetic test fixtures and rights-cleared benchmark records through the applicant's public GitHub research repository. Publish a concise technical report describing limitations and results. Full-text documents will not be redistributed unless their licences expressly permit it.

**AWS resources and rationale:** Amazon Bedrock is required for controlled model-inference experiments, including Claude Fable 5.2 if AWS confirms this model's usage is eligible for the research award. S3 will store only permitted project inputs and structured outputs. Lambda and Step Functions will orchestrate repeatable jobs with hard limits and human approval checkpoints. DynamoDB will track source/run metadata, evaluation status and token usage. CloudWatch will provide operational logs and cost visibility. No long-running production service, general lab operations or unrelated administrative workload is requested.

**Milestones and duration:** Six months from award activation: (M1) source and rights protocol; (M2) prototype and synthetic tests; (M3) bounded benchmark runs; (M4) human verification; (M5) analysis and error taxonomy; (M6) public code, documentation and report.

**Sharing plan:** Release the workflow code, schemas, synthetic tests, rights-cleared metadata and benchmark results through GitHub. Publish a methods report so other design researchers can reproduce the evaluation. Any copyrighted full text or restricted extracts will remain excluded from the public release.

**Future use:** After the award period, the released workflow may be reused by the applicant and other design researchers for bounded, rights-aware evaluation of AI-assisted research methods. Any further AWS usage will be separately monitored and will not rely on continued grant funding.

**Public datasets:** No AWS Public Dataset is planned for this project.

## Cost estimate and application budget

Requested ceiling: **USD 5,000** for up to one year of eligible usage.

A working workload envelope for the Pricing Calculator and proposal is:
- up to 400 million input tokens and 30 million output tokens across the bounded benchmark and controlled repetitions;
- S3 storage for permitted source material and structured outputs;
- Lambda / Step Functions orchestration, DynamoDB run metadata and CloudWatch logging.

The Amazon Bedrock Fable public offer rate card retrieved in `us-east-1` lists standard/global token dimensions at 8 (input) and 40 (output) per pricing unit. Do not treat this as a final application estimate until the unit basis and current calculator pricing are confirmed. The Bedrock amount must be expressly itemised in the proposal because AWS states that service eligibility can be designated by the credit; applicants requiring a specific service should name it in the proposal so AWS can verify eligibility.

**Mandatory missing item:** the AWS application form requires a saved-and-shared AWS Pricing Calculator estimate URL. The public calculator is https://calculator.aws/ . The estimate must be created and saved in the calculator; this file intentionally does not invent a share URL. If the public calculator does not expose Bedrock inference in its service selector, attach the calculator estimate for the infrastructure portion and retain the explicit Bedrock token workload/budget explanation above for the programme reviewer.

## Submission checklist

- [x] Student category and student award ceiling verified against AWS FAQ
- [x] AHO institutional affiliation identified
- [x] AWS account ID verified against AWS Account API
- [x] Finite benchmark project, milestones, sharing and future-use plan drafted
- [x] Bedrock explicitly identified as a required service
- [ ] Confirm the institution-issued student email is accessible for AWS verification
- [ ] Generate and save the AWS Pricing Calculator estimate; paste its share URL into the form
- [ ] Submit the official AWS application form
- [ ] Record application confirmation and send any requested follow-up to `aws-research-credit@amazon.com`

**Important separation:** a research-credit award does not itself clear the separate account-level Bedrock Fable quota / entitlement case. AWS must still approve the pending quota request before the Fable smoke test can succeed. Research credits also cannot be assumed to pay previously incurred charges; they apply only to eligible charges under the applicable promotional-credit terms.


## Eligibility confirmation and submission blocker — 10 November 2026

### Institution

NOKUT's current list of Norwegian higher-education institutions places **The Oslo School of Architecture and Design** under specialised university colleges. This supports the accredited-institution criterion in AWS's research-credit FAQ:
- NOKUT list: https://www.nokut.no/en/higher-education/higher-education-institutions/
- AHO appears explicitly in the specialised universities list.

### Programme team contacted

A pre-submission clarification email was sent to `aws-research-credit@amazon.com` on 10 November 2026 from the connected account. Gmail thread ID: `1a1c3ec113fbc7a3`.

The message asks whether Bedrock inference (including Claude Fable 5.2) can be explicitly designated as eligible, how to represent Bedrock token usage if the pricing calculator cannot model it, and what workaround is accepted while the account's Pricing Calculator API returns `DataUnavailableException`.

This is **not** an application submission or an award. Await written guidance before claiming Bedrock credit eligibility or declaring the application submitted.

### Pricing Calculator attempt

AWS's current Pricing Calculator API is documented under `bcm-pricing-calculator`. AWS Core calls to `ListWorkloadEstimates`, `GetPreferences`, and `CreateWorkloadEstimate` returned `DataUnavailableException: Data is not available. Please try to adjust the time period. If just enabled Cost Explorer, data might not be ingested yet`. The attempted `CreateWorkloadEstimate` did not create an estimate. No public calculator share URL exists yet.

AWS documentation for sharing an estimate explains that a unique public URL is generated only after an estimate is created and shared: https://docs.aws.amazon.com/pricing-calculator/latest/userguide/save-share-estimate.html

### Current completion state

- Proposal text and project milestones: prepared.
- Student eligibility and AHO accreditation evidence: checked.
- AWS account number: verified.
- Required institution-issued AHO email is known from previous correspondence; no personal contact details are stored in this public repository file.
- Bedrock eligibility: clarification requested from programme team; not yet confirmed.
- Saved Pricing Calculator URL: **not yet available**.
- Official application form: **not submitted**.
