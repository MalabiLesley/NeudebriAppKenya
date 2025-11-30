import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import create_db_and_tables

# Import models (register with SQLModel)
from app.models.organization import Organization
from app.models.users import User
from app.models.patients import Patient
from app.models.cases import Case
from app.models.visits import Visit
from app.models.invoices import Invoice, Payment

# Import routers
from app.routers import auth, patients, cases, visits, invoices, dashboard

load_dotenv()

app = FastAPI(
    title="Nuedebri Health App Kenya",
    version="1.0.0",
    description="Healthcare management system for Nuedebri.com"
)

# CORS
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://192.168.0.107:3000,https://neudebri-app-frontend.vercel.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    try:
        create_db_and_tables()
        print("✓ Application startup complete")
    except Exception as e:
        print(f"✗ Startup error (continuing anyway): {e}")

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {
        "message": "Nuedebri Health App Kenya — Backend Running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/status")
def status():
    return {"status": "ok", "service": "Nuedebri Health App Kenya"}

@app.get("/health")
def health():
    return {"status": "healthy"}