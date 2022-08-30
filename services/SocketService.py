from typing import Union
import socketio
import constants
import json

class SocketService():
    def __init__(self, host: str=constants.DEFAULT_ADDRESS, port: Union[int, str]=constants.DEFAULT_PORT):
        self.sio = socketio.Client()

        try:
            self.sio.connect(f'{host}:{str(port)}')
        except socketio.exceptions.ConnectionError:
            # print("Unable to connect to socket")
            raise Exception("Unable to connect to socket")
        
    def emit(self, event=constants.DEFAULT_READING_EMIT_EVENT):
        def decorate(func):
            def emit(*args):
                message = func(*args)
                try:
                    self.sio.emit(event, json.dumps(message))
                except socketio.exceptions.ConnectionError:
                    # print(f"Unable to emit {event}, {message}")
                    self.sio.disconnect()
                    raise Exception(f"Unable to emit {event}, {message}")
            return emit
        return decorate
    
    def disconnect(self):
        self.sio.disconnect()



