"""Transparent business-domain router for the analytics copilot."""

import re

DOMAIN_TERMS = {
    "inventory": ("inventory", "stock", "stocks", "sku", "skus", "reorder", "understocked", "overstocked"),
    "procurement": ("supplier", "suppliers", "purchase", "procurement", "po", "receipt", "receipts"),
    "fulfillment": ("backorder", "backorders", "fulfillment", "pick", "picking", "shipment", "shipments"),
    "sales": ("sales", "revenue", "profit", "margin", "demand", "customer", "customers"),
}

HIGH_SIGNAL_TERMS = {
    "inventory": ("reorder", "understocked", "overstocked", "stockout"),
    "procurement": ("supplier", "suppliers", "procurement", "receipt", "receipts"),
    "fulfillment": ("backorder", "backorders", "fulfillment", "picking", "shipment", "shipments"),
    "sales": ("revenue", "profit", "margin", "sales", "demand"),
}

def route_question(question: str) -> str:
    text = question.lower()
    tokens = set(re.findall(r"[a-z0-9]+", text))

    # Strong business terms resolve common cross-domain wording first.
    for domain, terms in HIGH_SIGNAL_TERMS.items():
        if any(term in tokens for term in terms):
            return domain

    scores = {
        domain: sum(term in tokens for term in terms)
        for domain, terms in DOMAIN_TERMS.items()
    }
    best_score = max(scores.values())
    if not best_score:
        return "general"
    return next(domain for domain, score in scores.items() if score == best_score)
