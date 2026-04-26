import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # Carga la URL desde el .env

# Reemplazo directo para forzar la creación hoy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:club360bd2026@db.lvmhuwoqaxmvrhxuevdn.supabase.co:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()