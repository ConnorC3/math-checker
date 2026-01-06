from app.core.algebra import equations_equal
from app.core.models import AlgebraStep

def find_first_error(equations: list[AlgebraStep]) -> int | None:
    for i in range(len(equations) - 1):
        eq1 = equations[i].equation
        eq2 = equations[i+1].equation

        if not equations_equal(eq1, eq2):
            return i + 1
    return None


