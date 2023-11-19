"""Module for chat operations"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import magic

import os

from src.database.db import get_db
from src.services.chat import WebSocketManager
from src.services.document import save_received_file
from src.services.request import request_answer_from_llm
from src.services.vectorstore import doc_to_vectorstore
from src.html.chat import html


router = APIRouter(tags=["chat"])

ws_manager = WebSocketManager()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket,  db: Session = Depends(get_db)):
    await ws_manager.connect(websocket)
    file_received = False

    try:
        while True:
            data = await websocket.receive()
            if "bytes" in data:
                received_file = data["bytes"]
                try:
                    file_type = magic.from_buffer(received_file, mime=True)
                    if file_type != "application/pdf":
                        await websocket.send_text("Invalid file format. Only PDF files are allowed.")
                    else:
                        file_path = os.path.join(
                            UPLOAD_DIR, "received_file.pdf")
                        file_received = True
                        await websocket.send_text("Thank you! Now you can ask your question.")
                        await save_received_file(received_file, file_path)
                        question = await websocket.receive_text()
                        vectorstore = await doc_to_vectorstore(file_path)
                        answer = request_answer_from_llm(vectorstore, question)
                        await websocket.send_text(f"{question}<br><br> {answer}")
                except Exception as e:
                    await websocket.send_text(f"Error processing file - {str(e)}")

            elif file_received:
                while True:
                    question = await websocket.receive_text()
                    if question == "disconnect":
                        await websocket.send_text("Disconnected")
                        ws_manager.disconnect(websocket)
                    else:
                        await websocket.send_text(f"{question}<br><br> miu")

    except WebSocketDisconnect:
        pass
    except Exception as error:
        await websocket.send_text(f"Unexpected error - {str(error)}")
    finally:
        ws_manager.disconnect(websocket)


@router.get('/chat', response_class=HTMLResponse)
async def get():
    return HTMLResponse(html)


