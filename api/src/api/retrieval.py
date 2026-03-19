from __future__ import annotations

from functools import lru_cache

from llama_index.embeddings.bedrock import BedrockEmbedding

from . import config
from .db import connect, fetch_evidence


@lru_cache(maxsize=1)
def get_embedding_model() -> BedrockEmbedding:
    kwargs: dict = {
        "model_name": config.BEDROCK_EMBED_MODEL_ID,
        "region_name": config.AWS_REGION,
    }
    if config.AWS_PROFILE:
        kwargs["profile_name"] = config.AWS_PROFILE
    return BedrockEmbedding(**kwargs)


def retrieve(question: str) -> list[dict]:
    embed_model = get_embedding_model()
    query_embedding = embed_model.get_text_embedding(question)

    with connect() as conn:
        rows = fetch_evidence(conn, query_embedding, config.TOP_K)

    return [
        {
            "page": row.page_title,
            "section": row.section_title,
            "url": row.url,
            "revision_id": row.revision_id,
            "excerpt": row.text,
        }
        for row in rows
    ]
