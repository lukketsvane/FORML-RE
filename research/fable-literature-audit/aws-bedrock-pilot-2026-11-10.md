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


## Account-level entitlement diagnosis — 10 November 2026, 04:57–05:00 UTC

### Current read-only control-plane state

At 2026-11-10T04:57:30.900545Z, AWS Core checked account `092509667825`:

- STS identity: `arn:aws:iam::092509667825:root`
- Account state: `ACTIVE` (confirmed separately through Account `GetAccountInformation` at 04:59:17Z)
- Primary contact verification: `VERIFIED` (Account `GetContactInformation`, 04:59:17Z)
- Base model: `anthropic.claude-fable-5-2`, lifecycle `ACTIVE`
- `GetFoundationModelAvailability`: `agreementAvailability.status=AVAILABLE`, `authorizationStatus=AUTHORIZED`, `entitlementAvailability=AVAILABLE`, `regionAvailability=AVAILABLE` in each of `us-east-1`, `us-east-2`, and `us-west-2`
- US inference profile: `us.anthropic.claude-fable-5-2`, `ACTIVE`, system-defined; routes across the three US regions
- Account `GetUseCaseForModelAccess`: stored Anthropic first-time-use form exists
- `GetAccountDataRetention`: `aws_review` in all three US destination regions

Retention snapshots and their reported update times:
- `us-east-1`: `aws_review`, updated `2026-11-10T04:36:46.958Z`
- `us-east-2`: `aws_review`, updated `2026-11-10T04:36:47.625Z`
- `us-west-2`: `aws_review`, updated `2026-11-10T04:36:47.704Z`

### Retention change audit — important

CloudTrail `LookupEvents` found one `PutAccountDataRetention` write in each region at 04:36:46–04:36:47Z. All three events record:
- principal: account root (`092509667825`)
- invoker / source: `aws-mcp.amazonaws.com`
- requested mode: `aws_review`
- event names: `PutAccountDataRetention`

This investigation did **not** make these writes. CloudTrail attributes them to a root session invoked through AWS MCP, but does not identify which earlier conversation or automation initiated them. This is a material correction to the earlier snapshot showing `inherit`. AWS documents that Fable prompts and outputs under `aws_review` may be retained within AWS for up to 30 days and may be reviewed by AWS; they are not shared with Anthropic. Do not make any further retention changes without explicit direction.

### One correctly configured runtime test — 10 November 2026, 04:57:51.885810 UTC

Exactly one small synthetic Converse request was made in `us-east-1` using:
- model ID: `us.anthropic.claude-fable-5-2`
- operation: `bedrock-runtime:Converse`
- maxTokens: `900`
- temperature: `1.0` (Fable 5.2-compatible setting)
- prompt: `Reply with exactly this string and nothing else: FABLE_52_SMOKE_OK`

Exact AWS error:
```
AccessDeniedException: An error occurred (AccessDeniedException) when calling the Converse operation: anthropic.claude-fable-5-2 is not available for this account. You can explore other available models on Amazon Bedrock. For additional access options, contact AWS Sales at https://aws.amazon.com/contact-us/sales-support/
```

Status: **BLOCKED — additional account-level entitlement required**.
- Input tokens: none reported (request rejected)
- Output tokens: none
- Total tokens: none
- Response: none
- Temperature was corrected to the model's supported value; the same account-level denial persisted.
- No PDFs, manuscript material, or corpus text was processed.

### AWS support route findings

- AWS's Bedrock troubleshooting guidance says this exact `AccessDeniedException` wording with “contact AWS Sales” indicates an account-level restriction. It is not resolved by IAM policy edits, SCP changes, or toggling model access in the Bedrock console. AWS directs customers who meet the prerequisites but still receive this error to AWS Support / Sales.
- The account Support API `DescribeServices`, `DescribeSeverityLevels`, and `DescribeCases` each returned `SubscriptionRequiredException: Amazon Web Services Premium Support Subscription is required to use this service.` No support plan or billing setting was changed.
- A message previously sent to `aws-verification@amazon.com` bounced: AWS says that address is not monitored. The bounce directs account-verification enquiries to `https://support.aws.amazon.com/#/contacts/aws-account-verification`.
- The public AWS Sales Support form is at `https://aws.amazon.com/contact-us/sales-support/`. It is the available escalation path for the additional account-level Bedrock model entitlement. Do not purchase a paid support plan or alter payment settings as part of this work.

### Required next step

Submit an AWS Sales / account-verification escalation with:
1. Account ID `092509667825`.
2. Model `anthropic.claude-fable-5-2` and profile `us.anthropic.claude-fable-5-2`.
3. The fact that the account is `ACTIVE`, contact is `VERIFIED`, model agreement/authorization/entitlement/region states are all `AVAILABLE`, and the three US regions return `aws_review`.
4. The exact 04:57:51Z Converse denial above.
5. A request to identify and clear the remaining account-level restriction, or confirm the eligibility criteria and exact action required.

Do not retry Converse repeatedly while AWS's account-level restriction remains. Continue only the existing scheduled single-check process. Do not change retention, billing, payment, or model-access settings. Do not process designteori PDFs until a successful synthetic Converse response is committed.


## Service Quotas finding and AWS case — 10 November 2026, 05:04–05:06 UTC

### Fable cross-region quota is zero

Service Quotas `GetServiceQuota` in `us-east-1` returned the applied account value for:

- Quota: `Cross-region model inference tokens per minute for Anthropic Claude Fable 5`
- Quota code: `L-9B258944`
- Applied account value: `0`
- AWS default value (`GetAWSDefaultServiceQuota`): `4,000,000`
- Adjustable: `true`
- Applied at: `ACCOUNT`

This is consistent with the runtime entitlement denial. The name is for the Fable 5 model family and the account is attempting to use Fable 5.2. Two additional Bedrock Mantle endpoint Fable 5 quotas were also read as zero (input TPM quota `L-0F6BA833`, default 2,000,000; output TPM quota `L-D67748AD`, default 200,000); these are not the quota used by the current `bedrock-runtime` Converse smoke test, so no request was made for those Mantle quotas.

### Quota request submitted

An initial request for 10,000 tokens/minute was rejected by Service Quotas because the desired value must exceed the default quota of 4,000,000. No quota change resulted from that failed request.

The smallest valid request was then submitted:

- Service: `bedrock`
- Region: `us-east-1`
- Quota code: `L-9B258944`
- Desired value: `4,000,001`
- Submitted: `2026-11-10T05:05:45.632215Z`
- Request ID: `0dd2f2b07df043379f3d3dba610f288crtAaX3mW`
- AWS support case ID: `179428714700181`
- Latest request status read at `2026-11-10T05:06:00.626139Z`: `CASE_OPENED`

This does **not** mean quota/access has been granted. The request is with AWS for review. No inference retry was made after the earlier 04:57:51Z denial.

### Scheduled check updated

The existing hourly Fable access check is still enabled. Its prompt now gates any future synthetic inference on all existing US regional quota cases being approved and all applied quota values being non-zero, in addition to model authorization, entitlement, regional availability and `aws_review` checks. It will not repeatedly invoke while the quota requests remain pending. It still must stop and notify only after a successful synthetic Converse result is committed.

No account-wide data-retention setting, billing setting, payment setting or model agreement was changed by this investigation. No designteori PDFs or manuscript material were processed.
