# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:16:42 2020

@author: prakh
"""

import numpy as np
import cv2

import tensorflow as tf

from tensorflow.keras.models import load_model

classifier = load_model('model.h5')
size = 4
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
label_dict = {0:'WITHOUT MASK',1:'WITH MASK'}
color_dict = {0:(0,0,255),1:(0,255,0)}

class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()


    def get_frame(self):
        t = 0
        # extracting frames
        
        (rval, im) = self.video.read()
        im = cv2.flip(im, 1, 1)
        mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))
        faces = face_cascade.detectMultiScale(mini)
        for f in faces:
            (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
            #Save just the rectangle faces in SubRecFaces
            face_img = im[y:y+h, x:x+w]
            resized=cv2.resize(face_img,(224,224))
            normalized=resized/255.0
            reshaped=np.reshape(normalized,(1,224,224,3))
            reshaped = np.vstack([reshaped])
            result = classifier.predict(reshaped)

            label = result[0,0]
            if label > 0.5:
                t = 1 
            else:
                t = 0
            
            cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[t],2)
            cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[t],-1)
            cv2.putText(im, label_dict[t], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', im)
        return jpeg.tobytes()