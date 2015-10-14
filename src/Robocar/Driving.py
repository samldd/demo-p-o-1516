from BrickPi import *
from math import pi, copysign
import time


class Driving:
    def __init__(self, car):
        self.default_v = 130
        self.car = car
        self.target = 35
        self.perimeter = 0.056 * pi

    def drive_parallel(self, distance, sampling_time=.1, delay_when_stopping=.05, times=3):
        num_motor = 2
        port = [PORT_B, PORT_C]
        flag_goal = False

        previous = 0
        integral = 0

        kp = 3.75
        kd = 3
        ki = 1.5

        deg = 0.01 * distance / self.perimeter * 360

        init_val = [0] * num_motor
        final_val = [0] * num_motor
        run_stat = [0] * num_motor
        BrickPiUpdateValues()

        for i in range(num_motor):
            BrickPi.MotorEnable[port[i]] = 1
            BrickPi.MotorSpeed[port[i]] = self.default_v
            init_val[i] = BrickPi.Encoder[port[i]]
            final_val[i] = init_val[i] + (deg * 2)

        #TODO: add lego distance check
        while not flag_goal:
            result = BrickPiUpdateValues()
            if not result:
                distance_brick = self.car.get_brick_distance()
                if distance_brick < 80:
                    error = self.target - distance_brick
                    integral = integral + error * sampling_time
                    derivative = (error - previous) / sampling_time

                    output = kp * error + ki * integral + kd * derivative
                    previous = error

                    BrickPi.MotorSpeed[port[1]] = max(0, min(self.default_v + int(output), 250))
                else:
                    BrickPi.MotorSpeed[port[1]] = self.default_v

                if not flag_goal:
                    for i in range(num_motor):
                        if(deg > 0 and final_val[i] > init_val[i]) or (deg < 0 and final_val[i] < init_val[i]):
                            init_val[i] = BrickPi.Encoder[port[i]]
                        else:
                            flag_goal = True

            for i in range(times):
                BrickPiUpdateValues()

            time.sleep(sampling_time)

        for j in range(num_motor):
            BrickPi.MotorSpeed[port[j]] = -self.default_v if deg > 0 else self.default_v
            BrickPiUpdateValues()
            time.sleep(delay_when_stopping)
            BrickPi.MotorEnable[port[j]] = 0
            BrickPiUpdateValues()

        return 0

    def turn_sensor_island(self, degrees, sampling_time=.1, delay_when_stopping=0.05):
        port = PORT_D
        BrickPiUpdateValues()

        BrickPi.MotorEnable[port] = 1  # Enable the Motors
        BrickPi.MotorSpeed[port] = int(copysign(self.default_v, degrees))

        init_val = BrickPi.Encoder[port]  # Initial reading of the encoder
        # Final value when the motor has to be stopped;One encoder value counts
        # for 0.5 degrees
        final_val = init_val + (degrees * 2)

        while True:
            # Ask BrickPi to update values for sensors/motors
            result = BrickPiUpdateValues()
            if not result:
                init_val = BrickPi.Encoder[port]
                if (init_val > final_val and degrees > 0) or (init_val < final_val and degrees <= 0):
                    # Run the motors in reverse direction to stop instantly
                    BrickPi.MotorSpeed[port] = - \
                        int(copysign(self.default_v, degrees))
                    BrickPiUpdateValues()
                    time.sleep(delay_when_stopping)
                    break
            # sleep for the sampling time given (default:100 ms)
            time.sleep(sampling_time)
        BrickPi.MotorEnable[port] = 0
        BrickPiUpdateValues()
        return 0
