import time
import math

import driving
import value_updater
import camera


class RoboCar(object):
    def __init__(self):
        self.value_updater = value_updater.ValueUpdater()
        self.value_updater.start()
        self.driving = driving.Driving()
        self.driving.start()
        self.camera = camera.Camera()
    
    def drive_straight(self, distance):
        print "drive forward"
        self.driving.drive_straight()
        (init,_) = self.driving.get_driven_distance()
        (left,_) = self.driving.get_driven_distance()
        while left-init < distance:
            time.sleep(0.1)
            (left,_) = self.driving.get_driven_distance()
        self.driving.stop_driving()

    def drive_back(self,distance):
        print "drive back"
        self.driving.drive_back()
        (init,_) = self.driving.get_driven_distance()
        (left,_) = self.driving.get_driven_distance()
        while left-init > distance:
            print left-init
            time.sleep(0.1)
            (left,_) = self.driving.get_driven_distance()
        self.driving.stop_driving()

    def turn(self,degree):
        print "turn %d" %degree
        self.driving.turn(degree)
        while self.driving.get_status() == "turning":
            time.sleep(0.1)

    def drive_arc(self,degrees, radius):
        print "drive arc"
        radius *= 100
        self.driving.drive_arc(radius)
        (initl,initr) = self.driving.get_driven_distance()
        (left,right) = self.driving.get_driven_distance()
        goal = (math.fabs(radius)-7.5)/50*3.14*degrees/360
        print "GOAL: %d" %goal
        if radius < 0:
            while left-initl < goal:
                print left-initl
                time.sleep(0.1)
                (left,_) = self.driving.get_driven_distance()
        else:
            while right-initr < goal:
                print right-initr
                time.sleep(0.1)
                (_,right) = self.driving.get_driven_distance()
        self.driving.stop_driving()

    def corrigate(self,factor):
        print "corrigate with factor: %s" %factor
        if math.fabs(factor) > 50:
            self.driving.drive_straight()
        elif math.fabs(factor) < 20:
            self.driving.stop_driving()
        else:
            self.driving.drive_arc(factor)

    def get_picture(self):
        return self.camera.get_frame()

    def halt(self):
        self.driving.stop_driving()
        self.value_updater.stop()