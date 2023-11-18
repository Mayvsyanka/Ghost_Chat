from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from sqlalchemy.orm import Session

import os
import pickle

from src.services.request import load_vectorstore, request_answer_from_llm


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        await websocket.send_text('Please upload your file')

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def generate_answer(self, question: str):
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.endswith(".pkl"):
                vectorstore_path = os.path.join(cwd, file)
        with open(vectorstore_path, "rb") as f:
            vectorstore = pickle.load(f)
        answer, cb = request_answer_from_llm(vectorstore, question)
        return answer
