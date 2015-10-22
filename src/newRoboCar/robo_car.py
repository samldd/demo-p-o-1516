import time

from BrickPi import PORT_B, PORT_C, PORT_D #@UnresolvedImport
from driving import Driving
import motor as M

class RoboCar(object):

    def __init__(self):
        
        # Ports
        LEFT_PORT = PORT_C
        RIGHT_PORT = PORT_B
        
        # Hardware
        self.left_motor = M.Motor(LEFT_PORT)
        self.right_motor = M.Motor(RIGHT_PORT)
        
        # Driving
        self.driving = Driving(self)
        self.total_distance_driven = 0
    
    def get_left_motor(self):
        return self.left_motor

    def get_right_motor(self):
        return self.right_motor
    
    def drive_blind(self, distance):
        self.driving.drive_straight(distance)
    
    def turn(self, degree):
        self.driving.turn(degree)
    