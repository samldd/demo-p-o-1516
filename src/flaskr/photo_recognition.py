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
    t = 90-t if t>0 else -(90+t)

    return (480-b)/a , (240-b)/a

def detect_lines(im):
    resX = 400
    resY = 300
    im_gray = cv2.imdecode(np.fromstring(im, np.uint8),cv2.CV_LOAD_IMAGE_GRAYSCALE)
    im = cv2.imdecode(np.fromstring(im, np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

    blur = cv2.GaussianBlur(im_gray,(9,9),0)

    imthresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
    imthresh = cv2.morphologyEx(imthresh, 1, kernel = np.ones((3,3),np.uint8))

    pointsX = []
    for i in xrange(0,resY,20):
        li = imthresh[i,300-i/2:340+i/2]
        nonzero = np.nonzero(li)[0]
        if len(nonzero):
            av = np.average(nonzero)
            j = 0
            l = 0
            r = 0
            while True:
                if nonzero.item(j) < av:
                    l = nonzero[j]
                else:
                    r = nonzero[j]
                    break
                j +=1
            p = (l+r)/2
            std = np.std(nonzero)
            if 10 < std < 20+i/2:
               pointsX.append((300-i/2+int(p),i))

    pointsX = [] if len(pointsX) < 3 else pointsX

    res = get_line_param(pointsX) if pointsX else ""

    pointsYl = []
    for i in xrange(180,-1,-20):
        x = 1.5*i if 1.5*i < 220 else 220
        li = imthresh[220-x:260+x,180-i]
        nonzero = np.nonzero(li)
        if len(nonzero):
            av = np.average(nonzero)
            std = np.std(nonzero)
            if 10 < std < 20-i/3:
                pointsYl.append((180-i,int(220-x+av)))
    pointsYl = [] if len(pointsYl) < 3 else pointsYl

    pointsYr = []
    for i in xrange(0,180,20):
        y = i + 460
        x = 1.5*i if 1.5*i < 220 else 220
        li = imthresh[220-x:260+x,y]
        nonzero = np.nonzero(li)
        if len(nonzero):
            av = np.average(nonzero)
            std = np.std(nonzero)
            if 10 < std < 20+i/3:
                pointsYr.append((y,int(220-x+av)))
    pointsYr = [] if len(pointsYr) < 3 else pointsYr

    for i in xrange(0,480,20):
        im[i-1:i,300-i/2:340+i/2] = (0,255,0)
    for i in xrange(180,-1,-20):
        x = 1.5*i if 1.5*i < 220 else 220
        im[220-x:260+x,180-i:180-i+1] = (0,255,0)
    for i in xrange(0,181,20):
        j = i + 460
        x = 1.5*i if 1.5*i < 220 else 220
        im[220-x:260+x,j-1:j] = (0,255,0)

    for point in pointsX:
        cv2.circle(im,point,1,(255,0,0),thickness=4)
    for point in pointsYl:
        cv2.circle(im,point,1,(0,0,255),thickness=4)
    for point in pointsYr:
        cv2.circle(im,point,1,(0,0,255),thickness=4)

    if not(res == ""):
        res = (res[0],res[1])
        cv2.circle(im,(int(res[0]),480),1,(0,255,255),thickness=20)
        cv2.circle(im,(int(res[1]),240),1,(0,255,255),thickness=20)

    im = cv2.imencode(".jpg",im)[1].tostring()

    return im