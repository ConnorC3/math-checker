from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_check_all_correct():
    response = client.post(
        "/check",
        json=[
            {"expression": "2*x + 3 = 7", "operation": None},
            {"expression": "2*x = 4", "operation": None},
            {"expression": "x = 2", "operation": None},
        ],
    )

    assert response.status_code == 200
    data = response.json()

    assert data["valid"] is True
    assert data.get("error_step") is None


def test_check_detects_first_error():
    response = client.post(
        "/check",
        json=[
            {"expression": "2*x + 3 = 7", "operation": None},
            {"expression": "2*x = 5", "operation": None},  # wrong
            {"expression": "x = 2", "operation": None},
        ],
    )

    assert response.status_code == 200
    data = response.json()

    assert data["valid"] is False
    assert data["error_step"] == 2


def test_invalid_math_returns_400():
    response = client.post(
        "/check",
        json=[
            {"expression": "this is not math", "operation": None}
        ],
    )

    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert data["detail"]["step"] == 1


def test_missing_equals_sign_returns_400():
    response = client.post(
        "/check",
        json=[
            {"expression": "2*x + 3", "operation": None}
        ],
    )

    assert response.status_code == 400
    assert response.json()["detail"]["step"] == 1


def test_empty_steps_list():
    response = client.post("/check", json=[])

    assert response.status_code == 200
    assert response.json()["valid"] is True
