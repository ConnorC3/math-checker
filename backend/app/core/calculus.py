from sympy import Expr, Eq, integrate, diff, Symbol, symbols, simplify
from app.core.models import Operation

def _validate_differentiate(prev: Expr, curr: Expr, wrt: Symbol | None) -> bool:
    """Check that curr == d/dx(prev)."""
    var = wrt or _infer_variable(prev)
    expected = diff(prev, var)
    return simplify(expected - curr) == 0

def _validate_integrate(prev: Expr, curr: Expr, wrt: Symbol | None) -> bool:
    """
    Validate integration by differentiating student's answer.
    Strips the constant of integration (C) before checking.
    """
    var = wrt or _infer_variable(prev)
    student = _strip_integration_constant(curr, var)
    return simplify(diff(student, var) - prev) == 0

def _strip_integration_constant(expr: Expr, var: Symbol) -> Expr:
    """
    Remove terms that vanish under differentiation w.r.t. var.
    """
    C = Symbol('C')
    return expr.subs(C, 0)

def _infer_variable(expr: Expr) -> Symbol:
    syms = expr.free_symbols - {Symbol('C')}
    if len(syms) == 1:
        return syms.pop()
    raise ValueError(f"Cannot infer variable from expression with symbols: {syms}")
