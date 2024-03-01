For aiohttp (io & latency):
- Open a terminal
- Go to the directory: “aiohttp_server”
- Run Python3 random_float_server.py (pip3 install any required libraries)
- Open another terminal
- Go to the directory: “aiohttp_client”
- Run Python3 latency_benchmark.py or io_benchmark.py (pip3 install any required libraries)


For aiohttp (signal):
- Open a terminal
- Go to the directory: “aiohttp_server”
- Run Python3 signal_server.py (pip3 install any required libraries)
- Open another terminal
- Go to the directory: “aiohttp_client”
- Run Python3 signal_benchmark.py (pip3 install any required libraries)


For fastapi (io & latency):
- Open a terminal
- Go to the directory: “fastapi _server”
- Run python3 -m uvicorn random_float_server:app --host 0.0.0.0 --port 5001 --reload
- Open another terminal
- Go to the directory: “aiohttp_client”
- Run Python3 latency_benchmark.py or io_benchmark.py (pip3 install any required libraries)


For fastapi (signal):
- Open a terminal
- Go to the directory: “fastapi _server”
- Run python3 -m uvicorn signal_server:app --host 0.0.0.0 --port 5001 --reload - Open another terminal
- Go to the directory: “aiohttp_client”
- Run Python3 signal_benchmark.py (pip3 install any required libraries)


For comparison charts (fastapi vs aiohttp)(precondition: programs above have been run):
- Open a terminal
- Go to the directory: “aiohttp_client” - Run python3 wrangler.py
- Run python3 wrangler.py
