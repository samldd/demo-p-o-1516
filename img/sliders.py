import cv2
import numpy as np
def nothing(x):
    pass

# Create a black image, a window
img = cv2.imread('last_image (7).jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Hmin','image',0,255,nothing)
cv2.createTrackbar('Hmax','image',188,255,nothing)
cv2.createTrackbar('Smin','image',0,255,nothing)
cv2.createTrackbar('Smax','image',28,255,nothing)
cv2.createTrackbar('Vmin','image',217,255,nothing)
cv2.createTrackbar('Vmax','image',255,255,nothing)
cv2.createTrackbar('K','image',0,10,nothing)

while(1):
    # get current positions of four trackbars
    Hmin = cv2.getTrackbarPos('Hmin','image')
    Hmax = cv2.getTrackbarPos('Hmax','image')
    Smin = cv2.getTrackbarPos('Smin','image')
    Smax = cv2.getTrackbarPos('Smax','image')
    Vmin = cv2.getTrackbarPos('Vmin','image')
    Vmax = cv2.getTrackbarPos('Vmax','image')
    K = cv2.getTrackbarPos('K','image')

    im = cv2.inRange(img, np.array((Hmin, Smin, Vmin)), np.array((Hmax, Smax, Vmax)))

    if K > 0:
        kernel = np.ones((K*2+1,K*2+1),np.uint8)
        im = cv2.erode(im, kernel)


    cv2.imshow('image',im)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()