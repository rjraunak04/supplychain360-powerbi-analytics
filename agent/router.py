"""Transparent business-domain router for the analytics copilot."""

import re

DOMAIN_TERMS = {
    "inventory": ("inventory", "stock", "stocks", "sku", "skus", "reorder", "understocked", "overstocked"),
    "procurement": ("supplier", "suppliers", "purchase", "procurement", "po", "receipt", "receipts"),
    "fulfillment": ("backorder", "backorders", "fulfillment", "pick", "picking", "shipment", "shipments"),
    "sales": ("sales", "revenue", "profit", "margin", "demand", "customer", "customers"),
}

PHRASE_HINTS = {
    "procurement": ("purchase order", "purchase orders", "open order", "open orders"),
    "fulfillment": ("customer order", "customer orders", "picking delay", "picking delays"),
}

def route_question(question: str) -> str:
    text = question.lower()
    tokens = set(re.findall(r"[a-z0-9]+", text))
    scores = {
        domain: sum(term in tokens for term in terms)
        + 2 * sum(phrase in text for phrase in PHRASE_HINTS.get(domain, ()))
        for domain, terms in DOMAIN_TERMS.items()
    }
    best_score = max(scores.values())
    if not best_score:
        return "general"
    return next(domain for domain, score in scores.items() if score == best_score)
