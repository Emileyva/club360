import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Load environment from local dev files (Vercel uses Environment Variables).
load_dotenv()

Base = declarative_base()

_engine = None
_SessionLocal = None


def _get_database_url() -> Optional[str]:
    # Primary (current project)
    url = os.getenv("SQLALCHEMY_DATABASE_URL")
    # Common fallback name
    return url or os.getenv("DATABASE_URL")


def get_engine():
    global _engine, _SessionLocal

    if _engine is not None:
        return _engine

    database_url = _get_database_url()
    if not database_url:
        # Do NOT crash at import time (important for serverless cold starts).
        # Raise only when DB is actually used.
        raise RuntimeError(
            "Missing database URL env var. Set SQLALCHEMY_DATABASE_URL (or DATABASE_URL)."
        )

    _engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=0,
    )
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine


def get_db():
    global _SessionLocal
    if _SessionLocal is None:
        try:
            get_engine()
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            )

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()