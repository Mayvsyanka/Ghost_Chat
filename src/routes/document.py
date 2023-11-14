from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import FileModel, UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin


router = APIRouter(prefix="/document", tags=["document"])

# define a function for uploading documents


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(), db: Session = Depends(get_db)):
    """
    The create_upload_file function is used to upload a file to the database.
    It takes in a file object, which contains the data of the file, and a database session.
    It then creates a new file object, and adds it to the database.
    :param file: Get the file from the request body
    :type file: UploadFile
    :param db: Get the database session from the dependency injection
    :type db: Session
    :return: A dictionary with a message key
    :rtype: str
    """
    # read the contents of the file
    contents = await file.read()
    # create new file upload record
    file_upload = FileModel(name=file.filename, data=contents)
    # add the new file record to the database
    db.add(file_upload)
    # commit the changes to the database
    db.commit()
    # return a message

    return {"filename": file.filename}

# define a function for downloading documen


@router.get("/downloadfile/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    """
    The download_file function is used to download a file from the database.
    It takes in a file_id, which is the id of the file to download, and a database session.
    It then queries the database for the file with the given id, and returns the file data.
    :param file_id: The id of the file to download
    :type file_id: int
    :param db: Get the database session from the dependency injection
    :type db: Session
    :return: The file data
    :rtype: bytes
    """
    # query the database for the file with the given id
    file_upload = db.query(FileModel).filter(FileModel.id == file_id).first()
    # return the file data
    return file_upload.data
