#!/usr/bin/env python3
# PUB SUB client

import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server.")
socket.connect("tcp://localhost:5556")

zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

total_temp = 0
for update_nbr in range(100):
    string = socket.recv_string()
    print(string)
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print(f"Average temperature for zip code {zip_filter} was {total_temp /(update_nbr + 1)} F")
