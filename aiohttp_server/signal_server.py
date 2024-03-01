import asyncio
import aiohttp
from aiohttp import web
import random

async def sender_aiohttp(ws):
    try:
        while True:
            data = str(random.random())
            await ws.send_str(data)
            await asyncio.sleep(0.01)  # Adjust the sleep duration as needed
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed

async def acknowledgment_sender(ws):
    try:
        while True:
            msg = await ws.receive()
            if ws.closed:
                break

            if msg.type == aiohttp.WSMsgType.TEXT:
                message = msg.data
                if not message:
                    break

                print(f"Received message from client: {message}")

                # Send acknowledgment back to the client
                if random.random() > 0.5:
                    acknowledgment = f"Order FILLED: {message}"
                    await ws.send_str(acknowledgment)
                else:
                    acknowledgment = f"Order UNFILLED: {message}"
                    await ws.send_str(acknowledgment)
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    sender_task = asyncio.create_task(sender_aiohttp(ws))
    acknowledgment_sender_task = asyncio.create_task(acknowledgment_sender(ws))

    try:
        await asyncio.gather(sender_task, acknowledgment_sender_task)
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed
    finally:
        await ws.close()

app = web.Application()
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    web.run_app(app, port=5001)
