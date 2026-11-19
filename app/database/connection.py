import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Render, Heroku, and Supabase often provide URLs starting with postgres://
# SQLAlchemy 1.4+ / 2.0 requires postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        SessionLocal = sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )
    except Exception as exc:
        logger.exception("Failed to initialize database engine: %s", exc)
        engine = None
        SessionLocal = None
else:
    logger.warning("DATABASE_URL is not configured. Database operations will be unavailable.")


def get_db():
    """Dependency for providing database sessions.

    Raises an HTTP 500 error instead of crashing the server on startup
    if DATABASE_URL is not configured.
    """
    if not SessionLocal:
        raise HTTPException(
            status_code=500,
            detail=(
                "DATABASE_URL is not configured or database connection failed. "
                "Please configure DATABASE_URL in your deployment environment variables."
            ),
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
