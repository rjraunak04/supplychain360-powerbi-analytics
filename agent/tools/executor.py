from agent.db import query_rows
from agent.tools.queries import DOMAIN_QUERIES


def run_domain_tool(domain: str, limit: int = 10) -> list[dict]:
    if domain not in DOMAIN_QUERIES:
        return []
    safe_limit = max(1, min(int(limit), 50))
    return query_rows(DOMAIN_QUERIES[domain], (safe_limit,))
