from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.visits import Visit, Vitals, NurseActivityLog
from app.models.cases import Case

router = APIRouter(tags=["Visits"], prefix="/visits")

@router.post("/", response_model=Visit)
def schedule_visit(visit: Visit, session: Session = Depends(get_session)):
    if not session.get(Case, visit.case_id):
        raise HTTPException(status_code=404, detail="Case not found")
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit

@router.post("/{visit_id}/vitals", response_model=Vitals)
def record_vitals(visit_id: int, vitals: Vitals, session: Session = Depends(get_session)):
    v = session.get(Visit, visit_id)
    if not v:
        raise HTTPException(status_code=404, detail="Visit not found")
    vitals.visit_id = visit_id
    if not vitals.patient_id:
        # derive patient via case
        case = session.get(Case, v.case_id)
        if case:
            vitals.patient_id = case.patient_id
    session.add(vitals)
    session.commit()
    session.refresh(vitals)
    return vitals

@router.post("/{visit_id}/activity", response_model=NurseActivityLog)
def log_activity(visit_id: int, activity: NurseActivityLog, session: Session = Depends(get_session)):
    v = session.get(Visit, visit_id)
    if not v:
        raise HTTPException(status_code=404, detail="Visit not found")
    activity.visit_id = visit_id
    activity.case_id = v.case_id
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity
