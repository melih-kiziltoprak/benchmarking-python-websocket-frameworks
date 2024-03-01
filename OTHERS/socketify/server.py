"""
from socketify import App, AppOptions, OpCode, CompressOptions
import random

def ws_open(ws):
    print('A WebSocket got connected!')
    ws.send("Hello World!", OpCode.TEXT)

def ws_message(ws, message, opcode):
    # Ok is false if backpressure was built up, wait for drain
    ok = ws.send(message, opcode)

app = App()    
app.ws("/*", {
    'compression': CompressOptions.SHARED_COMPRESSOR,
    'max_payload_length': 16 * 1024 * 1024,
    'idle_timeout': 12,
    'open': ws_open,
    'message': ws_message,
    'drain': lambda ws: print('WebSocket backpressure: %i' % ws.get_buffered_amount()),
    'close': lambda ws, code, message: print('WebSocket closed')
})
app.any("/", lambda res, req: res.end("Nothing to see here!'"))
app.listen(3000, lambda config: print("Listening on port http://localhost:%d now\n" % (config.port)))
app.run()
"""

from socketify import App, OpCode, CompressOptions
import asyncio
import random

async def ws_handler(ws):
    print('A WebSocket got connected!')
    try:
        while True:
            #data = str(random.random())
            ok = ws.send("data", OpCode.TEXT)
            if not ok:
                print('WebSocket backpressure: %i' % ws.get_buffered_amount())
            #await asyncio.sleep(0.001)
    finally:
        await ws.close()
        print('WebSocket closed')
"""
i = 0
while(True):
    try: 
"""
app = App()

app.ws("/*", {
    'compression': CompressOptions.SHARED_COMPRESSOR,
    'max_payload_length': 16 * 1024 * 1024 * 1024 * 1024,
    'idle_timeout': 120,
    'open': lambda ws: asyncio.create_task(ws_handler(ws)),
    'message': lambda ws, message, opcode: None,  # No specific message handling
    #'drain': lambda ws: print('WebSocket backpressure: %i' % ws.get_buffered_amount()),
    'close': lambda ws, code, message: print('WebSocket closed')
})

app.any("/", lambda res, req: res.end("Nothing to see here!'"))

app.listen(3000, lambda config: print("Listening on port http://localhost:%d now\n" % (config.port)))

app.run()
"""
    except:
        print("problem        " + str(i))
        i += 1
"""