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
        self.__add_driving_session(ticks,ticks)
        self.drive_ticks_velocity(1)
        self.__end_driving_session()

    def drive_arc(self, degrees, radius):
        "Drive a circle arc with radius radius and arc angle degrees. Give a positive radius for a circle to the left "
        if degrees < 0:
            raise NameError("degrees has to be a positive integer!")
        if radius > 0:
            left_ticks = self.__get_number_ticks(radius + self.d_wheel/2)
            right_ticks = self.__get_number_ticks(radius - self.d_wheel/2)
        else:
            left_ticks = self.__get_number_ticks(radius - self.d_wheel/2)
            right_ticks = self.__get_number_ticks(radius + self.d_wheel/2)
        factor = left_ticks/right_ticks
        self.__add_driving_session(left_ticks,right_ticks)
        self.drive_ticks(factor)
        self.__end_driving_session()

    def drive_ticks(self,correction):
        self.right_motor.set_velocity(200)
        self.left_motor.set_velocity(200*correction)
        while not self.__goal_reached():
            # Initialize PID values and constants
            integral = 0
            previous = 0

            kp = 1          # proportionele factor
            kd = 0.1        # afgeleide     factor
            ki = 0          # integraal     factor

            # Calculate PID values
            error = self.left_motor.get_encoder_value() - self.right_motor.get_encoder_value()
            integral = integral + error * 0.05
            derivative = (error - previous) / 0.05

            output = kp * error + ki * integral + kd * derivative

            previous = error

            self.left_motor.set_velocity(200-output)
            time.sleep(.05)

    def drive_ticks_velocity(self,correction):
        self.right_motor.set_velocity(250)
        self.left_motor.set_velocity(250*correction)
        while not self.__goal_reached():
            debL = self.left_motor.get_encoder_value()
            debR = self.right_motor.get_encoder_value()

            # Initialize PID values and constants
            integral = 0
            previous = 0

            kp = 0.25          # proportionele factor
            kd = 0.02          # afgeleide     factor
            ki = 10             # integraal     factor

            # Calculate PID values
            left = self.left_motor.get_encoder_velocity()
            right = self.right_motor.get_encoder_velocity()

            error = (left - right)/self.sampeling_time*0.25

            integral = (debL - debR)*0.25
            derivative = (error - previous) / self.sampeling_time


            output = kp * error + ki * integral + kd * derivative
            output = math.copysign(min(output,15),output) if output > 0 else math.copysign(max(output,-15),output)
            print debL,left,debR,right, output
            previous = error
            self.left_motor.set_velocity(self.left_motor.get_velocity()- output)
            time.sleep(.05)

    def __goal_reached(self):
        return self.session.goal_reached(self.left_motor.get_encoder_value(),self.right_motor.get_encoder_value())

    def __get_number_ticks(self, distance):
        "De waarde TICKSP360 moet gecalibreert worden aan het aantal ticks dat de motoren doen per 360 graden"
        TICKSP360 = 725
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