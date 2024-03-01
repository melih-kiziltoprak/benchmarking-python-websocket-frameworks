import asyncio
import aiohttp
from aiohttp import web
import random

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    try:
        while True:
            data = str(random.random())
            await ws.send_str(data)
    except aiohttp.web.HTTPException as ex:
        print(f"WebSocket connection closed with code {ex.status}")
    except asyncio.CancelledError:
        pass  # Ignore cancelled errors when the connection is closed
    finally:
        await ws.close()

app = web.Application()
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    web.run_app(app, port=5001)