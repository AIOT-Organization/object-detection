from pal.products.qcar import QCar

 
myCar = QCar(readMode=0)

# Define speed settings
throttle = 0.0
steering = 0.0

def forward():
    
    myCar.write(throttle=throttle, steering=0)

def backward():
    
    myCar.write(throttle=-throttle, steering=0)

def left():
    
    myCar.write(throttle=throttle, steering=-0.5)

def right():
    
    myCar.write(throttle=throttle, steering=0.5)

def stop():
    
    myCar.write(throttle=0.0, steering=0.0)

def update_leds(LEDs):
    
    myCar.write(throttle=0, steering=0, LEDs=LEDs)
