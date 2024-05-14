import cv2
import socket
import math
import pickle
import sys
import numpy as np

max_length = 65000
host = sys.argv[1]
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)


def recv_back():
    data, _ = sock.recvfrom(max_length)

    if len(data) < 100:
        frame_info = pickle.loads(data)
        if frame_info:
            nums_of_packs = frame_info["packs"]
            print(nums_of_packs)

            for i in range(nums_of_packs):
                data, _ = sock.recvfrom(max_length)

                if i == 0:
                    print('new buffer')
                    buffer = data
                else:
                    print('add buffer')
                    buffer += data

            print(len(buffer))
            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape((height, width, channels))
            print(frame)

            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            # frame = cv2.flip(frame, 1)

            return frame
            
ret, frame = cap.read()
height, width, channels = frame.shape

while ret:
    # compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        frame_info = {"packs": num_of_packs}

        # send the number of packs to be expected
        sock.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length

        for i in range(num_of_packs):
            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (host, port))

        # frame = recv_back()
        # print("recv back ", frame)
        # if frame is not None and type(frame) == np.ndarray:
        #     cv2.imshow("Main", frame)
        #     if cv2.waitKey(1) == 27:
        #         break


    ret, frame = cap.read()

