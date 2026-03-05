# wiki-rag

Terraform + ECS Fargate pipeline that:
1) ingests Wikipedia content into S3
2) indexes into Postgres (pgvector) using embeddings
3) serves a FastAPI RAG API behind an ALB

## Prereqs

- Terraform >= 1.6
- AWS CLI configured for the target account
- jq
- psql (optional, for DB inspection)

## 1) Secrets (required)

Create a Secrets Manager secret named:

wiki-rag/app

SecretString must be JSON:

```json
{
  "DB_PASSWORD": "your-db-password",
  "OPENAI_API_KEY": "your-openai-key"
}
```

## 2) Stand up infra

From terraform/:

```bash
terraform init
terraform apply
```

## 3) Deploy containers (push images)

ECS task defs reference :latest, so you must push images before tasks can start.

Use GitHub Actions workflows:

deploy-api
deploy-ingest
deploy-indexer

Verify API service is running:

```bash
REGION=ap-southeast-2
CLUSTER=wiki-rag
SERVICE=wiki-rag-api

aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --query 'services[0].{desired:desiredCount,running:runningCount,taskDef:taskDefinition}' --output table
```

Healthcheck:

```bash
ALB=$(terraform output -raw api_url)
curl -i "$ALB/health"
```

## 4) Bootstrap data (first run)

Scheduled EventBridge runs will eventually populate the system, but for a fresh environment do:

1) Run ingest once
2) Run indexer once

### Run ingest

```bash
bash scripts/run_ingest.sh
```

### Run indexer

```bash
bash scripts/run_indexer.sh
```

## 5) Test the API

```
ALB=$(terraform output -raw api_url)
curl -sS -i -H "Content-Type: application/json"   -d '{"question":"What documents were indexed?"}' "$ALB/ask"
```

Expected: HTTP/1.1 200 OK with answer + evidence.

## Tear down

Terraform destroy will fail if:

- ECR repos are not empty
- S3 buckets contain objects

Run cleanup scripts first if needed, then:

```bash
terraform destroy
```

## License

MIT.
