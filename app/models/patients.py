from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Patient(SQLModel, table=True):
    __tablename__ = "patients"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)