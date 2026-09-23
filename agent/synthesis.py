from __future__ import annotations

from typing import Any


def deterministic_summary(domain: str, evidence: list[dict[str, Any]]) -> str:
    if not evidence:
        return f"No {domain} exceptions were returned by the governed analytics tool."
    lead = evidence[0]
    if domain == "inventory":
        return f"{len(evidence)} inventory exceptions returned. Highest-priority item: {lead.get('Stock Item', 'unknown')} ({lead.get('Inventory Status', 'unknown')})."
    if domain == "procurement":
        return f"{len(evidence)} procurement exceptions returned. Largest listed issue is with {lead.get('Supplier', 'unknown')}."
    if domain == "fulfillment":
        return f"{len(evidence)} fulfillment exceptions returned. First listed order is {lead.get('WWI Order ID', 'unknown')}."
    if domain == "sales":
        return f"{len(evidence)} leading sales rows returned. Top listed product is {lead.get('Stock Item', 'unknown')}."
    return f"{len(evidence)} evidence rows returned."
