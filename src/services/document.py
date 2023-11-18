from fastapi import APIRouter, Depends, UploadFile
import PyPDF2
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.db import get_db
from src.database.models import File
from src.schemas import FileModel
from src.services.roles import allowed_operation_admin

async def save_received_file(received_data, file_path, db: Session = Depends(get_db)):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        file_content = ''
        for page in pdf_reader.pages:
            file_content += page.extract_text()

    file_upload = File(file_name=received_data.filename, data=file_content)
    db.add(file_upload)
    db.commit()



