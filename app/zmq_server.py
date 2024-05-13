#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import numpy as np
import cv2
from detection import Detector

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

detector = Detector()

while True:
    frame_bytes = socket.recv()

    frame = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = frame.reshape(frame.shape[0], 1)

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)

    frame = detector.detect(frame)

    socket.send(frame.tobytes())
