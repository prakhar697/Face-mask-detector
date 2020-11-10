# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:19:48 2020

@author: prakh
"""

from flask import Flask, render_template, Response
from deployment import VideoCamera

from gevent.pywsgi import WSGIServer

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app = Flask(__name__)

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    # defining server ip address and port
    app.run()