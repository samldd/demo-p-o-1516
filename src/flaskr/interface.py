import subprocess
import sys
import traceback
import math
from PID import PID
from time import gmtime, strftime, sleep

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if sys.platform != 'win32':
    import robo_car
    import line_follower
    from BrickPi import *
    import value_updater

    vu = value_updater.ValueUpdater()
    vu.start()
    rob = robo_car.RoboCar()

    import motor
    right_motor = motor.Motor.left
    left_motor = motor.Motor.right

lastDirectionForward = True
is_driving = False
drive_manual = True
last_pid_in = None
last_pid_out = None
last_motor_left = None
last_motor_right = None

def brake():
    setMotorSpeeds(0, 0)

def forward(motorvalue=200):
    global lastDirectionForward, left_motor, right_motor, drive_manual, is_driving
    if drive_manual:
        if not lastDirectionForward and is_driving:
            brake()
        else:
            setMotorSpeeds(motorvalue, motorvalue)
            lastDirectionForward = True

def manual():
    global drive_manual,rob
    drive_manual = True
    rob.deactivate_automatic_driving()

def backward(motorvalue=-200):
    global lastDirectionForward, left_motor, right_motor, drive_manual, is_driving
    if drive_manual:
        if is_driving and lastDirectionForward:
            forward(0)
        else:
            setMotorSpeeds(motorvalue, motorvalue)
            lastDirectionForward = False

import time
def sharpleft():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        if lastDirectionForward:
            setMotorSpeeds(-200,200)
        else:
            setMotorSpeeds(200, -200)
        time.sleep(1)
        setMotorSpeeds(0, 0)

def sharpright():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        if lastDirectionForward:
            setMotorSpeeds(200,-200)
        else:
            setMotorSpeeds(-200,200)
        time.sleep(1)
        setMotorSpeeds(0, 0)

def left(leftMotorAbsSpeed = 100, rightMotorAbsSpeed = 250):
    global left_motor, right_motor, drive_manual
    if drive_manual:
        if lastDirectionForward:
            setMotorSpeeds(leftMotorAbsSpeed, rightMotorAbsSpeed)
        else:
            setMotorSpeeds(-leftMotorAbsSpeed, -rightMotorAbsSpeed)

def right():
    global drive_manual
    if drive_manual:
        left(250,100)

def setMotorSpeeds(left, right):
    global left_motor, right_motor, is_driving
    if left == 0 and right == 0:
        is_driving = False
    else:
        is_driving = True
    left_motor.set_velocity(left)    #Set the speed of MotorA (-255 to 255)
    right_motor.set_velocity(right)

def drive_auto():
    global drive_manual,rob
    drive_manual = False
    rob.activate_automatic_driving()

def drive_accelerometer(xValue, yValue):
    global left_motor, right_motor
    #hier xValue tussen -90 en 90
    #-90 = hard vooruit
    # ]-10, 10[ is stil staan
    # 90 = hard achteruit
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

from logger import Logger
logger = Logger("interface")

debuginfo = ""
def get_debug_info():
    global logger,debuginfo
    if sys.platform == 'win32':
        return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())
    try:
        debuginfo = logger.get_log() + debuginfo
        return debuginfo
    except:
        return traceback.format_exc().replace('\n', '<br />')


def addCommand(command):
    global rob
    rob.add_instruction(command)

def getCommandQueue():
    global rob
    return rob.get_commands()

def removeCommand():
    global rob
    rob.remove_instruction()

import numpy as np

def follow_line(x):
    global rob,follow_info,logger,drive_manual
    if drive_manual:
        logger.reset_logger()
        logger.add_log("cameraInfo: " + str(np.array(eval(x))))
    rob.follow_the_line(x)

try: import driving
except: pass
def set_power_factor(x):
    print "try to set battery factor"
    driving.Driving.battery_factor = x
    print driving.Driving.battery_factor

def tune_parameter(key, value):
    print key, value
    pass