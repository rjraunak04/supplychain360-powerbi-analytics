from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "supplychain360-ai-copilot",
    }


def test_ask_route_only_does_not_require_database():
    response = client.post(
        "/ask",
        json={
            "question": "Which SKUs are understocked and need reorder?",
            "limit": 5,
            "execute": False,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["domain"] == "inventory"
    assert payload["mode"] == "route-only"
    assert payload["evidence"] == []


def test_ask_rejects_invalid_limit():
    response = client.post(
        "/ask",
        json={"question": "Show revenue", "limit": 51, "execute": False},
    )
    assert response.status_code == 422
