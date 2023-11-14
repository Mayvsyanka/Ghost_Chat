import enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from fastapi import WebSocket, WebSocketDisconnect

from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class Role (enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class SortField(str, enum.Enum):
    date = "date"
    rating = "rating"

class UpdateUser(BaseModel):
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    crated_at: datetime
    avatar: str
    roles: Role

    class Config:
        orm_mode = True

class Profile(BaseModel):
    username: str
    email: str
    crated_at: datetime
    avatar: str
    images: int

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class RequestEmail(BaseModel):
    email: EmailStr


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()


class FileModel(BaseModel):
    id: int
    # user_id: int
    file_name: str
    file_created_at: datetime


class FileResponse(BaseModel):
    id: int
    data: bytes
    user_id: int
    file_created_at: datetime
