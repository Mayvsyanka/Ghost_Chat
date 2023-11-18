from fastapi import WebSocket, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db


class WebSocketManager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket: WebSocket, db: Session = Depends(get_db)):
        await websocket.accept()
        self.active_connections.add(websocket)
        await websocket.send_text('Please upload your file')

    def disconnect(self, websocket: WebSocket, db: Session = Depends(get_db)):
        self.active_connections.remove(websocket)




