"""Module for chat operations"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
from src.services.chat import WebSocketManager

# from src.database.models import Document

from src.conf.config import settings

router = APIRouter(prefix='/chat', tags=["Chat"])
security = HTTPBearer()

manager = WebSocketManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("Question: "):
                question = data[len("Question: "):]
                await manager.process_question(websocket, question)
            else:
                await manager.notify('Sorry, an error occurred')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.notify("User left the chat.")
