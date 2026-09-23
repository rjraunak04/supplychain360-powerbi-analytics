"""Transparent business-domain router for the analytics copilot."""

import re

DOMAIN_TERMS = {
    "inventory": ("inventory", "stock", "stocks", "sku", "skus", "reorder", "understocked", "overstocked"),
    "procurement": ("supplier", "suppliers", "purchase", "procurement", "po", "receipt", "receipts"),
    "fulfillment": ("backorder", "backorders", "fulfillment", "pick", "picking", "shipment", "shipments", "order", "orders"),
    "sales": ("sales", "revenue", "profit", "margin", "demand", "customer", "customers"),
}

def route_question(question: str) -> str:
    tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
    scores = {
        domain: sum(term in tokens for term in terms)
        for domain, terms in DOMAIN_TERMS.items()
    }
    best_score = max(scores.values())
    if not best_score:
        return "general"
    # Stable priority follows the business domains above when scores tie.
    return next(domain for domain, score in scores.items() if score == best_score)
