import asyncio
import websockets
import random

async def server_handler(websocket, path):
    while True:
        data  = str(random.random())
        await websocket.send(data)
        #await asyncio.sleep(0.001)

start_server = websockets.serve(server_handler, "localhost", 5001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
