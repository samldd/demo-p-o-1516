from BrickPi import *
import motorSession
import time

class Motor(object):
    def __init__(self, port):
        BrickPiSetup()
        BrickPiSetupSensors()
        self.motorSession = None
        self.port = port

    def enable_motor(self):
        BrickPi.MotorEnable[self.port] = 1
        time.sleep(0.10)
        self.motorSession = motorSession.MotorSession(self.port)

    def disable_motor(self):
        self.motorSession.end_session()
        BrickPi.MotorEnable[self.port] = 0

    def get_encoder_value(self):
        encoder = self.motorSession.get_session_encoder()
        return encoder

    def get_velocity(self):
        self.motorSession.get_velocity()

    def set_velocity(self,velocity):
        self.motorSession.set_velocity(velocity)

