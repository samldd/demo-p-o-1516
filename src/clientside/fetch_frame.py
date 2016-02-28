import cv2
import numpy as np
import urllib, cStringIO
from PIL import Image
import time
import threading
import photo_recognition
url = "http://192.168.42.1:5000/video_frame.jpg"

class FileFetcher(object):
    thread = None       # background thread that reads frames from FileFetcher
    frame = None        # current frame is stored here by background thread
    last_access = 0     # time of last client access to the FileFetcher

    def initialize(self):
        if FileFetcher.thread is None:
            # start background frame thread
            FileFetcher.thread = threading.Thread(target=self._thread)
            FileFetcher.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        FileFetcher.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        while True:
            req = urllib.urlopen(url).read()
            file = cStringIO.StringIO(req)

            img = Image.open(file)
            opencv_image = np.array(img)
            opencv_image = opencv_image[:,:,::-1]
            cls.frame, x = photo_recognition.detect_lines(opencv_image)
            #cls.frame = opencv_image
            print str(x)
            urllib.urlopen("http://192.168.42.1:5000/line_info?x="+str(x))

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds stop the thread
            # if time.time() - cls.last_access > 10:
            #     break
        cls.thread = None


