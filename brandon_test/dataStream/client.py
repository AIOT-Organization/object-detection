import io
import socket
import struct
import time
import cv2
from urllib.parse import urlparse

import capture

clientSocket = socket.socket()

# modification for ngrok
parsed_url = urlparse('tcp://8.tcp.ngrok.io:19530')
ngrok_host = parsed_url.hostname
ngrok_port = parsed_url.port
# 

IP = '134.71.68.175'
PORT = 42322
WIDTH, HEIGHT = 540, 320

try:
    clientSocket.connect((ngrok_host, ngrok_port))
except Exception as e:
    print(f"Connection error: {e}")

connection = clientSocket.makefile('wb')


try:
    #QCar
    capture_image_thread = capture.CaptureImageThread(WIDTH, HEIGHT)
    capture_image_thread.start()

    start = time.time()
    

    while True:
        image = capture_image_thread.buffer.get()
        _, encoded_image = cv2.imencode('.jpg', image)
        byteImage = encoded_image.tobytes()
        stream = io.BytesIO(byteImage)

        connection.write(struct.pack('<L', stream.tell() ))
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())

        if time.time() - start > 60:
            break
        
        stream.seek(0)
        stream.truncate()
finally:
    print('done')