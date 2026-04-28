import enum
from sqlalchemy import DateTime, Column, Integer, String, Boolean, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class MembershipType(enum.Enum):
    SUBSCRIBER = "subscriber" #abonado
    NON_SUBSCRIBER = "non_subscriber" #no abonado

class Member(Base):
    __tablename__ = "members"

    id_member = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dni = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_suspended = Column(Boolean, default=False)

    # Relación: Un miembro puede tener varias membresías
    memberships = relationship("Membership", back_populates="owner")
    credits = relationship("Credit", back_populates="owner")

class Membership(Base):
    __tablename__ = "memberships"

    id_membership = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id_member"))
    type = Column(Enum(MembershipType), nullable=False)
    is_active = Column(Boolean, default=True)

    owner = relationship("Member", back_populates="memberships")

class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id_member"))

    # Must be used in the SAME activity (e.g., "football", "paddle")
    activity = Column(String, nullable=False)
    amount = Column(Integer, nullable=False) #valor de la sena

    # fecha de creacion del credito para luego validar
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)

    owner = relationship("Member", back_populates="credits")