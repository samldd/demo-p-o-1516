__author__ = 'sam_l'
from robo_car import RoboCar
from value_updater import ValueUpdater
import time


roboCar = RoboCar()

#value_updater = ValueUpdater()
#value_updater.start()

roboCar.drive_blind(100)

print "end script"

# time.sleep(100000)

value_updater.stop()