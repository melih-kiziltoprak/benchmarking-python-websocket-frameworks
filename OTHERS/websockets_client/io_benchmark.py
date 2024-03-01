import time
import psutil
import asyncio
import websockets
from websockets import connect
import matplotlib.pyplot as plt
import os
import csv
SERVER = "websockets"

MSG_CNT_VALUES = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000] 
MAX_CONN = 502
MSG_CNT = 0 
STEP_SIZE = 100

async def websockets_test(id = 0):
    uri = "ws://localhost:5001"
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
    print(str(num_connections) + " concurrent websockets test result: " + str(latency)) 

async def run_tests():
    results = []
    for num_connections in range(1, MAX_CONN, STEP_SIZE):
        try:
            result = await concurrent_websockets_test(num_connections)
            results.append((num_connections, result))
        except:
            print(f"Error in concurrent_websockets_test({num_connections}) !!!")

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

        output_directory = f'{SERVER}_latency_output_graphs'
        os.makedirs(output_directory, exist_ok=True)

        x_values, y_values = zip(*results)
        plt.plot(x_values, y_values, marker='o')
        plt.title(f'Concurrent {SERVER} Test Results')
        plt.xlabel(f'Number of Connections - {MSG_CNT} Messages Per Connection')
        plt.ylabel(f'Seconds')
        plt.savefig(os.path.join(output_directory,  f'{MSG_CNT}msg_{MAX_CONN}conn.png')) 
        plt.close()

        csv_filename = 'benchmark.csv'
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Connection_Count", "Seconds", "MSG_CNT", "SERVER", "MAX_CONN"])
            csv_writer.writerows(zip(x_values, y_values, [MSG_CNT] * len(x_values), [SERVER] * len(x_values), [MAX_CONN] * len(x_values)))


if __name__ == "__main__":
    asyncio.run(main())
