"""Allow-listed analytics tools.

The copilot should query governed views/KPIs rather than execute arbitrary
LLM-generated SQL. This catalog is the contract between the agent and BI layer.
"""

TOOLS = {
    "inventory": {"purpose": "Inventory health, replenishment and stock movement", "source": "validated inventory analytics views"},
    "procurement": {"purpose": "Supplier, purchase-order and receipt exceptions", "source": "validated procurement analytics views"},
    "fulfillment": {"purpose": "Backorders, picking and fulfillment exceptions", "source": "validated fulfillment analytics views"},
    "sales": {"purpose": "Sales, demand, margin and customer trends", "source": "validated sales analytics views"},
}

def get_tool(domain: str) -> dict[str, str] | None:
    return TOOLS.get(domain)
