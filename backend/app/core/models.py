from sympy import Expr, Eq
from dataclasses import dataclass
from enum import Enum

class Operation(Enum):
    DIFF = "differentiate"
    INTEG = "integrate"
    SIMP = "simplify"

@dataclass
class AlgebraStep:
    equation: Eq
    operation: Operation | None = None

@dataclass
class CalculusStep:
    expression: Expr
    operation: Operation

from pydantic import BaseModel

class StepSchema(BaseModel):
    expression: str
    operation: Operation | None = None
