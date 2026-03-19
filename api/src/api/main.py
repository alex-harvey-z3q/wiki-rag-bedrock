from fastapi import FastAPI, Query

from .llm import answer_with_evidence
from .models import AskResponse
from .retrieval import retrieve

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/query", response_model=AskResponse)
def query(q: str = Query(..., min_length=1, max_length=2000)):
    evidence = retrieve(q)
    answer = answer_with_evidence(q, evidence)
    return {"answer": answer, "evidence": evidence}
