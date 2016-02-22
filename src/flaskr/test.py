__author__ = 'sam_l'
from robo_car import RoboCar
import line_follower

rob = RoboCar()

# # Test 1: turn smooth left
# print "turn smooth left"
#rob.drive_arc(360,-0.45)
# # Test 2: turn smooth right
# print "turn smooth right"
# rob.drive_arc(-90,1)


# Test 3: turn 90 degree left
#rob.turn(180)
#time.sleep(1)
# Test 4: turn 90 degree right
#rob.turn(-90)
#time.sleep(1)

# Test 5: drive straight
#rob.drive_straight(1)
# Test 6: drive back
#rob.drive_back(-1)

linef = line_follower.Follower(rob)
linef.run()