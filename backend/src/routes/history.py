import pickle
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes.users import get_profile

router = APIRouter( tags=["history"])

@router.get("/open_history/{username}")
async def open_history(username: str, db: Session = Depends(get_db)):
    """
    The open_history function is used to open a user's chat history.
    It takes in the username of the user whose history you want to open, and an optional database session.
    If no database session is provided, it will create one using get_db().

    :param username: str: Specify the username of the user whose history is to be opened
    :param db: Session: Get the database session
    :return: A dictionary with two keys:
    :doc-author: Trelent
    """

    try:
        user_profile = await get_profile(username, db)
        history_file_path = f'src/history/{user_profile["username"]}_chat_history.pkl'

        with open(history_file_path, 'rb') as f:
            loaded_history = pickle.load(f)

        return {"message": "History loaded successfully", "history": loaded_history}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="History file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/delete_history/{username}")
async def delete_history(username: str, db: Session = Depends(get_db)):
    """
    The delete_history function deletes the chat history of a user.
    
    :param username: str: Specify the username of the user whose chat history is to be deleted
    :param db: Session: Get the database session
    :return: A dictionary with a message key
    :doc-author: Trelent
    """
    
    try:
        user_profile = await get_profile(username, db)
        history_file_path = f'src/history/{user_profile["username"]}_chat_history.pkl'

        os.remove(history_file_path)

        return {"message": "History deleted successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="History file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")