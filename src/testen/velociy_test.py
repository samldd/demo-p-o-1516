__author__ = 'sam_l'


from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_C] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1
BrickPi.MotorSpeed[PORT_C] = -255    #Set the speed of MotorA (-255 to 255)
BrickPi.MotorSpeed[PORT_B] = -255

BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

result = BrickPiUpdateValues()
referenceB = BrickPi.Encoder[PORT_B]
referenceC = BrickPi.Encoder[PORT_C]
i = 0

while i < 20:
    result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
    C = ( BrickPi.Encoder[PORT_C] - referenceC )  # print the encoder degrees
    B = ( BrickPi.Encoder[PORT_B] - referenceB )
    print "%d: %d , %d" %(i,C,B)
    i = i+1
    time.sleep(.05)		#sleep for 100 ms

# Note: One encoder value counts for 0.5 degrees. So 360 degrees = 720 enc. Hence, to get degress = (enc%720)/2
