from __future__ import division
import threading
import numpy as np
from collections import deque
import math
import time
from logger import Logger


class Follower(threading.Thread):

    def __init__(self,driving,rob):
        threading.Thread.__init__(self)
        self.driving = driving
        self.rob = rob

        self.running = True
        self.active = False

        self.logger = Logger("LineFollowing")

        self.instructions = ["straight"]
        self.latest_action = ""
        self.last_update = 0

        self.cameraInfo = [None,None,None,None]
        self.history = deque([],maxlen=5)
        self.turn = [False,False]

    def add_history(self,element):
        self.history.appendleft(element)

    def add_instruction(self,instruction):
        if not(instruction in ["left","straight","right"]):
            raise Exception
        self.logger.add_log("instruction added: " + instruction)
        self.instruction.append(instruction)

    def set_camera_info(self,cameraInfo):
        self.cameraInfo = np.array(eval(cameraInfo))
        self.last_update = time.time()
        return self.latest_action

    def run(self):
        while self.running:
            if self.active:
                if time.time() - self.last_update < 0.25:
                    self.check_crossing()
                    time.sleep(0.10)
                else:
                    print "no camera image in time"
                    self.driving.stop_driving()
                    time.sleep(0.20)
            else:
                time.sleep(1)

    def follow_road(self):
        [_,down,_,up] = self.cameraInfo
        if up and down:
            (_,angleUp) = up
            (_,angleDown) = down
            if abs(angleUp) > 20 and abs(angleDown) < 20:
                fact = -angleUp/10
                corr = self.calculate_correction((None,fact,None))
                self.driving.drive_correction(corr)
                self.write_debug_info("correction = %s" %corr)
                return
            if abs(angleDown) > 15:
                fact = -angleUp/8
                corr = self.calculate_correction((None,fact,None))
                self.driving.drive_correction(corr)
                self.write_debug_info("correction = %s" %corr)
                return
        if down:
            (mid,angle) = down
            mid = 320-mid
            if abs(mid) > 80:
                fact = mid/40
                corr = self.calculate_correction((None,fact,None))
                self.correction(corr)
            else:
                fact = -angle/2.5
                corr = self.calculate_correction((None,fact,None))
                self.correction(corr)
        elif up:
            (mid,angle) = up
            mid = 320 - mid
            if abs(mid) > 70:
                fact = mid/40
                corr = self.calculate_correction((None,fact,None))
                self.correction(corr)
            else:
                fact = angle/5
                corr = self.calculate_correction((None,fact,None))
                self.correction(corr)
        else:
            self.search_line()

    def calculate_correction(self,present):
        self.add_history(present)
        hist = list(self.history)
        count = 1
        result = 0
        wtot = 0
        for e in hist:
            try:
                (_,mid,_) = e
                w = 1/(count**2+1)
                wtot += w
                result += w*mid
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

    def search_line(self):
        time.sleep(0.10)
        self.driving.stop_driving()
        print "searching line ... latest action was: " + self.latest_action
        if not self.latest_action == "stop":
            if "search:" in self.latest_action:
                num = self.latest_action.split(":")[1]
                num = int(eval(num))
                num = (abs(num) + 15)*-math.copysign(1,num)
                if abs(num) >= 61:
                    self.rob.turn(num/2)
                    self.write_debug_info("stop")
                    self.history.clear()
                    return
                else:
                    self.rob.turn(num)
                    self.write_debug_info("search:%s" %num)
                    return
            while len(self.history):
                (_,f,_) = self.history.popleft()
                if f:
                    if f > 0:
                        self.rob.turn(15)
                        self.write_debug_info("search:15")
                    else:
                        self.rob.turn(-15)
                        self.write_debug_info("search:-15")
                    break
        self.history.clear()

    def write_debug_info(self,text):
        self.latest_action = text
        self.logger.add_log("latest action = " + text)
        with open('debug.txt' ,"a") as tf:
                    tf.write(text + "\n")

    def resume(self):
        self.active = True

    def pauze(self):
        self.active = False

    def stop(self):
        self.running = False

    def check_crossing(self):
        [left,down,right,up] = self.cameraInfo
        if down and list(self.cameraInfo).count(None) < 2:
            print "possible crossing !!"
            if len(self.instructions) == 0:
                print "no instruction available.. pls give an instruction."
                self.driving.stop_driving()
                time.sleep(1)
                return

            self.driving.stop_driving()
            if up and left and right:
                print "kruispunt"
                (midL, angleL) = left
                (midR, angleR) = right
                if midL > 300 and midR > 300:
                    self.driving.drive_straight()
                    time.sleep(0.10)
                    self.driving.stop_driving()
                    time.sleep(0.10)
                    [left,_,right,up] = self.cameraInfo
                    if list(self.cameraInfo).count(None)<3:
                        time.sleep(0.05)
                        self.check_crossing()
                    else:
                        if self.instructions[0] == "left" and left:
                            (mid,angle) = left
                            self.rob.drive_straight(mid/50/100)
                            self.rob.turn(90)
                            self.instructions = self.instructions[1:]
                            return True
                        elif self.instructions[0] == "right" and right:
                            (mid,angle) = right
                            self.rob.drive_straight(mid/50/100)
                            self.rob.turn(-90)
                            self.instructions = self.instructions[1:]
                            return True
                        elif self.instructions[0] == "straight" and left and right:
                            self.instructions = self.instructions[1:]
                            print "ERROR no case.."
            elif up and left:
                print "links is een afslag"
                (midL,angleL) = left
                if midL > 300:
                    self.driving.drive_straight()
                    time.sleep(0.10)
                    self.driving.stop_driving()
                    time.sleep(0.10)
                    [left,_,right,up] = self.cameraInfo
                    if list(self.cameraInfo).count(None)<3:
                        time.sleep(0.05)
                        self.check_crossing()
                    else:
                        if self.instructions[0] == "left" and left:
                            (mid,angle) = left
                            self.rob.drive_straight(mid/50/100)
                            self.rob.turn(90)
                            self.instructions = self.instructions[1:]
                        elif self.instructions[0] == "right" and left:
                            self.drive_over_crossing()
                        elif self.instructions[0] == "straight" and left:
                            self.drive_over_crossing()
            elif up and right:
                print "recht is een afslag"
                (mid,angle) = right
                if mid > 300:
                    self.driving.drive_straight()
                    time.sleep(0.10)
                    self.driving.stop_driving()
                    time.sleep(0.10)
                    [left,_,right,up] = self.cameraInfo
                    if self.instructions[0] == "left" and right:
                        self.drive_over_crossing()
                    elif self.instructions[0] == "right" and right:
                        (mid,angle) = left
                        self.rob.drive_straight(mid/50/100)
                        self.rob.turn(90)
                        self.instructions = self.instructions[1:]
                    elif self.instructions[0] == "straight" and right:
                        self.drive_over_crossing()
            elif left and right:
                print "probably T crossing.. checking.."
                (midL,angleL) = left
                (midR,angleR) = right
                if midL > 300 and midR > 300:
                    self.driving.drive_straight()
                    time.sleep(0.10)
                    self.driving.stop_driving()
                    time.sleep(0.10)
                    [left,_,right,up] = self.cameraInfo
                    if not up:
                        if self.instructions[0] == "left" and left:
                            (mid,angle) = left
                            self.rob.drive_straight(mid/50/100)
                            self.rob.turn(90)
                            self.instructions = self.instructions[1:]
                            return True
                        elif self.instructions[0] == "right" and right:
                            (mid,angle) = right
                            self.rob.drive_straight(mid/50/100)
                            self.rob.turn(-90)
                            self.instructions = self.instructions[1:]
                            return True
                        elif self.instructions[0] == "straight" and left and right:
                            self.instructions = self.instructions[1:]
                            print "ERROR no case.."
                    elif self.instructions[0] == "straight":
                            print "toch geen T splisting, volg de weg"
                            self.instructions = self.instructions[1:]
                            self.follow_road()
                else:
                    self.driving.drive_back()
                    time.sleep(0.05)
                    self.check_crossing()
        else:
            print "no crossing, follow the road."
            self.follow_road()

    def drive_over_crossing(self):
        while True:
            [left,down,right,up] = self.cameraInfo
            if left == None and right == None:
                break;
            self.follow_road()
            time.sleep(0.10)



