__author__ = 'sam_l'
from BrickPi import BrickPi
import time

class MotorSession(object):

    def __init__(self, port):
        self.velocity = 0
        self.port = port
        self.previous = 0
        self.encoder_reference = BrickPi.Encoder[self.port]

    def get_velocity(self):
        return self.velocity

    def set_velocity(self,velocity):
        if not(type(velocity) == int):
            velocity = int(velocity)
        self.velocity = max(-250, min(velocity, 250)) # bereik snelheid [-255,255]
        BrickPi.MotorSpeed[self.port] = velocity

    def get_session_encoder(self):
        current_ticks = BrickPi.Encoder[self.port]
        if current_ticks == 0:
            self.port_switch()
        current_ticks = BrickPi.Encoder[self.port]
        new_val = current_ticks - self.encoder_reference
        return new_val

    def end_session(self):
        self.set_velocity(-self.get_velocity())
        time.sleep(0.05)
        self.set_velocity(0)

    def port_switch(self):
        if self.port == BrickPi.PORT_A:
            self.port = BrickPi.port_C
        elif self.port == BrickPi.PORT_B:
            self.port = BrickPi.port_D
        elif self.port == BrickPi.PORT_C:
            self.port = BrickPi.port_A
        elif self.port == BrickPi.PORT_D:
            self.port = BrickPi.port_B