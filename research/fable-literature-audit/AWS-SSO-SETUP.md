# Run FORMLÆRE's Fable reader with your AWS console login

This uses temporary AWS CLI credentials from the existing AWS console login.
It does not require a Bedrock API key.

## 1. On your Mac or PC

Install/update AWS CLI v2. It must be version 2.32.0 or later for `aws login`.

Open Terminal and run:

```sh
aws login --profile formlare --region us-east-1
```

A browser window opens. Select your active AWS console account/session and complete sign-in.

Check that it is the expected account:

```sh
aws sts get-caller-identity --profile formlare
```

The returned account must be `092509667825`.

If `aws login` returns an authorization error, the IAM identity needs the AWS-managed
`SignInLocalDevelopmentAccess` policy. In IAM, open **Users → admin → Add permissions
→ Attach policies directly**, find `SignInLocalDevelopmentAccess`, and attach it.
Then run `aws login` again.

If your current console session is actually an IAM Identity Center role rather than
an IAM user, use the Identity Center flow instead:

```sh
aws configure sso --profile formlare
aws sso login --profile formlare
aws sts get-caller-identity --profile formlare
```

Use the AWS access-portal start URL and SSO Region shown by your organisation's
AWS access portal; choose account `092509667825` and the role assigned to you.

## 2. Check Bedrock's retention mode

Run:

```sh
aws bedrock get-account-data-retention --region us-east-1 --profile formlare
```

Fable 5.2 requires `aws_review` (or the legacy `provider_data_share`) in the
Region you invoke it from. If the result is `default`, `none` or `inherit`,
the model will not run until the account is configured.

To enable the required mode, run this only after accepting the scope:

```sh
aws bedrock put-account-data-retention --region us-east-1 --mode aws_review --profile formlare
```

This is an account-level setting for the whole account in `us-east-1`, not a
setting just for FORMLÆRE. Fable 5.2 prompts and outputs may be retained by AWS
for up to 30 days and reviewed by AWS; the content is not shared with Anthropic.
The model ID is `global.anthropic.claude-fable-5-2`.

## 3. Prepare the first batch locally

Clone the two repositories on your computer:

```sh
git clone --depth 1 https://github.com/lukketsvane/FORML-RE.git
git clone --depth 1 https://github.com/lukketsvane/designteori.git
cd FORML-RE
python -m pip install --upgrade boto3 pymupdf
```

Create a local CSV from the template:

```sh
cp research/fable-literature-audit/rights-review-template.csv rights-review.csv
```

Add only corpus work IDs whose PDF rights have been checked for this proposed
analysis. The rights-review file stays local; do not commit it. A blank file
will correctly result in zero eligible papers.

## 4. Dry run — no model call

```sh
export AWS_PROFILE=formlare
python research/fable-literature-audit/batch_reader.py \
  --manifest ../designteori/pdf/manifest.json \
  --pdf-root ../designteori \
  --rights-review-csv rights-review.csv \
  --max-documents 3
```

Check the listed document IDs, rights status and chunk count. No inference is
made in dry-run mode.

## 5. Run the pilot

The pilot is deliberately capped at five text segments. It is billable.

```sh
python research/fable-literature-audit/batch_reader.py \
  --manifest ../designteori/pdf/manifest.json \
  --pdf-root ../designteori \
  --rights-review-csv rights-review.csv \
  --max-documents 3 \
  --max-total-chunks 5 \
  --execute \
  --confirm-paid-inference \
  --confirm-aws-review-retention
```

The script checks the account retention mode before sending the first request.
It writes structured page-referenced records to
`~/.cache/formlaere-fable-audit`; it does not write extracted full PDF text.
