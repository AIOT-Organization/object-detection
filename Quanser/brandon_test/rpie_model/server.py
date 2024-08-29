import argparse
import numpy as np
from pid_controller import PIDController
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}
import cv2
from pal.products.qcar import QCar, QCarRealSense
import DetectLane as DetectLane




parser = argparse.ArgumentParser(
                                    prog='Q Car Contorl Handler',
                                    description='Handles Image Processing and QCar Control'
                                )
parser.add_argument(
                    "-v", "--video",
                    action='store_true',
                    help="Enable or Disable Video Capture."
                    )

args = parser.parse_args()
videoRecording = False
if args.video:
    videoRecording = True

if videoRecording:
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed (e.g., 'XVID')
    out = cv2.VideoWriter('videos/1.mp4', fourcc, fps=30.0, frameSize=(480, 270))  # 'output.mp4' is the output file name

    # Add this line before the main loop to start recording
    out.open('videos/1.mp4', fourcc, fps=30.0, frameSize=(480, 270))

stopthread = False

myCar = QCar(readMode=0)
max_throttle = 0.2
min_throttle = -0.2
max_steering = 0.5
min_steering = -0.5

steering = 0
throttle = 0.05
reverse = False

sampleRate = 45.0
sampleTime = 1/sampleRate

    
def main():
    def exiting():
        camera_realsense_rgb.terminate()
        if videoRecording:
            out.release()
        cv2.destroyWindow("RealSense Camera")
        global stopthread
        stopthread = True
        cv2.destroyAllWindows()
        quit()

    # Initialize the lane detection and PID controller
    # lane_detector = DetectLane.DetectLane()
    # pid_controller = PIDController(kp=0.1, ki=0.01, kd=0.005)  # PID coefficients


    # Set up camera
    camera_realsense_rgb = QCarRealSense(mode='RGB')

    
    
    last_time = time.time()
    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        camera_realsense_rgb.read_RGB()
        img = cv2.resize(camera_realsense_rgb.imageBufferRGB, (480, 240))
        # Lane detection and steering angle calculation
        # result, steer_angle = lane_detector.detectLanes(img)
        # PID controller for smoother steering
        # steering = pid_controller.update(steer_angle, dt)
        # Clamp the steering value to prevent excessive steering angles
        # steering = np.clip(steering, min_steering, max_steering)
        # Vehicle control
        # myCar.write(throttle=throttle, steering=steering)

        # Video recording (if enabled)
        if videoRecording:
            out.write(img)
        # Display the result
        # cv2.imshow("RealSense Camera", result)
        cv2.imshow("RealSense Camera",img)
        key = cv2.waitKey(1)
        if key == 27:
            # myCar.write(throttle=0, steering=0)
            exiting()

        # print(f"Computation Time: {dt}")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()