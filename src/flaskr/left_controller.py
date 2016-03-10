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
        if left:
            print "possible left turn.. double check"
            self.straightController.follow_road()
            time.sleep(0.10)
            self.driving.stop_driving()
            time.sleep(0.10)
            [left,_,_,up] = self.cameraInfo
            if left and up:
                print "turn left"
                (mid,angle) = left
                self.rob.drive_straight(mid/50/100)
                self.rob.turn(90)
                return True
            elif left:
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





