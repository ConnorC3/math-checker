from sympy import Eq, solve, simplify, Expr
from sympy.core.relational import Relational
from sympy.logic.boolalg import BooleanTrue, BooleanFalse

def _validate_simplify(prev: Expr, curr: Expr) -> bool:
    """Algebraic equivalence. Works for both raw exps and equations."""
    if isinstance(prev, Relational) and isinstance(curr, Relational):
        return _equations_equivalent(prev, curr)
    else:
        return simplify(prev - curr) == 0

def _equations_equivalent(eq1: Eq, eq2: Eq) -> bool:
    if isinstance(eq1, (bool, BooleanTrue, BooleanFalse)) or isinstance(eq2, (bool, BooleanTrue, BooleanFalse)):
        return eq1 == eq2

    syms = list(eq1.free_symbols | eq2.free_symbols)

    if len(syms) == 0:
        return simplify(eq1.lhs - eq1.rhs) == simplify(eq2.lhs - eq2.rhs)

    if len(syms) != 1:
        raise ValueError(f"Only single-variable algebraic expressions supported.")
    x = syms[0]
    return set(solve(eq1, x)) == set(solve(eq2, x))
