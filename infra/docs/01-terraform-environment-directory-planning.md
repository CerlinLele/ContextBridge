# Terraform Environment Directory Planning

## 1. Goal

Use Terraform to manage separate AWS environments for the RAG system:

```text
dev
staging
prod
```

The directory structure should separate reusable infrastructure modules from environment-specific entry points and configuration.

## 2. Recommended Directory Structure

```text
infra/
  README.md

  docs/
    01-terraform-environment-directory-planning.md

  modules/
    storage/              # S3 source/artifact buckets, KMS
    iam/                  # app role, ingestion role, policies
    registry/             # DynamoDB tables
    vector-store/         # OpenSearch Serverless or Aurora pgvector
    runtime/              # Lambda / ECS / App Runner
    events/               # S3 events, SQS, EventBridge
    observability/        # CloudWatch logs, metrics, alarms

  envs/
    dev/
      main.tf
      providers.tf
      backend.tf
      variables.tf
      terraform.tfvars.example

    staging/
      main.tf
      providers.tf
      backend.tf
      variables.tf
      terraform.tfvars.example

    prod/
      main.tf
      providers.tf
      backend.tf
      variables.tf
      terraform.tfvars.example

  configs/
    dev/
      model-profiles.json
      parser-profiles.json
      retrieval-profiles.json

    staging/
      model-profiles.json
      parser-profiles.json
      retrieval-profiles.json

    prod/
      model-profiles.json
      parser-profiles.json
      retrieval-profiles.json
```

## 3. Directory Responsibilities

### 3.1 `modules/`

`modules/` contains reusable Terraform modules.

Modules should not hard-code a specific environment such as `dev`, `staging`, or `prod`.

They should receive environment-specific values through variables, for example:

```text
environment
aws_region
bucket_name_prefix
model_profile_config_path
parser_profile_config_path
```

Recommended modules:

```text
storage
iam
registry
vector-store
runtime
events
observability
```

### 3.2 `envs/`

`envs/` contains Terraform root modules.

Each environment should have its own Terraform entry point:

```text
infra/envs/dev
infra/envs/staging
infra/envs/prod
```

Each environment should have its own:

```text
backend.tf
providers.tf
variables.tf
terraform.tfvars
```

Terraform should be run from the target environment directory:

```powershell
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```

### 3.3 `configs/`

`configs/` contains non-secret RAG runtime configuration that varies by environment.

Examples:

```text
model-profiles.json
parser-profiles.json
retrieval-profiles.json
```

These files can define environment-specific choices such as:

```text
embedding provider
embedding model
embedding dimension
LLM provider
LLM model
parser type
chunk size
chunk overlap
retrieval top_k
```

Do not store secrets in these files.

## 4. Environment Isolation

Each environment should have isolated infrastructure.

Minimum isolation:

```text
separate Terraform state
separate resource names
separate IAM roles
separate S3 buckets
separate DynamoDB tables
separate vector indexes or collections
```

Recommended isolation:

```text
dev      -> separate AWS account if possible
staging  -> separate AWS account, close to prod
prod     -> separate AWS account, strict permissions and approval
```

If separate AWS accounts are not available at the beginning, use separate Terraform state and strict resource naming per environment.

## 5. Naming Convention

Use the environment name in every resource name.

Recommended pattern:

```text
contextbridge-{env}-{component}
```

Examples:

```text
contextbridge-dev-kb-sources
contextbridge-dev-kb-artifacts
contextbridge-dev-rag-sources
contextbridge-dev-rag-ingestion-runs
contextbridge-dev-model-profiles
contextbridge-dev-vector-index
```

For vector indexes, include embedding profile information when needed:

```text
rag-{env}-{embedding_provider}-{embedding_model_slug}-{dimension}
```

Examples:

```text
rag-dev-bedrock-titan-v2-1024
rag-prod-openai-text-embedding-3-large-3072
```

## 6. Terraform State

Each environment should have its own remote state.

Recommended backend resources:

```text
S3 bucket for Terraform state
DynamoDB table for state locking
KMS encryption for state bucket
```

Example state key layout:

```text
contextbridge/dev/terraform.tfstate
contextbridge/staging/terraform.tfstate
contextbridge/prod/terraform.tfstate
```

Do not share one state file across all environments.

## 7. Secrets

Do not commit secrets to the repository.

Secrets should be stored in AWS Secrets Manager, for example:

```text
/contextbridge/dev/openai/api-key
/contextbridge/staging/openai/api-key
/contextbridge/prod/openai/api-key
```

Terraform may reference secret names or ARNs, but the secret values should not be stored in `.tfvars`, JSON config files, or committed code.

## 8. Suggested First Step

Start with the directory structure only:

```text
infra/
  modules/
  envs/dev/
  envs/staging/
  envs/prod/
  configs/dev/
  configs/staging/
  configs/prod/
```

Then implement the Terraform modules in this order:

```text
1. storage
2. registry
3. iam
4. vector-store
5. runtime
6. events
7. observability
```

This order matches the RAG implementation plan and keeps the foundation stable before adding ingestion and query runtime infrastructure.
