from sympy import Expr, Symbol, Eq
from dataclasses import dataclass
from enum import Enum

class Operation(Enum):
    DIFFERENTIATE = "differentiate"
    INTEGRATE = "integrate"
    SIMPLIFY = "simplify"
    EVALUATE = "evaluate" # substitution

class Step:
    expression: Expr
    operation: Operation = Operation.SIMPLIFY
    wrt: Symbol | None = None

    def __init__(self, expression, operation, wrt=None):
        self.expression = expression
        self.operation = operation
        self.wrt = wrt

    def free_symbols(self):
        return self.expression.free_symbols

from pydantic import BaseModel

class StepSchema(BaseModel):
    expression: str
    operation: Operation
    wrt: str | None = None
