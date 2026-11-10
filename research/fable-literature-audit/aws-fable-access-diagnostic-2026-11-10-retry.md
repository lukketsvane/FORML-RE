# Fable 5.2 access diagnostic — 10 November 2026 (retry)

## Result

The AWS account verification block observed in the previous smoke test has changed. The latest invocation now returns:

`AccessDeniedException: anthropic.claude-fable-5-2 is not available for this account.`

Identity is still verified as account `092509667825`, root ARN
`arn:aws:iam::092509667825:root`.

## Exact availability state

Bedrock `GetFoundationModelAvailability(modelId="anthropic.claude-fable-5-2")` returned:

- `agreementAvailability.status = NOT_AVAILABLE`
- `authorizationStatus = AUTHORIZED`
- `entitlementAvailability = AVAILABLE`
- `regionAvailability = AVAILABLE`

Interpretation: the account's Anthropic first-time-use-case authorization is present; the model agreement is not yet activated. This is the next access gate.

## Stored first-time use-case form

`GetUseCaseForModelAccess` returned a saved form. Decoded fields:
- Company: `finne koder`
- Website: `http://iverfinne.no`
- Intended users: `0` (internal)
- Industry: `MediaAndEntertainment`
- Description is the previous internal software-engineering / technical-research text, but begins with an accidental period.

Do not include the returned Base64 form payload in this report.

## Agreement offer

`ListFoundationModelAgreementOffers(modelId="anthropic.claude-fable-5-2", offerType="ALL")` returned one usage-based offer. The offer token is intentionally not stored in GitHub.

The response contained these Global standard rates:
- Input: 8 units per million tokens
- Output: 40 units per million tokens
- Cache read: 0.2 units per million tokens
- Cache write: 10 units per million tokens (5 min)
- Cache write: 16 units per million tokens (1 hour)

It contained US standard rates:
- Input: 8.8 units per million tokens
- Output: 44 units per million tokens
- Cache read: 0.22 units per million tokens
- Cache write: 11 units per million tokens (5 min)
- Cache write: 17.6 units per million tokens (1 hour)

The offer's support term stated **No refunds**. A foundation-model agreement is a usage-based commercial agreement and must not be created without clear user authorization. AWS describes the sequence as listing offers, submitting the first-time Anthropic use case, creating the model agreement, and checking availability.

## Retention state

Bedrock `GetAccountDataRetention` returned `{"mode":"inherit"}`.

Fable 5.2 requires `aws_review` or another explicitly qualifying mode. The `inherit` setting does not itself establish that this requirement is met. Retention is configured at the account level separately in each AWS Region. For this profile, all three destination Regions must be checked and configured. `aws_review` permits AWS review, with eligible Fable prompts and outputs retained within AWS for up to 30 days; content is not shared with Anthropic.

## No inference result

The second Converse smoke test did not return a model response. No research PDFs or manuscript text were submitted.

## Required next actions

The user has approved both the usage-based agreement and regional `aws_review` retention. The agreement and retention updates have now been applied; see the dated execution record below.


---

## Approved activation actions — 10 November 2026

The user explicitly approved both the usage-based Fable agreement and the AWS review retention setting.

### Retention update completed

AWS `PutAccountDataRetention(mode="aws_review")` succeeded in all three destinations of the active US inference profile:

| Region | Result |
|---|---|
| `us-east-1` | `aws_review` |
| `us-east-2` | `aws_review` |
| `us-west-2` | `aws_review` |

All three settings were re-read with `GetAccountDataRetention` and confirmed as `aws_review`. These are account-level settings per Region, not one worldwide/global switch. AWS states that eligible Fable prompts and outputs may be retained within AWS for up to 30 days and may be reviewed by AWS; they are not sent to Anthropic for that review.

### Model agreement request completed

A fresh offer was retrieved and `CreateFoundationModelAgreement(modelId="anthropic.claude-fable-5-2", offerToken=<fresh offer token>)` returned success. Offer token deliberately not recorded.

