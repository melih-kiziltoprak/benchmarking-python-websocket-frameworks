# python3 -m uvicorn signal_server:app --host 0.0.0.0 --port 5001 --reload
import asyncio
from fastapi import FastAPI, WebSocket
import random
app = FastAPI()

async def sender_aiohttp(websocket: WebSocket):
    try:
        while True:
            data = str(random.random())
            await websocket.send_text(data)
            await asyncio.sleep(0.01)  # Adjust the sleep duration as needed
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed

async def acknowledgment_sender(websocket: WebSocket):
    try:
        while True:
            message = await websocket.receive_text()

            print(f"Received message from client: {message}")

            # Send acknowledgment back to the client
            if random.random() > 0.5:
                acknowledgment = f"Order FILLED: {message}"
                await websocket.send_text(acknowledgment)
            else:
                acknowledgment = f"Order UNFILLED: {message}"
                await websocket.send_text(acknowledgment)
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed

@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()

    sender_task = asyncio.create_task(sender_aiohttp(websocket))
    acknowledgment_sender_task = asyncio.create_task(acknowledgment_sender(websocket))

    try:
        await asyncio.gather(sender_task, acknowledgment_sender_task)
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed
    finally:
        await websocket.close()
