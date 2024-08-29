'''This example demonstrates how to read and display data from the QCar Lidar
'''
import time
import numpy as np
import matplotlib.pyplot as plt
from pal.products.qcar import QCar, QCarLidar

def objectAvoidance(myLidar,qcar):
    radius = 0.25
    leftWheeltoRightWheel = 0.18
    stoppingDistance = 0.8
    countRight = 0
    countLeft = 0
    #isBlocked = False
    for i in myLidar.distances[98:128]:
        if i >= 0.9:
            countRight += 1
    for i in myLidar.distances[52:82]:
        if i >= 0.9:
            countLeft += 1
    if countRight == 0 and countLeft == 0:
       #isBlocked = True
       return    
    if countLeft >= countRight :
        #print("left turn")
        leftTurn(myLidar,qcar)
    else:
        #print("right turn")
        rightTurn(myLidar,qcar)
    #return isBlocked

def rightTurn(myLidar,qcar):
    
    steering = -0.5

    while True:
        count = 0
        #qcar.write(steering=steering, throttle=0.07)
        myLidar.read()
        for i in myLidar.distances[70:100]:
            if i <= 1 and i >= 0.4:
               count += 1
        if count > 0:
            print("right turn")  
            qcar.write(steering=steering, throttle=0.07)
        else:
            steering = 0
            print(" stop right turn")
            qcar.write(steering=steering, throttle=0)
            break
 
        """count = 0
        myLidar.read()
        #qcar.write(steering=steering, throttle=throttle)
        for i in myLidar.distances[90:128]: #83:97
            if i <= 0.8 :
               count += 1
        if count > 0:
            print("right turn")
            #steering -= 0.1
            print(steering)
            
            qcar.write(steering=steering, throttle=0.02)
            #time.sleep(1.0)
            
            
        else:
            steering = -0.5
            throttle = 0
            print(" stop right turn")
            qcar.write(steering=steering, throttle=0.02)
            break"""
 
        

def leftTurn(myLidar,qcar):
    
    steering = 0.5

    while True:
        count = 0
        #qcar.write(steering=steering, throttle=0.07)
        myLidar.read()
        for i in myLidar.distances[80:110]:
            if i <= 1 and i >= 0.4:
               count += 1
        if count > 0:
            print("left turn")  
            qcar.write(steering=steering, throttle=0.07)
        else:
            steering = 0
            print(" stop left turn")
            qcar.write(steering=steering, throttle=0)
            break
        """#qcar.write(steering=steering, throttle=0.05)
        for i in myLidar.distances[52:90]:
            if i <= 0.8 :
               count += 1
        if count > 0:
            #steering += 0.1
            print("left turn")
            print(steering)
            
            qcar.write(steering=steering, throttle=0.07)
            for j in myLidar.distances[37:82]:
                if j <= 0.5:
                    return
            #time.sleep(1.0)
            
        else:
            steering = 0
            throttle = 0
            print(" stop left turn")
            qcar.write(steering=steering, throttle=0)
            break"""
       
        

# polar plot object for displaying LIDAR data later on
ax = plt.subplot(111, projection='polar')
plt.show(block=False)

# def __init__(
#             self,
#             numMeasurements=384,
#             rangingDistanceMode=0,
#             interpolationMode=1,
#             interpolationMaxDistance=1,
#             interpolationMaxAngle=0,
#             enableFiltering=True,
#             angularResolution=1*np.pi/180
#         ):



runTime = 20.0 # seconds
with QCarLidar(numMeasurements=360,rangingDistanceMode=0, interpolationMode=1, interpolationMaxDistance=1, interpolationMaxAngle=np.pi) as myLidar:
    #init qcar
    qcar = QCar(readMode=0)
    steering, throttle = 0, 0.1
    qcar.write(steering=steering, throttle=throttle)
    
    t0 = time.time()
    while True:
    # while time.time() - t0  < runTime:
        plt.cla()

        # Capture LIDAR data
        myLidar.read()
        print("distance \n")
        print(myLidar.distances[83:97])
        print("angles \n")
        print(myLidar.angles[83:97])
        # from 80 degree to 100 degree, and distance is < 0.4 meters
        # throttle need to be 0 whenever the condition is match
        # angle, distance = myLidar.filter_rplidar_data(myLidar.angles,myLidar.distances)
        ax.scatter(myLidar.angles[83:97], myLidar.distances[83:97], marker='.')
        
        isBlocked = False
        count = 0
        for i in myLidar.distances[83:97]:
            if i <= 0.8 and i >=0.1:
                count += 1
        
        if count > 1:
            print("stoppp")
            throttle = 0
            objectAvoidance(myLidar,qcar)
            isBlocked = True
            qcar.write(steering=steering, throttle=throttle)
        
        if not isBlocked:
            throttle = .07
            throttle = qcar.write(steering=steering, throttle=throttle)
            
            
        #ax.scatter(myLidar.angles, myLidar.distances, marker='.')
        ax.set_theta_zero_location("W")
        ax.set_theta_direction(-1)

        plt.pause(0.1)

    #if objects detected around 2x size of the car, so approximately 80cm
    #Angle from lidar to both side of the wheels approximately 13 degree if object at 80cm away( assuming front camera is 90' hence if object in 83 degree or 97) we need to stop and try to mitigate
    #check if right side have any object blocking typically around 30 to 60 degrees, if there are none turn right slightly with minor increase in speed and throttle until nothing detect within 83 degree or 97 
    #now direction back to 0 and speed back to normal, same thing apply to the left side

