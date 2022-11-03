# You can run this app in local with your terminal with
# $ flask --app app run

from flask import Flask, Response, render_template
import cv2
import os
import torch
import numpy as np


app = Flask(__name__)

#face_cascade = cv2.CascadeClassifier()
#face_cascade.load(cv2.samples.findFile("haarcascade_frontalface_alt.xml"))
# model = torch.hub.load('ultralytics/yolov5'
#                            ,"custom"
#                            ,os.path.join("rtfer/models/yolov5_custom/","exp0","best.pt"))



@app.route('/')
def index():
    return render_template("home.html")

def gen():
    video = cv2.VideoCapture(0)
    while True:
        success, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        result = model(image)
        # NEVER USE result.show() IT OPEN A WINDOW FOR EACH IMAGE
        image_numpy = np.squeeze(result.render())
        ret, jpeg = cv2.imencode('.jpeg', image_numpy)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
