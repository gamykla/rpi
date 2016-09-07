import logging
import math

from PIL import ImageChops
import numpy as np


logger = logging.getLogger(__name__)


def _image_entropy(img):
    w, h = img.size
    a = np.array(img.convert('RGB')).reshape((w * h, 3))
    h, e = np.histogramdd(a, bins=(16, ) * 3, range=((0, 256), ) * 3)
    prob = h/np.sum(h)  # normalize
    prob = prob[prob > 0]  # remove zeros
    entropy = -np.sum(prob * np.log2(prob))
    logger.debug("Entropy = {}".format(entropy))
    return entropy


class MotionDetector(object):

    THRESHOLD = 2.0

    def __init__(self, entropy_function=_image_entropy):
        self.entropy_calculator = entropy_function

    def is_motion_detected(self, image1, image2):
        """returns True if there is a difference in image2 which would suggest motion
        having occurred if image2 was taken after image1. Both images are PIL.Image's"""
        difference_image = ImageChops.difference(image1, image2)
        entropy = self.entropy_calculator(difference_image)
        return math.fabs(entropy) > MotionDetector.THRESHOLD

if __name__ == "__main__":
    from io import BytesIO
    stream = BytesIO()
    stream.write(bytes("abc"))
