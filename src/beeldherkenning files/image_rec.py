import numpy as np
import math
import cv2
import time


def get_line_param(points,vertical=True):
    x = np.array(points)
    m = x.size/2

    if vertical:
        tmp = x[:,0].copy()
        x[:,0] = x[:,1]
        x[:,1] = tmp

    a = np.matrix([np.ones(m), x[:,0]]).T
    b = np.matrix(x[:,1]).T
    yy = (a.T * a).I * a.T * b

    if vertical:
        a = 1/yy[1]
        b = -yy[0]/yy[1]
    else:
        a = yy[1]
        b = yy[0]

    t = math.atan(a)*180/3.14
    t = 180-t if t>0 else -t

    print (480-b)/a , 90-t


def detect_lines(im):
    t = time.time()
    cvim = cv2.imdecode(np.fromstring(im, np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    blur = cv2.GaussianBlur(cvim,(9,9),0)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imthresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
    print "algorithm time: %s" %(time.time()-t)
    pointsX = []
    for i in range(0,480,20):
        li = imthresh[i,300-i/2:340+i/2]
        nonzero = [j for j in range(len(li)) if li[j] != 0]
        if nonzero:
            av = np.average(nonzero)
            std = np.std(nonzero)
            if 10 < std < 20+i/3:
                pointsX.append((300-i/2+int(av),i))
    pointsX = [] if len(pointsX) < 3 else pointsX

    pointsYl = []
    for i in range(180,-1,-20):
        x = 1.5*i if 1.5*i < 220 else 220
        li = imthresh[220-x:260+x,180-i]
        nonzero = [j for j in range(len(li)) if li[j] != 0]
        if nonzero:
            av = np.average(nonzero)
            std = np.std(nonzero)
            if 10 < std < 20-i/3:
                pointsYl.append((180-i,int(220-x+av)))
    pointsYl = [] if len(pointsYl) < 3 else pointsYl

    pointsYr = []
    for i in range(0,180,20):
        y = i + 460
        x = 1.5*i if 1.5*i < 220 else 220
        li = imthresh[220-x:260+x,y]
        nonzero = [j for j in range(len(li)) if li[j] != 0]
        if nonzero:
            av = np.average(nonzero)
            std = np.std(nonzero)
            if 10 < std < 20+i/3:
                pointsYr.append((y,int(220-x+av)))
    pointsYr = [] if len(pointsYr) < 3 else pointsYr

    result = [None,None,None]
    if pointsX:
        result[0] = get_line_param(pointsX)
    if pointsYl:
        result[1] = get_line_param(pointsYl,False)
    if pointsYr:
        result[2] = get_line_param(pointsYr,False)

    return result