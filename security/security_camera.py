#!/usr/bin/env python
import logging
import sys
import logging.handlers
from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera

import motion_detector


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(filename)s %(name)s %(asctime)s - %(levelname)s - %(message)s')

syslogHandler = logging.handlers.SysLogHandler(address='/dev/log')
syslogHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)
logger.addHandler(syslogHandler)

logging.basicConfig(format='%(asctime)-15s  %(message)s', level=logging.DEBUG)


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

    def _is_motion_detected(self, new_image_captured):
        if not self.last_image_captured:
            return False
        return self.motion_sensor.is_motion_detected(self.last_image_captured, new_image_captured)

    def _capture_image(self):
        try:
            stream = BytesIO()
            self.camera.capture(stream, format='jpeg')
            stream.seek(0)
            captured_image = Image.open(stream)
            captured_image.load()
            stream.close()
            return captured_image
        except:
            logger.exception("An error occured capturing image.")

    def capture_loop(self):
        try:
            self.camera.start_preview()
            sleep(2)

            while True:
                sleep(0.5)
                logger.debug("Capturing image.")

                captured_image = self._capture_image()

                if self._is_motion_detected(captured_image):
                    logger.debug("MOTION DETECTED!")

                    stream = BytesIO()
                    captured_image.save(stream, format='jpeg')
                    stream.seek(0)
                    image_bytes = stream.getvalue()
                    stream.close()
                    logger.info(len(image_bytes))

                else:
                    logger.debug("No motion.")

                self.last_image_captured = captured_image
        finally:
            logger.debug("Shutting down SecurityCamera.")
            self.camera.close()


def main():
    motion_sensor = motion_detector.MotionDetector()
    security_camera = SecurityCamera(_build_camera(), motion_sensor)
    security_camera.start_cam()

if __name__ == "__main__":
    try:
        main()
    except:
        logger.exception("Crash!")
        sys.exit(-1)
