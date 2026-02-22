from fastapi import APIRouter, HTTPException, Depends
from sympy import sympify
from app.core.models import StepSchema
from app.core.parser import parse_equation, parse_expression
from app.core.validator import find_first_error
from app.core.models import Step as CoreStep, Operation
from app.db.database import get_db
from app.db.models import Session as SessionModel, Step as StepModel
from sqlalchemy.orm import Session as DBSession

router = APIRouter()

@router.post("/check")
def check_steps(steps: list[StepSchema], db: DBSession = Depends(get_db)):
    equations = []

    for i, step in enumerate(steps):
        print(f"step {i}: operation={step.operation}, wrt={step.wrt}, type={type(step.wrt)}")
        try:
            if "=" in step.expression:
                expr = parse_equation(step.expression)
            else:
                expr = parse_expression(step.expression)
            
            equations.append(CoreStep(expr, step.operation, step.wrt))
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

    # Save to database
    session = SessionModel(
        valid=error_index is None,
        error_step=error_index + 1 if error_index is not None else None
    )
    db.add(session)
    db.flush()

    for i, step in enumerate(steps):
        db.add(StepModel(
            session_id=session.id,
            position=i,
            expression=step.expression,
            operation=step.operation.value,
            wrt=step.wrt,
            is_error=(error_index == i)
        ))
    
    db.commit()
    
    if error_index is None:
        return {
            "valid": True, 
            "error_step": None,
            "message": "All steps are correct!"
        }
    else:
        return {
            "valid": False,
            "error_step": error_index + 1,
            "message": f"Step {error_index + 1} is incorrect."
        }
