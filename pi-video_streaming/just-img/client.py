import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()

# change for server IP address
client_socket.connect(('my_server', 8000))

# connect to server
connection = client_socket.makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30   # 30fps
        
        # warm-up
        time.sleep(2)
        
        start = time.time()
        count = 0
        stream = io.BytesIO()
        
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # writes image size?
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()

            # writes image data
            stream.seek(0)
            connection.write(stream.read())

            count += 1

            if time.time() - start > 30:
                break
            stream.seek(0)
            stream.truncate()

    # writes a 0 to inform server that video is finished
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))