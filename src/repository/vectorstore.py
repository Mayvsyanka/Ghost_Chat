from sqlalchemy import select
from sqlalchemy.orm import Session
from .users import User

from database.models import VectorStore


def get_all_vectorstores(db: Session, current_user: User):

    query = select(VectorStore).filter_by(user_id=current_user.id)
    query_res = db.execute(query)

    return query_res.scalars().all()

def get_vectorstore_by_name(name: str, db: Session, current_user: User):

    query = select(VectorStore).filter_by(name=name)
    query_res = db.execute(query)
    vectorstore_res = query_res.scalar_one_or_none()
    
    if vectorstore_res.user_id != current_user.id:
        return None
    
    return vectorstore_res