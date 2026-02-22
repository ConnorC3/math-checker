import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHistory:

    # Only works with nothing in db
    # def test_empty_history(self):
    #     r = client.get("/history")
    #     assert r.status_code == 200
    #     assert r.json() == []

    def test_history_after_submission(self):
        # Submit a valid solution first
        client.post("/check", json=[
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "x = 3", "operation": "simplify"},
        ])

        r = client.get("/history")
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 1
        assert "id" in data[0]
        assert "created_at" in data[0]
        assert data[0]["valid"] is True
