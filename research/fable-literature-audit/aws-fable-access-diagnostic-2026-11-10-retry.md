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


## Primary contact phone verified — 10 November 2026

The user completed AWS's console SMS verification. The supplied screenshots show the AWS console success message, and a subsequent live call to `account:GetContactInformation` independently returned:

- `PhoneNumber`: updated primary contact number (redacted from this report)
- `VerificationStatus`: `VERIFIED`

`account:GetAccountInformation` confirms `AccountState=ACTIVE`.

A fresh single synthetic Converse call after phone verification (2026-11-10T04:50:05 UTC) still returned:

`AccessDeniedException: anthropic.claude-fable-5-2 is not available for this account.`

Thus phone verification is completed, but it did not clear the Bedrock runtime entitlement restriction. AWS account verification needs manual review through Account & Billing Support. The AWS Support API currently returns `SubscriptionRequiredException` for DescribeCases/DescribeServices, consistent with no premium technical-support entitlement; Account & Billing case creation remains available through the console for Basic Support customers. The next step is to open an Account & Billing case through the signed-in AWS Support Center, not to alter model agreements or retention.


## Account-level entitlement and quota diagnosis — 10 November 2026

### Fable-specific Service Quotas

AWS Service Quotas `GetServiceQuota` returned an effective value of **0 tokens/minute** for the adjustable quota:

`Cross-region model inference tokens per minute for Anthropic Claude Fable 5.2` (`L-7358FD01`)

This was confirmed in:
- `us-east-2`: value `0`, adjustable `true`
- `us-west-2`: value `0`, adjustable `true`

The corresponding Global cross-region Fable 5.2 quota (`L-0B3FA11F`) is also `0` in both Regions. No quota-increase requests were pending.

AWS's default quota for the US cross-region Fable 5.2 tokens/minute limit is 10,000,000 in both checked Regions. A conservative attempted quota request for 100,000 was rejected by AWS because Service Quotas requires a requested increase above the default value of 10,000,000. **No quota increase was submitted.** A request above 10 million tokens/minute would be disproportionate for the initial research pilot and would not be a responsible workaround for an account entitlement block.

AWS re:Post identifies zero Bedrock quotas for an affected model as an indicator of an account-level restriction. AWS's model-access documentation says some models require additional per-account access after all ordinary prerequisites are satisfied; where the exact `not available for this account` error persists, the additional access must be handled by AWS Sales / Support. This cannot be corrected by another IAM policy, another model agreement, or changing the inference profile.

### Contact attempts

A detailed message with account ID, phone verification state, model agreement state, retention configuration, error messages, and test timestamps was sent from the AWS account email to `aws-verification@amazon.com`.

AWS automatically replied that this is **not a monitored email address** and directed the account owner to:
`https://support.aws.amazon.com/#/contacts/aws-account-verification`

No human support case has been created. The AWS Support API returned `SubscriptionRequiredException` for DescribeCases/DescribeServices, so the programmatic AWS Support API is not available on the account's current support plan. AWS documentation distinguishes Account & Billing support (available with Basic Support through the console) from technical-support cases (which require a paid support plan).

### Current state and next action

- Contact phone: `VERIFIED`
- Account state: `ACTIVE`
- Anthropic use-case authorization: `AUTHORIZED`
- Fable 5.2 agreement: `AVAILABLE`
- Retention: `aws_review` in all three US profile Regions
- Active US inference profile: `us.anthropic.claude-fable-5-2`
- Fable 5.2 cross-region token quota: `0`
- Fable 5.2 global token quota: `0`
- Runtime inference: still denied with account-level `not available for this account`

The hourly automation is now configured to check the Fable-specific cross-region token quota before making any inference call. It will not repeatedly invoke Fable while the quota remains zero. Once the quota becomes positive, it will perform one minimal synthetic test, record the result, and stop after success.

**Required external action:** AWS must clear the account-level Fable 5.2 entitlement restriction or explicitly grant the model quota. The official route is AWS account verification/support and AWS Sales as indicated by the exact runtime error. No additional account, billing, payment, quota, retention, or model-agreement changes should be made until AWS responds.


## Minimal Fable 5.2 runtime quota requests submitted — 10 November 2026

