from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Enum, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.schemas import Role
from typing import List

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    bio = Column(String(500))
    location = Column(String(500))
    password = Column(String(255), nullable=False)
    crated_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    roles = Column('roles', Enum(Role), default=Role.user)
    access = Column(Boolean, default=True)
