from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext

from indexer.settings import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    PGVECTOR_TABLE, PGVECTOR_SCHEMA
)

EMBED_DIM = 1536  # <-- set this to whatever embedding model dimension you use

def get_storage_context():
    vector_store = PGVectorStore.from_params(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        table_name=PGVECTOR_TABLE,
        schema_name=PGVECTOR_SCHEMA,
        embed_dim=EMBED_DIM,
    )
    return StorageContext.from_defaults(vector_store=vector_store)
