import BrickPi
import motorSession

class Motor(object):
    def __init__(self, port):
        BrickPi.BrickPiSetup()
        BrickPi.BrickPiSetupSensors()
        self.motorSession = None
        self.port = port

    def enable_motor(self):
        self.motorSession = motorSession.MotorSession(self.port)
        BrickPi.MotorEnable[self.port] = 1

    def disable_motor(self):
        self.motorSession.end_session()
        BrickPi.MotorEnable[self.port] = 0

    def get_encoder_value(self):
        self.motorSession.get_session_encoder()

    def get_velocity(self):
        self.motorSession.get_velocity()

    def set_velocity(self,velocity):
        self.motorSession.set_velocity(velocity)
