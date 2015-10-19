from BrickPi import BrickPiUpdateValues #@UnresolvedImport
import threading

class ValueUpdater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.should_stop = False
        print "value updater gestart"

    def run(self):
        while not self.should_stop:
            BrickPiUpdateValues()

    def stop(self):
        self.should_stop = True
        print "value updater gestopt"
