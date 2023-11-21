from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import magic
import os

from src.database.db import get_db


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        await websocket.send_text('Please upload your file')

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
