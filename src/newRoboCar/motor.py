from BrickPi import *
import math
import time

class Motor(object):

    def __init__(self, port):
        BrickPiSetup()
        BrickPiSetupSensors()
        self.port = port
        self.perimeter = 0.056 * math.pi  # perimeter in meters
        self.wheel_distance = 0.13
        self.reference_value = 0
        self.current_speed = 0
        self.running = False

    def start(self, speed):
        self.reset_encoder()
        BrickPi.MotorEnable[self.port] = 1
        self.set_speed(speed)
        self.running = True

    def stop(self, delay_when_stopping=0.05):
        self.set_speed(-self.current_speed)
        time.sleep(delay_when_stopping)
        self.set_speed(0)
        BrickPi.MotorEnable[self.port] = 0
        self.running = False

    def reset_encoder(self):
        BrickPiUpdateValues()
        time.sleep(0.2)
        self.reference_value = BrickPi.Encoder[self.port]

    def get_encoder(self):
        return BrickPi.Encoder[self.port] - self.reference_value

    def set_speed(self, speed):
        speed = int(max(-250, min(speed, 250)))
        BrickPi.MotorSpeed[self.port] = speed
        self.current_speed = speed

    def is_running(self):
        return self.running
