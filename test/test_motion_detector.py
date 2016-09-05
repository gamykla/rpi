import os

from nose.tools import ok_
from PIL import Image

from security import motion_detector


def _fqfilename(image_filename):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "resources", image_filename)


def test_motion_is_detected():
    img1 = Image.open(_fqfilename("far1.JPG"))
    img2 = Image.open(_fqfilename("far3.JPG"))
    ok_(motion_detector.is_motion_detected(img1, img2))


def test_motion_is_not_detected():
    img1 = Image.open(_fqfilename("far1.JPG"))
    img2 = Image.open(_fqfilename("far2.JPG"))
    ok_(not motion_detector.is_motion_detected(img1, img2))
