from BrickPi import BrickPi, BrickPiSetup, BrickPiUpdateValues, motorRotateDegree, BrickPiSetupSensors
from BrickPi import PORT_A, PORT_B, PORT_C
import math


class Motor(object):

    def __init__(self, port):
        #port= [PORT_A]
        BrickPiSetup()
        self.port = port
        self.perimeter = 0.056 * math.pi  # perimeter in meters

    def turn_degrees(self, degrees, power):
        BrickPiUpdateValues()
        motorRotateDegree(power, degrees, self.port, 0)


class MotorWheels(Motor):

    def __init__(self):
        super(MotorWheels, self).__init__([PORT_C, PORT_B])
        self.wheel_distance = 0.13
        BrickPi.MotorEnable[PORT_B] = 1  # right wheel
        BrickPi.MotorEnable[PORT_C] = 1  # left wheel
        BrickPiSetupSensors()

    def drive(self, distance):
        #distance in meters
        degrees = distance / self.perimeter * 360
        self.turn_degrees([degrees, degrees], [150, 150])

    def turn(self, degree):
        wheel_degrees = self.wheel_distance * math.pi * degree / self.perimeter
        self.turn_degrees([-wheel_degrees, wheel_degrees], [200, 200])
    
    def stop(self):
        self.turn_degrees([0, 0], [0, 0])
    

class MotorSensor(Motor):

    def __init__(self):
        super(MotorSensor, self).__init__([PORT_A])
        BrickPi.MotorEnable[PORT_A] = 1  # motor on top
        BrickPiSetupSensors()

    def turn(self, degree):
        self.turn_degrees([degree], [100])
