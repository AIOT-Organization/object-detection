import argparse
import io
import pygame
import threading
import time
import numpy as np
import cv2
from wasd_manual import wasd_drive
from pal.products.qcar import QCar, QCarRealSense
import DetectLane as DetectLane
import sys
import os


sys.path.append('/home/nvidia/Documents/brandon_test/rpie_model')

folderName = "image_data"



myCar = QCar(readMode=0)
is_capture_running = False
key = 'stop'
camera_realsense_rgb = QCarRealSense(mode='RGB')



def wasd_drive():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("QCar Manual Control")

    throttle_increment = 0.0001
    steering_increment = 0.005
    max_throttle = 0.2
    min_throttle = -0.2
    max_steering = 0.5
    min_steering = -0.5

    throttle = 0.0
    steering = 0.0

    running = True
    LEDs = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    isReverse = False
    headlights_on = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        
        myCar.read_write_std(throttle=throttle, steering=steering, LEDs=LEDs)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    myCar.terminate()
    pygame.quit()
    sys.exit()

# Thread for car control
t1 = threading.Thread(target=wasd_drive)

try:
    t1.start()
except KeyboardInterrupt:
    # Handle clean up on keyboard interrupt
    myCar.terminate()
    pygame.quit()
    sys.exit()

class SplitFrames(object):
    def __init__(self):
        self.frame_num = 0
        self.output = None

    def write(self, buf):
        global key
        if buf.startswith(b'\xff\xd8'):
            if self.output:
                self.output.close()
            self.frame_num += 1
            timestamp = int(time.time())
            filename = f'{key}_image{timestamp}.jpg'
            self.output = io.open(filename, 'wb')
        self.output.write(buf)

def qcar_capture():
    global is_capture_running, key
    
    print("Start capture")
    is_capture_running = True

    while is_capture_running:
        # Capture image from the QCar's camera
        camera_realsense_rgb.read_RGB()
        img = cv2.resize(camera_realsense_rgb.imageBufferRGB, (160, 120))
        filename = f'{key}_{int(time.time())}.jpg'
        cv2.imwrite(os.path.join(folderName, filename), img)
        time.sleep(0.1)  # Sleep to control the capture rate

    print("Stop capture")


if __name__ == '__main__':
    print("Start data collection")
    capture_thread = threading.Thread(target=qcar_capture)
    control_thread = threading.Thread(target=wasd_drive)

    capture_thread.start()
    control_thread.start()

    capture_thread.join()
    control_thread.join()

    print("Data collection complete")
