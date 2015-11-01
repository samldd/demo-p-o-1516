__author__ = 'sam_l'
import BrickPi
import time

class MotorSession(object):

    def __init__(self, port):
        self.encoder_reference = BrickPi.Encoder[self.port]
        self.velocity = 0
        self.port = port

    def get_velocity(self):
        return self.velocity

    def set_velocity(self,velocity):
        if not(type(velocity) == int):
            velocity = int(velocity)
        self.velocity = max(-250, min(velocity, 250)) # bereik snelheid [-255,255]
        BrickPi.MotorSpeed[self.port] = velocity

    def get_session_encoder(self):
        current_ticks = BrickPi.Encoder[self.port]
        return current_ticks - self.encoder_reference

    def end_session(self):
        self.set_velocity(-self.get_velocity())
        time.sleep(0.05)
        self.set_speed(0)