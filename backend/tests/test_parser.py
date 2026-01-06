import pytest
from app.core.parser import parse_equation
from sympy import Eq, symbols

x = symbols("x")

def test_parse_valid_equation():
    eq = parse_equation("2*x + 3 = 7")
    assert isinstance(eq, Eq)
    assert eq.lhs == 2*x + 3
    assert eq.rhs == 7

def test_parse_invalid_equation():
    with pytest.raises(ValueError):
        parse_equation("2*x + 3")
