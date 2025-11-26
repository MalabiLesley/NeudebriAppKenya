from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id")
    case_id: Optional[int] = Field(default=None, foreign_key="cases.id")
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    amount: float
    status: str = "pending"
    invoice_date: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    amount: float
    method: Optional[str] = None
    reference: Optional[str] = None
    paid_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
