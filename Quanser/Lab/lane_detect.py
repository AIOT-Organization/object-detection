'''hardware_test_csi_cameras.py

This example demonstrates how to read and display images from the CSI cameras.
'''
import sys
import math
import cv2
from tensorflow.keras.models import load_model
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pal.products.qcar import QCarCameras
from pal.products.qcar import QCarRealSense
from pal.utilities.vision import Camera2D, Camera3D
import tensorflow as tf

# # Limit GPU memory growth
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         for gpu in gpus:
#             tf.config.experimental.set_virtual_device_configuration(
#                 gpu,
#                 [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)]
#             )
#     except RuntimeError as e:
#         print(e)


# # Lane detection using Hough Line Transform
# def detect_lanes(frame):
#     # Preprocess the frame (convert to grayscale and apply Gaussian blur)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
#     # Perform edge detection (Canny)
#     edges = cv2.Canny(blurred, 50, 150)
    
#     # Define ROI (Region of Interest)
#     height, width = frame.shape[:2]
#     roi_vertices = [(0, height), (width / 2, height / 2), (width, height)]
#     mask = np.zeros_like(edges)
#     cv2.fillPoly(mask, [np.array(roi_vertices, np.int32)], 255)
#     masked_edges = cv2.bitwise_and(edges, mask)
    
#     # Use Hough Line Transform to detect lines
#     lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 100, minLineLength=10, maxLineGap=250)
    
#     # Draw the detected lines on the frame
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

# # Class to average lanes with
# class Lanes():
#     def __init__(self):
#         self.recent_fit = []
#         self.avg_fit = []


# def lanes_region(image):
#     """ Takes in a road image, re-sizes for the model,
#     predicts the lane to be drawn from the model then merge with
#     original road image.
#     """

#     # Get image ready for feeding into model
#     small_img = cv2.resize(image, (160, 80))
#     small_img = np.array(small_img)
#     small_img = small_img[None, :, :, :]


#     # Make prediction with neural network (un-normalize value by multiplying by 255)
#     prediction = model.predict(small_img)[0] * 255

#     # Add lane prediction to list for averaging
#     lanes.recent_fit.append(prediction)
#     # Only using last five for average
#     if len(lanes.recent_fit) > 5:
#         lanes.recent_fit = lanes.recent_fit[1:]

#     # Calculate average detection
#     lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis=0)


#     blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
#     lane_drawn = np.dstack((lanes.avg_fit, blanks, blanks))

#     # Re-size to match the original image
#     lane_image = cv2.resize(lane_drawn, (image.shape[1], image.shape[0]))

#     # Merge the lane drawing onto the original image
#     result = cv2.addWeighted(image, 1, lane_image, 1, 0, dtype=cv2.CV_8UC3)
    





#Initial Setup
runTime = 1000.0 # seconds

cameras = QCarCameras(
    enableBack=False,
    enableFront=True,
    enableLeft=False,
    enableRight=False,
)

# with QCarRealSense(mode='RGB'
#                    ) as myCam:
#     # Load model
#     model = load_model('model.h5')
#     # Create lanes object
#     lanes = Lanes()
#     t0 = time.time()
#     while True:
#     # while time.time() - t0 < runTime: 
#         myCam.read_RGB()
#         image = myCam.imageBufferRGB
#         image = cv2.resize(image, (int(480), int(270)))
       
#         # Get image ready for feeding into model
#         small_img = cv2.resize(image, (160, 80))
#         small_img = np.array(small_img)
#         small_img = small_img[None, :, :, :]
    
    
#         # Make prediction with neural network (un-normalize value by multiplying by 255)
#         prediction = model.predict(small_img)[0] * 255
    
#         # Add lane prediction to list for averaging
#         lanes.recent_fit.append(prediction)
#         # Only using last five for average
#         if len(lanes.recent_fit) > 5:
#             lanes.recent_fit = lanes.recent_fit[1:]
    
#         # Calculate average detection
#         lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis=0)
    
    
#         blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
#         lane_drawn = np.dstack((lanes.avg_fit, blanks, blanks))
    
#         # Re-size to match the original image
#         lane_image = cv2.resize(lane_drawn, (image.shape[1], image.shape[0]))
    
#         # Merge the lane drawing onto the original image
#         result = cv2.addWeighted(image, 1, lane_image, 1, 0, dtype=cv2.CV_8UC3)
        
#         print("before imshow")
#         cv2.imshow('My RGB', result)
        
#         key = cv2.waitKey(100)
#         if key == 27:
#             myCam.terminate()
#             cv2.destroyAllWindows()
        
#             sys.exit()
    
with cameras:
    # Load model
    model = load_model('model.h5')
    # Create lanes object
    lanes = Lanes()
    t0 = time.time()
    while time.time() - t0 < runTime:
        cameras.readAll()

        for i, c in enumerate(cameras.csi):
            if c is not None:
                image = c.imageData
                #lanes_region(c.imageData)
                # Get image ready for feeding into model
                small_img = cv2.resize(image, (160, 80))
                small_img = np.array(small_img)
                small_img = small_img[None, :, :, :]
            
            
                # Make prediction with neural network (un-normalize value by multiplying by 255)
                prediction = model.predict(small_img)[0] * 255
            
                # Add lane prediction to list for averaging
                lanes.recent_fit.append(prediction)
                # Only using last five for average
                if len(lanes.recent_fit) > 5:
                    lanes.recent_fit = lanes.recent_fit[1:]
            
                # Calculate average detection
                lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis=0)
            
            
                blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
                lane_drawn = np.dstack((lanes.avg_fit, blanks, blanks))
            
                # Re-size to match the original image
                lane_image = cv2.resize(lane_drawn, (image.shape[1], image.shape[0]))
            
                # Merge the lane drawing onto the original image
                result = cv2.addWeighted(image, 1, lane_image, 1, 0, dtype=cv2.CV_8UC3)
                
                cv2.imshow(('CSI '+str(i)+':'), result)

        # Note: You can also access specific cameras directly if you know
        # which one you want. For example:
        #   cv2.imshow('CSI Front', cameras.csiFront.imageData)

        cv2.waitKey(100)
