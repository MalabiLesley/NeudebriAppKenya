import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Database
from app.database import create_db_and_tables

# Models (auto-register via import)
from app.models.organization import Organization
from app.models.users import User
from app.models.patients import Patient
from app.models.cases import Case
from app.models.visits import Visit
from app.models.invoices import Invoice, Payment

# Routers
from app.routers import auth, patients, cases, visits, invoices, dashboard

# Load environment variables
load_dotenv()

# ------------------------------------------------------
#                  FASTAPI CONFIGURATION
# ------------------------------------------------------
app = FastAPI(
    title="Nuedebri Health App Kenya",
    version="1.0.0",
    description="A reliable and scalable healthcare management backend for Nuedebri Health."
)

# ------------------------------------------------------
#                       CORS
# ------------------------------------------------------
# Hard-coded allowed origins for production stability
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://neudebri-app-frontend.vercel.app",
    "https://neudebri-frontend-1.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
#                SAFE STARTUP INITIALIZATION
# ------------------------------------------------------
@app.on_event("startup")
def startup_event():
    """
    Runs when the application starts.
    DB errors are logged but DO NOT stop the app.
    This guarantees CORS still loads and frontend can connect.
    """
    try:
        create_db_and_tables()
        print("✓ Database initialized successfully.")
    except Exception as e:
        print(f"⚠️ Database initialization failed (non-blocking): {e}")


# ------------------------------------------------------
#                      ROUTERS
# ------------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


# ------------------------------------------------------
#                    HEALTH & STATUS ROUTES
# ------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint for uptime, environment tracking and connection tests.
    """
    return {
        "message": "Nuedebri Health App Kenya — Backend Running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "status": "online"
    }


@app.get("/api/status", tags=["System"])
def status():
    return {
        "status": "ok",
        "service": "Nuedebri Health App Kenya",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy"}


# ------------------------------------------------------
#                 END OF MAIN APPLICATION
# ------------------------------------------------------
