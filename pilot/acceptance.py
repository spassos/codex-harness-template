"""Evaluator-only checks. Run the cases for one task against the candidate application."""

from fastapi.testclient import TestClient
from pilot_api.entrypoints.http.app import create_app
from structlog.testing import capture_logs


def test_warning() -> None:
    with TestClient(create_app()) as client, capture_logs() as events:
        response = client.post("/items", json={"name": "   ", "private_marker": "pilot-secret-marker"})

    assert response.status_code == 422
    assert response.json() == {"detail": "Item name must not be blank"}
    warnings = [e for e in events if e.get("event") == "invalid_item" and e.get("log_level") == "warning"]
    assert len(warnings) == 1
    assert all(key not in warnings[0] for key in ("name", "body", "payload", "request"))
    assert "pilot-secret-marker" not in str(events)
    assert "   " not in str(warnings[0])


def test_note() -> None:
    with TestClient(create_app()) as client:
        for fields in ({"note": "nota São Paulo"}, {"note": ""}, {"note": None}, {}):
            response = client.post("/items", json={"name": "book", **fields})
            assert response.status_code == 201
            created = response.json()
            assert created["name"] == "book" and created.get("note") == fields.get("note")
            for _ in range(2):
                fetched = client.get("/items/" + created["id"])
                assert fetched.status_code == 200
                assert fetched.json() == created
