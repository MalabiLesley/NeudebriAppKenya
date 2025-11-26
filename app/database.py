import os
from typing import Generator
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthapp.db")

# Create engine with optimized settings
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "check_same_thread": False,
        "timeout": 10
    } if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
    pool_recycle=3600,
)

def create_db_and_tables():
    """Create all database tables — with error handling"""
    try:
        print("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database creation error: {e}")
        raise

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"✗ Session error: {e}")
        raise