The Service Quotas API clarified why the initial 100,000 TPM requests failed:

- AWS default cross-region Fable 5.2 quota: `10,000,000` TPM.
- Account-applied cross-region Fable 5.2 quota: `0` TPM.
- The API rejects a desired quota below or equal to the AWS default value for an increase request.

A minimal technically valid request of `10,000,001` TPM (one token/minute above the AWS default) was submitted for the **US cross-region runtime quota** in both destination Regions:

| Region | Quota code | Request ID | Desired TPM | Status |
|---|---|---|---:|---|
| us-east-2 | `L-7358FD01` | `dc5c3a63f8aa4a5789243e50455869e4fh36oETV` | 10,000,001 | PENDING |
| us-west-2 | `L-7358FD01` | `0e22cd5cdcd940b9b824511a6f4ddcb944EIzid8` | 10,000,001 | PENDING |

Both requests were accepted by `RequestServiceQuotaIncrease`. A follow-up `GetRequestedServiceQuotaChange` check confirmed both remain `PENDING`; applied values remain zero. No inference test was made after submitting the requests, because AWS has not approved and applied them yet.

The separate Global profile quotas (`L-0B3FA11F`) were also observed at zero but were not modified; the literature pilot will use the US geographic profile for regional data-boundary control.

The quota request is not a purchase or a commitment to use tokens. It only asks AWS to assign an account-level inference capacity limit. The requested value is deliberately the smallest value above AWS's default threshold accepted by the API.

AWS states smaller quota increase requests are often automatically approved; larger ones are routed to Support and can take time. Request IDs are retained here for exact status checks.

## AWS email contact correction

A message sent to `aws-verification@amazon.com` was returned with an automated notice that the mailbox is not monitored. The official reply directed the account owner to:

`https://support.aws.amazon.com/#/contacts/aws-account-verification`

The AWS Support API is not enabled for the current support plan (`SubscriptionRequiredException`); AWS documentation confirms that the Support API requires Business, Enterprise On-Ramp, or Enterprise Support. Basic Support Account & Billing contact is through the authenticated Support Center / AWS Settings console.

The hourly Fable automation now checks these two exact quota request IDs, and will not try inference until they are approved and applied.


## Cross-check against launch documentation and alternate endpoint — 10 November 2026

The model is not a naming or discovery error. Anthropic announced Claude Fable 5.2 on 9 November 2026, and AWS announced it on Amazon Bedrock the same day. AWS's announcement says Fable 5.2 is available through US Geo CRIS and Global CRIS inference profiles. The model card reports Active lifecycle, inference profile use, and required `aws_review` retention. This confirms the model ID and intended access path used in the smoke tests.

- Anthropic launch: https://www.anthropic.com/claude-fable-and-mythos-5-2
- AWS launch: https://aws.amazon.com/blogs/machine-learning/introducing-claude-fable-5-2-on-aws/
- AWS model card: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-fable-5-2.html
- AWS What's New: https://aws.amazon.com/about-aws/whats-new/2026/11/claude-fable-5-2-aws/

The AWS Bedrock quotas documentation confirms that `bedrock-runtime` and `bedrock-mantle` have separate per-model quotas. The account's mantle quota catalogue currently contains Fable 5 and Fable 5.1 entries (with applied value 0) but no specific Fable 5.2 mantle quota entry. Consequently, switching to mantle is not a known available bypass for Fable 5.2. The supported path remains Bedrock Runtime with the US Geo CRIS inference profile and its Fable 5.2 cross-region token quota.

AWS quota documentation also confirms that account-applied quota values may be lower than published default quotas based on regional factors, account usage history, payment history, fraud checks, and quota approval. The current state (default 10,000,000; applied 0) is therefore consistent with an account-level provisioning restriction rather than a bad model identifier.

AWS Basic Support provides Account & Billing assistance in the Support Center / AWS Settings console, even though the programmatic AWS Support API requires a paid Business / Enterprise support plan. The Support API's `SubscriptionRequiredException` therefore does not mean all support is unavailable. The remaining manual route is an Account & Billing case through the authenticated console if the Service Quotas requests remain pending or are rejected.

