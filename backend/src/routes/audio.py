from fastapi import APIRouter, Depends, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
import nbimporter
from src.database.db import get_db
from src.database.models import File, User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import FileModel, UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin
from src.repository.Speech2text import speech2text

router = APIRouter(prefix="/audio", tags=["audio"])

@router.post('/audio')
async def audio(route:str):
    text = await speech2text(route)
    return(text)