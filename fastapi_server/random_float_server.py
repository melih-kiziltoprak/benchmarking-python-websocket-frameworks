from fastapi import FastAPI, WebSocket
import asyncio
import random

# python3 -m uvicorn random_float_server:app --host 0.0.0.0 --port 5001 --reload

app = FastAPI()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data  = str(random.random())
        await websocket.send_text(data)
