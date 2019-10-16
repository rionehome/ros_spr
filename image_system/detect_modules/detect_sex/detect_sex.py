"""detect sex"""
import cv2

from cv_bridge import CvBridge

from face_recognition import face_locations

from PIL import Image

from matplotlib import pyplot as plt

from detect_modules.detect_sex.classifier import detect_human_sex
from detect_modules.detect_human.entity import params

import numpy as np
from numpy import array, float32, asarray, uint8

import os

cascade_path = os.path.abspath(__file__).replace(
        'detect_modules/detect_sex/detect_sex.py', 'model/haarcascade_frontalface_default.xml'
        )

print(cascade_path, flush=True)

cascade = cv2.CascadeClassifier(cascade_path)


def detect_sex(image_data):
    facerects = face_locations(image_data, model="cnn")
    print("Found human : {0}".format(len(facerects)), flush=True)

    if len(facerects) > 0:
        woman = 0
        man = 0
        for top, right, bottom, left in facerects:
            facerect = (left, top, right - left, bottom - top)
            cropped_face, face_left_top = crop_face(image_data, facerect)
            cropped_face = array(cv2.resize(cropped_face, (96, 96)), dtype=float32)

            sex = detect_human_sex(cropped_face)

            print("SEX : {0}".format(sex), flush=True)

            if sex == 0:
                woman += 1
            elif sex == 1:
                man += 1
            else:
                pass
        return str(woman), str(man)

    else:
        return "0", "0"


def crop_face(img, rect):
    orig_img_h, orig_img_w, _ = img.shape
    crop_center_x = rect[0] + rect[2] / 2
    crop_center_y = rect[1] + rect[3] / 2
    crop_width = rect[2] * params['face_crop_scale']
    crop_height = rect[3] * params['face_crop_scale']
    crop_left = max(0, int(crop_center_x - crop_width / 2))
    crop_top = max(0, int(crop_center_y - crop_height / 2))
    crop_right = min(orig_img_w, int(crop_center_x + crop_width / 2))
    crop_bottom = min(orig_img_h, int(crop_center_y + crop_height / 2))
    cropped_face = img[crop_top:crop_bottom, crop_left:crop_right]
    max_edge_len = np.max(cropped_face.shape[:-1])
    padded_face = np.zeros((max_edge_len, max_edge_len, cropped_face.shape[-1]), dtype=np.uint8)
    padded_face[0:cropped_face.shape[0], 0:cropped_face.shape[1]] = cropped_face
    return padded_face, (crop_left, crop_top)
