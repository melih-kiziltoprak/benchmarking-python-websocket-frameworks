
import asyncio
import websockets

async def client_handler():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print("Received:", data)

asyncio.get_event_loop().run_until_complete(client_handler())
