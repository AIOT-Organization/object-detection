from pal.products.qcar import QCar
import threading
import socket

import payload

class SteeringWheelThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.stoppingFlag = False

        self.steeringAngle = 0.0
        self.throttle = 0.0
        self.reverse = False

        self.max_throttle = 0.2
        self.min_throttle = -0.2
        self.max_steering = 0.5
        self.min_steering = -0.5

        self.myCar = QCar(readMode=0)
        self.PORT = 38821  # Port to listen on (non-privileged ports are > 1023)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', self.PORT))
            
            while not self.stoppingFlag:
                data = s.recvfrom(100)[0].decode('utf-8')
                if not data:
                    pass

                packet = payload.payload_handler(data)
                buffer = []
                try:
                    if packet.read(buffer, 4) == -1 or \
                    packet.read(buffer, 4) == -1 or \
                    packet.read(buffer, 8) == -1 or \
                    packet.read(buffer, 8) == -1:
                        print("Warning: Packet Length Too short")
                        continue
                    
                    event = int(buffer[1])

                    if event == 1536:
                        #IF Axis is Steering Wheel
                        if float(buffer[2]) == 0:
                            steer = -1* float(buffer[3]) * 2
                            if abs(self.steeringAngle - steer) < 0.01:
                                continue

                            if (self.steeringAngle == self.min_steering and steer < self.min_steering
                                or
                                self.steeringAngle == self.max_steering and steer > self.max_steering):
                                continue

                            if steer < 0:
                                self.steeringAngle = max(steer, self.min_steering)
                            else:
                                self.steeringAngle = min(steer, self.max_steering)
                            
                        #IF Axis is Throttle
                        elif float(buffer[2]) == 1:
                            
                            th = 0.6 * ((abs(float(buffer[3]) -1 ) /2 ) * 0.2)
                            if th < 0:
                                self.throttle = max(th, self.min_throttle)
                            else:
                                self.throttle = min(th, self.max_throttle)

                    if event == 1539:
                        if float(buffer[2]) == 5:
                            print("Reverse Triggered")
                            self.reverse = True
                        elif float(buffer[2]) == 4:
                            print("Forward Triggered")
                            self.reverse = False
                        elif float(buffer[2]) == 0:
                            self.steeringAngle = 0
                            self.throttle = 0
                            self.reverse = False

                    if self.reverse:
                        if self.throttle > 0:
                            self.throttle *= -1
                    else:
                        self.throttle = abs(self.throttle)
                    
                    self.myCar.write(throttle=self.throttle, steering=self.steeringAngle)
                        
                except Exception as e:
                    print("Invalid Packet Size")
                    print(e)

        self.myCar.terminate()   

    def getData(self):
        return self.steeringAngle, self.throttle, self.reverse



    
    