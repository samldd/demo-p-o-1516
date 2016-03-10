from BrickPi import *

class Motor(object):

    left = None
    right = None

    def __init__(self, port):
        self.velocity = 0
        self.port = port
        self.enable_motor()
        self.encoder_reference = BrickPi.Encoder[port]

    def set_velocity(self,velocity):
        if not(type(velocity) == int):
            velocity = int(velocity)
        self.velocity = max(-250, min(velocity, 250)) # bereik snelheid [-255,255]
        BrickPi.MotorSpeed[self.port] = velocity
        BrickPi.MotorSpeed[(self.port+2)%4] = velocity

    def get_encoder_value(self):
        current_ticks = self.__encoder()
        new_val = current_ticks - self.encoder_reference
        return new_val

    def __encoder(self):
        if self.port == 1:
            A = BrickPi.Encoder[1]
            B = BrickPi.Encoder[3]
            return A if B == 0 else B
        else:
            A = BrickPi.Encoder[2]
            B = BrickPi.Encoder[0]
            return A if B == 0 else B

    def reset_motor(self):
        self.encoder_reference = self.__encoder()

    def enable_motor(self):
        BrickPiSetup()
        BrickPi.MotorEnable[self.port] = 1
        BrickPi.MotorEnable[(self.port+2) % 4] = 1
        BrickPiSetupSensors()
        BrickPiUpdateValues()
        time.sleep(0.10)

    def disable_motor(self):
        self.stop()
        MotorEnable[self.port] = 0
        MotorEnable[(self.port+2)%4] = 0

    def stop(self):
        self.set_velocity(-self.velocity)
        time.sleep(0.05)
        self.set_velocity(0)

if not(Motor.left and Motor.right):
    Motor.left = Motor(1)
    Motor.right = Motor(2)