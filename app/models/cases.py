from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Case(SQLModel, table=True):
    __tablename__ = "cases"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id")
    title: str
    description: Optional[str] = None
    status: str = "open"
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WoundRecord(SQLModel, table=True):
    __tablename__ = "wound_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: Optional[int] = Field(default=None, foreign_key="cases.id")
    description: Optional[str] = None
    severity: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)