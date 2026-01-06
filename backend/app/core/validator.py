from app.core.algebra import equations_equal
from sympy import Eq

def find_first_error(equations: list[Eq]) -> int | None:
    for i in range(len(equations) - 1):
        if not equations_equal(equations[i], equations[i+1]):
            return i + 1
    return None


