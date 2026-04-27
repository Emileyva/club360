import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Carga la URL desde el .env (local) o las Variables de Entorno (Vercel)
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No se encontró la variable SQLALCHEMY_DATABASE_URL")

# 2. Configuración optimizada para Vercel (Serverless)
# pool_pre_ping: verifica que la conexión siga viva antes de usarla
# pool_size: limita cuántas conexiones mantiene abiertas cada instancia
# max_overflow: evita que se creen conexiones infinitas en picos de tráfico
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 3. Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()