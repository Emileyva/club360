#archivo será el encargado de transformar las contraseñas planas en hashes de Bcrypt.

from passlib.context import CryptContext

# Configuramos Passlib para usar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Transforma la contraseña plana en un hash seguro"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)