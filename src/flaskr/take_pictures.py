__author__ = 'sam_l'

# sudo apt-get install python-setuptools
# easy_install --user picamera
# easy_install --user -U picamera
import picamera
import time
import io
class Camera():

    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 480

    '''
    This method returns the image taken by the robocar as a io.BytesIO object
    '''
    def get_image(self):
        with picamera.PiCamera() as camera:
            self.__initialize_camera(camera)
            return self.__take_image(camera)


    def __initialize_camera(self, camera):
        camera.resolution = self.WIDTH, self.HEIGHT
        camera.start_preview()
        time.sleep(0.5)

    def __take_image(self, camera):
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg')
        stream.seek(0)
        return stream

if __name__ == '__main__':
    camera = Camera()
    camera.get_image()
