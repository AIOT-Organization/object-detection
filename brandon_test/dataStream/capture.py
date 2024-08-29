import threading
import queue

from pal.utilities.vision import Camera2D
import numpy as np

class CaptureImageThread(threading.Thread):
    def __init__(self, imageWidth, imageHeight):
        super().__init__()
        self.myCam = Camera2D(cameraId="3", frameWidth=imageWidth, frameHeight=imageHeight)
        self.buffer = queue.Queue()
        self.stoppingFlag = False
    def run(self):
        while not self.stoppingFlag:
            self.myCam.read()

            self.buffer.put(self.myCam.imageData)
        self.myCam.terminate()

