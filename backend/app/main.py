from fastapi import FastAPI
from backend.app.database import engine, Base
from backend.app.models.member import Member, Membership, Credit
from backend.app.routes import auth


# 1. Crear la instancia de FastAPI
app = FastAPI(title="CLUB360 API")

# 2. Crear las tablas en la base de datos (Ejecuta al arrancar)
print("Conectando con Supabase y sincronizando tablas...")
#Base.metadata.create_all(bind=engine)
print("¡Tablas 'members', 'memberships' y 'credits' verificadas/creadas!")

# 3. Endpoints (Tus rutas)
@app.get("/")
def home():
    return {"mensaje": "¡Bienvenido al backend de CLUB360!"}

@app.get("/estado-centro")
def estado():
    return {
        "nombre": "CLUB360",
        "horario": "08:00 a 22:00 hs",
        "actividades": ["Fútbol", "Básquet", "Vóley", "Pádel"]
    }

app.include_router(auth.router)
app = app