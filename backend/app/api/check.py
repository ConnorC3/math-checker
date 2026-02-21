from fastapi import APIRouter, HTTPException
from sympy import sympify
from app.core.models import StepSchema
from app.core.parser import parse_equation, parse_expression
from app.core.validator import find_first_error
from app.core.models import Step, Operation

router = APIRouter()

@router.post("/check")
def check_steps(steps: list[StepSchema]):
    equations = []

    for i, step in enumerate(steps):
        print(f"step {i}: operation={step.operation}, wrt={step.wrt}, type={type(step.wrt)}")
        try:
            if "=" in step.expression:
                expr = parse_equation(step.expression)
            else:
                expr = parse_expression(step.expression)
            
            equations.append(Step(expr, step.operation, step.wrt))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "step": i + 1,
                    "error": str(e),
                    "type": type(e).__name__,
                }
            )

    error_index = find_first_error(equations)
    
    if error_index is None:
        return {"valid": True, "error_step": None, "message": "All steps are correct!"}
    else:
        return {
            "valid": False,
            "error_step": error_index + 1,
            "message": f"Step {error_index + 1} is incorrect."
        }
