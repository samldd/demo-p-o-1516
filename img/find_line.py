from skimage.morphology import skeletonize
from skimage import draw, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

def line_angle(l):
    return int(math.degrees(math.atan2(-(l[3]-l[1]),(l[2]-l[0]))))+180

for i in range(22,23):
    im = cv2.imread('last_image (%d).jpg'%i)
    im = im[:, :]

    blur = cv2.medianBlur(im,31)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imthresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

    cv2.imshow("", im)
    cv2.waitKey()
    cv2.imshow("", imthresh)
    cv2.waitKey()

    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(imthresh,1,np.pi/180,100,minLineLength,maxLineGap)

    print len(lines[0])
    if lines != None and lines[0] != None:
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(im,(x1,y1),(x2,y2),(0,255,0),2)

    angles = map(lambda l: line_angle(l), lines[0])
    print "angles:", angles
    average = sum(angles)/len(angles)
    print "average:", average

    print "draai", abs(average-90),"graden naar", "rechts" if (average - 90) < 0 else "links"
    cv2.imshow("", im )
    cv2.waitKey()
