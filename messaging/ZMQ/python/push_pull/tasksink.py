#!/usr/bin/env python3
# Task sink

import sys
import time
import zmq

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

s = receiver.recv()

tstart = time.time()

for task_nbr in range(100):
    s = receiver.recv()
    if task_nbr % 10 == 0:
        sys.stdout.write(':')
    else:
        sys.stdout.write('.')
    sys.stdout.flush()

tend = time.time()
print(f"Total elapsed time: {(tend-tstart)*1000} msec")

