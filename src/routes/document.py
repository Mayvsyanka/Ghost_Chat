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
#from src.repository.Speech2text import speech2text



router = APIRouter(prefix="/document", tags=["document"])


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
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
    file_upload = File(file_name=file.filename, data=contents)
    # add the new file record to the database
    db.add(file_upload)
    # commit the changes to the database
    db.commit()
    # return a message

    return {"filename": f'{file.filename} load succesfully'}

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
    file_upload = db.query(File).filter(File.id == file_id).first()
    # return the file data
    return file_upload.data

'''
#get file name and created date from database
@router.get("/getfile/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    """
    The get_file function is used to get a file from the database.
    It takes in a file_id, which is the id of the file to be retrieved, and a database session.
    It then queries the database for the file with that id, and returns it.
    :param file_id: Get the id of the file to be retrieved
    :type file_id: int
    :param db: Get the database session from the dependency injection
    :type db: Session
    :return: A dictionary with the name and data of the file
    :rtype: dict
    """
    # query the database for the file with the given id
    file_upload = db.query(File).filter(File.id == file_id).first()
    # return the file
    return {"name": file_upload.name, "data": file_upload.data}


# delete file from database

@router.delete("/deletefile/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    """
    The delete_file function is used to delete a file from the database.
    It takes in a file_id, which is the id of the file to be deleted, and a database session.
    It then queries the database for the file with that id, and deletes it.
    :param file_id: Get the id of the file to be deleted
    :type file_id: int
    :param db: Get the database session from the dependency injection
    :type db: Session
    :return: A dictionary with a message key
    :rtype: dict
    """
    # query the database for the file with the given id
    file_upload = db.query(File).filter(File.id == file_id).first()
    # delete the file
    db.delete(file_upload)
    # commit the changes to the database
    db.commit()
    # return a message
    return {"message": "File deleted successfully"}
    '''
