import json
from pathlib import Path
from agent.router import route_question

def test_golden_question_routing():
    cases = json.loads(Path("evals/golden_questions.json").read_text(encoding="utf-8"))
    for case in cases:
        assert route_question(case["question"]) == case["expected_domain"]
