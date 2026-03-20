from __future__ import annotations

from functools import lru_cache
from typing import Any, Mapping

import boto3

from .config import AWS_REGION, BEDROCK_CHAT_MODEL_ID, MAX_TOKENS, TEMPERATURE


@lru_cache(maxsize=1)
def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def answer_with_evidence(
    question: str,
    evidence_items: list[Mapping[str, Any]],
) -> str:
    evidence_block = "\n\n".join(
        f"[{i+1}] {item['page']} — {item['section']}\n"
        f"URL: {item['url']}\n"
        f"Excerpt: {item['excerpt']}"
        for i, item in enumerate(evidence_items)
    )

    system_prompt = (
        "You are a careful assistant answering questions using ONLY the provided "
        "evidence excerpts from Wikipedia. If the evidence is insufficient, say "
        "you do not know. Always cite evidence items like [1], [2]."
    )

    user_prompt = f"Question: {question}\n\nEvidence:\n{evidence_block}"

    response = get_bedrock_client().converse(
        modelId=BEDROCK_CHAT_MODEL_ID,
        system=[{"text": system_prompt}],
        messages=[{
            "role": "user",
            "content": [{"text": user_prompt}],
        }],
        inferenceConfig={
            "maxTokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        },
    )

    content = response["output"]["message"]["content"]
    text_parts = [part.get("text", "") for part in content if "text" in part]
    return "\n".join(part for part in text_parts if part).strip()
