"""
Tests for POST /check API endpoint (app/api/check.py)

Run with:
    pytest tests/test_api_check.py -v

Requires:
    pip install pytest httpx fastapi
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app  # adjust if your FastAPI app is instantiated elsewhere

client = TestClient(app)

URL = "/check"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def post_steps(steps: list[dict]) -> dict:
    response = client.post(URL, json=steps)
    return response


# ---------------------------------------------------------------------------
# Happy path — all steps correct
# ---------------------------------------------------------------------------

class TestAllCorrect:
    def test_single_algebra_step(self):
        # A single step has nothing to compare against, should always be valid
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"}
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True
        assert r.json()["error_step"] is None

    def test_two_correct_algebra_steps(self):
        # 2x + 4 = 10  →  2x = 6
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "2*x = 6",       "operation": "simplify"},
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True

    def test_full_algebra_solution(self):
        # 2x + 4 = 10  →  2x = 6  →  x = 3
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "2*x = 6",       "operation": "simplify"},
            {"expression": "x = 3",         "operation": "simplify"},
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True
        assert r.json()["error_step"] is None

    def test_correct_derivative(self):
        # d/dx(x^2 + 3x) = 2x + 3
        r = post_steps([
            {"expression": "x**2 + 3*x", "operation": "simplify"},
            {"expression": "2*x + 3",    "operation": "differentiate", "wrt": "x"},
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True

    def test_correct_integral(self):
        # ∫ 6x dx = 3x^2 + C
        r = post_steps([
            {"expression": "6*x",       "operation": "simplify"},
            {"expression": "3*x**2",    "operation": "integrate", "wrt": "x"},
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True

    def test_mixed_simplify_then_integrate(self):
        # ∫ (2x + 4x) dx → ∫ 6x dx → 3x^2 + C
        r = post_steps([
            {"expression": "2*x + 4*x", "operation": "simplify"},
            {"expression": "6*x",       "operation": "simplify"},
            {"expression": "3*x**2",    "operation": "integrate", "wrt": "x"},
        ])
        assert r.status_code == 200
        assert r.json()["valid"] is True


# ---------------------------------------------------------------------------
# Incorrect steps — error_step should be returned
# ---------------------------------------------------------------------------

class TestIncorrectSteps:
    def test_wrong_second_algebra_step(self):
        # 2x + 4 = 10  →  2x = 8 (wrong, should be 6)
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "2*x = 8",       "operation": "simplify"},
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 2

    def test_wrong_third_step(self):
        # 2x + 4 = 10  →  2x = 6  →  x = 4 (wrong, should be 3)
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "2*x = 6",       "operation": "simplify"},
            {"expression": "x = 4",         "operation": "simplify"},
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 3

    def test_wrong_derivative(self):
        # d/dx(x^2) should be 2x, student writes 3x
        r = post_steps([
            {"expression": "x**2",  "operation": "simplify"},
            {"expression": "3*x",   "operation": "differentiate", "wrt": "x"},
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 2

    def test_wrong_integral(self):
        # ∫ x dx should be x^2/2, student writes x^2
        r = post_steps([
            {"expression": "x",     "operation": "simplify"},
            {"expression": "x**2",  "operation": "integrate", "wrt": "x"},
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 2

    def test_error_reported_at_first_mistake(self):
        # Step 2 is wrong — step 3 should not be reported even if also wrong
        r = post_steps([
            {"expression": "2*x + 4 = 10", "operation": "simplify"},
            {"expression": "2*x = 8",       "operation": "simplify"},  # wrong
            {"expression": "x = 3",         "operation": "simplify"},  # may or may not be wrong
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 2  # first error, not a later one

    def test_wrong_simplify_before_integrate(self):
        # 2x + 4x simplified to 7x (wrong) before integrating
        r = post_steps([
            {"expression": "2*x + 4*x", "operation": "simplify"},
            {"expression": "7*x",        "operation": "simplify"},   # wrong
            {"expression": "3*x**2",     "operation": "integrate", "wrt": "x"},
        ])
        assert r.status_code == 200
        data = r.json()
        assert data["valid"] is False
        assert data["error_step"] == 2


# ---------------------------------------------------------------------------
# Response shape
# ---------------------------------------------------------------------------

class TestResponseShape:
    def test_valid_response_has_correct_keys(self):
        r = post_steps([
            {"expression": "x = 3", "operation": "simplify"}
        ])
        assert r.status_code == 200
        data = r.json()
        assert "valid" in data
        assert "error_step" in data
        assert "message" in data

    def test_valid_response_values(self):
        r = post_steps([
            {"expression": "2*x = 6", "operation": "simplify"},
            {"expression": "x = 3",   "operation": "simplify"},
        ])
        data = r.json()
        assert data["valid"] is True
        assert data["error_step"] is None
        assert "correct" in data["message"].lower()

    def test_invalid_response_error_step_is_int(self):
        r = post_steps([
            {"expression": "2*x = 6", "operation": "simplify"},
            {"expression": "x = 4",   "operation": "simplify"},
        ])
        data = r.json()
        assert isinstance(data["error_step"], int)

    def test_invalid_response_message_mentions_step(self):
        r = post_steps([
            {"expression": "2*x = 6", "operation": "simplify"},
            {"expression": "x = 4",   "operation": "simplify"},
        ])
        data = r.json()
        assert "2" in data["message"]  # error_step number appears in message


# ---------------------------------------------------------------------------
# Bad input — 400 errors
# ---------------------------------------------------------------------------

class TestBadInput:
    def test_invalid_expression_returns_400(self):
        r = post_steps([
            {"expression": "2x + @@ = 5", "operation": "simplify"}
        ])
        assert r.status_code == 400

    def test_400_detail_contains_step_number(self):
        r = post_steps([
            {"expression": "x = 3",        "operation": "simplify"},
            {"expression": "2x + @@ = 5",  "operation": "simplify"},
        ])
        assert r.status_code == 400
        detail = r.json()["detail"]
        assert detail["step"] == 2

    def test_400_detail_contains_error_message(self):
        r = post_steps([
            {"expression": "bad @@", "operation": "simplify"}
        ])
        assert r.status_code == 400
        detail = r.json()["detail"]
        assert "error" in detail
        assert len(detail["error"]) > 0

    def test_empty_steps_list(self):
        r = post_steps([])
        # No steps to validate — should return valid with no error
        assert r.status_code == 200
        assert r.json()["valid"] is True

    def test_missing_expression_field_returns_422(self):
        # Pydantic validation failure — missing required field
        r = post_steps([
            {"operation": "simplify"}  # no expression
        ])
        assert r.status_code == 422

    def test_invalid_operation_returns_422(self):
        r = post_steps([
            {"expression": "x = 3", "operation": "not_a_real_operation"}
        ])
        assert r.status_code == 422
