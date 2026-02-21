"""Tests for algebra.py — _equations_equivalent"""

import pytest
from sympy import Symbol, Eq
from app.core.algebra import _equations_equivalent

x = Symbol('x')
y = Symbol('y')


class TestEquationsEqual:
    # --- Equivalent equations ---

    def test_identical_equations(self):
        eq = Eq(2*x + 4, 10)
        assert _equations_equivalent(eq, eq) is True

    def test_rearranged_same_solution(self):
        # 2x + 4 = 10  and  2x = 6 both solve to x=3
        eq1 = Eq(2*x + 4, 10)
        eq2 = Eq(2*x, 6)
        assert _equations_equivalent(eq1, eq2) is True

    def test_fully_simplified(self):
        eq1 = Eq(2*x, 6)
        eq2 = Eq(x, 3)
        assert _equations_equivalent(eq1, eq2) is True

    def test_different_form_same_roots(self):
        # x^2 - 5x + 6 = 0  and  (x-2)(x-3) = 0
        eq1 = Eq(x**2 - 5*x + 6, 0)
        eq2 = Eq((x - 2)*(x - 3), 0)
        assert _equations_equivalent(eq1, eq2) is True

    def test_scaled_equation(self):
        # 4x = 12  same as  x = 3
        eq1 = Eq(4*x, 12)
        eq2 = Eq(x, 3)
        assert _equations_equivalent(eq1, eq2) is True

    # --- Non-equivalent equations ---

    def test_different_solutions(self):
        eq1 = Eq(x, 3)
        eq2 = Eq(x, 4)
        assert _equations_equivalent(eq1, eq2) is False

    def test_different_solution_sets(self):
        # x^2 = 4 has solutions {-2, 2}; x = 2 has {2}
        eq1 = Eq(x**2, 4)
        eq2 = Eq(x, 2)
        assert _equations_equivalent(eq1, eq2) is False

    # --- Constant equations (no symbols) ---

    def test_true_constant_equation(self):
        eq1 = Eq(4, 4)
        eq2 = Eq(2 + 2, 4)
        assert _equations_equivalent(eq1, eq2) is True

    def test_false_constant_equation(self):
        eq1 = Eq(4, 4)
        eq2 = Eq(4, 5)
        assert _equations_equivalent(eq1, eq2) is False

    # --- Error cases ---

    def test_multi_variable_raises(self):
        eq1 = Eq(x + y, 5)
        eq2 = Eq(x, 5 - y)
        with pytest.raises(ValueError, match="single-variable"):
            _equations_equivalent(eq1, eq2)
