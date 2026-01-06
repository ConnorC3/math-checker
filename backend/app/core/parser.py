from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import Eq

transformations = standard_transformations + (implicit_multiplication_application,)

def parse_equation(eq_str: str) -> Eq:
    if "=" not in eq_str:
        raise ValueError("Equation must contain '='")
    left, right = eq_str.split("=")
    left_expr = parse_expr(left, transformations=transformations)
    right_expr = parse_expr(right, transformations=transformations)
    return Eq(left_expr, right_expr, evaluate=False)