### Availability remains pending

At 2026-11-10 04:37:23 UTC and again at 04:37:42 UTC, `GetFoundationModelAvailability` returned:

- `agreementAvailability.status = PENDING`
- `authorizationStatus = AUTHORIZED`
- `entitlementAvailability = AVAILABLE`
- `regionAvailability = AVAILABLE`

AWS documentation defines `PENDING` as agreement provisioning still in progress; invocations can return AccessDenied until it changes to `AVAILABLE`. An inference call was therefore **not** attempted while pending. No PDFs or manuscript material were submitted.

### Follow-up

The hourly Fable access check has been re-enabled. It should run a single synthetic Converse test only after agreement availability is `AVAILABLE`, then record exact response, timestamp and token usage in this branch. If status becomes `ERROR`, record AWS's error message rather than retrying invocations.


## Runtime verification retry — 10 November 2026

After the retention changes and successful agreement creation:

- `GetFoundationModelAvailability` returned `AVAILABLE` for the foundation model in `us-east-1`, `us-east-2`, and `us-west-2`.
- The `us.anthropic.claude-fable-5-2` inference profile remained `ACTIVE` in all three Regions.
- Account retention remained `aws_review` in all three Regions.
- `GetFoundationModel` confirms `inferenceTypesSupported=["INFERENCE_PROFILE"]`; the profile ID is required.
- The first runtime attempt in `us-east-1` returned `AccessDeniedException: anthropic.claude-fable-5-2 is not available for this account.`
- A second minimal runtime attempt in `us-east-2` returned the explicit AWS message: `Your account is currently being verified. Verification normally takes less than 2 hours. Until your account is verified, you may not have access to this operation.`

The successful control-plane agreement and the failed runtime verification are distinct states. The model is not yet usable through Converse. No PDFs, manuscript content, or private source documents have been submitted. Only short synthetic prompts were used, and both failed before a model response was returned.

**Current state:** retention configured; usage agreement accepted; regional model availability reports AVAILABLE; AWS runtime account verification remains the blocking condition. Continue the hourly verification check and make only one small synthetic call per run once the model agreement remains AVAILABLE. Do not alter retention, billing, or agreement settings again.


## Live recheck — 10 November 2026, 04:42 UTC

A fresh direct AWS Core check reconfirmed all preconditions across all three US routing Regions:

| Region | Agreement | Authorization | Entitlement | Region | Retention |
|---|---|---|---|---|---|
| us-east-1 | AVAILABLE | AUTHORIZED | AVAILABLE | AVAILABLE | aws_review |
| us-east-2 | AVAILABLE | AUTHORIZED | AVAILABLE | AVAILABLE | aws_review |
| us-west-2 | AVAILABLE | AUTHORIZED | AVAILABLE | AVAILABLE | aws_review |

The `us.anthropic.claude-fable-5-2` profile remains ACTIVE. One new synthetic Converse attempt was made through the documented US profile from `us-east-1`, with `maxTokens=128` and `temperature=1.0`. It failed at 2026-11-10T04:42:31 UTC:

`AccessDeniedException: anthropic.claude-fable-5-2 is not available for this account. You can explore other available models on Amazon Bedrock.`

No model response or token usage was returned. No source corpus or manuscript data was sent.

### Interpretation

The official AWS model-access guide defines `agreementAvailability=AVAILABLE` as access existing. The model card confirms the model ID and geo profile are correct, identifies `bedrock-runtime` as a supported endpoint, and requires `aws_review` retention. These checks are now all satisfied. Nevertheless the runtime is still denying the account. This is an AWS-side entitlement/account restriction not explained by the currently visible Bedrock control-plane state. AWS Support should inspect the account's Fable 5.2 runtime entitlement and verification status; do not keep repeatedly attempting inference.

References:
- AWS model access: https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
- AWS Claude Fable 5.2 model card: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-fable-5-2.html
- AWS announcement: https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-2-on-aws/

Hourly check remains enabled to detect a change, but no further settings or agreements should be modified.
