import math
import cv2
import socket
import pickle
import numpy as np
from detection import Detector

host = "127.0.0.1"
port = 5000
max_length = 65000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

frame_info = None
buffer = None
frame = None

detector = Detector()


def send_back(frame, address):
    # convert to byte array
    buffer = frame.tobytes()
    # get size of the frame
    buffer_size = len(buffer)

    num_of_packs = 1
    if buffer_size > max_length:
        num_of_packs = math.ceil(buffer_size/max_length)

    frame_info = {"packs": num_of_packs}

    # send the number of packs to be expected
    sock.sendto(pickle.dumps(frame_info), address)

    left = 0
    right = max_length

    for i in range(num_of_packs):
        # truncate data to send
        data = buffer[left:right]
        left = right
        right += max_length

        # send the frames accordingly
        sock.sendto(data, address)

    print("Server: sent", num_of_packs)

def run():
    print("waiting for connection")

    while True:
        data, address = sock.recvfrom(max_length)

        if len(data) < 100:
            frame_info = pickle.loads(data)

            if frame_info:
                nums_of_packs = frame_info["packs"]

                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)

                    if i == 0:
                        buffer = data
                    else:
                        buffer += data

                frame = np.frombuffer(buffer, dtype=np.uint8)
                frame = frame.reshape(frame.shape[0], 1)

                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame = cv2.flip(frame, 1)

                frame = detector.detect(frame)

                send_back(frame, address)

if __name__ == "__main__":
    run()



