import threading
import numpy as np

import time
from logger import Logger

import straight_controller
import left_controller
import right_controller


class Follower(threading.Thread):

    def __init__(self,driving,rob):
        threading.Thread.__init__(self)

        self.running = True
        self.active = False
        self.logger = Logger("LineFollowing")

        self.instructions = []
        self.latest_action = ""
        self.last_update = 0
        self.cameraInfo = [None,None,None,None]

        self.driving = driving

        self.straightController = straight_controller.Straight(driving,rob)
        self.leftController = left_controller.Left(driving,rob,self.straightController)
        self.rightController = right_controller.Right(driving,rob,self.straightController)

    def get_instructions(self):
        return self.instructions

    def add_instruction(self,instruction):
        if not(instruction in ["left","forward","right"]):
            raise Exception
        self.logger.add_log("instruction added: " + instruction)
        self.instructions.append(instruction)

    def remove_instruction(self):
        self.logger.add_log("instruction removed: " + self.instructions[-1])
        self.instructions = self.instructions[:-1]

    def set_camera_info(self,cameraInfo):
        self.cameraInfo = np.array(eval(cameraInfo))
        self.straightController.set_camera_info(self.cameraInfo)
        self.leftController.set_camera_info(self.cameraInfo)
        self.rightController.set_camera_info(self.cameraInfo)
        self.last_update = time.time()
        return self.latest_action

    def run(self):
        while self.running:
            if self.active:
                if len(self.instructions) == 0:
                    self.logger.add_log("awaiting instructions...")
                    self.driving.stop_driving()
                    time.sleep(1)
                elif time.time() - self.last_update < 0.25:
                    self.control()
                    time.sleep(0.10)
                else:
                    print "no camera image in time"
                    self.driving.stop_driving()
                    time.sleep(0.10)
            else:
                time.sleep(1)

    def control(self):
        if self.instructions[0] == "right":
            if self.rightController.check_crossing():
                self.instructions = self.instructions[:-1]

        elif self.instructions[0] == "left":
            if self.leftController.check_crossing():
                self.instructions = self.instructions[:-1]
        else:
            if self.straightController.check_crossing():
                self.instructions = self.instructions[:-1]

    def resume(self):
        self.active = True

    def pauze(self):
        self.active = False

    def stop(self):
        self.running = False

    def write_debug_info(self,text):
        self.latest_action = text
        self.logger.add_log("latest action = " + text)
        with open('debug.txt' ,"a") as tf:
                    tf.write(text + "\n")





