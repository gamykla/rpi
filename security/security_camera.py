from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera



stream = BytesIO()

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
sleep(2)
camera.capture(stream, format='jpeg')

stream.seek(0)
image = Image.open(stream)