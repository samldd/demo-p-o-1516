import subprocess, sys, traceback, math
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

def forward(motorvalue=200):
    global lastDirectionForward
    BrickPi.MotorSpeed[PORT_C] = motorvalue    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = motorvalue
    BrickPiUpdateValues()
    lastDirectionForward = True

def backward(motorvalue=-200):
    global lastDirectionForward
    BrickPi.MotorSpeed[PORT_C] = motorvalue    #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = motorvalue
    BrickPiUpdateValues()
    lastDirectionForward = False

def sharpleft():
    startval = BrickPi.Encoder[PORT_C]
    while abs(BrickPi.Encoder[PORT_C] - startval) < 1000:
        if lastDirectionForward:
            BrickPi.MotorSpeed[PORT_C] = 100    #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = 0
        else:
            BrickPi.MotorSpeed[PORT_C] = -100    #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

def sharpright():
    startval = BrickPi.Encoder[PORT_C]
    while abs(BrickPi.Encoder[PORT_C] - startval) < 1000:
        if lastDirectionForward:
            BrickPi.MotorSpeed[PORT_C] = 250    #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = 0
        else:
            BrickPi.MotorSpeed[PORT_C] = -250    #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

def left(leftMotorAbsSpeed = 100, rightMotorAbsSpeed = 250):
    if lastDirectionForward:
        BrickPi.MotorSpeed[PORT_C] = leftMotorAbsSpeed    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = rightMotorAbsSpeed
    else:
        BrickPi.MotorSpeed[PORT_C] = -leftMotorAbsSpeed    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = -rightMotorAbsSpeed
    BrickPiUpdateValues()

def right():
    left(250,100)

def line():
    pass

def square():
    pass

def circle():
    startval = BrickPi.Encoder[PORT_B]
    while BrickPi.Encoder[PORT_B] - startval < 15000:
        BrickPi.MotorSpeed[PORT_C] = 175    #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 250
        BrickPiUpdateValues()

def followline():
    while True:
        picture()
        #BEREKEN HOEK met code in find_line.py
        #draai juiste hoek
        #rij rechtdoor

def stream():
    time = 20 #stream time in seconds
    timelapse = 100 #milliseconds between pics, make twice as fast than actual wanted fps
    #-q set jpeg quality
    #-sh set sharpness (-100 to 100)
    subprocess.Popen(["raspistill", "-o", "/home/pi/robot/flaskr/static/last_image.jpg", "-t", str(time*1000), "-tl", str(timelapse), "-n", "-w", "640", "-h", "480", "-md", "6"])

def picture():
    width =2592
    height=1944
    scale = 4

    subprocess.call(["raspistill", "-o", "/home/pi/robot/flaskr/static/last_image.jpg", "-t", "1", "-n", "-w", str(width/scale), "-h", str(height/scale)])

def drive_accelerometer(xValue, yValue):
    if -10 < yValue < 10 and -10 < xValue < 10:
		BrickPi.MotorSpeed[PORT_C] = 0
		BrickPi.MotorSpeed[PORT_B] = 0
		BrickPiUpdateValues()
		return #dead zone


	totalpower = float(abs(xValue)-10)/80*510

	leftMotorFrac = float(yValue+170)/340
	BrickPi.MotorSpeed[PORT_C] = (-math.copysign(1, xValue))*leftMotorFrac*totalpower    #Set the speed of MotorA (-255 to 255)
	BrickPi.MotorSpeed[PORT_B] = (-math.copysign(1, xValue))*(1-leftMotorFrac)*totalpower

	BrickPiUpdateValues()


def kill():
    if sys.platform == 'win32':
        subprocess.call(["Taskkill", "/F", "/IM", "python.exe"])
    else:
        subprocess.call(["sudo", "killall", "python", "-9"])

def get_debug_info():
    if sys.platform == 'win32':
        return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())
    try:
        global referenceB, referenceC

        C = BrickPi.Encoder[PORT_C] - referenceC  # print the encoder degrees
        B = BrickPi.Encoder[PORT_B] - referenceB

        debuginfo = "it is now: %s<br><br>"%strftime("%d/%m/%Y %H:%M:%S", gmtime())
        debuginfo+= "motor left encoder: " + str(C)
        debuginfo+= "<br>" #newline in html
        debuginfo+= "motor right encoder:" + str(B)
        return debuginfo
    except:
        return traceback.format_exc().replace('\n', '<br />')
