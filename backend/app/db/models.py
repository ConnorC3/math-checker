from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id          = Column(Integer, primary_key=True)
    created_at  = Column(DateTime, server_default=func.now())
    valid       = Column(Boolean, nullable=False)
    error_step  = Column(Integer, nullable=True)
    steps       = relationship("Step", back_populates="session", cascade="all, delete")

class Step(Base):
    __tablename__ = "steps"

    id          = Column(Integer, primary_key=True)
    session_id  = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    position    = Column(Integer, nullable=False) # 0-indexed
    expression  = Column(String, nullable=False)
    operation   = Column(String, nullable=False)
    wrt         = Column(String, nullable=True)
    is_error    = Column(Boolean, default=False)
    session     = relationship("Session", back_populates="steps")
