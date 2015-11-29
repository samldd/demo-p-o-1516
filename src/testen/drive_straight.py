import sys

from BrickPi import *

BrickPiSetup()  # setup the serial port for communication
BrickPi.MotorEnable[PORT_A] = 1  # Enable the left motor.
BrickPi.MotorEnable[PORT_D] = 1  # Enable the right motor.
BrickPiSetupSensors()  # Send the properties of sensors to BrickPi.

BrickPi.EncoderOffset[PORT_A] = BrickPi.Encoder[PORT_A]
BrickPi.EncoderOffset[PORT_D] = BrickPi.Encoder[PORT_D]

BrickPiUpdateValues()

time.sleep(1)

power = 200
factor = -0.8

BrickPi.MotorSpeed[PORT_A] = int(power * factor)
BrickPi.MotorSpeed[PORT_D] = power

left_start = BrickPi.Encoder[PORT_A]
right_start = BrickPi.Encoder[PORT_D]

count = 0

while count < 1000:
    BrickPiUpdateValues()
    print BrickPi.Encoder[PORT_A] - left_start, ', ', BrickPi.Encoder[PORT_D] - right_start
    time.sleep(0.1)
    count += 1

BrickPi.MotorSpeed[PORT_A] = 0
BrickPi.MotorSpeed[PORT_D] = 0

