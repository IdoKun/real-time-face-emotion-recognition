from flask import Flask, Response
import cv2
from fer import FER


app = Flask(__name__)
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("haarcascade_frontalface_alt.xml"))

@app.route('/')
def index():
    return "Root of the Real Time Facial Emotion Recognition app"
import cv2

detector = FER()


def gen(video):
    while True:
        success, image = video.read()
        result = detector.detect_emotions(image)
        camera_height, camera_weight, chanel = image.shape
        if  len(result)==0:
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            continue
        result =result[0]
        #        [{'box': [277, 90, 48, 63], 'emotions': {'angry': 0.02, 'disgust': 0.0, 'fear': 0.05, 'happy': 0.16, 'neutral': 0.09, 'sad': 0.27, 'surprise': 0.41}]
        box,emotions = result["box"],result["emotions"]
        for i,emotion in enumerate(emotions.keys()):
            cv2.putText(image, f"{emotion} : {emotions[emotion]} ",
                        (50, 50+i*camera_height//len(emotions.keys())),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        print(box,box.shape,emotions)
        (x, y, w, h) = box
        # frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # frame_gray = cv2.equalizeHist(frame_gray)

        # faces = face_cascade.detectMultiScale(frame_gray)
        center = (x + w//2, y + h//2)
        #cv2.putText(image, "X: " + str(center[0]) + " Y: " + str(center[1]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #faceROI = frame_gray[y:y+h, x:x+w]
        ret, jpeg = cv2.imencode('.jpg', image)

        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
