from __future__ import division
import time
from logger import Logger
from collections import deque
import math
__author__ = 'sam_l'


class Straight(object):

    def __init__(self,driving,rob):
        self.logger = Logger("straightController")
        self.latest_action = ""
        self.driving = driving
        self.rob = rob
        self.history = deque([],maxlen=5)
        self.cameraInfo = [None,None,None,None]

    def set_camera_info(self,cameraInfo):
        self.cameraInfo = cameraInfo

    def add_history(self,element):
        self.history.appendleft(element)

    def follow_road(self):
        [_,down,_,up] = self.cameraInfo
        if up:
            (mid,angle) = up
            fact = 0
            if angle > 30:
                fact = angle/35
                print "angle: %s" %fact
            else:
                mid = 320 - mid
                fact = mid/70
                print "mid: %s" %fact
            corr = self.calculate_correction(fact)
            self.correction(corr)
        elif down:
            (mid,angle) = down
            mid = 320 - mid
            fact = mid/90
            print "down: %s" %fact
            corr = self.calculate_correction(fact)
            self.correction(corr)
        else:
            self.search_line()

    def search_line(self):
        self.driving.stop_driving()
        print "searching line ... latest action was: " + self.latest_action
        if not self.latest_action == "stop":
            if "search:" in self.latest_action:
                num = self.latest_action.split(":")[1]
                num = int(eval(num))
                num = (abs(num) + 15)*-math.copysign(1,num)
                if abs(num) >= 61:
                    self.rotate(num/2)
                    self.write_debug_info("stop")
                    self.history.clear()
                    return
                else:
                    self.rotate(num)
                    self.write_debug_info("search:%s" %num)
                    return
            while len(self.history):
                f = self.history.popleft()
                if f:
                    if f > 0:
                        self.rotate(15)
                        self.write_debug_info("search:15")
                    else:
                        self.rotate(-15)
                        self.write_debug_info("search:-15")
                    break
        time.sleep(0.15)
        self.history.clear()

    def calculate_correction(self,present):
        self.add_history(present)
        hist = list(self.history)
        count = 1
        result = 0
        wtot = 0
        for e in hist:
            try:
                w = 1/(count**3+1)
                wtot += w
                result += w*e
            except:
                pass
            count += 1
        result /= wtot
        return result

    def correction(self,correction):
        if abs(correction) > 3:
            correction = math.copysign(3,correction)
        self.driving.drive_correction(correction)
        self.logger.add_log("correction = %s" %correction)
        self.write_debug_info("correction = %s" %correction)

    def rotate(self,degrees):
        speed = 65
        wheel_degrees = self.driving.turn(degrees,speed)
        pleft,pright = self.driving.get_driven_distance()
        while True:
            time.sleep(0.07)
            [_,down,_,up] = self.cameraInfo
            if up or down:
                self.driving.stop_driving()
                break
            left,right = self.driving.get_driven_distance()
            if left > abs(wheel_degrees) or right > abs(wheel_degrees):
                self.driving.stop_driving()
                break
            if abs(left-pleft) < 5 or abs(right-pright) < 5:
                speed += 5
                self.driving.turn(degrees,speed)
            pleft = left
            pright = right

    def check_crossing(self):
        [left,_,right,_] = self.cameraInfo
        if left or right:
            print "possible crossing.. double check"
            self.driving.drive_straight(60)
            time.sleep(0.05)
            self.driving.stop_driving()
            time.sleep(0.13)
            [left,_,right,up] = self.cameraInfo
            if left and up == None:
                print "hoek bocht links"
                (mid,angle) = left
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(90)
                return False
            elif right and up == None:
                print "hoek bocht rechts"
                (mid,angle) = right
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(-90)
                return False
            elif up and (left or right):
                print "drive over crossing"
                self.drive_over_crossing()
                return True
            else:
                print "no crossing"
                self.follow_road()
                return False
        else:
            self.follow_road()
            return False

    def drive_over_crossing(self):
        prev = ["","","",""]
        while True:
            [pleft,_,pright,_] = prev
            [left,_,right,_] = self.cameraInfo
            if left == None and right == None and pleft == None and pright == None:
                break
            self.follow_road()
            prev = self.cameraInfo
            time.sleep(0.10)

    def write_debug_info(self,text):
        self.latest_action = text
        self.logger.add_log("latest action = " + text)
        with open('debug.txt' ,"a") as tf:
                    tf.write(text + "\n")