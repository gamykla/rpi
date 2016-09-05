import logging
from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera

import motion_detector

logging.basicConfig(format='%(asctime)-15s  %(message)s')
logger = logging.getLogger(__name__)


def _build_camera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    return camera

def main():
    camera = _build_camera()
    camera.start_preview()
    sleep(2)

    last_image = None

    while True:
        sleep(1)
        stream = BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        image = Image.open(stream)
        if not last_image:
            last_image = image

        if motion_detector.is_motion_detected(image, last_image):
            logger.debug("Motion is detected!")
        else:
            logger.debug("No motion.")

        last_image = image


if __name__ == "__main__":
    main()
