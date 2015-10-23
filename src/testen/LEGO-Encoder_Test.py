#!/usr/bin/env python
# Jaikrishna
# Initial Date: June 24, 2013
# Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_C] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1
BrickPi.MotorSpeed[PORT_C] = 100    #Set the speed of MotorA (-255 to 255)
BrickPi.MotorSpeed[PORT_B] = 250

BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

result = BrickPiUpdateValues()
referenceB = BrickPi.Encoder[PORT_B]
referenceC = BrickPi.Encoder[PORT_C]
i = 0
while True:
    result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
    if not result :                 # if updating values succeeded
        C = ( BrickPi.Encoder[PORT_C] - referenceC )  # print the encoder degrees
        B = ( BrickPi.Encoder[PORT_B] - referenceB )
        print "%d: %d , %d" %(i,C,B)
        i = i +1
    time.sleep(.1)		#sleep for 100 ms

# Note: One encoder value counts for 0.5 degrees. So 360 degrees = 720 enc. Hence, to get degress = (enc%720)/2
