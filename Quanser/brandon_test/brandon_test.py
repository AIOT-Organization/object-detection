'''hardware_test_basic_io.py

This example demonstrates how to use the QCar class to perform basic I/O.
Learn how to write throttle and steering, as well as LED commands to the
vehicle, and read sensor data such as battery voltage. See the QCar class
definition for other sensor buffers such as motorTach, accelometer, gyroscope
etc.
'''
import numpy as np
import time
from pal.products.qcar import QCar, IS_PHYSICAL_QCAR

if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    qlabs_setup.setup()


#Initial Setup
sampleRate = 200
runTime = 20.0 # seconds

with QCar(readMode=1, frequency=sampleRate) as myCar:
    t0 = time.time()
    
    while time.time() - t0  < runTime:

        t = time.time()
        LEDs = np.array([0, 0, 0, 0, 0, 0, 0, 0])

        # Read from onboard sensors
        myCar.read()

        # Basic IO - write motor commands


        throttle = 0
        steering = 0

        tmp = int(input("Turn Light On: "))
        LEDs[tmp] = 1


        myCar.write(throttle, steering, LEDs)

        print(
            f'time: {(t-t0):.2f}'
            + f', Motor Encoder: {myCar.motorEncoder}'
            + f', Motor Tach: {myCar.motorTach:.2f}'
            + f', Accelerometer: {myCar.accelerometer}'
            + f', Gyroscope: {myCar.gyroscope}'
        )