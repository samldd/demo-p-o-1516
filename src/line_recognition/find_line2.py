from skimage.morphology import skeletonize
from skimage import draw, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

def line_angle(l):
    return int(math.degrees(math.atan2(-(l[3]-l[1]),(l[2]-l[0]))))+180


def sameAngle(line, others):
    for other in others:
        if abs(line_angle(line)%180-line_angle(other)%180) < 40:
            return True
    return False

def onSameLine(line, others):
    other = others[0]
    p1 = (other[0],other[1])
    p2 = (other[2], other[3])
    p3 = (line[0], line[1])
    u = ((p3[0]-p1[0])*(p2[0]-p1[0])+(p3[1]-p1[1])*(p2[1]-p1[1]))/(dist(p2,p1)**2)
    x = p1[0]+u*(p2[0]-p1[0])
    y = p1[1]+u*(p2[1]-p1[1])
    return dist((x,y),p3) < 10

def dist(p1, p2):
    return math.hypot(p1[0]-p2[0],p1[1]-p2[1])

def horizontal(line):
    return -45 < line_angle(line) < 45 or 135 < line_angle(line) < 225 or 315 < line_angle(line) < 360

for i in range(1,56):
    im = cv2.imread('images/%d.jpg'%i)
    print 'image %d'%i
    im = im[:, :]

    blur = cv2.medianBlur(im,31)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imthresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

    cv2.imshow("thresh", imthresh)
    cv2.waitKey()
