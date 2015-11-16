import socket               # Import socket module

import cv2
import math
import numpy as np

def line_angle(l):
    return int(math.degrees(math.atan2(-(l[3]-l[1]),(l[2]-l[0]))))+180

def get_angle():
    im = cv2.imread('torecv.jpg')
    im = im[len(im)/3:, :]

    blur = cv2.medianBlur(im,31)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imthresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(imthresh,1,np.pi/180,100,minLineLength,maxLineGap)

    angles = map(lambda l: line_angle(l), lines[0])
    average = sum(angles)/len(angles)

    return average-90



s = socket.socket()         # Create a socket object
host = '192.168.42.1'       # IP adres van de Pi
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
f = open('torecv.jpg','wb')
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    print "Receiving..."
    l = c.recv(1024)
    while (l):
        print "Receiving..."
        f.write(l)
        l = c.recv(1024)
    f.close()
    print "Done Receiving"
    c.send(str(get_angle()))
    c.close()                # Close the connection