import io
import socket
import struct
import time
import picamera
from PIL import Image

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 10   # 30fps
        
        # warm-up
        time.sleep(2)
        
        start = time.time()
        count = 0
        sec = 1

        for foo in camera.capture_continuous('/tmp/streaming/img{counter:02}.jpeg', 'jpeg', use_video_port=True):
            count += 1

            if time.time() - start > 9.5:
                break
            if time.time() - start > sec:
                print("%d secs..." % sec)
                sec += 1

finally:
    finish = time.time()
print('Captured %d images in %d seconds' % (
    count, finish-start))
