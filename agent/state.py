from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    question: str
    domain: str = "general"
    evidence: list[dict[str, Any]] = field(default_factory=list)
    answer: str = ""
