import time
import psutil
import asyncio
import websockets
from websockets import connect

MSG_CNT = 1000
CONN_CNT = 10

async def websockets_test(id = 0):
    uri = "ws://localhost:3000"
    try:
        async with connect(uri) as websocket:
            message_count = MSG_CNT
            start_time = time.time()
            for i in range(message_count): 
                message = await websocket.recv()
                with open("websockets.txt", 'a') as file:
                    file.write(f"id#{id}, data#{i}: {message}\n")
            latency = time.time() - start_time
            print(f"id#{id}: {message_count} messages recieved in {latency} seconds.")
    finally:
        await websocket.close()

async def concurrent_websockets_test(num_connections):
    with open("websockets.txt", 'w'):
        pass
    start_time = time.time()
    tasks = [asyncio.create_task(websockets_test(i)) for i in range(num_connections)]
    await asyncio.gather(*tasks)
    latency = time.time() - start_time
    #cpu_utilization = psutil.cpu_percent(interval=latency)
    #print(str(num_connections) + " concurrent websockets test result: " + str(latency) + "\n" + str(cpu_utilization)+ "%")
    print(str(num_connections) + " concurrent websockets test result: " + str(latency)) 

async def main():
    with open("aiohttp.txt", 'w'):
        pass

    print("\nTesting scalability with websockets library:")
    num_connections = CONN_CNT
    while (True):
        try: 
            await concurrent_websockets_test(num_connections)
            break
        except:
            num_connections = (int(num_connections * 0.95))
            print("new num of connections: " + str(num_connections))
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
