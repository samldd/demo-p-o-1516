#This file contains all classes concerning the distancesensors
from BrickPi import BrickPiSetup, BrickPiSetupSensors, BrickPi, TYPE_SENSOR_ULTRASONIC_CONT, BrickPiUpdateValues
from BrickPi import PORT_4
import RPi.GPIO as GPIO  # @UnresolvedImport
import threading
import time
import socket

# Super abstract class
class DistanceSensor(threading.Thread):

    def __init__(self, address=('192.168.0.100', 3000)):
        threading.Thread.__init__(self)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)

        self.terminated = False

        self.ADDRESS = address

    def get_distance(self):
        raise NotImplementedError("Should have implemented this")

    def run(self):
        raise NotImplementedError("Call the corresponding subclass method instead of this one")

    def send_data_to_computer(self, message, distance):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(0.5)
            self.socket.connect(self.ADDRESS)
            self.socket.send(message)   # Message = 'distance brickpi' of 'distance lego'
            
            self.socket.recv(32)
            self.socket.send(str(distance))
            self.socket.close()
            # print "Data sent successfully: %s\t%f" % (message, distance)
            time.sleep(1)

        except socket.error, e:
            print "Couldn't send data to the computer", e
            time.sleep(2)

        
    def stop(self):
        self.terminated = True


#DistanceSensor from the BrickPi
class DistanceSensorBrickPi(DistanceSensor):

    def __init__(self, ADDRESS=('192.168.0.100', 3000)):
        super(DistanceSensorBrickPi, self).__init__(ADDRESS)
        self.echo_gpio = 17
        self.trig_gpio = 4
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.echo_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( self.trig_gpio, GPIO.OUT )
        GPIO.output( self.trig_gpio, False )
        self.trig_duration = 0.0001        # Trigger duration
        self.inttimeout = 2100        # Timeout on echo signal
        self.v_snd = 340.29

    def get_distance(self):
        arr = []
        for i in range(20):
            arr.append(self.get_distance2())
        arr = filter(lambda x: isinstance(x, float), arr)
        arr = sorted(arr)
        if len(arr) < 5:
            return 255
        return arr[len(arr)/2]

    def get_distance2(self):
        GPIO.output( self.trig_gpio, True )
        time.sleep( self.trig_duration )
        GPIO.output( self.trig_gpio, False )

        countdown_high = self.inttimeout
        while ( GPIO.input( self.echo_gpio ) == 0 and countdown_high > 0 ):
            countdown_high -= 1

        if countdown_high > 0:
            echo_start = time.time()
            countdown_low = self.inttimeout
            while( GPIO.input( self.echo_gpio ) == 1 and countdown_low > 0 ):
                countdown_low -= 1
            echo_end = time.time()
            echo_duration = echo_end - echo_start

            if countdown_high > 0 and countdown_low > 0:
                distance = echo_duration * self.v_snd * 100 / 2
                return distance
            else:
                return "Timeout"

    def run(self):
        while not self.terminated:
            distance = self.get_distance()
            super(DistanceSensorBrickPi, self).send_data_to_computer('distance brickpi', distance)

##########################
## DISTANCE SENSOR LEGO ##
##########################

class DistanceSensorLego(DistanceSensor):
    def __init__(self, ADDRESS=('192.168.0.100', 3000)):
        super(DistanceSensorLego, self).__init__(ADDRESS)
        BrickPiSetup()
        BrickPi.SensorType[PORT_4] = TYPE_SENSOR_ULTRASONIC_CONT
        BrickPiSetupSensors() 
        
    def get_distance(self):
        result = BrickPiUpdateValues()
        if not result :
            return BrickPi.Sensor[PORT_4]
    def run(self):
        while not self.terminated:
            distance = self.get_distance()
            super(DistanceSensorLego, self).send_data_to_computer('distance lego', distance)
