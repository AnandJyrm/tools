#!/usr/bin/env python3

# Hello world client in python
# client says hello, server says world

import zmq

print("Connecting to server")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    print(f"Sending request {request}")
    socket.send_string("Hello")

    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")

