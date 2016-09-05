import logging
import math
import os

from PIL import Image, ImageChops
import numpy as np

THRESHOLD = 2.0

logger = logging.getLogger(__name__)

def _image_entropy(img):
    w,h = img.size
    a = np.array(img.convert('RGB')).reshape((w * h, 3))
    h,e = np.histogramdd(a, bins=(16,) * 3, range=((0, 256),) * 3)
    prob = h/np.sum(h) # normalize
    prob = prob[prob > 0] # remove zeros
    entropy = -np.sum(prob * np.log2(prob))
    logger.debug("Entropy = {}".format(entropy))
    return entropy

def is_motion_detected(image1, image2):
    difference_image = ImageChops.difference(image1, image2)
    entropy = _image_entropy(difference_image)
    return math.fabs(_image_entropy(difference_image)) > THRESHOLD

