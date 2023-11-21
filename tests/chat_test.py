import pytest
from httpx import AsyncWebSocket, WebSocketDisconnect
from fastapi.testclient import TestClient
from your_main_file import app
from src.services.document import


@pytest.mark.asyncio
async def test_websocket_chat():
    with TestClient(app) as client:
        async with client.websocket_connect("/chat") as websocket:
            pdf_contents = b"%PDF-1.0\n1 0 obj\n<< /Type /Catalog\n/Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages\n/Kids [3 0 R]\n/Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 300 144]\n/Resources\n<< /Font\n<< /F1\n<< /Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\n>>\n>>\n/Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 55 >>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello, this is a test PDF file.) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000056 00000 n \n0000000101 00000 n \n0000000238 00000 n \ntrailer\n<< /Size 5\n/Root 1 0 R\n>>\nstartxref\n293\n%%EOF\n"

            await websocket.send_bytes(pdf_contents)

            response = await websocket.receive_text()
            assert response == "Thank you! Now you can ask your question."

            await websocket.send_text("What is the answer?")

            response = await websocket.receive_text()
            assert "What is the answer?<br><br>" in response