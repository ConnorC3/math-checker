"""Tests for calculus.py — _validate_differentiate, _validate_integrate"""

import pytest
from sympy import Symbol, symbols, sin, cos, exp, ln, sqrt, pi
from app.core.calculus import _validate_differentiate, _validate_integrate

x = Symbol('x')
t = Symbol('t')


class TestValidateDifferentiate:
    # --- Correct derivatives ---

    def test_power_rule(self):
        # d/dx(x^2) = 2x
        assert _validate_differentiate(x**2, 2*x, x) is True

    def test_polynomial(self):
        # d/dx(x^2 + 3x) = 2x + 3
        assert _validate_differentiate(x**2 + 3*x, 2*x + 3, x) is True

    def test_constant_vanishes(self):
        # d/dx(x^2 + 5) = 2x
        assert _validate_differentiate(x**2 + 5, 2*x, x) is True

    def test_trig_sin(self):
        # d/dx(sin(x)) = cos(x)
        assert _validate_differentiate(sin(x), cos(x), x) is True

    def test_trig_cos(self):
        # d/dx(cos(x)) = -sin(x)
        assert _validate_differentiate(cos(x), -sin(x), x) is True

    def test_exponential(self):
        # d/dx(e^x) = e^x
        assert _validate_differentiate(exp(x), exp(x), x) is True

    def test_natural_log(self):
        # d/dx(ln(x)) = 1/x
        assert _validate_differentiate(ln(x), 1/x, x) is True

    def test_chain_rule(self):
        # d/dx(sin(x^2)) = 2x*cos(x^2)
        assert _validate_differentiate(sin(x**2), 2*x*cos(x**2), x) is True

    def test_different_variable(self):
        # d/dt(t^3) = 3t^2
        assert _validate_differentiate(t**3, 3*t**2, t) is True

    # --- Incorrect derivatives ---

    def test_wrong_coefficient(self):
        # d/dx(x^2) != 3x
        assert _validate_differentiate(x**2, 3*x, x) is False

    def test_wrong_function(self):
        # d/dx(x^2) != x^2
        assert _validate_differentiate(x**2, x**2, x) is False

    def test_missing_chain_rule(self):
        # d/dx(sin(x^2)) != cos(x^2) — forgot the 2x factor
        assert _validate_differentiate(sin(x**2), cos(x**2), x) is False


class TestValidateIntegrate:
    # --- Correct antiderivatives ---

    def test_power_rule(self):
        # ∫ x dx = x^2/2 + C
        assert _validate_integrate(x, x**2/2, x) is True

    def test_polynomial(self):
        # ∫ (2x + 3) dx = x^2 + 3x + C
        assert _validate_integrate(2*x + 3, x**2 + 3*x, x) is True

    def test_constant_integrand(self):
        # ∫ 6 dx = 6x + C
        assert _validate_integrate(6, 6*x, x) is True

    def test_sin_integral(self):
        # ∫ cos(x) dx = sin(x) + C
        assert _validate_integrate(cos(x), sin(x), x) is True

    def test_cos_integral(self):
        # ∫ -sin(x) dx = cos(x) + C
        assert _validate_integrate(-sin(x), cos(x), x) is True

    def test_exponential_integral(self):
        # ∫ e^x dx = e^x + C
        assert _validate_integrate(exp(x), exp(x), x) is True

    def test_with_explicit_constant_C(self):
        # Student writes 3x^2 + C — the C should be stripped
        C = Symbol('C')
        assert _validate_integrate(6*x, 3*x**2 + C, x) is True

    def test_different_constant_symbol(self):
        # Some students write K instead of C — still valid antiderivative
        K = Symbol('K')
        # Without stripping K, diff(3x^2 + K, x) = 6x still ✓ since dK/dx=0
        assert _validate_integrate(6*x, 3*x**2 + K, x) is True

    def test_different_variable(self):
        # ∫ 3t^2 dt = t^3 + C
        assert _validate_integrate(3*t**2, t**3, t) is True

    # --- Incorrect antiderivatives ---

    def test_wrong_power(self):
        # ∫ x dx != x^2  (missing /2)
        assert _validate_integrate(x, x**2, x) is False

    def test_wrong_function(self):
        # ∫ cos(x) dx != cos(x)
        assert _validate_integrate(cos(x), cos(x), x) is False

    def test_derivative_instead_of_integral(self):
        # Student differentiates instead of integrating x^2 → 2x (wrong)
        assert _validate_integrate(x**2, 2*x, x) is False
