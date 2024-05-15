import argparse
import cv2
import imagezmq
import simplejpeg
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from detection import Detector


def sendImagesToWeb():
    while True:
        sent_from, jpg_buffer = hub.recv_jpg()
        frame = simplejpeg.decode_jpeg(jpg_buffer, colorspace='BGR')

        frame = detector.detect(frame)

        jpg = cv2.imencode('.jpg', frame)[1]
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tobytes()+b'\r\n\r\n'


@Request.application
def application(request):
    return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port_hub', default=5555)
    parser.add_argument('--port_web', default=4000)
    args = parser.parse_args()

    global detector, hub
    detector = Detector()
    hub = imagezmq.ImageHub(open_port=f"tcp://{args.host}:{args.port_hub}")

    run_simple(args.host, int(args.port_web), application)
