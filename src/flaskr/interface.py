import subprocess, sys
from time import gmtime, strftime, sleep

if sys.platform != 'win32':
    from BrickPi import *   #import BrickPi.py file to use BrickPi operations

from threading import Thread

lastDirectionForward = True

def setup_brickpi():
    global referenceB, referenceC
    BrickPiSetup()  # setup the serial port for communication

    BrickPi.MotorEnable[PORT_C] = 1     #Enable the Motor A
    BrickPi.MotorEnable[PORT_B] = 1
    BrickPiSetupSensors()       #Send the properties of sensors to BrickPi

    BrickPiUpdateValues()
    referenceB = BrickPi.Encoder[PORT_B]
    referenceC = BrickPi.Encoder[PORT_C]

if sys.platform != 'win32':
    setup_brickpi()

def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it

def forward():
    global lastDirectionForward
    BrickPi.MotorSpeed[PORT_C] = 200    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = 200
    BrickPiUpdateValues()
    lastDirectionForward = True

def backward():
    global lastDirectionForward
    BrickPi.MotorSpeed[PORT_C] = -200    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = -200
    BrickPiUpdateValues()
    lastDirectionForward = False

def left():
    if lastDirectionForward:
        BrickPi.MotorSpeed[PORT_C] = 100    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 250
    else:
        BrickPi.MotorSpeed[PORT_C] = -100    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = -250
    BrickPiUpdateValues()

def right():
    if lastDirectionForward:
        BrickPi.MotorSpeed[PORT_C] = 250    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 100
    else:
        BrickPi.MotorSpeed[PORT_C] = -250    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = -100
    BrickPiUpdateValues()

def line():
    pass

def square():
    pass

def circle():
    for i in range(10):
        BrickPi.MotorSpeed[PORT_C] = 100    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 250
        BrickPiUpdatesValues()

def picture():
    subprocess.call(["raspistill", "-0", "/robot/flaskr/static/last_image.jpg", "-t", "1"])


def kill():
    if sys.platform == 'win32':
        subprocess.call(["Taskkill", "/F", "/IM", "python.exe"])
    else:
        subprocess.call(["sudo", "killall", "python", "-9"])

def get_debug_info():
    global referenceB, referenceC
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