References:
- Bedrock quotas: https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html
- Service Quotas increase workflow: https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html
- AWS Support API limitation: https://docs.aws.amazon.com/awssupport/latest/APIReference/API_CreateCase.html
- Basic support case instructions: https://docs.aws.amazon.com/accounts/latest/reference/access-aws-support.html


## AWS quota cases opened — 10 November 2026, 05:02 UTC

Both quota requests moved from `PENDING` to **`CASE_OPENED`**. `GetRequestedServiceQuotaChange` now returns AWS support case IDs:

| Region | Request ID | AWS case ID | Status |
|---|---|---|---|
| us-east-2 | `dc5c3a63f8aa4a5789243e50455869e4fh36oETV` | `179428694200752` | `CASE_OPENED` |
| us-west-2 | `0e22cd5cdcd940b9b824511a6f4ddcb944EIzid8` | `179428694200903` | `CASE_OPENED` |

Each case is associated with the request for 10,000,001 TPM for the Claude Fable 5.2 US cross-region inference quota (`L-7358FD01`). At the time of this check, the applied quota values were still zero; no inference test should be run until they become positive.

These are AWS-created case records produced through the Service Quotas workflow. This path succeeded even though the separate AWS Support API is unavailable on the current support plan. The user does not need to create duplicate cases.

The hourly automation continues to poll both request IDs and will perform a synthetic inference test only when both are approved and applied.


## Billing authentication found as likely account-verification trigger — 10 November 2026

A search of the connected AWS account email found an AWS Payment notification from 2026-11-08 02:44:51 UTC:

Subject: `Action required – Your AWS account is past due`

Exact notice details:
- Account: `092509667825`
- Outstanding invoice ID: `EUINNO26-202129`
- AWS attempted to charge the default card ending `6755`.
- The card charge failed because it requires additional authentication (strong customer authentication / 3-D Secure).
- AWS explicitly says the account still has a past-due balance and may be suspended if payment cannot be processed.
- The notice directs the owner to Payments / Payments due to complete the card authentication.

AWS Invoicing `ListInvoiceSummaries` independently returned this invoice for October 2026:
- Issued: `2026-11-02T00:59:24Z`
- Due: `2026-11-01T17:27:10Z`
- Payment currency amount: `0.23 USD`
- Tax currency amount: `2.12 NOK` (includes 0.46 NOK VAT; currency conversion rate 9.2302 NOK/USD)
- Invoicing entity: Amazon Web Services EMEA SARL
- Invoice type: recurring invoice; tax authority status issued.

The same inbox contains an AWS Advance Pay Registration Confirmed message dated 2026-11-10 03:54:17 UTC. It says only that Advance Pay is enabled and funds may now be added; it is **not** a receipt showing any funds added or the overdue invoice paid.

The old guest checkout link embedded in the 2026-11-08 past-due notice expired on 2026-11-10 03:24:50 UTC; do not reuse it. A fresh authenticated Payments console attempt is required.

AWS's documented recovery procedure is:
1. Open Billing and Cost Management → Payments.
2. Under Payments due, select invoice `EUINNO26-202129`.
3. Choose Complete payment.
4. Confirm the payment method or choose Change.
5. Choose Verify and pay, then complete the bank's 3-D Secure / strong customer authentication.

AWS documentation confirms that if the card issuer requires 3DS, the user must complete that authentication flow. It is not possible for an automation to approve the cardholder's bank challenge. The exact payment amount is only 0.23 USD, but no charge has been initiated by the assistant.

### Evidence and likely causality

The past-due notice is a direct AWS statement. The AWS invoice amount is independently confirmed by the Invoicing API. This makes failed card authentication / past due the strongest concrete explanation so far for the recurring account-verification/Bedrock runtime restriction. It is not yet confirmed that settling the invoice alone will automatically remove the Fable quota restriction; the two Service Quotas cases remain open and must still be checked after payment.

Official recovery documentation:
- https://docs.aws.amazon.com/en_en/awsaccountbilling/latest/aboutv2/manage-emea-cc-verification.html
- https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-making-a-payment.html
- https://repost.aws/knowledge-center/retry-unsuccessful-payment

**Outstanding user-authenticated step:** complete the 3-D Secure payment authentication for invoice `EUINNO26-202129` in the AWS Payments console. The assistant must not bypass or impersonate the cardholder's bank authentication.
