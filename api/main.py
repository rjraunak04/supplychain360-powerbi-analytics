from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent.router import route_question
from agent.tools.catalog import get_tool

app = FastAPI(title="SupplyChain360 AI Copilot", version="0.1.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/ask")
def ask(request: AskRequest) -> dict:
    domain = route_question(request.question)
    tool = get_tool(domain)
    return {
        "question": request.question,
        "domain": domain,
        "tool": tool,
        "status": "routed",
        "message": "Foundation mode: question routed to a governed analytics domain; database execution is added in the next stage.",
    }
