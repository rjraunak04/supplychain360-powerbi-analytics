from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent.monitor import build_exception_digest
from agent.service import answer_question

app = FastAPI(title="SupplyChain360 AI Copilot", version="1.0.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    execute: bool = True

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "supplychain360-ai-copilot"}

@app.post("/ask")
def ask(request: AskRequest) -> dict:
    try:
        return answer_question(request.question, request.limit, request.execute)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Analytics execution unavailable: {exc}") from exc

@app.get("/exceptions")
def exceptions(limit: int = 5) -> dict:
    try:
        return build_exception_digest(max(1, min(limit, 20)))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Exception monitor unavailable: {exc}") from exc
