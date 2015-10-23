import subprocess
from time import gmtime, strftime
#from src.newRoboCar import robo_car
from BrickPi import *   #import BrickPi.py file to use BrickPi operations


def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it

@debug
def forward():
    BrickPi.MotorSpeed[PORT_C] = 200    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 200
    BrickPiUpdateValues()

@debug
def backward():
    BrickPi.MotorSpeed[PORT_C] = -200    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = -200
    BrickPiUpdateValues()

@debug
def left():
    BrickPi.MotorSpeed[PORT_C] = 100    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 250
    BrickPiUpdateValues()

@debug
def right():
    BrickPi.MotorSpeed[PORT_C] = 250    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 100
    BrickPiUpdateValues()

@debug
def kill():
    ##windows
    #subprocess.call(["Taskkill", "/F", "/IM", "python.exe"])
    subprocess.call(["sudo", "killall", "python", "-9"])

@debug
def get_debug_info():
    # result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
    # if not result :                 # if updating values succeeded
    #     C = ( BrickPi.Encoder[PORT_C] - referenceC )  # print the encoder degrees
    #     B = ( BrickPi.Encoder[PORT_B] - referenceB )
    #     print "%d: %d , %d" %(i,C,B)
    #     i = i +1
    #
    # debuginfo = "motor left speed:",C
    # debuginfo+= "<br>" #newline in html
    # debuginfo = "motor right speed:", B
    # return debuginfo

    return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_C] = 1     #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1
BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

#result = BrickPiUpdateValues()
#global referenceB, referenceC
#referenceB = BrickPi.Encoder[PORT_B]
#referenceC = BrickPi.Encoder[PORT_C]
