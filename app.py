from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected')

@socketio.on('start')
def handle_start():
    print('Start')

@socketio.on('log')
def handle_log(data):
    print('Log: ' + str(data)) 

if __name__ == '__main__':
    socketio.run(app)