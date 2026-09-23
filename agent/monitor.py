from agent.tools.executor import run_domain_tool


def collect_exceptions(limit_per_domain: int = 5) -> dict[str, list[dict]]:
    return {domain: run_domain_tool(domain, limit_per_domain) for domain in ("inventory", "procurement", "fulfillment")}


def build_exception_digest(limit_per_domain: int = 5) -> dict:
    exceptions = collect_exceptions(limit_per_domain)
    return {"counts": {k: len(v) for k, v in exceptions.items()}, "exceptions": exceptions}
