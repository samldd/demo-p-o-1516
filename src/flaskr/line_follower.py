import math
import time

import image_rec


class Follower(object):

    def __init__(self,rob):
        self.rob = rob

    def run(self):
        while True:
            time.sleep(0.1)
            im = self.rob.get_picture()
            result = image_rec.detect_lines(im)
            if not(result[0] == None):
                mid, rico = result[0]
                center = -50/math.atan((320-mid)/130)
                angle = 50-(math.fabs(rico)-10)*20/50
                angle = angle * rico/math.fabs(rico)
                print "rico = %s" %rico
                print "correctionfactor = %s" %angle
                #self.rob.corrigate(-angle)
            else:
                self.rob.corrigate(0)

