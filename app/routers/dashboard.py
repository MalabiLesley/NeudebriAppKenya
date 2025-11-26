from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.patients import Patient
from app.models.cases import Case
from app.models.invoices import Invoice
from app.models.visits import Visit
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(session: Session = Depends(get_session)):
    total_patients = session.exec(select(func.count()).select_from(Patient)).one()
    total_cases = session.exec(select(func.count()).select_from(Case)).one()
    total_unpaid = session.exec(
        select(func.count()).select_from(Invoice).where(Invoice.status != "paid")
    ).one()

    # sample of critical cases
    critical = session.exec(select(Case).where(Case.critical == True).limit(10)).all()

    # visits scheduled today
    start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    visits_today = session.exec(
        select(func.count()).select_from(Visit).where(
            Visit.scheduled_time >= start, Visit.scheduled_time < end
        )
    ).one()

    return {
        "total_patients": total_patients,
        "total_cases": total_cases,
        "critical_cases_count": len(critical),
        "critical_cases_sample": [
            {
                "id": c.id,
                "patient_id": c.patient_id,
                "primary_diagnosis": c.primary_diagnosis,
            }
            for c in critical
        ],
        "total_unpaid_invoices": total_unpaid,
        "visits_today": visits_today,
    }
