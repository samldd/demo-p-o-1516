import cv2
import numpy as np
import time

for i in range(1,55):
    t = time.time()
    im = cv2.imread('images/%d.jpg'%i)

    blur = cv2.medianBlur(im,31)
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    imthresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
    (shapeX,shapeY) = imthresh.shape

    imthresh = imthresh

    pointsX = []
    for i in range(0,480,20):
        li = imthresh[i,120:520]
        nonzero = [j for j in range(len(li)) if li[j] != 0]
        if nonzero:
            av = np.average(nonzero)
            std = np.std(nonzero)
            if std > 10 and std < 120:
                pointsX.append((120+int(av),i))

    pointsY = []
    for i in range(0,140,20) + range(520,640,20):
        li = imthresh[80:400,i]
        nonzero = [j for j in range(len(li)) if li[j] != 0]
        if nonzero:
            av = np.average(nonzero)
            std = np.std(nonzero)
            if std > 10 and std < 120:
                pointsY.append((i,80+int(av)))

    for i in range(0,480,20):
        im[i-1:i,120:520] = (0,255,0)
    for i in range(0,140,20) + range(520,640,20):
        im[80:400,i-1:i] = (0,255,0)

    for point in pointsX:
        cv2.circle(im,point,1,(255,0,0),thickness=4)
    for point in pointsY:
        cv2.circle(im,point,1,(0,0,255),thickness=4)

    print time.time()-t

    cv2.imshow("original", im)
    cv2.waitKey()
