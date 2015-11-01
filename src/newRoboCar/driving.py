import math
import time
import BrickPi
import motor

class Driving(object):

    def __init__(self):
        self.left_motor = motor.Motor(BrickPi.PORT_C)
        self.right_motor = motor.Motor(BrickPi.PORT_B)

        self.sampeling_time = 0.1
        self.default_speed = 210
        self.perimeter = 0.056 * math.pi
        self.WHEEL_DISTANCE = 0.1521

    def turn(self, degree):
        wheel_degrees = 2 * self.WHEEL_DISTANCE * math.pi * degree / self.perimeter
        speed = 180 if wheel_degrees >= 0 else -180
        self.__start_motors()
        self.left_motor.set_velocity(speed)
        self.right_motor.set_velocity(-speed)

        while not self.__goal_reached():
            time.sleep(self.sampeling_time)
        self.__stop_motors()

    def drive_straight(self, distance):
        speed = self.default_speed

        # Start motors
        self.__start_motors()
        self.right_motor.set_velocity(speed)
        self.left_motor.set_velocity(speed)

        # Initialize PID values and constants
        integral = 0
        previous = 0

        kp = 1          # proportionele factor
        kd = 0.1        # afgeleide     factor
        ki = 0          # integraal     factor

        while not (self.__goal_reached(distance)):
            # Calculate PID values
            error = self.left_motor.get_encoder_value() - self.right_motor.get_encoder_value()
            integral = integral + error * self.sampling_time
            derivative = (error - previous) / self.sampling_time
            output = kp * error + ki * integral + kd * derivative
            previous = error

            self.left_motor.set_velocity(speed-output)
            time.sleep(self.sampling_time)

        self.__stop_motors()

    def drive_arc(self, degrees, radius):
        pass

    def __get_number_ticks(self, distance):
        pass

    def __goal_reached(self,distance):
        ticks = self.get_number_ticks(distance)
        abs(self.left_motor.get_encoder_value()) > abs(ticks) or abs(self.right_motor.get_encoder_value()) > abs(ticks)
        return False

    def __start_motors(self):
        self.left_motor.enable_motor()
        self.right_motor.enable_motor()

    def __stop_motors(self):
        self.left_motor.disable_motor()
        self.right_motor.disable_motor()