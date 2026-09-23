from agent.router import route_question
from agent.synthesis import deterministic_summary
from agent.tools.catalog import get_tool
from agent.tools.executor import run_domain_tool


def answer_question(question: str, limit: int = 10, execute: bool = True) -> dict:
    domain = route_question(question)
    tool = get_tool(domain)
    if domain == "general":
        return {"question": question, "domain": domain, "tool": None, "evidence": [], "answer": "Ask a question about inventory, procurement, fulfillment, sales, demand or profitability.", "mode": "guidance"}
    if not execute:
        return {"question": question, "domain": domain, "tool": tool, "evidence": [], "answer": "Question routed successfully. Live SQL execution is disabled.", "mode": "route-only"}
    evidence = run_domain_tool(domain, limit)
    return {"question": question, "domain": domain, "tool": tool, "evidence": evidence, "answer": deterministic_summary(domain, evidence), "mode": "evidence-first"}
