import driving
import value_updater


class RoboCar(object):
    def __init__(self):
        self.driving = driving.Driving()
        self.value_updater = value_updater.ValueUpdater()
    
    def drive_straight(self, distance):
        self.value_updater.start()
        self.driving.drive_straight(distance)
        self.value_updater.stop()

    def turn(self,degrees):
        self.value_updater.start()
        self.driving.turn(degrees)
        self.value_updater.stop()

    def drive_arc(self,degrees, radius):
        self.value_updater.start()
        self.driving.drive_arc(degrees,radius)
        self.value_updater.stop()

    def drive_square(self, size):
        for _ in range(0,3):
            self.drive_straight(size)
            self.turn(90)
