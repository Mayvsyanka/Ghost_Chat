"""Module for User's operations"""

from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from sqlalchemy import func
import os

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/me/", response_model=UserDb)
async def update_profile(body: UpdateUser, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_profile function updates the user's profile information.
        
    
    :param body: UpdateUser: Get the data from the request body
    :param current_user: User: Access the current user's information
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    user = await repository_users.update_profile(body, current_user, db)
    return user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.

    
    :param file: Get the file from the request body
    :type file: UploadFile
    :param current_user: Get the current user from the database
    :type current_user: User
    :param db: Pass the database session to the repository layer
    :type db: Session
    :return: User with updated avatar
    :rtype: User
    """
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

@router.get("/profile/{user}", response_model=Profile)
async def get_profile(username: str, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_profile function returns a user's profile information.
    
    :param username: str: Get the username of the user whose profile is being requested
    :param _: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A user's profile information
    :doc-author: Trelent
    """
    user_info = await repository_users.get_user_info(username, db)
    return {"username": user_info.username, 
            "email": user_info.email,
            "crated_at": user_info.crated_at,
            "avatar": user_info.avatar,
            "images": 'None'}


@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удаление пользователя.

    :param current_user: Текущий пользователь (полученный из зависимости get_current_user).
    :param db: Объект сессии SQLAlchemy (полученный из зависимости get_db).
    """

    if current_user:
        try:
            user_profile = await get_profile(current_user.username, db)
            history_file_path = f'src/history/{user_profile["username"]}_chat_history.pkl'

            os.remove(history_file_path)

            db.delete(current_user)
            db.commit()

            return {"message": "History deleted successfully"}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="History file not found")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred: {str(e)}")
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
