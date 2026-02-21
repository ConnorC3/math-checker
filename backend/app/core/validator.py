from app.core.algebra import _validate_simplify
from app.core.calculus import _validate_differentiate, _validate_integrate
from app.core.models import Step, Operation
from sympy import simplify, diff, integrate, symbols


def validate_step(prev: Step, curr: Step) -> bool:
    op = curr.operation

    if op == Operation.SIMPLIFY:
        return _validate_simplify(prev.expression, curr.expression)
    elif op == Operation.DIFFERENTIATE:
        return _validate_differentiate(prev.expression, curr.expression, curr.wrt)
    elif op == Operation.INTEGRATE:
        return _validate_integrate(prev.expression, curr.expression, curr.wrt)
    else:
        raise NotImplementedError(f"Operation {op} not supported")

def find_first_error(steps: list[Step]) -> int | None:
    for i in range(len(steps) - 1):
        if not validate_step(steps[i], steps[i + 1]):
            return i + 1
    return None


