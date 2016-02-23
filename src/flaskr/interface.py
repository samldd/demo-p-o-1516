import subprocess
import sys
import traceback
import math
from time import gmtime, strftime, sleep
import robo_car
import line_follower

if sys.platform != 'win32':
    from BrickPi import *
    import value_updater

    vu = value_updater.ValueUpdater()
    vu.start()

    from motor import Motor
    right_motor = Motor(PORT_B)
    left_motor = Motor(PORT_C)

lastDirectionForward = True
drive_manual = True

def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it

def forward(motorvalue=200):
    global lastDirectionForward, left_motor, right_motor, drive_manual
    if drive_manual:
        left_motor.set_velocity(motorvalue)    #Set the speed of MotorA (-255 to 255)
        right_motor.set_velocity(motorvalue)
        lastDirectionForward = True

def manual():
    global drive_manual
    drive_manual = True

def backward(motorvalue=-200):
    global lastDirectionForward, left_motor, right_motor, drive_manual
    if drive_manual:
        left_motor.set_velocity(motorvalue)
        right_motor.set_velocity(motorvalue)
        lastDirectionForward = False

def sharpleft():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        startval = left_motor.get_encoder_value()
        while abs(left_motor.get_encoder_value() - startval) < 1000:
            if lastDirectionForward:
                left_motor.set_velocity(-200)    #Set the speed of MotorA (-255 to 255)
                right_motor.set_velocity(200)
            else:
                left_motor.set_velocity(200)    #Set the speed of MotorA (-255 to 255)
                right_motor.set_velocity(-200)

def sharpright():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        startval = left_motor.get_encoder_value()
        while abs(left_motor.get_encoder_value() - startval) < 1000:
            if lastDirectionForward:
                left_motor.set_velocity(200)    #Set the speed of MotorA (-255 to 255)
                right_motor.set_velocity(-200)
            else:
                left_motor.set_velocity(-200)    #Set the speed of MotorA (-255 to 255)
                right_motor.set_velocity(200)

def left(leftMotorAbsSpeed = 100, rightMotorAbsSpeed = 250):
    global left_motor, right_motor, drive_manual
    if drive_manual:
        if lastDirectionForward:
            left_motor.set_velocity(leftMotorAbsSpeed)
            right_motor.set_velocity(rightMotorAbsSpeed)
        else:
            left_motor.set_velocity(-leftMotorAbsSpeed)
            right_motor.set_velocity(-rightMotorAbsSpeed)

def right():
    global drive_manual
    if drive_manual:
        left(250,100)

def followline():
    global drive_manual
    drive_manual = False

def drive_accelerometer(xValue, yValue):
    global left_motor, right_motor
    if drive_manual:
        if -10 < yValue < 10 and -10 < xValue < 10:
            left_motor.set_velocity(0)
            right_motor.set_velocity(0)
            return #dead zone

        basePower = 55
        totalpower = float(abs(xValue)-10)/80*(255-basePower)

        leftMotorFrac = float(yValue+80)/160
        direction = (-math.copysign(1, xValue)) #1 is vooruit, -1 is achteruit

        if leftMotorFrac >= 0.5:
            print "left motor power:" + str(direction*(totalpower+basePower))
            print "right motor power:" + str(direction*((1-leftMotorFrac)*(totalpower/leftMotorFrac)+basePower))
            left_motor.set_velocity(int(direction*(totalpower+basePower)))
            right_motor.set_velocity(int(direction*((1-leftMotorFrac)*(totalpower/leftMotorFrac)+basePower)))
        elif leftMotorFrac < 0.5:
            print "left motor power:" + str(direction*(leftMotorFrac)*(totalpower/(1-leftMotorFrac)+basePower))
            print "right motor power:" + str(direction*(totalpower+basePower))

            left_motor.set_velocity(int(direction*(leftMotorFrac)*(totalpower/(1-leftMotorFrac)+basePower)))
            right_motor.set_velocity(int(direction*(totalpower+basePower)))

def kill():
    if sys.platform == 'win32':
        subprocess.call(["Taskkill", "/F", "/IM", "python.exe"])
    else:
        subprocess.call(["sudo", "killall", "python", "-9"])

def get_debug_info():
    global left_motor, right_motor
    if sys.platform == 'win32':
        return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())
    try:
        C = str(left_motor.get_encoder_value())  # print the encoder degrees
        B = str(right_motor.get_encoder_value())

        style100 = "style=\"width:100" + "%" + "\""
        debuginfo = "<table  " + style100 + "><tr><td>motor left encoder: %s</td><td style=\"text-align: right\">time: %s</td></tr>" % (C, strftime("%H:%M:%S", gmtime()))
        debuginfo += "<tr><td colspan=\"2\">motor right encoder: %s</td></tr></table>" % B
        return debuginfo
    except:
        return traceback.format_exc().replace('\n', '<br />')















#OBSOLETE?
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
