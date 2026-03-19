from __future__ import annotations

from dataclasses import dataclass

import psycopg
from pgvector.psycopg import register_vector

from . import config


@dataclass(frozen=True)
class EvidenceRow:
    page_title: str
    section_title: str
    url: str
    revision_id: int | None
    text: str
    distance: float | None


def connect() -> psycopg.Connection:
    conn = psycopg.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        connect_timeout=10,
    )
    register_vector(conn)
    return conn


def fetch_evidence(
    conn: psycopg.Connection,
    query_embedding: list[float],
    k: int,
) -> list[EvidenceRow]:
    sql = f"""
      SELECT
        page_title,
        section_title,
        url,
        revision_id,
        text,
        (embedding <-> %s) AS distance
      FROM {config.VEC_TABLE}
      ORDER BY embedding <-> %s
      LIMIT %s
    """

    with conn.cursor() as cur:
        cur.execute(sql, (query_embedding, query_embedding, k))
        rows = cur.fetchall()

    out: list[EvidenceRow] = []
    for r in rows:
        out.append(
            EvidenceRow(
                page_title=r[0] or "",
                section_title=r[1] or "",
                url=r[2] or "",
                revision_id=r[3],
                text=r[4] or "",
                distance=float(r[5]) if r[5] is not None else None,
            )
        )
    return out
