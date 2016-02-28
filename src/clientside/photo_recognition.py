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

    if vertical:
        t = math.atan2(a,1)*180/3.14
        return int(240-b)/a,t
    else:
        t = math.atan2(1,a)*180/3.14
        return int(320*a+b),t

def detect_lines(im):
    im_gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(im_gray,(9,9),0)
    imthresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
    imthresh = cv2.morphologyEx(imthresh, 1, kernel = np.ones((3,3),np.uint8))

    pointsXDown = []
    for i in range(380,480,10):
        nonzero = np.nonzero(imthresh[i,:])[0]
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
            dist = r-l
            if 45 < dist < 250:
                pointsXDown.append((int(p),i))

    if len(pointsXDown)>0:
        avg = np.average(np.array(pointsXDown)[:,0])
        std = np.std(np.array(pointsXDown)[:,0])
        npointsXDown = []
        std = 15 if std < 15 else std
        for (x,y) in pointsXDown:
            if abs(x-avg) < 2*std:
                npointsXDown.append((x,y))
        pointsXDown = [] if len(npointsXDown) < 3 else npointsXDown

    pointsXUp = []
    for i in range(0,100,10):
        nonzero = np.nonzero(imthresh[i,:])[0]
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
            dist = r-l
            if 30 < dist < 100:
                pointsXUp.append((int(p),i))

    if len(pointsXUp)>0:
        avg = np.average(np.array(pointsXUp)[:,0])
        std = np.std(np.array(pointsXUp)[:,0])/5
        std = 15 if std < 15 else std
        npointsXUp = []
        for (x,y) in pointsXUp:
            if abs(x-avg) < 1.5*std:
                npointsXUp.append((x,y))
        pointsXUp = [] if len(npointsXUp) < 3 else npointsXUp

    pointsYl = []
    for i in xrange(0,80,10):
        nonzero = np.nonzero(imthresh[:,i])[0]
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
            dist = r-l
            if 20 < dist < 120:
                pointsYl.append((i,int(p)))

    if len(pointsYl)>0:
        avg = np.average(np.array(pointsYl)[:,1])
        std = np.std(np.array(pointsYl)[:,1])
        npointsYl = []
        for (x,y) in pointsYl:
            if abs(y-avg) < 2*std:
                npointsYl.append((x,y))
        pointsYl = [] if len(npointsYl) < 4 else npointsYl

    pointsYr = []
    for i in xrange(560,640,10):
        nonzero = np.nonzero(imthresh[:,i])[0]
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
            dist = r-l
            if 20 < dist < 120:
                pointsYr.append((i,int(p)))

    if len(pointsYr)>0:
        avg = np.average(np.array(pointsYr)[:,1])
        std = np.std(np.array(pointsYr)[:,1])
        npointsYr = []
        for (x,y) in pointsYr:
            if abs(y-avg) < 2*std:
                npointsYr.append((x,y))
        pointsYr = [] if len(npointsYr) < 4 else npointsYr

    response = [None,None,None,None]

    im = im.copy()

    if len(pointsYl) > 0:
        mid,angle = get_line_param(pointsYl,vertical=False)
        response[0] = (int(480-mid),float(90-angle))
        under = int(mid-math.tan(3.14/2-angle/180*3.14)*320)
        cv2.circle(im,(320,mid),1,(0,255,255),thickness=10)
        cv2.line(im,(320,mid),(0,under),(0,255,255))

    if len(pointsXDown) > 0:
        mid,angle = get_line_param(pointsXDown)
        under = int(mid+math.tan(3.14/2-angle/180*3.14)*240)
        angle = 90+angle if angle < 0 else -90+angle
        response[1] = (int(mid),angle)
        cv2.circle(im,(mid,240),1,(255,255,255),thickness=10)
        cv2.line(im,(mid,240),(under,480),(255,255,255))

    if len(pointsYr) > 0:
        mid,angle = get_line_param(pointsYr,vertical=False)
        response[2] = (int(480-mid),90-angle)
        under = int(mid+math.tan(3.14/2-angle/180*3.14)*320)
        cv2.circle(im,(320,mid),1,(0,255,255),thickness=10)
        cv2.line(im,(320,mid),(640,under),(0,255,255))

    if len(pointsXUp) > 0:
        response[3] = True

    for i in range(0,100,10):
        im[i:i+1,:] = (0,255,0)
    for point in pointsXUp:
        cv2.circle(im,point,1,(255,0,0),thickness=4)

    for i in range(380,480,10):
        im[i-1:i,:] = (0,255,0)
    for point in pointsXDown:
        cv2.circle(im,point,1,(255,0,0),thickness=4)

    for i in range(0,80,10):
        im[:,i:i+1] = (0,0,255)
    for point in pointsYl:
        cv2.circle(im,point,1,(0,0,255),thickness=4)
    for i in range(560,640,10):
        im[:,i-1:i] = (0,0,255)
    for point in pointsYr:
        cv2.circle(im,point,1,(0,0,255),thickness=4)

    print response
    im = cv2.imencode(".jpg",im)[1].tostring()
    return im,response