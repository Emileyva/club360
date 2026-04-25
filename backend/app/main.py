from fastapi import FastAPI

app = FastAPI()

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