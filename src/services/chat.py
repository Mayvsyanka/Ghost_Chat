from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

import os
import pickle
from src.database.models import File

from src.services.request import request_answer_from_llm, load_vectorstore


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, db: Session, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, db: Session, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def notify(self, db: Session, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


    async def process_question(self, db: Session, websocket: WebSocket, question: str):
        answer = generate_answer(question)
        await websocket.send_text(f"Bot: {answer}")


    def generate_answer(self, db: Session, question: str,  ) -> str:
        #код для генерації відповіді за допомогою нейромережі
        file_name = None #отримати через бд
        path_to_vectorstore ="src/store/"+ file_name +".pkl"
    
        vectorstore = load_vectorstore(path_to_vectorstore)

        answer = request_answer_from_llm(vectorstore, question)
        
        return answer

