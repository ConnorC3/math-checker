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

# def equations_equal(prev: Eq, curr: Eq) -> bool:
#     # Get all symbols
#     symbols_set = list(prev.free_symbols.union(curr.free_symbols))

#     # Handle constants
#     if not symbols_set:
#         return simplify(prev.lhs - prev.rhs) == simplify(curr.lhs - curr.rhs)

#     if len(symbols_set) != 1:
#         raise ValueError("Only single-variable equations supported here")

#     x = symbols_set[0]

#     # Solve each equation for x
#     sol_prev = solve(prev, x)
#     sol_curr = solve(curr, x)

#     # Compare sets ignoring order
#     return set(sol_prev) == set(sol_curr)
