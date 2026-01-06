from fastapi import APIRouter, HTTPException
from sympy import sympify
from app.core.models import StepSchema
from app.core.parser import parse_equation
from app.core.validator import find_first_error
from app.core.models import AlgebraStep

router = APIRouter()

@router.post("/check")
def check_steps(steps: list[StepSchema]):
    equations = []

    for i, step in enumerate(steps):
        try:
            equations.append(
                AlgebraStep(parse_equation(step.expression))
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "step": i + 1,
                    "error": str(e),
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
