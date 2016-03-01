import cv2
import numpy as np
import urllib, cStringIO
from PIL import Image
import time
import threading
import photo_recognition
import socket
import urllib2
url = "http://192.168.42.1:5000/video_frame.jpg"

class FileFetcher(object):
    thread = None       # background thread that reads frames from FileFetcher
    frame = None        # current frame is stored here by background thread

    def initialize(self):
        if FileFetcher.thread is None:
            # start background frame thread
            FileFetcher.thread = threading.Thread(target=self._thread)
            FileFetcher.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        while True:
            try:
                req = urllib2.urlopen(url, None, timeout=2).read()
                file = cStringIO.StringIO(req)

                img = Image.open(file)
                opencv_image = np.array(img)
                opencv_image = opencv_image[:,:,::-1]
                cls.frame, x = photo_recognition.detect_lines(opencv_image)
                #cls.frame = opencv_image
                print str(x)
                urllib.urlopen("http://192.168.42.1:5000/line_info?x="+str(x))
            except (IOError, urllib2.URLError, socket.timeout) as e:
                print "Error in communication: Trying again in 5 seconds"
                time.sleep(5)


