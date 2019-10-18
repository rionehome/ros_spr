import os
from glob import glob

from PIL import Image

import chainer
import chainer.computational_graph as c
from chainer import links as L
from chainer import optimizers
from chainer import serializers

from matplotlib import pyplot as plt

from numpy import argmax, array, float32

from .model import VGG_16


print('[INFO] [DetectHuman]: LOADING MODEL',flush=True)
model = L.Classifier(VGG_16())
optimizer = optimizers.Adam()
optimizer.setup(model)
print('[INFO] [DetectHuman]: DONE',flush=True)
npz_path = os.path.abspath(__file__).replace(
    'detect_modules/detect_sex/classifier.py', 'model/cifier_adam.npz')

serializers.load_npz(npz_path, model)


def detect_human_sex(image):
    # image must be numpy array
    image = image.transpose(2, 0, 1).reshape(1, 3, 96, 96)
    predicted = model.predictor(image)
    data = predicted.data[0]
    if data[0] > data[1]:
        return 0
    elif data[0] < data[1]:
        return 1
    else:
        return 2
