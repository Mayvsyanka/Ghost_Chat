from fastapi import APIRouter, Depends, UploadFile
import PyPDF2
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.db import get_db
from src.database.models import File
from src.schemas import FileModel
from src.services.roles import allowed_operation_admin


async def save_received_file(received_file, file_path):
    with open(file_path, "wb") as file:
        file.write(received_file)

    #file_upload = File(file_name=received_data.filename, data=file_content)
    #db.add(file_upload)
    #db.commit()
