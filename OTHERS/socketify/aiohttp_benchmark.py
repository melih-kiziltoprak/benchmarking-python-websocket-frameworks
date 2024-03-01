import asyncio
import time
import aiohttp
import psutil

MSG_CNT = 1000
CONN_CNT = 1

async def client_aiohttp(id = 0):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:3000/ws") as websocket:
            message_count = MSG_CNT
            start_time = time.time()
            for i in range(message_count): 
                message = await websocket.receive_str()
                """
                with open("aiohttp.txt", 'a') as file:
                    file.write(f"id#{id}, data#{i}: {message}\n")
                """
            latency = time.time() - start_time
            print(f"id#{id}: {message_count} messages recieved in {latency} seconds.")
            await session.close()

async def parallel_aiohttp_test(num_connections):
    with open("aiohttp.txt", 'w'):
        pass
    start_time = time.time()
    #uri = "ws://localhost:5001"

    for i in range(10):
        await client_aiohttp(i)
    #tasks = [asyncio.create_task(client_aiohttp(i)) for i in range(num_connections)]
    #await asyncio.gather(*tasks)
    latency = time.time() - start_time
    #cpu_utilization = psutil.cpu_percent(interval=latency)
    #print(str(num_connections) + " parallel aiohttp test result: " + str(latency) + "\n" + str(cpu_utilization)+ "%")
    print(str(num_connections) + " parallel aiohttp test result: " + str(latency))

    #initial_memory = get_memory_usage()

async def main():
    with open("aiohttp.txt", 'w'):
        pass

    print("\nTesting scalability with aiohttp library:")
    num_connections = CONN_CNT
    while (True):
        try: 
            await parallel_aiohttp_test(num_connections)
            break
        except:
            num_connections = (int(num_connections * 0.95))
            print("new num of connections: " + str(num_connections))
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
