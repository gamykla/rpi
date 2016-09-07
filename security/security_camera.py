import logging
from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera

import motion_detector

logging.basicConfig(format='%(asctime)-15s  %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_IMAGE_WIDTH = 1024
DEFAULT_IMAGE_HEIGHT = 768


def _build_camera():
    camera = PiCamera()
    camera.resolution = (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT)
    return camera


class SecurityCamera():

    def __init__(self, camera, motion_sensor):
        self.camera = camera
        self.motion_sensor = motion_sensor
        self.last_image_captured = None

    def start_cam(self):
        self.capture_loop()

    def _is_motion_detected(self, image_captured):
        if not image_captured:
            return False
        return self.motion_sensor.is_motion_detected(self.last_image_captured, image_captured)

    def capture_loop(self):
        self.camera.start_preview()
        sleep(2)

        while True:
            sleep(0.5)
            logger.debug("Capturing image.")

            stream = BytesIO()
            self.camera.capture(stream, format='jpeg')

            stream.seek(0)
            captured_image = Image.open(stream)
            stream.close()

            if self._is_motion_detected(captured_image):
                logger.debug("Motion detected.")
            else:
                logger.debug("No motion.")

            self.last_image_captured = captured_image


def main():
    motion_sensor = motion_detector.MotionDetector()
    security_camera = SecurityCamera(_build_camera(), motion_sensor)
    security_camera.start_cam()

if __name__ == "__main__":
    main()
