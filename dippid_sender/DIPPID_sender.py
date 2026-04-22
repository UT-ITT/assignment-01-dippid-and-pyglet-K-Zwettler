import socket
import time
import json
import numpy as np
import random

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# different frequencies for X Y and Z axis
freq1 = 5
freq2 = 10
freq3 = 15

# timer for toggling the value for the button
start_time = time.time()
next_toggle_time = random.uniform(1,5)
toggle_timer = time.time()

button_1 = 0

while True:
    t = time.time() - start_time

    # after random amount of time, toggle the button value
    if (time.time() - toggle_timer >= next_toggle_time):
        button_1 = 1 - button_1
        toggle_timer = time.time()
        next_toggle_time = random.uniform(1,5)

    data = {
        "accelerometer": {
            # different sine values for different axes
            "X": float(np.sin(2*np.pi*freq1*t)),
            "Y": float(np.sin(2*np.pi*freq2*t)),
            "Z": float(np.sin(2*np.pi*freq3*t))
        },
        "button_1": button_1
    }

    # send data to address
    sock.sendto(json.dumps(data).encode(), (IP, PORT))

    print(data)
    time.sleep(0.3)
