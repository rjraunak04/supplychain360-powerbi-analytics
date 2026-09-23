from agent.service import answer_question

def test_route_only_does_not_require_database():
    result = answer_question("Which SKUs need reorder?", execute=False)
    assert result["domain"] == "inventory"
    assert result["mode"] == "route-only"
    assert result["evidence"] == []

def test_general_question_returns_guidance():
    result = answer_question("hello there")
    assert result["domain"] == "general"
    assert result["mode"] == "guidance"
