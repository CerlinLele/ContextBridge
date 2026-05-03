# Sandbox Redeployment Notes

## 1. Context

Development may happen in a temporary AWS sandbox environment.

In this setup, AWS resources may disappear after a period of time. When redeploying with Terraform, the main risk is that Terraform state and real AWS resources may no longer match.

Common cases:

```text
Terraform state still exists, but AWS resources are gone.
Terraform state is gone, and AWS resources are gone.
Some AWS resources remain, but Terraform state is gone.
```

The infrastructure should be designed so the sandbox environment can be recreated from code.

## 2. Keep Terraform State Separate When Possible

If possible, do not store Terraform remote state inside the temporary sandbox account.

Recommended setup:

```text
persistent/bootstrap AWS account or stable AWS environment
  -> S3 backend bucket
  -> DynamoDB lock table
  -> KMS key

temporary sandbox AWS account
  -> dev/staging/prod RAG resources managed by Terraform
```

This keeps Terraform state available even if sandbox resources disappear.

If the state backend also lives in the sandbox, losing the sandbox may also delete the Terraform state. In that case, redeployment should be treated as a fresh environment creation.

## 3. Case 1: State Exists but AWS Resources Are Gone

This means Terraform still remembers resources that no longer exist in AWS.

Start by checking the plan:

```powershell
cd infra/envs/dev
terraform init
terraform plan
```

If Terraform shows that many resources need to be recreated, that is expected.

If Terraform fails because a resource recorded in state no longer exists, inspect state:

```powershell
terraform state list
```

Then remove only the missing resource from state:

```powershell
terraform state rm <resource_address>
```

After that, run:

```powershell
terraform plan
terraform apply
```

Do not delete the whole state unless the environment is intentionally disposable and can be fully recreated.

## 4. Case 2: State Is Gone

If Terraform state is gone, Terraform will treat the environment as new.

Redeploy from the environment directory:

```powershell
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```

In this case, resource names must avoid conflicts with any old resources that may still exist.

Pay special attention to:

```text
S3 bucket names
IAM role names
OpenSearch collection names
DynamoDB table names
Secrets Manager secret names
CloudWatch log group names
```

S3 bucket names are globally unique, so include enough uniqueness in bucket names.

## 5. Case 3: Some AWS Resources Remain but State Is Gone

This is the most awkward case.

Options:

```text
1. Import existing resources into Terraform state.
2. Delete the remaining sandbox resources manually, then redeploy.
3. Change resource names and create a fresh set of resources.
```

For disposable sandbox environments, option 2 or 3 is usually simpler.

For important environments, prefer importing existing resources:

```powershell
terraform import <resource_address> <resource_id>
```

Only import resources that should continue to be managed by Terraform.

## 6. Use a Sandbox Identifier

For sandbox development, include a sandbox identifier in resource names.

Example variables:

```hcl
environment = "dev"
sandbox_id  = "hy120"
aws_region  = "ap-southeast-2"
```

Recommended naming pattern:

```text
contextbridge-{env}-{sandbox_id}-{component}
```

Examples:

```text
contextbridge-dev-hy120-kb-sources
contextbridge-dev-hy120-kb-artifacts
contextbridge-dev-hy120-rag-sources
contextbridge-dev-hy120-model-profiles
```

For globally unique resources such as S3 buckets, include account and region when useful:

```text
contextbridge-{env}-{sandbox_id}-{account_id}-{region}-{component}
```

Example:

```text
contextbridge-dev-hy120-123456789012-ap-southeast-2-kb-sources
```

## 7. Do Not Store Important Data Only in Sandbox

Important source data should be recoverable outside the temporary sandbox.

Keep these in Git or another persistent storage location:

```text
Terraform code
model profile config
parser profile config
retrieval profile config
knowledge source files
seed data
evaluation dataset
```

Do not rely on temporary sandbox S3 buckets as the only copy of important knowledge source files.

## 8. Treat RAG Derived Data as Rebuildable

For the RAG system, these should be considered source-of-truth inputs:

```text
raw knowledge files
model profile config
parser profile config
ingestion code
Terraform code
```

These should be considered rebuildable outputs:

```text
parsed artifacts
nodes
chunks
embeddings
vector indexes
ingestion reports
```

After recreating the sandbox, rebuild derived data by rerunning ingestion.

## 9. Recommended Redeployment Flow

When the sandbox disappears, use this flow:

```text
1. Confirm whether Terraform state still exists.
2. Run terraform init in the target environment directory.
3. Run terraform plan.
4. If state references missing resources, remove only those addresses from state.
5. Run terraform apply.
6. Upload or sync knowledge source files.
7. Run ingestion.
8. Run a query smoke test.
9. Run evaluation if model, parser, retrieval, or vector settings changed.
```

Example:

```powershell
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```

Then:

```text
sync source files
run ingestion worker
run query smoke test
```

## 10. Design Rule

Sandbox infrastructure should be disposable.

The project should be able to recreate the sandbox from:

```text
Terraform code
configuration files
source knowledge files
ingestion code
```

Terraform state should either be stored in a stable backend or treated as disposable together with the sandbox.

The vector store, parsed artifacts, and embeddings should not be treated as permanent data in a temporary sandbox.
