from math import pi
import math
from BrickPi import *
import time

class AI(object):

    def __init__(self, car):
        self.car = car
        self.TARGET_DISTANCE = 35
        self.error = self.TARGET_DISTANCE / 10
        self.default_v = 130
        self.perimeter = 0.056 * math.pi
        self.WHEEL_DISTANCE = 0.1471
        self.island_angle = -1
        self.port = [PORT_C, PORT_B]
        self.sensor_port = PORT_D
        
    def execute_instructions(self, instructions):
        for instr in instructions:
            commando = instr[0]
            argument1 = instr[1]

            if commando == "drive_turn":
                self.turn(argument1)
            elif commando == "drive_forward":
                argument2 = instr[2]
                if argument2 == 2:
                    self.drive_straight(argument1)
                else:
                    self.drive_parallel(argument1, argument2 == 0, instr[3])
            
            time.sleep(1)


    def turn(self, degree):
        wheel_degrees = self.WHEEL_DISTANCE * math.pi * degree / self.perimeter
        BrickPiUpdateValues()
        motorRotateDegree([150, 150], [-wheel_degrees, wheel_degrees], [PORT_C, PORT_B], 0)

    def drive_straight(self, distance):
        perimeter = 0.056 * pi
        degrees = 0.01 * distance / perimeter * 360
        motorRotateDegree([self.default_v, self.default_v - 5], [degrees, degrees], [PORT_C, PORT_B], 0)

    def drive_parallel(self, distance, left, stop_distance, sampling_time=.1, delay_when_stopping=.05, times=3):
        distance = int(distance)
        self.set_sensor_island(left)
        num_motor = 2

        flag_goal = False

        previous = 0
        integral = 0

        kp = 3.75
        kd = 3
        ki = 1.5

        deg = 0.01 * distance / self.perimeter * 360

        init_val = [0] * num_motor
        final_val = [0] * num_motor
        BrickPiUpdateValues()

        for i in range(num_motor):
            BrickPi.MotorEnable[self.port[i]] = 1
            BrickPi.MotorSpeed[self.port[i]] = self.default_v
            init_val[i] = BrickPi.Encoder[self.port[i]]
            final_val[i] = init_val[i] + (deg * 2)
        
        if stop_distance > 40:
            stop_distance = 2048
            
        while not flag_goal or self.car.get_lego_distance() > stop_distance:
            result = BrickPiUpdateValues()
            if not result:
                distance_brick = self.car.get_brick_distance()
                if True:
                    error = self.TARGET_DISTANCE - distance_brick
                    integral = integral + error * sampling_time
                    derivative = (error - previous) / sampling_time

                    output = kp * error + ki * integral + kd * derivative
                    previous = error

                    if not left:
                        output = -output

                    BrickPi.MotorSpeed[self.port[1]] = max(0, min(self.default_v + int(output), 250))
                else:
                    BrickPi.MotorSpeed[self.port[1]] = self.default_v

                if not flag_goal:
                    for i in range(num_motor):
                        if(deg > 0 and final_val[i] > init_val[i]) or (deg < 0 and final_val[i] < init_val[i]):
                            init_val[i] = BrickPi.Encoder[self.port[i]]
                        else:
                            flag_goal = True

            for i in range(times):
                BrickPiUpdateValues()

            time.sleep(sampling_time)

        for j in range(num_motor):
            BrickPi.MotorSpeed[self.port[j]] = -self.default_v if deg > 0 else self.default_v
            BrickPiUpdateValues()
            time.sleep(delay_when_stopping)
            BrickPi.MotorEnable[self.port[j]] = 0
            BrickPiUpdateValues()

        return 0

    def set_sensor_island(self, left):
        if left and self.island_angle == -90:
            return
        if not left and self.island_angle == 90:
            return

        BrickPiSetup()
        power = 100
        BrickPiUpdateValues()
        BrickPi.MotorEnable[self.sensor_port] = 1
        BrickPi.MotorSpeed[self.sensor_port] = -power
        for _ in range(300):
            BrickPiUpdateValues()
        BrickPi.MotorEnable[self.sensor_port] = 0
        self.island_angle = 0

        motorRotateDegree([power], [20], [self.sensor_port], 0)
        self.island_angle = 90

        if left:
            motorRotateDegree([power], [180], [self.sensor_port], 0)
            self.island_angle = -90

            
