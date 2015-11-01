__author__ = 'sam_l'
from robo_car import RoboCar
from value_updater import ValueUpdater

roboCar = RoboCar()

print "test script"

v = ValueUpdater()
v.start()
print "value updater gestart"

roboCar.drive_blind(100)

v.stop()