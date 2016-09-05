from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera

import motion_detector


stream = BytesIO()


camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
sleep(2)
camera.capture(stream, format='jpeg')

stream.seek(0)
image = Image.open(stream)


def main():
    pass

if __name__ == "__main__":
    main()
