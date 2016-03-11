from __future__ import division
import time
from logger import Logger
__author__ = 'sam_l'


class Right(object):

    def __init__(self,driving,rob,straight):
        self.logger = Logger("straightController")
        self.driving = driving
        self.rob = rob
        self.straightController = straight
        self.cameraInfo = [None,None,None,None]

    def set_camera_info(self,cameraInfo):
        self.cameraInfo = cameraInfo

    def check_crossing(self):
        [_,_,right,_] = self.cameraInfo
        if right:
            print "possible left turn.. double check"
            self.driving.drive_straight(60)
            time.sleep(0.05)
            self.driving.stop_driving()
            time.sleep(0.13)
            [left,_,right,up] = self.cameraInfo
            if right and up:
                print "turn right"
                (mid,angle) = right
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(-90)
                return True
            elif right and left:
                print "T splitsing"
                (mid,angle) = right
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(-90)
                return True
            elif right:
                print "hoek bocht"
                (mid,angle) = right
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(-90)
                return False
            else:
                print "no crossing"
                self.straightController.follow_road()
                return False
        else:
            self.straightController.follow_road()
            return False