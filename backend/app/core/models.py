from dataclasses import dataclass
from sympy import Expr

@dataclass
class Step:
    expression: Expr
    operation: str | None = None
