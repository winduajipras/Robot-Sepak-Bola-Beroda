from picamera import picamera
from time import sleep

camera = Picamera()

camera.start_preview()
sleep(10)
camera.stop_preview()

