from flask import Flask, render_template
from flask_socketio import SocketIO, send
import random
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

"""
@socketio.on('message')
def handle_message(message):
    #print('Received message:', message)
"""

def server_task():
    while True:
        data = str(random.random())
        socketio.emit('message', data)
        socketio.sleep(0.01)

if __name__ == '__main__':
    import eventlet
    eventlet.spawn(server_task)
    socketio.run(app, host='localhost', port=5002)
