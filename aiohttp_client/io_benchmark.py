import asyncio
import time
import aiohttp
import psutil
import matplotlib.pyplot as plt
import os
import csv
# Precondition: random_float_server.py is running

SERVER = input("Enter server you are using (0: aiohttp/ 1: fastapi): ")
while(SERVER != "0" and SERVER != "1"):
    SERVER = input("Enter 0 or 1!!! (0: aiohttp/1: fastapi): ")
if(SERVER == "0"):
    SERVER = "aiohttp"
else:
    SERVER = "fastapi"
    

MSG_CNT = 10000 # for using run_tests()
MSG_CNT_VALUES = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000] # for using run_tests_all()
MAX_CONN = 201
# Pick step count smaller than max_conn
STEP_COUNT = 20

STEP_SIZE = 1
if(STEP_COUNT < MAX_CONN):
    STEP_SIZE = int(MAX_CONN * (1 / STEP_COUNT))
STEP_SIZE = 25
OUTPUT_FILE = "io_benchmark.txt"

async def client_aiohttp(id = 0):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:5001/ws") as websocket:
            message_count = MSG_CNT
            start_time = time.time()
            
            for i in range(message_count): 
                message = await websocket.receive_str()
                with open(OUTPUT_FILE, 'a') as file:
                    file.write(f"id#{id}, data#{i}: {message}\n")
            latency = time.time() - start_time
            print(f"id#{id}: {message_count} messages recieved in {latency} seconds.")

            await session.close()





async def concurrent_aiohttp_test(num_connections):
    # clear file:
    with open(OUTPUT_FILE, 'w'):
        pass
    start_time = time.time()
    tasks = [asyncio.create_task(client_aiohttp(i)) for i in range(num_connections)]
    await asyncio.gather(*tasks)
    latency = time.time() - start_time
    print(str(num_connections) + " concurrent aiohttp test result: " + str(latency))
    return latency



async def run_tests():
    results = []
    
    # Loop over num_connections with a step of 5
    for num_connections in range(1, MAX_CONN, STEP_SIZE):
        try:
            result = await concurrent_aiohttp_test(num_connections)
            results.append((num_connections, result))
        except:
            print(f"Error in concurrent_aiohttp_test({num_connections}) !!!")
        #await asyncio.sleep(3)

    return results



async def main():
    for msg_cnt in MSG_CNT_VALUES:
        print(f"Running tests for MSG_CNT = {msg_cnt}")
        global MSG_CNT
        MSG_CNT = msg_cnt
        try: 
            results = await run_tests()
        except:
            print("Error in run_tests() !!!")
            
        output_directory = f'{SERVER}_io_output_graphs'
        os.makedirs(output_directory, exist_ok=True)

        x_values, y_values = zip(*results)
        plt.plot(x_values, y_values, marker='o')
        plt.title(f'Concurrent {SERVER} Test Results')
        plt.xlabel(f'Number of Connections - {MSG_CNT} Messages Per Connection')
        plt.ylabel(f'Seconds')

        plt.savefig(os.path.join(output_directory,  f'{MSG_CNT}msg_{MAX_CONN}conn.png'))
        plt.close()

        csv_filename = os.path.join(f'io_benchmark.csv')
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Connection_Count", "Seconds", "MSG_CNT", "SERVER", "MAX_CONN"])
            csv_writer.writerows(zip(x_values, y_values, [MSG_CNT] * len(x_values), [SERVER] * len(x_values), [MAX_CONN] * len(x_values)))

if __name__ == "__main__":
    asyncio.run(main())
