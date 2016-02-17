import image_rec
import time
import numpy as np
import PIL as pillow


class Follower(object):

    def __init__(self,rob):
        self.rob = rob

    def run(self):
        while True:
            im = self.rob.get_picture()
            result = image_rec.detect_lines(im)
            if result[0]:
                print result[0]
            time.sleep(1)
