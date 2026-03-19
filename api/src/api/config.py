import os

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
AWS_PROFILE = os.getenv("AWS_PROFILE")

BEDROCK_CHAT_MODEL_ID = os.getenv(
    "BEDROCK_CHAT_MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0",
)
BEDROCK_EMBED_MODEL_ID = os.getenv(
    "BEDROCK_EMBED_MODEL_ID",
    "amazon.titan-embed-text-v2:0",
)

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

VEC_TABLE = os.getenv("PGVECTOR_TABLE", "wiki_rag_nodes")
TOP_K = int(os.getenv("TOP_K", "5"))

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))
