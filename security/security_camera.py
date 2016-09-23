#!/usr/bin/env python
import logging
import multiprocessing
import sys
import json
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

    def __init__(self, camera, motion_sensor, image_data_queue):
        self.camera = camera
        self.motion_sensor = motion_sensor
        self.image_data_queue = image_data_queue
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

                    self.image_data_queue.put(image_bytes)
                else:
                    logger.debug("No motion.")

                self.last_image_captured = captured_image
        finally:
            logger.debug("Shutting down SecurityCamera.")
            self.camera.close()


class ImageUploader(multiprocessing.Process):
    """ Upload captured images to camera server """
    def __init__(self, image_data_queue):
        super(ImageUploader, self).__init__()
        self.image_data_queue = image_data_queue

    def _load_server_credentials(self):
        with open("/home/pi/cam_server_credentials.json") as f:
            cam_server_credentials = f.read()
        credentials_json = json.loads(cam_server_credentials)
        self.client_key = credentials_json['CLIENT_KEY']
        self.client_secret = credentials_json['CLIENT_SECRET']

    def run(self):
        while True:
            try:
                image_data = self.image_data_queue.get()
                logger.debug("Got image: {}".format(image_data))
            except:
                logger.exception("Image uploader exception")


def main():
    try:
        image_data_queue = multiprocessing.Queue()
        image_uploader_process = ImageUploader(image_data_queue)
        image_uploader_process.start()

        motion_sensor = motion_detector.MotionDetector()
        security_camera = SecurityCamera(_build_camera(), motion_sensor, image_data_queue)
        security_camera.start_cam()
    finally:
        if image_uploader_process.is_alive():
            image_uploader_process.terminate()
            image_uploader_process.join()

if __name__ == "__main__":
    try:
        main()
    except:
        logger.exception("Crash!")
        sys.exit(-1)
