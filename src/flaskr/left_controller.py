from __future__ import division
from logger import Logger
import time
__author__ = 'sam_l'


class Left(object):
    def __init__(self,driving,rob,straight):
        self.logger = Logger("straightController")
        self.driving = driving
        self.rob = rob
        self.straightController = straight
        self.cameraInfo = [None,None,None,None]

    def set_camera_info(self,cameraInfo):
        self.cameraInfo = cameraInfo

    def check_crossing(self):
        [left,_,_,_] = self.cameraInfo
        if left != None:
            print "possible left turn.. double check"
            self.driving.drive_straight(60)
            time.sleep(0.05)
            self.driving.stop_driving()
            time.sleep(0.13)
            [left,_,right,up] = self.cameraInfo
            if left != None and up != None:
                print "turn left"
                (mid,angle) = left
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(90)
                return True
            elif right != None and left != None:
                print "T splitsing"
                (mid,angle) = right
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(90)
                return True
            elif left != None:
                print "hoek bocht"
                (mid,angle) = left
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(90)
                return False
            else:
                print "no crossing"
                self.straightController.follow_road()
                return False
        else:
            self.straightController.follow_road()
            return False





