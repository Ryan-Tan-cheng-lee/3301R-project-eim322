import sys
import os
sys.path.append(os.getcwd())

import socketio
import bluetooth
import constants

sio = socketio.Client()

def simulate():
    pass


if __name__ == '__main__':
    address = os.getenv(constants.ADDRESS_ENV_VAR, 'http://127.0.0.1')
    port = os.getenv(constants.PORT_ENV_VAR, '5000')
    num_of_sensors = os.getenv(constants.NUM_OF_SENSORS_ENV_VAR, '4')
    print(f'Address: {address}')
    print(f'Port: {port}')
    print(f'Number of sensors: {num_of_sensors}')

    try:
        sio.connect(f'{address}:{port}/')
    except socketio.exceptions.ConnectionError:
        print("Unable to connect to socket.")
        exit()

    
    

