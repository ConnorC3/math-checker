"""Tests for parser.py — parse_equation"""

import pytest
from sympy import Symbol, Eq, SympifyError, sin, cos, exp
from app.core.parser import parse_equation, parse_expression

x = Symbol('x')


class TestParseEquation:
    def test_simple_linear_equation(self):
        eq = parse_equation("2*x + 4 = 10")
        assert isinstance(eq, Eq)

    def test_implicit_multiplication(self):
        # implicit_multiplication_application should handle '2x'
        eq = parse_equation("2x + 4 = 10")
        assert isinstance(eq, Eq)

    def test_lhs_and_rhs_parsed_correctly(self):
        eq = parse_equation("x + 1 = 5")
        assert eq.lhs == x + 1
        assert eq.rhs == 5

    def test_quadratic_equation(self):
        eq = parse_equation("x**2 - 5*x + 6 = 0")
        assert isinstance(eq, Eq)

    def test_equation_without_equals_raises(self):
        with pytest.raises(ValueError, match="must contain '='"):
            parse_equation("2x + 4")

    def test_invalid_expression_raises(self):
        with pytest.raises(ValueError, match="Invalid math expression"):
            parse_equation("2x + @@ = 5")

    def test_constants_only(self):
        eq = parse_equation("4 = 4")
        assert isinstance(eq, Eq)

    def test_evaluate_false_preserves_form(self):
        # Eq with evaluate=False should not collapse 'x = x' to True
        eq = parse_equation("x = x")
        assert isinstance(eq, Eq)

class TestParseExpression:
    def test_simple_polynomial(self):
        expr = parse_expression("x**2 + 3*x")
        assert expr == x**2 + 3*x

    def test_implicit_multiplication(self):
        expr = parse_expression("2x")
        assert expr == 2*x

    def test_no_equals_sign_does_not_raise(self):
        # Key difference from parse_equation — bare expressions are valid
        expr = parse_expression("2*x + 3")
        assert expr is not None

    def test_trig_expression(self):
        expr = parse_expression("sin(x)")
        assert expr == sin(x)

    def test_constant(self):
        expr = parse_expression("42")
        from sympy import Integer
        assert expr == Integer(42)

    def test_invalid_expression_raises(self):
        with pytest.raises(ValueError, match="Invalid math expression"):
            parse_expression("2x + @@")

    def test_empty_string_raises(self):
        with pytest.raises((ValueError, SympifyError)):
            parse_expression("")
