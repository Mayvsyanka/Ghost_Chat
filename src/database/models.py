from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Enum, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.schemas import Role
from typing import List
from sqlalchemy import LargeBinary

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    crated_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    roles = Column('roles', Enum(Role), default=Role.user)
    access = Column(Boolean, default=True)
    files = relationship("File", back_populates="user")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255))
    data = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")
    file_created_at = Column("file_created_at", DateTime, default=func.now())

# create response models for the file


class VectorStore(Base):
    __tablename__ = 'vector_stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    url = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship(User, backref="vector_stores")

