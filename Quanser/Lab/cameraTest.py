## imaging_360.py
# This example demonstrates how to read all 4 csi cameras and display in a single openCV window. If you encounter any errors, 
# use the hardware_test_csi_camera_single.py script to find out which camera is giving you trouble. 

from pal.utilities.vision import Camera2D
import time
import struct
import numpy as np 
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate     = 30.0
sampleTime     = 1/sampleRate
simulationTime = 60.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480
imageBuffer360 = np.zeros((imageHeight + 40, 4*imageWidth + 120, 3), dtype=np.uint8) # 20 px padding between pieces  

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the CSI cameras
# myCam1 = Camera2D(cameraId="0", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
# myCam2 = Camera2D(cameraId="1", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
# myCam3 = Camera2D(cameraId="2", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam4 = Camera2D(cameraId="3", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
    # while elapsed_time() < simulationTime:
    while True:
        
        # Start timing this iteration
        start = time.time()

        # Capture RGB Image from CSI
        # myCam1.read()
        # myCam2.read()
        # myCam3.read()
        myCam4.read()

        counter += 1

        # End timing this iteration
        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )
        
        # Stitch images together with black padding
        horizontalBlank     = np.zeros((20, 4*imageWidth+120, 3), dtype=np.uint8)
        verticalBlank       = np.zeros((imageHeight, 20, 3), dtype=np.uint8)

        # imageBuffer360 = np.concatenate(
        #                                    (horizontalBlank, 
        #                                     np.concatenate((    verticalBlank, 
        #                                                         # myCam2.imageData[:,320:640], 
        #                                                         # verticalBlank, 
        #                                                         # myCam3.imageData, 
        #                                                         # verticalBlank, 
        #                                                         myCam4.imageData, 
        #                                                         # verticalBlank, 
        #                                                         # myCam1.imageData, 
        #                                                         # verticalBlank, 
        #                                                         # # myCam2.imageData[:,0:320], 
        #                                                         # verticalBlank
        #                                                         ), 
        #                                                         axis = 1), 
        #                                     horizontalBlank
        #                                     ), 
        #                                     axis=0
        #                                 )

        # Display the stitched image at half the resolution
        # cv2.imshow('Combined View', cv2.resize(imageBuffer360, (int(2*imageWidth), int(imageHeight/2))))
        # cv2.imshow('Combined View', myCam4.imageData)
        img = cv2.imread('LAneTest.png')
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        

        # Apply edge detection method on the image
        edges = cv2.Canny(gray, 200, 250, apertureSize=3)
        
        # This returns an array of r and theta values
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

        cv2.imshow('Combined Viewedge', edges)

        # The below for loop runs till r and theta values
        # are in the range of the 2d array
        if (lines is not None) :
            for r_theta in lines:
                arr = np.array(r_theta[0], dtype=np.float64)
                r, theta = arr
                # Stores the value of cos(theta) in a
                a = np.cos(theta)
            
                # Stores the value of sin(theta) in b
                b = np.sin(theta)
            
                # x0 stores the value rcos(theta)
                x0 = a*r
            
                # y0 stores the value rsin(theta)
                y0 = b*r
            
                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                x1 = int(x0 + 1500*(-b))
            
                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                y1 = int(y0 + 1500*(a))
            
                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                x2 = int(x0 - 1500*(-b))
            
                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                y2 = int(y0 - 1500*(a))
            
                # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
                # (0,0,255) denotes the colour of the line to be
                # drawn. In this case, it is red.
                cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.imshow('Combined View', gray)
        
        # Pause/sleep for sleepTime in milliseconds
        msSleepTime = int(1000*sleepTime)
        if msSleepTime <= 0:
            msSleepTime = 1 # this check prevents an indefinite sleep as cv2.waitKey waits indefinitely if input is 0
        cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate all webcam objects    
    # myCam1.terminate()
    # myCam2.terminate()
    # myCam3.terminate()
    myCam4.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 