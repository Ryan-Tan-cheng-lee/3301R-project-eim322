import sys
import os
from venv import create
sys.path.append(os.getcwd())

from random import random
import socketio
import bluetooth
import constants
import time
import json
from threading import Thread
from models import Reading

reading_attr = []
freq = 1

def simulate(duration, **kwargs):
    sio = socketio.Client()

    try:
        sio.connect(f'{address}:{port}/')
    except socketio.exceptions.ConnectionError:
        print("Unable to connect to socket.")
        return()

    start = time.time()
    print(kwargs.keys())
    id_name = list(kwargs.keys())[0]
    id = kwargs[id_name]
    while duration > time.time() - start:
        reading = {id_name: id}
        reading = reading | {attr: random() * 90 for attr in reading_attr}
        print(reading)
        reading = Reading(**reading)

        try:
            sio.emit(constants.DEFAULT_READING_EMIT_EVENT, reading.to_json())
        except:
            return()

        time.sleep(1/freq)

    sio.disconnect()

def create_threads(num_of_sensors, duration):
    threads = []
    for i in range(num_of_sensors):
        t = Thread(target=simulate, args=[duration], kwargs={'id': f'thread{i}'})
        threads.append(t)
    return threads


if __name__ == '__main__':
    address = os.getenv(constants.ADDRESS_ENV_VAR, constants.DEFAULT_ADDRESS)
    port = os.getenv(constants.PORT_ENV_VAR, constants.DEFAULT_PORT)
    num_of_sensors = int(os.getenv(constants.NUM_OF_SENSORS_ENV_VAR, constants.DEFAULT_NUM_OF_SENSORS))
    reading_attr = json.loads(os.getenv(constants.READING_ATTR_ENV_VAR, constants.DEFAULT_ATTR))[constants.READING_ATTR_VAR_NAME]
    freq = float(os.getenv(constants.FREQ_ENV_VAR, constants.DEFAULT_FREQ))
    duration = float(os.getenv('SIM_DURATION', 20))
    print(f'Address: {address}')
    print(f'Port: {port}')
    print(f'Number of sensors: {num_of_sensors}')
    print(f'Attributes: {reading_attr}')
    print(f'Emit frequency: {freq}')

    threads = create_threads(num_of_sensors, duration=20)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()



    
    

