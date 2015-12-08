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

    cv2.imshow("", im)
    cv2.waitKey()
    cv2.imshow("", imthresh)
    cv2.waitKey()

    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(imthresh,1,np.pi/180,100,minLineLength,maxLineGap)


    linepieces = []
    for line in lines[0]:
        cv2.line(im,(line[0],line[1]),(line[2],line[3]),(0,0,255),2)

        for pieces in linepieces:
            if(onSameLine(line, pieces)):
                pieces.append(line)
                break
        else:
            linepieces.append([line])

    print linepieces

    lines = []
    #lijnen samenvoegen
    for pieces in linepieces:
        if len(pieces) == 1:
            x1,y1,x2,y2 = pieces[0]
            cv2.line(im,(x1,y1),(x2,y2), (0,255,0),2)
            lines.append(pieces[0])
        else:
            farthestApart = ((0,0),(0,0))
            for i in range(1,len(pieces)):
                for j in range(i):
                    x1,y1,x2,y2=pieces[i]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))

                    x1,y1,x2,y2=pieces[j]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))

                    x1,y1, _, _ = pieces[i]
                    _, _, x2, y2 = pieces[j]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))
                    x2, y2, _, _ = pieces[j]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))

                    _, _, x1, y1 = pieces[i]
                    _, _, x2, y2 = pieces[j]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))
                    x2, y2, _,_ = pieces[j]
                    if math.hypot(x1-x2,y1-y2) > dist(farthestApart[0], farthestApart[1]):
                        farthestApart = ((x1,y1),(x2,y2))
            lines.append((farthestApart[0][0],farthestApart[0][1],farthestApart[1][0],farthestApart[1][1]))
            cv2.line(im,farthestApart[0],farthestApart[1],(0,255,0),2)

    print lines

    # #horizontale blauw?
    # for line in lines:
    #     x1,y1,x2,y2 = line
    #     if horizontal(line):
    #         cv2.line(im,(x1,y1),(x2,y2), (255,0 ,0),2)

    #eindstukken van plakband wegfilteren
    nuttigeLines = []
    for k in range(len(lines)):
        toevoegen = True
        x1,y1,x2,y2 = lines[k]
        for i in range(1, len(lines)):
            for j in range(i):
                if i == k or j == k:
                    continue
                if abs(line_angle(lines[i]) - line_angle(lines[j]))%180 > 45:
                    continue

                A = (lines[i][0], lines[i][1])
                B = (lines[i][2], lines[i][3])
                position1 = ((B[0] - A[0]) * (y1 - A[0]) - (B[1] - A[1]) * (x1 - A[0])) > 0

                A = (lines[j][0], lines[j][1])
                B = (lines[j][2], lines[j][3])
                position2 = ((B[0] - A[0]) * (y1 - A[0]) - (B[1] - A[1]) * (x1 - A[0])) > 0

                if(position2 != position1): #lijn k ligt tussen lijn i en lijn j
                     cv2.line(im,(x1,y1),(x2,y2), (255,255 ,0),2)
                     toevoegen = False
        if toevoegen:
            nuttigeLines.append(lines[k])

    nuttigeLinesMetZelfdeHoek = []
    for line in nuttigeLines:
        for pieces in nuttigeLinesMetZelfdeHoek:
            if sameAngle(line, pieces):
                pieces.append(line)
                break
        else:
            nuttigeLinesMetZelfdeHoek.append([line])

    print nuttigeLinesMetZelfdeHoek

    nuttigeLines = []
    for lines in nuttigeLinesMetZelfdeHoek:
        if len(lines) == 1:
            continue
        if len(lines) == 2:
            x1,y1,x2,y2 = lines[0]
            x11,y11,x21,y21 = lines[1]

            cv2.line(im,(x1,y1),(x2,y2), (0,255,255),3)
            cv2.line(im,(x11,y11),(x21,y21), (0,255,255),3)
            nuttigeLines.append(((x1+x11)/2, (y1+y11)/2,(x2+x21)/2,(y2+y21)/2))
        else:
            for line in lines:
                nuttigeLines.append(line)
    for lijn in nuttigeLines:
        x1,y1,x2,y2 = lijn

        cv2.line(im,(x1,y1),(x2,y2), (0,0,255),3)

    hoofdLijn = None
    for lijn in nuttigeLines:
        print line_angle(lijn)
        if not horizontal(lijn):
            if hoofdLijn == None or hoofdLijn[1] < lijn[1]:
                hoofdLijn = lijn

    if hoofdLijn != None:
        x1,y1,x2,y2 = hoofdLijn
        cv2.line(im,(x1,y1),(x2,y2), (255,0,255),3)


        A = (hoofdLijn[0], hoofdLijn[1])
        B = (hoofdLijn[2], hoofdLijn[3])
        for line in nuttigeLines:
            if horizontal(line):
                position1 = ((B[0] - A[0]) * (y1 - A[0]) - (B[1] - A[1]) * (x1 - A[0])) > 0
                if position1:
                    print "er is nieuwe straat links"
                else:
                    print "er is nieuwe straat rechts"

    cv2.imshow("", im)
    cv2.waitKey()
