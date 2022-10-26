# Loads a yolov5 model to perform real time inference on a webcam

# Imports
import numpy as np
import cv2
import os
import torch


# Basic
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def live_feels(path_to_model='rtfer/models/yolov5_custom/',exp="exp0",path_to_weight=None):
    path_to_weight = os.path.join(path_to_model,exp,"best.pt") if path_to_weight == None else path_to_weight
    print(f"Loading weight  in {path_to_weight}")
    model = torch.hub.load('ultralytics/yolov5'
                           ,"custom"
                           ,path_to_weight)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        # Make detections
        results = model(frame)

        cv2.imshow('YOLO', np.squeeze(results.render()))

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
