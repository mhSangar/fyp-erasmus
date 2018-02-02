import io
import socket
import struct
from PIL import Image

# socket listening for all interfaces
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# only one connection accepted
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # reads length of img, if =0 finishes loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        # reads data in stream obj
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # rewinds stream to read it
        image_stream.seek(0)
        image = Image.open(image_stream)

        print('Image received...')
        #image.verify()
        #print('Image is verified')
#        image.show()
        image.close()
        print('\n')
finally:
    connection.close()
    server_socket.close()
