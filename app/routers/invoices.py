from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.invoices import Invoice, Payment
from app.models.patients import Patient
from app.models.cases import Case

router = APIRouter(tags=["Billing"], prefix="/billing")

@router.post("/invoice", response_model=Invoice)
def create_invoice(invoice: Invoice, session: Session = Depends(get_session)):
    if invoice.patient_id and not session.get(Patient, invoice.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    if invoice.case_id and not session.get(Case, invoice.case_id):
        raise HTTPException(status_code=404, detail="Case not found")
    # compute totals if items supplied
    if invoice.items:
        subtotal = sum(item.get("total", 0) for item in invoice.items)
        invoice.subtotal = subtotal
        invoice.total = subtotal + (invoice.tax or 0)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

@router.post("/invoice/{invoice_id}/pay", response_model=Payment)
def pay_invoice(invoice_id: int, payment: Payment, session: Session = Depends(get_session)):
    inv = session.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    payment.invoice_id = invoice_id
    session.add(payment)
    inv.paid_amount = (inv.paid_amount or 0) + payment.amount
    if inv.total and inv.paid_amount >= inv.total:
        inv.status = "paid"
    else:
        inv.status = "partially_paid" if inv.paid_amount > 0 else "unpaid"
    session.add(inv)
    session.commit()
    session.refresh(payment)
    return payment

@router.get("/invoices/unpaid", response_model=List[Invoice])
def unpaid(session: Session = Depends(get_session)):
    return session.exec(select(Invoice).where(Invoice.status != "paid")).all()
