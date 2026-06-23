from fastapi.testclient import TestClient

from app.main import app


def test_ticket_endpoint_returns_response():
    client = TestClient(app)
    response = client.post(
        "/api/tickets",
        json={"customer_id": "cust_001", "message": "My order #1234 is delayed. Can I get a refund?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["ticket_id"].startswith("ticket_")
    assert "response" in payload
