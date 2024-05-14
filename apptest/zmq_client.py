#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import cv2
import numpy as np

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

cap = cv2.VideoCapture(0)

def send_frame(frame):
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        buffer = buffer.tobytes()

    socket.send(buffer)

while True:
    ret, frame = cap.read()
    if ret == False:
        break

    frame_shape = frame.shape

    send_frame(frame)

    detected = socket.recv()

    frame = np.frombuffer(detected, dtype=np.uint8)
    frame = frame.reshape(frame_shape)
    print(frame.shape)

    # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    if frame is not None and type(frame) == np.ndarray:
        cv2.imshow("Main", frame)
        if cv2.waitKey(1) == 27:
            break
