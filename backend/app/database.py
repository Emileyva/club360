import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
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


def _normalize_database_url(database_url: str) -> str:
    # Supabase/Heroku style URLs sometimes use postgres:// which SQLAlchemy 2 may reject.
    if database_url.startswith("postgres://"):
        return "postgresql://" + database_url[len("postgres://") :]
    return database_url


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

    database_url = _normalize_database_url(database_url)

    try:
        engine_kwargs = {"pool_pre_ping": True}

        # Serverless: avoid long-lived pools / connection storms.
        if os.getenv("VERCEL"):
            engine_kwargs["poolclass"] = NullPool
        else:
            engine_kwargs["pool_size"] = 5
            engine_kwargs["max_overflow"] = 0

        _engine = create_engine(database_url, **engine_kwargs)
    except Exception as exc:
        # Avoid leaking the full URL, but still provide useful diagnostics.
        raise RuntimeError(
            f"Database engine init failed: {exc.__class__.__name__}: {exc}"
        ) from exc

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