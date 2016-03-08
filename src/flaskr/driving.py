from __future__ import division
import math
import time
import threading

import BrickPi

import motor


class Driving(threading.Thread):

    battery_factor = 1

    def __init__(self):
        threading.Thread.__init__(self)
        self.sample_time = 0.05
        self.default_speed = 70
        self.d_wheel = 0.145
        self.perimeter_wheel = 0.055 * math.pi

        self.left_motor = motor.left
        self.right_motor = motor.right

        self.left_speed = 0
        self.right_speed = 0

        self.left_ticks = self.left_motor.get_encoder_value()
        self.right_ticks = self.right_motor.get_encoder_value()

        self.active = True
        self.paused = True
        self.direction = ""
        self.factor = 0

    def set_battery_factor(self,factor):
        if factor > 2.5:
            factor = 2.5
        elif factor < 0.5:
            factor = 0.5
        Driving.battery_factor = factor

    def get_status(self):
        return self.direction

    def drive_arc(self, radius):
        if not self.direction == "forward":
            self.stop_driving()
        self.direction = "forward"
        self.paused = False
        self.default_speed = (90+3.66*(math.fabs(radius)-20))*Driving.battery_factor
        if radius < 0:
            self.factor = -(2.5-(math.fabs(radius)-20)*0.038)
            self.left_speed = self.default_speed/-self.factor
            self.right_speed = self.default_speed
        elif radius > 0:
            self.factor = (2.5-(radius-20)*0.038)
            self.left_speed = self.default_speed
            self.right_speed = self.default_speed/self.factor

    def drive_correction(self,correction):
        if abs(correction) < 1:
            self.drive_straight(self.battery_factor*80)
        else:
            if not self.direction == "forward":
                self.stop_driving()
            self.direction = "forward"
            self.paused = False
            self.default_speed = 60*math.pow(abs(correction),1/3) if abs(correction)> 1.75 else 80*math.sqrt(abs(correction))
            self.factor = correction
            if correction > 0:
                self.left_speed = Driving.battery_factor*self.default_speed/correction
                self.right_speed = Driving.battery_factor*self.default_speed
            else:
                self.left_speed = Driving.battery_factor*self.default_speed
                self.right_speed = Driving.battery_factor*self.default_speed/abs(correction)
            self.left_speed *= Driving.battery_factor
            self.right_speed *= Driving.battery_factor

    def get_driven_distance(self):
        Ticks360 = 700
        factor = self.perimeter_wheel/Ticks360
        left = (self.left_motor.get_encoder_value() - self.left_ticks)*factor
        right = (self.right_motor.get_encoder_value() - self.right_ticks)*factor
        return left,right

    def drive_straight(self, speed=80):
        speed = speed*Driving.battery_factor
        if not self.direction == "forward":
            self.stop_driving()
        self.paused = False
        self.direction = "forward"
        self.factor = 0
        self.left_speed = speed
        self.right_speed = speed

    def stop_driving(self):
        self.paused = True
        self.left_speed = 0
        self.right_speed = 0
        self.left_motor.stop()
        self.right_motor.stop()
        self.direction = ""

    def drive_back(self):
        if not self.direction == "back":
            self.stop_driving()
        self.paused = False
        self.direction = "back"
        self.factor = 0
        self.left_speed = Driving.battery_factor*-50
        self.right_speed = Driving.battery_factor*-50

    def turn(self,degrees):
        "PID ????"
        self.stop_driving()
        self.factor = 0
        self.direction = "turning"
        wheel_degrees = self.d_wheel * math.pi * degrees/360
        speed = Driving.battery_factor*80 if wheel_degrees >= 0 else Driving.battery_factor*-80
        self.left_motor.set_velocity(speed)
        self.right_motor.set_velocity(-speed)
        self.reset()
        while True:
            time.sleep(0.05)
            left,right = self.get_driven_distance()
            if left > abs(wheel_degrees) or right > abs(wheel_degrees):
                self.stop_driving()
                break

    def reset(self):
        self.left_ticks = self.left_motor.get_encoder_value()
        self.right_ticks = self.right_motor.get_encoder_value()

    def run(self):
        self.__start_motors()
        pleft = self.left_motor.get_encoder_value()
        pright = self.right_motor.get_encoder_value()
        while self.active:
            if not self.paused:
                # Initialize PID values and constants
                integral = 0
                previous = 0

                ki = 1           # integraal     factor
                kp = 0.1         # proportionele factor
                kd = 0.001          # afgeleide     factor

                # Calculate PID values
                tleft = self.left_motor.get_encoder_value()
                tright = self.right_motor.get_encoder_value()

                left = (tleft-pleft)/self.sample_time
                right = (tright-pright)/self.sample_time

                pleft = tleft
                pright = tright

                if self.factor < 0:
                    error = right+left*self.factor
                elif self.factor > 0:
                    error = left+right *-self.factor
                else:
                    error = right - left

                integral += error * self.sample_time
                derivative = (error - previous) / self.sample_time

                output = kp * error + ki * integral + kd * derivative
                previous = error

                if self.factor > 0:
                    self.left_motor.set_velocity(self.left_speed-output)
                    self.right_motor.set_velocity(self.right_speed)
                else:
                    self.right_motor.set_velocity(self.right_speed-output)
                    self.left_motor.set_velocity(self.left_speed)

            time.sleep(self.sample_time)
        self.__stop_motors()

    def end(self):
        self.active = False

    def __start_motors(self):
        self.left_motor.enable_motor()
        self.right_motor.enable_motor()

    def __stop_motors(self):
        self.left_motor.disable_motor()
        self.right_motor.disable_motor()