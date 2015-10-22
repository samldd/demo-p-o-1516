import math
import time
from BrickPi import *

class Driving(object):

    def __init__(self, car):
        self.car = car
        self.default_v = 210
        self.perimeter = 0.056 * math.pi

        self.WHEEL_DISTANCE = 0.1521
        self.total_distance_driven = 0

        # Motors
        self.left_motor = self.car.get_left_motor()
        self.right_motor = self.car.get_right_motor()

    def turn(self, degree):
        wheel_degrees = 2 * self.WHEEL_DISTANCE * math.pi * degree / self.perimeter
        speed = 130 if wheel_degrees >= 0 else -130
        self.__start_motors([self.left_motor, self.right_motor],[speed, -speed])

        while True:
            if abs(self.left_motor.get_encoder()) > abs(wheel_degrees) or abs(self.right_motor.get_encoder()) > abs(wheel_degrees):
                self.__stop_motors([self.left_motor, self.right_motor])
                break

    def drive_straight(self, distance):
        degrees = 0.02 * distance / self.perimeter * 360
        speed = self.default_v
        sampling_time = 0.1
        # delay_when_stopping = 0.05

        # Start motors
        self.__start_motors([self.left_motor, self.right_motor], [speed, speed])

        # Initialize PID values and constants
        integral = 0
        previous = 0
        kp = 4          # proportionele factor
        kd = 0.1        # afgeleide     factor
        ki = 0          # integraal     factor

        while True:
            print "driving"
            BrickPiUpdateValues()
            # Check if both motors have stopped
            print self.left_motor.get_encoder()
            print self.right_motor.get_encoder()
            if abs(self.left_motor.get_encoder()) > abs(degrees) or abs(self.right_motor.get_encoder()) > abs(degrees):
                self.__stop_motors([self.left_motor, self.right_motor])
                break

            # Calculate PID values
            error = self.left_motor.get_encoder() - self.right_motor.get_encoder()
            integral = integral + error * sampling_time
            derivative = (error - previous) / sampling_time
            output = kp * error + ki * integral + kd * derivative
            previous = error

            # Add output to speed left motor
            # mogelijk -output
            self.left_motor.set_speed(speed-output)
            time.sleep(sampling_time)


    def __start_motors(self, motors, speeds):
        print "start motors"
        for motor in motors:
            motor.reset_encoder()

        for i in range(len(motors)):
            motors[i].start(speeds[i])

    def __stop_motors(self, motors, delay_when_stopping=0.05):
        print "stop motors"
        for motor in motors:
            motor.set_speed(-motor.current_speed)
        time.sleep(delay_when_stopping)
        for motor in motors:
            motor.set_speed(0)
            BrickPi.MotorEnable[motor.port] = 0
            self.running = False
        print "end"

