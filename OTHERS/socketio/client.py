import socketio

sio = socketio.Client()

message_count = 0
max_messages = 1000

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def message(data):
    global message_count
    message_count += 1
    with open("socketio.txt", 'a') as file:
        file.write(f"id#{id}, data#{message_count}: {data}\n")

    if message_count >= max_messages:
        print(f"Received {max_messages} messages. Disconnecting.")
        sio.disconnect()

try:
    sio.connect('http://localhost:5002')
    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
