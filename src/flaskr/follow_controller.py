import math
import time
import numpy as np
import threading


class Follower(threading.Thread):

    def __init__(self,driving,rob):
        threading.Thread.__init__(self)
        self.driving = driving
        self.rob = rob
        self.running = True
        self.pauzed = False
        self.instructions = ["straight"]

        self.last_update = 0
        self.cameraInfo1 = [None,None,None,None]
        self.cameraInfo2 = [None,None,None,None]

    def add_instruction(self,instruction):
        if not(instruction in ["left","straight","right"]):
            raise Exception
        self.instruction.append(instruction)

    def set_camera_info(self,cameraInfo):
        with open('debug.txt' ,"a") as tf:
            tf.write(str(self.last_update-time.time()) + " " + str(cameraInfo) + "\n")
        self.cameraInfo2 = self.cameraInfo1
        self.cameraInfo1 = np.array(eval(cameraInfo))
        self.last_update = time.time()

    def run(self):
        while self.running:
            if len(self.instructions) == 0:
                self.driving.stop_driving()
                time.sleep(0.30)
            if time.time() - self.last_update < 0.25:
                self.control()
                time.sleep(0.05)
            else:
                self.driving.stop_driving()
                time.sleep(0.20)

    def control(self):
        [left,_,right,up] = self.cameraInfo1
        if self.instructions[0] == "straight":
            self.follow_road()
        if self.instructions[0] == "left":
            if self.check_side(True) and up:
                self.turn(True,left)
            else:
                self.follow_road()
        if self.instructions[0] == "right":
            if self.check_side(False) and up:
                self.turn(False,right)
            else:
                self.follow_road()

    def follow_road(self):
        [left,down,right,up] = self.cameraInfo1
        if down and up:
            self.straight(down)
        elif up:
            self.straight((0,(320-up[0])/5))
        elif self.check_side(True) and not self.check_up():
            self.turn(True,left)
        elif self.check_side(False) and not self.check_up():
            self.turn(False,right)
        else:
            self.driving.stop_driving()

    def check_side(self,left):
        if left:
            return self.cameraInfo2[0] and self.cameraInfo1[0]
        else:
            return self.cameraInfo2[2] and self.cameraInfo1[2]

    def check_up(self):
        return self.cameraInfo2[3] or self.cameraInfo1[3]

    def turn(self,left,(mid,angle)):
        self.pauzed = True
        self.rob.drive_straight(mid/10000)
        if left:
            self.rob.turn(-angle)
        else:
            self.rob.turn(angle)
        self.pauzed = False

    def straight(self,down):
        (mid,angle) = down
        if -5 < angle < 5:
            self.driving.drive_straight()
            with open('debug.txt' ,"a") as tf:
                tf.write("straight" + "\n")
            return
        rad = 59-0.3*abs(angle)
        rad = rad if angle > 0 else -rad
        with open('debug.txt' ,"a") as tf:
                tf.write("drive arc %s radius" %rad + "\n")
        self.driving.drive_arc(rad)

    def stop(self):
        self.running = False


