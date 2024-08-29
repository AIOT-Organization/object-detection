import driving
import capture

import cv2
import datetime

import os
import shutil



WIDTH = 480
HEIGHT = 240
folderName = "/media/91C5-7087/image_data"

def main():
    if os.path.isdir(folderName):
        shutil.rmtree(folderName, ignore_errors=True)

    os.mkdir(folderName)

    steering_wheel_thread = driving.SteeringWheelThread()
    capture_image_thread = capture.CaptureImageThread(WIDTH, HEIGHT)

    steering_wheel_thread.start()
    capture_image_thread.start()

    while True:
        try:
            steering_angle, throttle, reverse = steering_wheel_thread.getData()
            
            image = capture_image_thread.buffer.get()
            time = datetime.datetime.now()
            
            cv2.imshow("test", image)
            cv2.waitKey(1)
            
            # filename = str(time).replace(" ", "") + "_" + str(steering_angle)
            # filename = filename.replace(".", "_") + ".jpg"
            # # print(os.path.join(folderName, filename))
            # cv2.imwrite(os.path.join(folderName, filename), image)

        except KeyboardInterrupt:
            print('Closing Program ...')
            steering_wheel_thread.stoppingFlag = True
            capture_image_thread.stoppingFlag = True
            steering_wheel_thread.join()
            capture_image_thread.join()
            exit()

    
if __name__ == '__main__':
    main()