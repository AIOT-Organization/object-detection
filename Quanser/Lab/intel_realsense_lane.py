'''lane_detect_intelrealsense.py

This example demonstrates how to perform lane detection using the Intel RealSense camera.
'''
import time
import cv2
import numpy as np
from pal.products.qcar import QCarRealSense, IS_PHYSICAL_QCAR

if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    qlabs_setup.setup()

# Lane detection using Hough Line Transform
def detect_lanes(frame):

    frame_color = cv2.applyColorMap(cv2.convertScaleAbs(frame, alpha=0.03), cv2.COLORMAP_JET)

    # Ensure the input frame is in grayscale
    gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection (Canny)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define ROI (Region of Interest)
    height, width = frame_color.shape[:2]
    roi_vertices = [(0, height), (width / 2, height / 2), (width, height)]
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array(roi_vertices, np.int32)], 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 100, minLineLength=10, maxLineGap=250)
    
    # Draw the detected lines on the frame
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame_color, (x1, y1), (x2, y2), (0, 0, 255), 5)
    
    cv2.imshow('Intel RealSense lane detect', frame_color)


# Initial Setup
runTime = 20.0  # seconds

# Configure Intel RealSense camera in depth mode
with QCarRealSense(mode='DEPTH') as myCam:
    t0 = time.time()
    while time.time() - t0 < runTime:
        myCam.read_depth(dataMode='M')
        
        # Perform lane detection on the depth image
        detect_lanes(myCam.imageBufferDepthPX)
        
        # Display the depth image with detected lanes
        cv2.imshow('Lane Detection with Intel RealSense', myCam.imageBufferDepthPX)

        cv2.waitKey(100)
