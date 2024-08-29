import time
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pal.products.qcar import QCarCameras, IS_PHYSICAL_QCAR

if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    qlabs_setup.setup()

def region_of_interest(image):
    height, width = image.shape[:2]
    polygons = np.array([
    [(0,int(height/2+110)),(int(width/2),int(height/2)),(width,int(height/2+110))]]) #(200,height),(1100, height),(550, 250)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

# Lane detection using Hough Line Transform
def detect_lanes(frame):
    # Preprocess the frame (convert to grayscale and apply Gaussian blur)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection (Canny)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define ROI (Region of Interest)
    cropped_roi = region_of_interest(edges)
    

    # Use Hough Line Transform to detect lines\
    lines_list =[]
    lines = cv2.HoughLinesP(
                cropped_roi, # Input edge image
                1, # Distance resolution in pixels
                np.pi/180, # Angle resolution in radians
                threshold=70, #50  Min number of votes for valid line
                minLineLength=1, #1  Min allowed length of line
                maxLineGap=10 #15 Max allowed gap between line for joining them
                )
    
    
    # Draw the detected lines on the frame
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imshow("GrayScale",gray)
            cv2.imshow("Cropped ROI",cropped_roi)
            


#Initial Setup
runTime = 100.0 # seconds

cameras = QCarCameras(
    enableBack=False,
    enableFront=True,
    enableLeft=False,
    enableRight=False,
)

with cameras:
    t0 = time.time()
    # while time.time() - t0 < runTime:
    while True:
        cameras.readAll()

        for c in cameras.csi:
            if c is not None:
                detect_lanes(c.imageData)
                
                cv2.imshow('CSI Front', c.imageData)

        # Note: You can also access specific cameras directly if you know
        # which one you want. For example:
        #   cv2.imshow('CSI Front', cameras.csiFront.imageData)

        cv2.waitKey(100)
