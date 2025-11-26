from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id")
    case_id: Optional[int] = Field(default=None, foreign_key="cases.id")
    visit_date: datetime
    notes: Optional[str] = None
    recorded_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Vitals(SQLModel, table=True):
    __tablename__ = "vitals"

    id: Optional[int] = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visits.id")
    temperature: Optional[float] = None
    pulse: Optional[int] = None
    blood_pressure: Optional[str] = None
    respiratory_rate: Optional[int] = None
    spo2: Optional[int] = None
    measured_at: datetime = Field(default_factory=datetime.utcnow)

class NurseActivityLog(SQLModel, table=True):
    __tablename__ = "nurse_activity_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visits.id")
    nurse_id: int = Field(foreign_key="users.id")
    activity: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
