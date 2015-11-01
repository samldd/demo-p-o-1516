import BrickPi
import threading
import time

class ValueUpdater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.should_stop = False

    def run(self):
        self.should_stop = False
        while not self.should_stop:
            time.sleep(0.05)
            BrickPi.BrickPiUpdateValues()

    def stop(self):
        self.should_stop = True
