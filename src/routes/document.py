from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin

router = APIRouter(prefix="/document", tags=["document"])