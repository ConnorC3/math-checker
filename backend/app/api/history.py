from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.db.database import get_db
from app.db.models import Session as SessionModel

router = APIRouter()

@router.get("/history")
def get_history(db: DBSession = Depends(get_db), limit: int = 20):
    sessions = (
        db.query(SessionModel)
            .order_by(SessionModel.created_at.desc())
            .limit(limit)
            .all()
    )

    return [
        {
            "id": s.id,
            "created_at": s.created_at.isoformat(),
            "valid": s.valid,
            "error_step": s.error_step,
            "steps": [
                {
                    "position": step.position,
                    "expression": step.expression,
                    "operation": step.operation,
                    "is_error": step.is_error,
                }
                for step in sorted(s.steps, key=lambda x: x.position)
            ],
        } 
        for s in sessions
    ]
