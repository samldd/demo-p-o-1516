import driving
import value_updater


class Manual(object):
    def __init__(self):
        self.Yspeed = 0
        self.Xspeed = 0
        self.driving = driving.Driving
        self.value_updater = value_updater.ValueUpdater

    def start(self):
        self.driving = driving.Driving
        self.value_updater = value_updater.ValueUpdater
        self.value_updater.start()
        self.driving.start()

    def stop(self):
        self.value_updater.stop()
        self.driving.stop_driving()

    def set_y_speed(self,speed):
        if speed > 210:
            speed = 210
        if speed < -210:
            speed = -210
        self.Yspeed = speed
        self.update()

    def get_y_speed(self):
        return self.Yspeed

    def set_x_speed(self,speed):
        if speed > 210:
            speed = 210
        if speed < -210:
            speed = -210
        self.Xspeed = speed
        self.update()

    def get_x_speed(self):
        return self.Xspeed

    def incrementY(self):
        speed = self.get_y_speed()+5
        self.set_y_speed(speed)

    def decrementY(self):
        speed = self.get_y_speed()-5
        self.set_y_speed(speed)

    def incrementX(self):
        speed = self.get_x_speed()+5
        self.set_x_speed(speed)

    def decrementX(self):
        speed = self.get_x_speed()-5
        self.set_x_speed(speed)

    def update(self):
        if self.Xspeed == 0 and self.Yspeed == 0:
            return
        if self.Xspeed < 0:
            self.set_y_speed(0)
            self.driving.drive_back()
        if self.Xspeed == 0:
            self.driving.turn(self.Yspeed/50)
        if self.get_x_speed()>0 and self.get_y_speed() == 0:
            self.driving.drive_straight(self.Xspeed)
        else:
            self.driving.drive_arc(self.get_x_speed()/self.get_y_speed())