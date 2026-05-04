# Infrastructure

This directory contains Terraform infrastructure code and environment-specific configuration for AWS resources.

## Directory Layout

```text
infra/
  configs/        # Runtime/config files consumed by environments
  docs/           # Infrastructure planning and operational notes
  envs/           # Terraform root modules, grouped by environment
  modules/        # Reusable Terraform modules
```

Environment entry points should live under `infra/envs/<environment>`, for example:

```text
infra/envs/dev
infra/envs/staging
infra/envs/prod
```

Run Terraform commands from the target environment directory, not from the repository root.

## AWS Credentials

Terraform uses the same AWS credential chain as the AWS CLI and AWS SDKs. Use one of the following options.

### Option 1: AWS CLI Profile

Install and configure AWS CLI:

```powershell
aws configure --profile contextbridge-dev
```

You will be prompted for:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

Recommended default region:

```text
ap-southeast-2
```

Then set the profile for the current PowerShell session:

```powershell
$env:AWS_PROFILE = "contextbridge-dev"
$env:AWS_REGION = "ap-southeast-2"
```

Verify the credentials:

```powershell
aws sts get-caller-identity
```

### Option 2: AWS SSO Profile

If the AWS account uses IAM Identity Center / SSO:

```powershell
aws configure sso --profile contextbridge-dev
aws sso login --profile contextbridge-dev
```

Then set:

```powershell
$env:AWS_PROFILE = "contextbridge-dev"
$env:AWS_REGION = "ap-southeast-2"
```

Verify:

```powershell
aws sts get-caller-identity
```

### Option 3: Environment Variables

For short-lived credentials:

```powershell
$env:AWS_ACCESS_KEY_ID = "<access-key-id>"
$env:AWS_SECRET_ACCESS_KEY = "<secret-access-key>"
$env:AWS_SESSION_TOKEN = "<session-token>"
$env:AWS_REGION = "ap-southeast-2"
```

Use this only for temporary local sessions or CI. Do not commit credentials to the repository.

## Terraform Environment

Install Terraform locally and confirm the version:

```powershell
terraform version
```

Use Terraform `1.6+` unless an environment pins a different version in `required_version`.

Recommended local tools:

```text
Terraform CLI
AWS CLI v2
```

Optional tools:

```text
tfenv or asdf       # Terraform version management
tflint              # Terraform linting
terraform-docs      # Module documentation generation
```

## Running Terraform

Select the target environment and run commands from that directory:

```powershell
cd infra/envs/dev
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

For later runs:

```powershell
cd infra/envs/dev
terraform plan
terraform apply
```

Destroy only disposable environments:

```powershell
terraform destroy
```

## Environment Variables And tfvars

Each environment can define variables through:

```text
terraform.tfvars
*.auto.tfvars
TF_VAR_<name> environment variables
```

If an environment provides `terraform.tfvars.example`, copy it before editing:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Keep real `terraform.tfvars` files local unless the values are intentionally non-sensitive and stable. Do not store secrets in tfvars files.

For secrets, prefer AWS Secrets Manager, SSM Parameter Store, or CI-managed secret variables.

## Remote State

Terraform state should be stored remotely for shared environments. Prefer:

```text
S3 backend bucket
DynamoDB lock table
KMS encryption key
```

State backend resources should ideally live in a persistent account or bootstrap environment, not in a disposable sandbox account.

When using a sandbox account, see:

```text
infra/docs/02-sandbox-redeployment-notes.md
```

## Operational Checklist

Before applying changes:

```text
1. Confirm AWS account with aws sts get-caller-identity.
2. Confirm AWS region.
3. Run terraform fmt.
4. Run terraform validate.
5. Review terraform plan.
6. Apply only from the intended environment directory.
```

