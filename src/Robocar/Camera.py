# sudo apt-get install python-setuptools
# easy_install --user picamera
# easy_install --user -U picamera
import picamera
import time
import threading
import socket
import io
from PIL import Image

class Camera(threading.Thread):
    def __init__(self, ADDRESS):
        threading.Thread.__init__(self)
        self.terminated = False
        self.WIDTH = 640
        self.HEIGHT = 480
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.ADDRESS = ADDRESS        
        
    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (self.WIDTH, self.HEIGHT)
            camera.start_preview()
            time.sleep(0.5)
            
            while not self.terminated:
                self.send_image_over_socket(self.take_image(camera))

    def take_image(self, camera):
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg')
        stream.seek(0)
        return Image.open(stream)

    def send_image_over_socket(self, image):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(6)
            self.socket.connect(self.ADDRESS)
            ######################################################
            ## Laten weten dat er een foto verzonden zal worden ##
            ######################################################
            self.socket.send('image camera')
            
            ######################################
            ## Size doorsturen naar de Computer ##
            ######################################
            (a, b) = image.size
            # print str(a) + " " + str(b)
            self.socket.recv(32)
            self.socket.send(str(a) + " " + str(b))
            
            
            #####################
            ## Foto doorsturen ##
            #####################
            self.socket.recv(32)
            self.socket.sendall(image.tostring())
            self.socket.close()
        except:
            print "Couldn't send image"
            time.sleep(1)
    
        time.sleep(1)
    
    def get_one_image(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (self.WIDTH, self.HEIGHT)
            camera.start_preview()
            time.sleep(0.5)
            self.send_image_over_socket(self.take_image(camera))

    def stop(self):
        self.terminated = True
        
