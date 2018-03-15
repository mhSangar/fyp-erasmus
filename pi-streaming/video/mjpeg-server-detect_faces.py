#!/usr/bin/python

#
# Original code:
#   Copyright (c) 2013 Arun Nair (http://nairteashop.org).
# Licensed under the MIT license.
#

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from threading import Thread
import logging
import time
import os
import io
import picamera
import cv2

port = 8001
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get info
        client = self.client_address
        
        logging.info("Serving client %s:%s from port %s", client[0], client[1], port)

        # Send headers
        self.send_response(200)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Pragma", "no-cache")
        self.send_header("Connection", "close")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=--myboundary")
        self.end_headers()

        o = self.wfile

        with picamera.PiCamera() as camera:
            camera.resolution = (480, 360)
            camera.rotation = 180

            # camera warm-up
            time.sleep(2)

            img_buffer = io.BytesIO()
            prev_completed_round = time.time()

            while True:
                for _ in range (10):
                    # clean and go back to first position to write
                    img_buffer.flush()
                    img_buffer.seek(0)
    
                    # capture to stream
                    camera.capture(img_buffer, "jpeg", use_video_port=True)
                    
                    # reach first position again to read it
                    img_buffer.seek(0)
                    img_string = img_buffer.read()

                    img_buffer.seek(0)
                    grayscale_img = cv2.imread(img_buffer, 0)

                    faces = classifier.detectMultiScale(grayscale_img, scaleFactor=1.3, minNeighbors=5)
                    if len(faces) > 0:
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img_string, (x,y), (x+w, y+h), (0, 0, 255), 2)
                            
                    try:
                        o.write("--myboundary\r\n")
                        o.write("Content-Type: image/jpeg\r\n")
                        o.write("Content-Length: %s\r\n" % len(img_string))
                        o.write("\r\n")
                        o.write(img_string)
                        o.write("\r\n")
                    except:
                        logging.info("Done serving client %s:%s from port %s", client[0], client[1], port)
                        return
    
                logging.info("Round completed, FPS: %.02f" % (10 / (time.time() - prev_completed_round)))
                prev_completed_round = time.time()

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def startServer():
    def target():
        server = ThreadingHTTPServer(("0.0.0.0", port), RequestHandler)
        server.serve_forever()

    t = Thread(target=target)
    t.start()

if __name__ == "__main__":
    # switch on the log notifications
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    startServer()
    logging.info("Serving 'pi-camera' on port %s" % port)
