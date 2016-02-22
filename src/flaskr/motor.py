from BrickPi import *
import time

class Motor(object):
    def __init__(self, port):
        BrickPiSetup()
        self.velocity = 0
        self.port = port
        self.enable_motor()
        self.encoder_reference = BrickPi.Encoder[port]

    def set_velocity(self,velocity):
        if not(type(velocity) == int):
            velocity = int(velocity)
        self.velocity = max(-250, min(velocity, 250)) # bereik snelheid [-255,255]
        BrickPi.MotorSpeed[self.port] = velocity

    def get_encoder_value(self):
        current_ticks = BrickPi.Encoder[self.port]
        while current_ticks == 0 and not(current_ticks == self.encoder_reference):
            self.port_switch()
            current_ticks = BrickPi.Encoder[self.port]
        new_val = current_ticks - self.encoder_reference
        return new_val

    def reset_motor(self):
        self.encoder_reference = self.get_encoder_value()

    def enable_motor(self):
        BrickPi.MotorEnable[self.port] = 1
        BrickPiSetupSensors()
        time.sleep(0.10)

    def disable_motor(self):
        self.stop()
        MotorEnable[self.port] = 0

    def stop(self):
        self.set_velocity(-self.velocity)
        time.sleep(0.05)
        self.set_velocity(0)

    def port_switch(self):
        print "!!!!!!!!!!  PORT SWITCH : PORT %s !!!!!!!!!!!!!" %self.port
        if self.port == 0:
            self.port = 2
        elif self.port == 1:
            self.port = 3
        elif self.port == 2:
            self.port = 0
        elif self.port == 3:
            self.port = 1
        print "NEW PORT: %s" %self.port

