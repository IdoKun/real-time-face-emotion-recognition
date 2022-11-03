# JINJA CHEATSHEAT
# {% ... %} for Statements
# {{ ... }} for Expressions to print to the template output
# {# ... #} for Comments not included in the template output
# # ... ## for Line Statements

import cv2
import os
import torch
import numpy as np
import datetime,time

from flask import Flask, redirect, url_for, request,render_template,Response
app = Flask(__name__)


global camera


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route('/login',methods = ['POST', 'GET'])
def login():
    return render_template("login.html")
    if request.method == 'POST':
        user = "bob"#request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = "bob"#request.args.get('nm')
        return redirect(url_for('success',name = user))

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/hello/<user>")
def hello(user):
    return render_template("hello.html",name=user)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/credits")
def credits():
    return render_template("credits.html")


@app.route("/ex_index", methods=['GET', 'POST'])
def ex_index():
    '''404 NOT WORKING '''
    if request.method == "POST":
        print(request.form.keys())
        return render_template("ex_button.html")
    # elif request.method == 'GET':
    #     return render_template('ex_button.html', form=None)
    print("post",request.form.keys())
    return render_template("ex_button.html")


face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("haarcascade_frontalface_alt.xml"))
model = torch.hub.load('ultralytics/yolov5'
                           ,"custom"
                           ,os.path.join("rtfer/models/yolov5_custom/","exp0","best.pt"))



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

@app.route('/requests',methods=['POST','GET'])
def tasks():
    pass
    # global switch,camera
    # if request.method == 'POST':
    #     if request.form.get('click') == 'Capture':
    #         global capture
    #         capture=1
    #     elif  request.form.get('grey') == 'Grey':
    #         global grey
    #         grey=not grey
    #     elif  request.form.get('neg') == 'Negative':
    #         global neg
    #         neg=not neg
    #     elif  request.form.get('face') == 'Face Only':
    #         global face
    #         face=not face
    #         if(face):
    #             time.sleep(4)
    #     elif  request.form.get('stop') == 'Stop/Start':

    #         if(switch==1):
    #             switch=0
    #             camera.release()
    #             cv2.destroyAllWindows()

    #         else:
    #             camera = cv2.VideoCapture(0)
    #             switch=1
    #     elif  request.form.get('rec') == 'Start/Stop Recording':
    #         global rec, out
    #         rec= not rec
    #         if(rec):
    #             now=datetime.datetime.now()
    #             fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #             out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
    #             #Start new thread for recording the video
    #             thread = Thread(target = record, args=[out,])
    #             thread.start()
    #         elif(rec==False):
    #             out.release()


@app.route('/live')
def live():
    return render_template("live.html")



if __name__ == '__main__':
   app.run(debug = True)
