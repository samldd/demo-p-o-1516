#This class represents a BrickPi car.
import DistanceSensor as D
import Camera as C
import Motor as M

class RoboCar(object):

    def __init__(self, IP='192.168.0.100'):
        # Het standaardadres waarnaar de PI zal proberen data te sturen is '192.168.0.100' op poort 3000 
        self.PORT_PC = 3000
        
        self.sensor_brick = D.DistanceSensorBrickPi((IP, self.PORT_PC))
        self.sensor_lego = D.DistanceSensorLego((IP, self.PORT_PC))
        self.camera = C.Camera((IP, self.PORT_PC))

        self.motor_wheels = M.MotorWheels()
        self.motor_sensor = M.MotorSensor()

    def get_brick_distance(self):
        return self.sensor_brick.get_distance()
    
    def get_lego_distance(self):
        return self.sensor_lego.get_distance()
    
    def stop_driving(self):
        self.motor_wheels.stop()

    # Take a picture and sends it over a socket to the computer
    def get_picture(self):
        self.camera.get_one_image()
    
    def start_threads(self):
        self.sensor_brick.start()
        self.sensor_lego.start()
        self.camera.start()
    
    def stop_threads(self):
        print "Stopping the distance brick thread"
        self.sensor_brick.stop()
        
        print "Stopping lego sensor"
        self.sensor_lego.stop()
        
        print "Stopping camera thread"
        self.camera.stop()


    def update_ip(self, ip):
        self.camera.ADDRESS = (ip, self.PORT_PC)
        self.sensor_brick.ADDRESS = (ip, self.PORT_PC)
        self.sensor_lego.ADDRESS = (ip, self.PORT_PC)
        print "Will be sending data to %s when starting ..." % ip
        
        