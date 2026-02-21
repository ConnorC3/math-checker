"""Tests for validator.py — validate_step and find_first_error"""

import pytest
from sympy import Symbol, sin, cos, exp, Eq
from app.core.models import Step, Operation
from app.core.validator import validate_step, find_first_error

x = Symbol('x')
C = Symbol('C')


# ---------------------------------------------------------------------------
# validate_step — SIMPLIFY (algebraic equivalence)
# ---------------------------------------------------------------------------

class TestValidateStepSimplify:
    def test_equivalent_expressions(self):
        prev = Step(expression=2*x + 4*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=6*x, operation=Operation.SIMPLIFY)
        assert validate_step(prev, curr) is True

    def test_non_equivalent_expressions(self):
        prev = Step(expression=2*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=3*x, operation=Operation.SIMPLIFY)
        assert validate_step(prev, curr) is False

    def test_equation_equivalence(self):
        prev = Step(expression=Eq(2*x + 4, 10), operation=Operation.SIMPLIFY)
        curr = Step(expression=Eq(2*x, 6), operation=Operation.SIMPLIFY)
        assert validate_step(prev, curr) is True

    def test_equation_non_equivalence(self):
        prev = Step(expression=Eq(2*x, 6), operation=Operation.SIMPLIFY)
        curr = Step(expression=Eq(2*x, 8), operation=Operation.SIMPLIFY)
        assert validate_step(prev, curr) is False


# ---------------------------------------------------------------------------
# validate_step — DIFFERENTIATE
# ---------------------------------------------------------------------------

class TestValidateStepDifferentiate:
    def test_correct_derivative(self):
        prev = Step(expression=x**2 + 3*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=2*x + 3, operation=Operation.DIFFERENTIATE, wrt=x)
        assert validate_step(prev, curr) is True

    def test_incorrect_derivative(self):
        prev = Step(expression=x**2, operation=Operation.SIMPLIFY)
        curr = Step(expression=3*x, operation=Operation.DIFFERENTIATE, wrt=x)
        assert validate_step(prev, curr) is False

    def test_derivative_infers_variable(self):
        # wrt=None, should infer x automatically
        prev = Step(expression=x**3, operation=Operation.SIMPLIFY)
        curr = Step(expression=3*x**2, operation=Operation.DIFFERENTIATE, wrt=None)
        assert validate_step(prev, curr) is True

    def test_trig_derivative(self):
        prev = Step(expression=sin(x), operation=Operation.SIMPLIFY)
        curr = Step(expression=cos(x), operation=Operation.DIFFERENTIATE, wrt=x)
        assert validate_step(prev, curr) is True


# ---------------------------------------------------------------------------
# validate_step — INTEGRATE
# ---------------------------------------------------------------------------

class TestValidateStepIntegrate:
    def test_correct_integral(self):
        prev = Step(expression=6*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=3*x**2 + C, operation=Operation.INTEGRATE, wrt=x)
        assert validate_step(prev, curr) is True

    def test_correct_integral_no_constant(self):
        # Antiderivative without explicit C is still valid
        prev = Step(expression=6*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=3*x**2, operation=Operation.INTEGRATE, wrt=x)
        assert validate_step(prev, curr) is True

    def test_incorrect_integral(self):
        prev = Step(expression=x, operation=Operation.SIMPLIFY)
        curr = Step(expression=x**2, operation=Operation.INTEGRATE, wrt=x)
        assert validate_step(prev, curr) is False

    def test_integral_infers_variable(self):
        prev = Step(expression=2*x, operation=Operation.SIMPLIFY)
        curr = Step(expression=x**2, operation=Operation.INTEGRATE, wrt=None)
        assert validate_step(prev, curr) is True

    def test_unsupported_operation_raises(self):
        prev = Step(expression=x, operation=Operation.SIMPLIFY)
        curr = Step(expression=x, operation="unknown_op")  # type: ignore
        with pytest.raises((NotImplementedError, AttributeError)):
            validate_step(prev, curr)


# ---------------------------------------------------------------------------
# find_first_error
# ---------------------------------------------------------------------------

class TestFindFirstError:
    def test_all_correct_returns_none(self):
        steps = [
            Step(expression=x**2 + 3*x, operation=Operation.SIMPLIFY),
            Step(expression=2*x + 3, operation=Operation.DIFFERENTIATE, wrt=x),
        ]
        assert find_first_error(steps) is None

    def test_error_at_second_step(self):
        steps = [
            Step(expression=x**2, operation=Operation.SIMPLIFY),
            Step(expression=3*x, operation=Operation.DIFFERENTIATE, wrt=x),  # wrong: should be 2x
        ]
        assert find_first_error(steps) == 1

    def test_error_at_third_step(self):
        steps = [
            Step(expression=2*x + 4*x, operation=Operation.SIMPLIFY),
            Step(expression=6*x, operation=Operation.SIMPLIFY),          # correct simplification
            Step(expression=2*x**2, operation=Operation.INTEGRATE, wrt=x),  # wrong: should be 3x^2
        ]
        assert find_first_error(steps) == 2

    def test_single_step_returns_none(self):
        steps = [Step(expression=x**2, operation=Operation.SIMPLIFY)]
        assert find_first_error(steps) is None

    def test_empty_list_returns_none(self):
        assert find_first_error([]) is None

    def test_mixed_algebra_and_calculus_all_correct(self):
        # ∫ (2x + 4x) dx
        # = ∫ 6x dx        (simplify integrand)
        # = 3x^2 + C       (integrate)
        steps = [
            Step(expression=2*x + 4*x, operation=Operation.SIMPLIFY),
            Step(expression=6*x,       operation=Operation.SIMPLIFY),
            Step(expression=3*x**2 + C, operation=Operation.INTEGRATE, wrt=x),
        ]
        assert find_first_error(steps) is None

    def test_mixed_algebra_and_calculus_error_in_simplify(self):
        steps = [
            Step(expression=2*x + 4*x, operation=Operation.SIMPLIFY),
            Step(expression=7*x,        operation=Operation.SIMPLIFY),  # wrong: 2x+4x=6x not 7x
            Step(expression=3*x**2 + C, operation=Operation.INTEGRATE, wrt=x),
        ]
        assert find_first_error(steps) == 1

    def test_error_in_derivative_step(self):
        # d/dx(x^3 + x^2) = 3x^2 + 2x, not 3x^2
        steps = [
            Step(expression=x**3 + x**2, operation=Operation.SIMPLIFY),
            Step(expression=3*x**2,       operation=Operation.DIFFERENTIATE, wrt=x),  # missing 2x
        ]
        assert find_first_error(steps) == 1
