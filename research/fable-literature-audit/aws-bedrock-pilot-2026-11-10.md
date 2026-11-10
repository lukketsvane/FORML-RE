# AWS Bedrock pilot — 10 November 2026

## Verification result

The AWS Core connector authenticated successfully to:

- Account: `092509667825`
- Identity ARN: `arn:aws:iam::092509667825:root`
- Region used for checks: `us-east-1`

The following AWS APIs succeeded:

- STS `GetCallerIdentity`
- EC2 `DescribeRegions`
- Bedrock `GetAccountDataRetention`
- Bedrock `GetUseCaseForModelAccess`
- Bedrock `GetFoundationModel`
- Bedrock `ListFoundationModels`
- Bedrock `ListInferenceProfiles`
- Bedrock `GetInferenceProfile` for both US and Global Fable 5.2 profiles
- Cost Explorer `GetCostAndUsage`

## Model found

Foundation model:

- Name: Claude Fable 5.2
- Model ID: `anthropic.claude-fable-5-2`
- Lifecycle: ACTIVE

Inference profiles:

- `us.anthropic.claude-fable-5-2` — ACTIVE; US East / US East 2 / US West 2
- `global.anthropic.claude-fable-5-2` — ACTIVE; global routing

## Use-case form already exists

Bedrock `GetUseCaseForModelAccess` returned a saved form. Its decoded fields are:

- Company: `finne koder`
- Website: `http://iverfinne.no`
- Industry: `MediaAndEntertainment`
- Intended users: `0` (stored internal-user selection)
- Use-case description: begins with an accidental period, followed by the software engineering / technical research text.

This confirms the form is stored, but not that it is the reason the invocation is blocked.

## Account-level retention

`GetAccountDataRetention` returned:

```json
{"mode":"inherit"}
```

No retention setting was changed during this test.

Fable 5.2 invocation must not proceed until the effective AWS retention mode is confirmed as appropriate. This is a separate gate from account verification.

## Billing signal

Cost Explorer returned estimated values of USD 0.00 for:
- October 2026
- November 1–10, 2026

These are Cost Explorer estimates and do not establish that previously overdue invoices have been paid or that there are no unpaid balances.

## Invocation smoke test

A single small public/synthetic test prompt was sent to:

- Operation: Bedrock Runtime `Converse`
- Region: `us-east-1`
- Model profile: `us.anthropic.claude-fable-5-2`
- maxTokens: 900
- temperature: 0.1

AWS returned:

```
AccessDeniedException:
Your account is currently being verified. Verification normally takes less than 2 hours.
Until your account is verified, you may not have access to this operation.
If you are still receiving this message after more than 2 hours,
please let us know by writing to aws-verification@amazon.com.
```

Status: **BLOCKED BY AWS ACCOUNT VERIFICATION**.

This is not a model ID, IAM permissions or inference-profile discovery failure. No model response was produced. Do not claim that the Fable literature batch has run.

## Resume checklist

1. Re-run a single smoke test after AWS verification clears.
2. Confirm effective retention mode and its scope before sending any corpus content.
3. Run only a rights-reviewed, public/synthetic pilot with a strict request cap.
4. Save each page-grounded Fable result locally, with PDF hash, work ID, page numbers, model ID and token usage.
5. Verify every cited page manually.
6. Commit only structured analysis records and source revisions to this FORMLÆRE research branch. Do not commit PDFs, credentials, raw extracted full text or private rights-review notes.
7. Revise the canonical LaTeX source only after evidence and counterevidence are verified; build PDF and website together.



## Scheduled smoke-test retry — 10 November 2026, 04:33:40 UTC

A single public/synthetic Converse smoke test was attempted through AWS Core.

- Account: `092509667825` (AWS Core connection previously verified as root)
- Region: `us-east-1`
- Requested inference profile: `us.anthropic.claude-fable-5-2`
- Underlying model ID in AWS error: `anthropic.claude-fable-5-2`
- Operation: `bedrock-runtime:Converse`
- Requested `maxTokens`: `900`
- Temperature: `0.1`
- Prompt: public synthetic methodological comparison question; no PDFs or corpus material
- Timestamp: `2026-11-10T04:33:40.485111+00:00`

### Exact AWS result

```
AccessDeniedException:
anthropic.claude-fable-5-2 is not available for this account.
You can explore other available models on Amazon Bedrock.
For additional access options, contact AWS Sales at
https://aws.amazon.com/contact-us/sales-support/
```

Status: **BLOCKED — model not available for this account**.

This differs from the prior response, which said the account was currently being verified. The inference profile had previously appeared as ACTIVE in Bedrock control-plane discovery, but an ACTIVE profile does not establish that this account is entitled to invoke the model. This run did not produce a model response.

- Input tokens: unavailable (request rejected)
- Output tokens: unavailable (no response)
- Total tokens: unavailable
- Inference charge: no successful inference occurred; billing data may update asynchronously.

No account-wide retention, billing, payment or model-access settings were changed. No designteori PDFs were processed.

### Next action

Resolve model entitlement with AWS Bedrock / AWS Sales using the account and exact error above. Once AWS confirms access, retry one public/synthetic Converse request against the US profile. Do not start corpus processing until that succeeds.
