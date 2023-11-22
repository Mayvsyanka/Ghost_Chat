from fastapi import APIRouter, Depends, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.db import get_db
from src.database.models import File, User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import FileModel, UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin
from src.repository.imagetotext import convert

router = APIRouter(prefix="/image", tags=["image"])


@router.post('/image')
async def image(route: str):
    text = await convert(route)
    return (text)
