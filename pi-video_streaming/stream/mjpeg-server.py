#!/usr/bin/python

#
# A simple Motion JPEG server in python for creating "virtual cameras" from video sequences.
# 
# The cameras will support MJPEG streaming over HTTP. The MJPEG streams are formed from static JPEG images.
# If you wish to stream a video file, use a tool like VirtualDub to break the video into a sequence of JPEGs.
# 
# The list of cameras should be defined as a series of entries in a file named 'mjpeg-server.conf', with
# each entry having the following format:
# 
# [Camera-1]
# images: /tmp/video-1/frames
# port: 8001
# maxfps: 10
# 
# The above entry creates a virtual camera named "Camera-1" on local port 8001. The .jpg files found in the
# "/tmp/video-1/frames" directory will be served as an MJPEG stream with a max speed of 10 fps. You can access
# this stream from any MJPEG client (such as your browser) at: http://<server ip>:8001
# 
# Copyright (c) 2013 Arun Nair (http://nairteashop.org).
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
#from Queue import Queue

SERVERS = {}
want_send = Semaphore(0)
want_capt = Semaphore(1)
alive = True

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get info
        client = self.client_address
        port = self.server.server_port
        imageDir = SERVERS[port]["images"]

        logging.info( "Serving client %s:%s from port %s", client[0], client[1], port )

        # Send headers
        self.send_response( 200 )
        self.send_header( "Cache-Control", "no-cache" )
        self.send_header( "Pragma", "no-cache" )
        self.send_header( "Connection", "close" )
        self.send_header( "Content-Type", "multipart/x-mixed-replace; boundary=--myboundary" )
        self.end_headers()

        o = self.wfile

        prev_completed_buff = time.time()

        while True:
            for index in range(10):
                #logging.info( "Before the acquire. Frame %02d", index )

                want_send.acquire()

                #logging.info( "After the acquire. Frame %02d", index )

                f = open( os.path.join(imageDir, 'img%02d.jpeg' % index) )
                contents = f.read()
                f.close()

                want_capt.release()

                try:
                    logging.debug( "Serving frame %02d", index )
                    o.write( "--myboundary\r\n" )
                    o.write( "Content-Type: image/jpeg\r\n" )
                    o.write( "Content-Length: %s\r\n" % len(contents) )
                    o.write( "\r\n" )
                    o.write( contents )
                    o.write( "\r\n" )
                except:
                    logging.info( "Done serving client %s:%s from port %s", client[0], client[1], port )
                    return

                index += 1

            logging.info( "Buffer completed, re-looping" )
            logging.info( "FPS: %.02f \n" % ((time.time() - prev_completed_buff) / 10) )
            prev_completed_buff = time.time()

class ThreadingHTTPServer( ThreadingMixIn, HTTPServer ):
    pass

def startServer( port ):
    def target( port ):
        server = ThreadingHTTPServer( ("0.0.0.0",port), RequestHandler )
        server.serve_forever()

    t = Thread( target=target, args=[port] )
    t.start()

def capture_images( port ):
    def target( port ):
        with picamera.PiCamera() as camera:
            camera.resolution = (480, 360)
            camera.rotation = 180
            
            # camera warm-up
            time.sleep(2)
            
            imageDir = "/tmp/streaming"
            
            while True:
                for index in range(10):
                    want_capt.acquire()
                    camera.capture( os.path.join(imageDir, 'img%02d.jpeg' % index) )
                    want_send.release()

                    index += 1

    t = Thread( target=target, args=[port] )
    t.start()

if __name__ == "__main__":
    logging.basicConfig( level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s" )

    config = ConfigParser.ConfigParser()
    config.read( "/home/pi/Documents/python-scripts/video-streaming/mjpeg-server.conf" )

    for section in config.sections():
        imagesDirectory = config.get( section, "images" )
        port   = config.getint( section, "port" )

        if not os.path.exists(imagesDirectory):
            os.makedirs(imagesDirectory)

        capture_images( port )
        logging.info( "Capturing images in '%s'" % imagesDirectory )

        SERVERS[port] = { "images": imagesDirectory }
        startServer( port )
        logging.info( "Serving '%s' on port %s" % (section, port) )
