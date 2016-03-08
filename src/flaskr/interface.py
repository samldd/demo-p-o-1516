import subprocess
import sys
import traceback
import math
from PID import PID
from time import gmtime, strftime, sleep

if sys.platform != 'win32':
    import robo_car
    import line_follower
    from BrickPi import *
    import value_updater

    vu = value_updater.ValueUpdater()
    vu.start()

    from motor import Motor
    right_motor = Motor(PORT_B)
    left_motor = Motor(PORT_C)

lastDirectionForward = True
is_driving = False
drive_manual = True
last_pid_in = None
last_pid_out = None
last_motor_left = None
last_motor_right = None

def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it

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
    global drive_manual
    drive_manual = True

def backward(motorvalue=-200):
    global lastDirectionForward, left_motor, right_motor, drive_manual, is_driving
    if drive_manual:
        if is_driving and lastDirectionForward:
            forward(0)
        else:
            setMotorSpeeds(motorvalue, motorvalue)
            lastDirectionForward = False

def sharpleft():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        startval = left_motor.get_encoder_value()
        while abs(left_motor.get_encoder_value() - startval) < 1000:
            if lastDirectionForward:
                setMotorSpeeds(-200,200)
            else:
                setMotorSpeeds(200, -200)

def sharpright():
    global left_motor, right_motor, drive_manual
    if drive_manual:
        startval = left_motor.get_encoder_value()
        while abs(left_motor.get_encoder_value() - startval) < 1000:
            if lastDirectionForward:
                setMotorSpeeds(200,-200)
            else:
                setMotorSpeeds(-200,200)

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
    global drive_manual
    drive_manual = False

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


commandQueue = []

def get_debug_info():
    global left_motor, right_motor, commandQueue, last_pid_out, last_pid_in, last_motor_left, last_motor_right
    if sys.platform == 'win32':
        return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())
    try:
        C = str(left_motor.get_encoder_value())  # print the encoder degrees
        B = str(right_motor.get_encoder_value())

        style100 = "style=\"width:100" + "%" + "\""
        debuginfo = "<table  " + style100 + "><tr><td>motor left encoder: %s</td><td style=\"text-align: right\">time: %s</td></tr>" % (C, strftime("%H:%M:%S", gmtime()))
        debuginfo += "<tr><td colspan=\"2\">motor right encoder: %s</td></tr></table>" % B
        debuginfo += "<p>Last PID in: "+str(last_pid_in) +"<br>Last PID out: " + str(last_pid_out) + "</p>"
        debuginfo += "<p>Last lefd t speed: "+str(last_motor_left) +"<br>Last right speed: " + str(last_motor_right) + "</p>"

        if commandQueue:
            debuginfo += "<p>command queue: " + commandQueue[0]

            for command in commandQueue[1:]:
                debuginfo+= " -> " + command
            debuginfo += "</p>"
        else:
            debuginfo += "command queue is empty, click \"next crossroad X\" to give directions to the robot."
        return debuginfo
    except:
        return traceback.format_exc().replace('\n', '<br />')

def addCommand(command):
    global commandQueue
    commandQueue.append(command)

def getNextCommand():
    global commandQueue
    rv = commandQueue[0]
    commandQueue = commandQueue[1:]
    return rv

p=PID(3.0,0.4,1.2)
p.setPoint(0)
basePower = 55
extrapower = 100
def follow_line(x):
    global last_pid_out, last_pid_in, last_motor_left, last_motor_right
    if not drive_manual:
        if eval(x)[1] == None:
            right_motor.set_velocity(0)
            left_motor.set_velocity(0)
            last_motor_left = 0
            last_motor_right = 0
            last_pid_in = None
        else:
            mikpunt = eval(x)[1][0]-320
            last_pid_in = mikpunt
            out = p.update(mikpunt)
            last_pid_out = out
            print "PID OUT: " + str(out)
            if out > 50:
                out = 50
            if out < -50:
                out = -50

            frac = float(out+50)/100
            if frac >= 0.5:
                lspeed = int(((1-frac)*(extrapower/frac)+basePower))
                rspeed = extrapower+basePower
                print "right motor power:" + str(rspeed)
                print "left motor power:" + str(lspeed)
                right_motor.set_velocity(rspeed)
                left_motor.set_velocity(lspeed)
                last_motor_right = rspeed
                last_motor_left = lspeed
            elif frac < 0.5:
                rspeed = int((frac)*(extrapower/(1-frac)+basePower))
                lspeed = int(extrapower+basePower)
                print "right motor power:" + str(rspeed)
                print "left motor power:" + str(lspeed)

                right_motor.set_velocity(rspeed)
                left_motor.set_velocity(lspeed)
                last_motor_left = lspeed
                last_motor_right = rspeed




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
