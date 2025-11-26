from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.cases import Case, WoundRecord
from app.models.patients import Patient

router = APIRouter(tags=["Cases"], prefix="/cases")

@router.post("/", response_model=Case)
def create_case(case: Case, session: Session = Depends(get_session)):
    if not session.get(Patient, case.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    session.add(case)
    session.commit()
    session.refresh(case)
    return case

@router.get("/", response_model=List[Case])
def list_cases(session: Session = Depends(get_session)):
    return session.exec(select(Case)).all()

@router.post("/{case_id}/wounds", response_model=WoundRecord)
def add_wound(case_id: int, record: WoundRecord, session: Session = Depends(get_session)):
    c = session.get(Case, case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    record.case_id = case_id
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
