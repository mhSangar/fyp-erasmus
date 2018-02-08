#!/usr/bin/python

#
# Original code:
#   Copyright (c) 2013 Arun Nair (http://nairteashop.org).
# Licensed under the MIT license.
#

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from threading import Thread
from threading import Semaphore
import ConfigParser
import logging
import time
import os
import picamera

imageDir = "/tmp/streaming"
port = 8001

want_send = Semaphore(0)
want_capt = Semaphore(1)

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

        prev_completed_buff = time.time()

        while True:
            for index in range(10):

                want_send.acquire()

                f = open(os.path.join(imageDir, 'img%02d.jpeg' % index))
                contents = f.read()
                f.close()

                want_capt.release()

                try:
                    o.write("--myboundary\r\n")
                    o.write("Content-Type: image/jpeg\r\n")
                    o.write("Content-Length: %s\r\n" % len(contents))
                    o.write("\r\n")
                    o.write(contents)
                    o.write("\r\n")
                except:
                    logging.info("Done serving client %s:%s from port %s", client[0], client[1], port)
                    return

                index += 1

            logging.info("Buffer completed, re-looping")
            logging.info("FPS: %.02f \n" % (10 / (time.time() - prev_completed_buff)))
            prev_completed_buff = time.time()

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def startServer():
    def target():
        server = ThreadingHTTPServer(("0.0.0.0", port), RequestHandler)
        server.serve_forever()

    t = Thread(target=target)
    t.start()

def capture_images():
    def target():
        with picamera.PiCamera() as camera:
            camera.resolution = (480, 360)
            camera.rotation = 180
            
            # camera warm-up
            time.sleep(2)
            
            imageDir = "/tmp/streaming"
            
            while True:
                for index in range(10):
                    want_capt.acquire()
                    camera.capture(os.path.join(imageDir, 'img%02d.jpeg' % index))
                    want_send.release()

                    index += 1

    t = Thread(target=target)
    t.start()

if __name__ == "__main__":
    # switch on the log notifications
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    # creates the path if it doesn't exists
    if not os.path.exists(imageDir):
        os.makedirs(imageDir)

    capture_images()
    logging.info("Capturing images in '%s'" % imageDir)

    startServer()
    logging.info("Serving 'pi-camera' on port %s" % port)