"""detect sex"""
import cv2

from cv_bridge import CvBridge

from PIL import Image

from detect_modules.detect_sex.model import Model

import numpy as np
from numpy import array, float32, asarray, uint8, argmax

import os

import shutil

from subprocess import check_output

from matplotlib import pyplot as plt

cascade_path = os.path.abspath(__file__).replace(
        'detect_modules/detect_sex/detect_sex.py', 'model/haarcascade_frontalface_default.xml'
        )

model_path = os.path.abspath(__file__).replace(
        'detect_modules/detect_sex/detect_sex.py', 'model/AlexlikeMSGD.model'
        )

sound_effect_path = os.path.abspath(__file__).replace(
        'detect_modules/detect_sex/detect_sex.py', 'model/camera-shutter3.wav'
        )

log_path = os.path.abspath(__file__).replace(
        'detect_modules/detect_sex/detect_sex.py', ''
        )

model = Model()

print(cascade_path, flush=True)

def detect_sex(image_data):
    reset_dir(log_path + "log")
    reset_dir(log_path + "male")
    reset_dir(log_path + "female")

    check_output(["aplay", sound_effect_path])

    gray_scale_image = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)

    while True:
        cascade = cv2.CascadeClassifier(cascade_path)
        face_rects = cascade.detectMultiScale(
            gray_scale_image,
            scaleFactor=1.2,
            minNeighbors=2,
            minSize=(2, 2)
        )

        if not(len(face_rects) == 0):
            break

    print("Found human : {0}".format(len(face_rects)), flush=True)

    woman = 0
    man = 0
    for i in range(0, len(face_rects)):
        
        left, top, width, height = face_rects[i]

        image = cv2.resize(image_data[top:top + height, left:left + width], (96, 96))

        file_name = "{0}/{1}.jpg".format(log_path + "log", i)

        #cv2.imwrite(file_name, image)

        plt.imshow(np.asarray(image))
        plt.savefig(file_name)

        transposed_image = (np.asarray(image).transpose((2, 0, 1)).astype(np.float32) / 255.).reshape(1, 3, 96, 96)

        model.load(model_path)

        data = model.predictor(transposed_image).data

        sex = argmax(array(data)[0])

        if sex == 0:
            woman += 1
        else:
            man += 1


    print("FEMALE , MALE : {0} , {1}".format(woman, man), flush=True)
    return str(woman), str(man)

def reset_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
