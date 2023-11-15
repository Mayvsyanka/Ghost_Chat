from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.services.auth import get_current_user
from src.database.models import User
from src.repository import vectorstores as repo_vectorstores
from src.schemas import Vectorstore

router = APIRouter(prefix="/vectorstore", tags=["vectorstore"])

@router.get('/', response_model=List[Vectorstore])
async def get_vectorstores(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):

    vector_stores = await repo_vectorstores.get_all_vectorstores(db, current_user)

    if not vector_stores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No vector stores found for the current user.'
        )
    
    return vector_stores

@router.get('/{name}', response_model=Vectorstore)
async def get_vectorstore_by_name(name: str,
                                  db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_user)):

    vector_store = await repo_vectorstores.get_vectorstore_by_name(name, db, current_user)

    if not vector_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Vector store with name "{name}" not found for the current user.'
        )
    
    return vector_store



