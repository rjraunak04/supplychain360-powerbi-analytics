"""Small deterministic router used before an LLM is introduced.

Keeping routing testable and transparent makes the first agent version easy to
explain, evaluate and extend.
"""

DOMAIN_TERMS = {
    "inventory": ("inventory", "stock", "sku", "reorder", "understock", "overstock"),
    "procurement": ("supplier", "purchase", "procurement", "po", "receipt"),
    "fulfillment": ("backorder", "fulfillment", "pick", "shipment", "order"),
    "sales": ("sales", "revenue", "profit", "margin", "demand", "customer"),
}

def route_question(question: str) -> str:
    text = question.lower()
    scores = {domain: sum(term in text for term in terms) for domain, terms in DOMAIN_TERMS.items()}
    domain, score = max(scores.items(), key=lambda item: item[1])
    return domain if score else "general"
