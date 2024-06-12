#!/usr/bin/env python3

# Hello world server in python
# client says hello, server says world

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Received message: {message}")

    time.sleep(1)

    socket.send_string("World")
