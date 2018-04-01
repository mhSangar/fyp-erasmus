#!/usr/bin/python

from picamera import PiCamera
from picamera.array import PiRGBArray
import logging
import time
import io
import cv2
import base64
import requests
import json 
import sys

port = 5000
route = "recognise_me"
_server_url = "http://192.168.1.105:{}/{}".format(port, route)

def capture_and_send(server_url, res_x, res_y, rotation):
    rawCapture = None

    with PiCamera() as camera:
        camera.resolution = (res_x, res_y)
        camera.rotation = rotation

        rawCapture = PiRGBArray(camera)

        # camera warm-up
        time.sleep(2)

        # show preview in the UI app
        #camera.start_preview()

        # counter of 3 seconds to take the photo
        #time.sleep(3)

        camera.capture(rawCapture, format="bgr")

    _, img_encoded = cv2.imencode(".jpg", rawCapture.array)
    img_as_text = base64.b64encode(img_encoded)

    data = {"image": str(img_as_text)}
    # send req by POST with the img
    try:
        response = requests.post(server_url, json=data)
    except requests.exceptions.RequestException:
        logging.error("Connection Exception")
        logging.info("Exiting...")
        sys.exit(1)

    print(json.loads(response.text))


if __name__ == "__main__":
    # switch on the log notifications
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s >>> %(message)s", datefmt="%H:%M:%S")

    logging.info("Capturing 'pi-camera' and sending to: {}".format(_server_url))
    capture_and_send(_server_url, 480, 720, 180)
    
