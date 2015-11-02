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
        self.perimeter = 0.055 * math.pi
        self.WHEEL_DISTANCE = 0.16

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

    def drive_straight2(self,d):
        # Start motors
        self.__start_motors()
        self.right_motor.set_velocity(250)
        self.left_motor.set_velocity(250)
        ticks = self.__get_number_ticks(d)
        self.drive_ticks(ticks)
        self.__stop_motors()


    def drive_arc(self, degrees, radius):
        speed_diff = 1 + 0.16/radius

        # Start motors
        self.__start_motors()
        self.right_motor.set_velocity(150*1.32)
        self.left_motor.set_velocity(150)
        ticks_left = self.__get_number_ticks(3.14)
        ticks_right = self.__get_number_ticks(3.14*1.16)

        init_value_left = self.left_motor.get_encoder_value()
        init_value_right = self.right_motor.get_encoder_value()
        final_value_l = init_value_left + ticks_left
        final_value_r = init_value_right + ticks_right

        while init_value_left < final_value_l or init_value_right < final_value_r:
            init_value_left = self.left_motor.get_encoder_value()
            init_value_right = self.right_motor.get_encoder_value()
            print "left: %s , right: %s" %(init_value_left,init_value_right)
            # Initialize PID values and constants
            integral = 0
            previous = 0

            kp = 1          # proportionele factor
            kd = 0.1        # afgeleide     factor
            ki = 0          # integraal     factor
            # Calculate PID values
            error = self.left_motor.get_encoder_value() - self.right_motor.get_encoder_value()*3.14*1.32
            integral = integral + error * 0.05
            derivative = (error - previous) / 0.05
            output = kp * error + ki * integral + kd * derivative
            previous = error

            self.left_motor.set_velocity(150-output)
            time.sleep(.05)
        print "end"
        print "last  - left: %s , right: %s" %(init_value_left,init_value_right)
        print "final - left: %s , right: %s" %(final_value_l,final_value_r)


    def drive_ticks(self,nb_ticks):
        init_value_left = self.left_motor.get_encoder_value()
        init_value_right = self.right_motor.get_encoder_value()
        final_value_l = init_value_left + nb_ticks
        final_value_r = init_value_right + nb_ticks

        while init_value_left < final_value_l or init_value_right < final_value_r:
            init_value_left = self.left_motor.get_encoder_value()
            init_value_right = self.right_motor.get_encoder_value()
            print "left: %s , right: %s" %(init_value_left,init_value_right)
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

            self.left_motor.set_velocity(250-output)
            time.sleep(.05)
        print "end"
        print "last  - left: %s , right: %s" %(init_value_left,init_value_right)
        print "final - left: %s , right: %s" %(final_value_l,final_value_r)

    def __get_number_ticks(self, distance):
        return int(distance/self.perimeter*725)

    def __start_motors(self):
        self.left_motor.enable_motor()
        self.right_motor.enable_motor()

    def __stop_motors(self):
        self.left_motor.disable_motor()
        self.right_motor.disable_motor()