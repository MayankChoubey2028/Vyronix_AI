from ultralytics import YOLO


class ObjectDetector:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")


    def detect(self, frame):

        results = self.model(frame)

        detected_objects = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                label = self.model.names[class_id]

                detected_objects.append(label)

        return list(set(detected_objects))