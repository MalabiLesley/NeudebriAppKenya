from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Organization(SQLModel, table=True):
    __tablename__ = "organization"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: Optional[str] = Field(default=None, unique=True)
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)