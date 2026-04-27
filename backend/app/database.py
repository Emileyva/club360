import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga la URL desde el .env (en local) o desde Vercel (en la nube)
load_dotenv()

# Usamos getenv para que sea dinámico y seguro
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Si por alguna razón no la encuentra, esto evitará que el código rompa silenciosamente
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No se encontró la variable SQLALCHEMY_DATABASE_URL")

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