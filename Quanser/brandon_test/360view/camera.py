## imaging_360.py
# This example demonstrates how to read all 4 csi cameras and display in a single openCV window. If you encounter any errors, 
# use the hardware_test_csi_camera_single.py script to find out which camera is giving you trouble. 

from pal.utilities.vision import Camera2D
import time
import numpy as np 
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate     = 45.0
sampleTime     = 1/sampleRate
simulationTime = 60.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480
totalWidth = 3 * imageWidth - 400 - 100
imageBuffer360 = np.zeros((imageHeight + 0, totalWidth, 3), dtype=np.uint8) # 20 px padding between pieces  

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the CSI cameras
myCam1 = Camera2D(cameraId="0", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam2 = Camera2D(cameraId="1", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam3 = Camera2D(cameraId="2", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam4 = Camera2D(cameraId="3", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
    # while elapsed_time() < simulationTime:
    while True:
        
        # Start timing this iteration
        start = time.time()

        # Capture RGB Image from CSI
        myCam1.read()
        myCam2.read()
        myCam3.read()
        myCam4.read()

        counter += 1

        # End timing this iteration
        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )
        
        # Stitch images together with black padding
        horizontalBlank     = np.zeros((20, totalWidth, 3), dtype=np.uint8)
        verticalBlank       = np.zeros((imageHeight, 20, 3), dtype=np.uint8)

        imageBuffer360 = np.concatenate(
                                           (#horizontalBlank, 
                                            np.concatenate(( 
                                                                myCam3.imageData[:, 100:-150], 
                                                                # verticalBlank, 
                                                                myCam4.imageData, 
                                                                # verticalBlank, 
                                                                myCam1.imageData[:, 150:-100],
                                                            ), 
                                                                axis = 1), 
                                            #horizontalBlank
                                            ), 
                                            axis=0
                                        )

        # Display the stitched image at half the resolution
        cv2.imshow('Combined View', cv2.resize(imageBuffer360, (int(2*imageWidth), int(imageHeight/2))))
        
        # Pause/sleep for sleepTime in milliseconds
        msSleepTime = int(1000*sleepTime)
        if msSleepTime <= 0:
            msSleepTime = 1 # this check prevents an indefinite sleep as cv2.waitKey waits indefinitely if input is 0
        cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate all webcam objects    
    myCam1.terminate()
    myCam2.terminate()
    myCam3.terminate()
    myCam4.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 