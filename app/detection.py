from ultralytics import YOLO
import cvzone
import math


class Detector:
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus",
                  "train", "truck", "boat", "cell phone"]

    def __init__(self, model="yolov8n.pt"):
        self.model = YOLO(model)

    def detect(self, frame):
        results = self.model(frame)
        for r in results:
            boxes = r.boxes
            for box in boxes:

                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2-x1, y2-y1
                cvzone.cornerRect(frame, (x1, y1, w, h))

                # Confidence
                conf = math.ceil((box.conf[0] * 100))/100

                # Class Name
                cls = int(box.cls[0])

                cvzone.putTextRect(frame, f'{Detector.classNames[cls]} {
                                   conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

        return frame
