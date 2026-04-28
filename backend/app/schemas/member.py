from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MembershipType(str, Enum):
    SUBSCRIBER = "subscriber"
    NON_SUBSCRIBER = "non_subscriber"

class MembershipSchema(BaseModel):
    type: MembershipType
    is_active: bool

    class Config:
        from_attributes = True

class CreditSchema(BaseModel):
    id: int
    activity_type: str
    amount: float
    created_at: datetime
    is_used: bool

    class Config:
        from_attributes = True

# Define qué le pedimos al usuario al registrarse.
#DNI tenga entre 7 y 10 caracteres y que el email sea válido.
class MemberCreate(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    dni: str = Field(..., min_length=7, max_length=10)
    email: EmailStr
    password: str

# Es lo que el servidor le responde al cliente.
class MemberResponse(BaseModel):
    id_member: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True