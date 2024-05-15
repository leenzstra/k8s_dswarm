import argparse
import sys
import socket
import time
import traceback
import cv2
import imagezmq
import simplejpeg

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host_hub', default='127.0.0.1')
    parser.add_argument('--port_hub', default=5555)
    args = parser.parse_args()

    hostname = socket.gethostname()
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)

    try:
        with imagezmq.ImageSender(connect_to=f"tcp://{args.host_hub}:{args.port_hub}") as sender:
            while True:
                ret, frame = cap.read()
                jpg_buffer = simplejpeg.encode_jpeg(frame, quality=95,
                                                    colorspace='BGR')
                sender.send_jpg(hostname, jpg_buffer)
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        print('Python error with no Exception handler:')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        sys.exit()
