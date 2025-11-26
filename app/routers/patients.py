from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlmodel import Session, select
from app.database import get_session
from app.models.patients import Patient
from app.utils.security import verify_token

router = APIRouter(tags=["Patients"])

@router.post("/", response_model=Patient)
def create_patient(
    payload: Patient,
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """Create a new patient - PROTECTED"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    verify_token(token)  # Verify token
    
    session.add(payload)
    session.commit()
    session.refresh(payload)
    return payload

@router.get("/", response_model=List[Patient])
def list_patients(
    q: Optional[str] = Query(None, description="Search by name or phone"),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """List all patients with optional search - PROTECTED"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    verify_token(token)  # Verify token
    
    stmt = select(Patient).offset(skip).limit(limit)
    
    if q:
        qterm = f"%{q}%"
        stmt = select(Patient).where(
            (Patient.first_name.ilike(qterm)) |
            (Patient.last_name.ilike(qterm)) |
            (Patient.phone.ilike(qterm))
        ).offset(skip).limit(limit)
    
    return session.exec(stmt).all()

@router.get("/{patient_id}", response_model=Patient)
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """Get specific patient - PROTECTED"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    verify_token(token)  # Verify token
    
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: int,
    payload: Patient,
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """Update patient - PROTECTED"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    verify_token(token)  # Verify token
    
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient.first_name = payload.first_name
    patient.last_name = payload.last_name
    patient.email = payload.email
    patient.phone = payload.phone
    patient.date_of_birth = payload.date_of_birth
    patient.gender = payload.gender
    patient.location = payload.location
    
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    authorization: str = Header(None)
):
    """Delete patient - PROTECTED"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    verify_token(token)  # Verify token
    
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    session.delete(patient)
    session.commit()
    return {"deleted": True}