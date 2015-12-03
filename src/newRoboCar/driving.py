import math
import time
import BrickPi
import motor
import drivingSession

class Driving(object):

    def __init__(self):
        self.left_motor = motor.Motor(BrickPi.PORT_C)
        self.right_motor = motor.Motor(BrickPi.PORT_B)

        self.sampeling_time = 0.05
        self.default_speed = 210

        self.perimeter_wheel = 0.055 * math.pi
        self.d_wheel = 0.16

        self.session = None

    def drive_straight(self,d):
        ticks = self.__get_number_ticks(d)
        self.__add_driving_session(ticks, ticks)
        self.drive_ticks(1)
        self.__end_driving_session()

    def drive_arc(self, degrees, radius):
        "Drive a circle arc with radius radius and arc angle degrees. Give a positive radius for a circle to the left "
        if radius > 0:
            left_ticks = self.__get_number_ticks(math.pi*(radius + self.d_wheel/2))
            right_ticks = self.__get_number_ticks(math.pi*(radius - self.d_wheel/2))
            factor = float(left_ticks)/right_ticks
            print left_ticks
            print right_ticks
            print factor
        elif radius < 0:
            left_ticks = self.__get_number_ticks(radius - self.d_wheel/2)
            right_ticks = self.__get_number_ticks(radius + self.d_wheel/2)
            factor = right_ticks/left_ticks
        else:
            if degrees > 0:
                left_ticks = self.__get_number_ticks(-self.d_wheel/2)
                right_ticks = self.__get_number_ticks(self.d_wheel/2)
                factor = left_ticks/right_ticks
            elif degrees < 0:
                left_ticks = self.__get_number_ticks( self.d_wheel/2)
                right_ticks = self.__get_number_ticks(-self.d_wheel/2)
                factor = right_ticks/left_ticks
            else:
                return
        self.__add_driving_session(left_ticks,right_ticks)
        self.drive_ticks(factor)
        self.__end_driving_session()

    def drive_ticks(self,correction):
        initial_right = 180
        initial_left = 180*correction
        self.right_motor.set_velocity(initial_right)
        self.left_motor.set_velocity(initial_left)
        while not self.__goal_reached():

            # Initialize PID values and constants
            integral = 0
            previous = 0

            kp = 1          # proportionele factor
            kd = 0.1        # afgeleide     factor
            ki = 0          # integraal     factor

            # Calculate PID values
            left = self.left_motor.get_encoder_value()
            right =  self.right_motor.get_encoder_value()
            error = left*correction - right
            integral = integral + error * 0.05
            derivative = (error - previous) / 0.05

            output = kp * error + ki * integral + kd * derivative
            previous = error
            self.left_motor.set_velocity(initial_left-output)
            time.sleep(.05)

    def __goal_reached(self):
        return self.session.goal_reached(self.left_motor.get_encoder_value(),self.right_motor.get_encoder_value())

    def __get_number_ticks(self, distance):
        "De waarde TICKSP360 moet gecalibreert worden aan het aantal ticks dat de motoren doen per 360 graden"
        TICKSP360 = 800
        return int(distance/self.perimeter_wheel*TICKSP360)

    def __start_motors(self):
        self.left_motor.enable_motor()
        self.right_motor.enable_motor()

    def __stop_motors(self):
        self.left_motor.disable_motor()
        self.right_motor.disable_motor()

    def __add_driving_session(self,left,right):
        self.__start_motors()
        left = self.left_motor.get_encoder_value() + left
        right = self.right_motor.get_encoder_value() + right
        self.session = drivingSession.drivingSession(left,right)

    def __end_driving_session(self):
        self.session = None
        self.__stop_motors()

    def is_busy(self):
        return not(self.session == None)