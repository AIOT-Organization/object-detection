import socket
import capture
import time
import cv2


# Weird Error: Seems like it is having difficulty with other modules importing modules of their own

# Traceback (most recent call last):
#   File "image-client.py", line 2, in <module>
#     import capture
#   File "/home/nvidia/Documents/brandon_test/dataCollection/capture.py", line 2, in <module>
#     import queue
# ImportError: No module named queue

def get_image_bytes(img_capture_thread):
    
    image = img_capture_thread.buffer.get()
    start = time.time()
    _, encoded_image = cv2.imencode('.jpg', image)
    byteImage = encoded_image.tobytes()
    
    return byteImage

def client_program():
    host = "134.71.68.251"  # The server's hostname or IP address
    port = 42322  # The port used by the server
    WIDTH, HEIGHT = 540, 320
    
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    img_capture_thread = capture.CaptureImageThread(WIDTH, HEIGHT)  # initializes image capture thread 
    img_capture_thread.start()

    byte_data = get_image_bytes(img_capture_thread)
    data_size = str(len(byte_data))
    
    

    while True:
        client_socket.send(data_size.encode())  # send image size
        client_socket.send(byte_data)  # send image data
        print('Image data sent: ' + str(data_size) + ' bytes')
        
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = img_capture_thread.buffer  # takes in a new image
        
        # Program way to get out
        
        

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()