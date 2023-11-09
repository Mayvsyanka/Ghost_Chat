import enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr

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
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    crated_at: datetime
    avatar: str
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    roles: Role

    class Config:
        orm_mode = True

class Profile(BaseModel):
    username: str
    email: str
    crated_at: datetime
    avatar: str
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    images: int

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class RequestEmail(BaseModel):
    email: EmailStr