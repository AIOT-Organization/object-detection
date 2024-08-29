# import lib
import pygame
from pal.products.qcar import QCar
from pal.utilities.math import *
import numpy as np
import time

# create qcar
myCar = QCar(readMode=0)

# init Pygame
pygame.init()

# setup screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("QCar Manual Control")

# set up +- increment and maximum
throttle_increment = 0.02
steering_increment = 0.1
max_throttle = 0.2
min_throttle = -0.2
max_steering = 0.5
min_steering = -0.5

w, a, s, d = False, False, False, False

# default speed and direction
throttle = 0.0
steering = 0.0

def stop():
    throttle = 0.0
    steering = 0.0

# main program
runTime = 10.0 # seconds
t0 = time.time()

while time.time() - t0  < runTime :
    # t = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or  event.key == pygame.K_d:
                steering = 0.0

            if event.key == pygame.K_w:
                if w:
                    throttle += throttle_increment
                    w = False
            if event.key == pygame.K_s:
                if s:
                    throttle -= throttle_increment
                    s = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                while True:
                    steering += steering_increment
            elif event.key == pygame.K_d:
                steering -= steering_increment
            elif event.key == pygame.K_s:
                s = True
            elif event.key == pygame.K_w:
                w = True

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_w]:
    #     throttle += throttle_increment
    #     throttle = min(throttle, max_throttle)
    # elif keys[pygame.K_s]:
    #     throttle -= throttle_increment
    #     throttle = max(throttle, min_throttle)

    # if keys[pygame.K_a]:
    #     steering -= steering_increment
    #     steering = max(steering, min_steering)
    # elif keys[pygame.K_d]:
    #     steering += steering_increment
    #     steering = min(steering, max_steering)
    
    if keys[pygame.K_q]:
        steering , throttle = 0.0 , 0.0

    # update qcar control
    myCar.read_write_std(throttle=throttle, steering=steering)
    print(throttle, steering)

   


myCar.terminate()

# exitPygame
pygame.quit()
