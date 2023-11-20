from langchain.memory import ChatMessageHistory

import pickle
import os

from sqlalchemy.orm import Session

from src.routes.users import get_profile

history = ChatMessageHistory()


async def save_chat_history(question, response, username: str, db: Session):

    user_profile = await get_profile(username, db)

    global history
    history.add_user_message(question)
    history.add_ai_message(response)
    full_history = history.messages

    output_folder = 'src/history'
    output_file = os.path.join(
        output_folder, f'{user_profile["username"]}_chat_history.pkl')

    with open(output_file, 'wb') as f:
        pickle.dump(full_history, f)

    return full_history
