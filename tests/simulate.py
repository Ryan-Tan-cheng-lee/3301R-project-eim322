import sys
import os
sys.path.append(os.getcwd())

from random import random
import socketio
import constants
import time
import json
from threading import Thread
from models import Reading
from services import SocketService

reading_attr = []
freq = 1

try:
    socketService = SocketService()
except Exception as e:
    print(e)
    exit()


@socketService.emit()
def getReading(message):
    return message

def simulate(**kwargs):
    # sio = socketio.Client()

    # try:
    #     sio.connect(f'{address}:{port}', namespaces=['/'])
    # except socketio.exceptions.ConnectionError:
    #     print("Unable to connect to socket.")
    #     return()

    reading_attr = json.loads(os.getenv(constants.READING_ATTR_ENV_VAR, constants.DEFAULT_ATTR))[constants.READING_ATTR_VAR_NAME]
    start = time.time()
    freq = float(os.getenv(constants.FREQ_ENV_VAR, constants.DEFAULT_FREQ))
    id = "null"
    duration = float(os.getenv('SIM_DURATION', 20))
    num_of_sensors = int(os.getenv(constants.NUM_OF_SENSORS_ENV_VAR, constants.DEFAULT_NUM_OF_SENSORS))
    mode = os.getenv(constants.SENSOR_MODE_ENV_VAR, constants.DEFAULT_SENSOR_MODE)
    
    if kwargs:
        id_name = list(kwargs.keys())[0] #First argument ALWAYS ID
        id = kwargs[id_name]
       
    while duration > time.time() - start:
        if mode == 'INDIVIDUAL':
            reading = {id_name: id}
            reading = reading | {attr: random() * 90 for attr in reading_attr}
            # print(reading)
            reading = Reading(**reading)
            
            try:
                # sio.emit(constants.DEFAULT_READING_EMIT_EVENT, reading.to_json())
                getReading(reading)
            except Exception as e:
                print(e)
                # sio.disconnect()
                return()

        elif mode == 'MASTER':
            reading = {f'sensor{i}': random() * 90 for i in range(num_of_sensors)}
            # print(reading)
            try:
                # sio.emit(constants.DEFAULT_READING_EMIT_EVENT, json.dumps(reading))
                getReading(reading)
            except Exception as e:
                print(e)
                # sio.disconnect()
                return()
        else:
            # sio.disconnect()
            raise Exception('Mode is either INDIVIDUAL or MASTER')
           
        time.sleep(1/freq)

    # sio.disconnect()
    socketService.disconnect()

def create_threads():
    threads = []
    num_of_sensors = int(os.getenv(constants.NUM_OF_SENSORS_ENV_VAR, constants.DEFAULT_NUM_OF_SENSORS))
    for i in range(num_of_sensors):
        t = Thread(target=simulate, args=[], kwargs={'id': f'thread{i}'})
        threads.append(t)
    return threads


if __name__ == '__main__':
    address = os.getenv(constants.ADDRESS_ENV_VAR, constants.DEFAULT_ADDRESS)
    port = os.getenv(constants.PORT_ENV_VAR, constants.DEFAULT_PORT)
    mode = os.getenv(constants.SENSOR_MODE_ENV_VAR, constants.DEFAULT_SENSOR_MODE)
    reading_attr = json.loads(os.getenv(constants.READING_ATTR_ENV_VAR, constants.DEFAULT_ATTR))[constants.READING_ATTR_VAR_NAME]
    freq = float(os.getenv(constants.FREQ_ENV_VAR, constants.DEFAULT_FREQ))
    duration = float(os.getenv('SIM_DURATION', 20))
    num_of_sensors = int(os.getenv(constants.NUM_OF_SENSORS_ENV_VAR, constants.DEFAULT_NUM_OF_SENSORS))
    mode = os.getenv(constants.SENSOR_MODE_ENV_VAR, constants.DEFAULT_SENSOR_MODE)
    
    print(f'Address: {address}')
    print(f'Port: {port}')
    print(f'Number of sensors: {num_of_sensors}')
    print(f'Attributes: {reading_attr}')
    print(f'Emit frequency: {freq}')
    print(f'Duration: {duration}')
    print(f'Mode: {mode}')

    if mode == "MASTER":
        simulate()
        exit()
    elif mode == "INDIVIDUAL":
        threads = create_threads()
    else:
        raise Exception('Mode is either INDIVIDUAL or MASTER')

    # if threads:
    #     for thread in threads:
    #         thread.start()
    #     for thread in threads:
    #         thread.join()



    
    

