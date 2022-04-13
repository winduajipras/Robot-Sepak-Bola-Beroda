
import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')
cv2.namedWindow('mask')

# Starting with 100's to prevent error while masking
h,s,v = 0,0,0
hU,sU,vU = 179,255,255
lastsu = 0

# Creating track bar
cv2.createTrackbar('h', 'result',0,180,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

cv2.createTrackbar('hU', 'mask',255,180,nothing)
cv2.createTrackbar('sU', 'mask',255,255,nothing)
cv2.createTrackbar('vU', 'mask',255,255,nothing)

while cv2.waitKey(1) !=27 and cap.isOpened():

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')

    hU = cv2.getTrackbarPos('hU','mask')
    sU = cv2.getTrackbarPos('sU','mask')
    vU = cv2.getTrackbarPos('vU','mask')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([hU,sU,vU])
##    upper_blue = np.array([180,255,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    ##mask = cv2.erode(mask,None,iterations=4)
    #mask = cv2.dilate(mask,None,iterations=4)
    result = cv2.bitwise_and(frame,frame,mask = mask)

    #cv2.imshow('result',result)
    cv2.imshow('mask', mask)

    if lastsu != sU:
        print('('+str(h)+', '+str(s)+', '+str(v)+'), ('+str(hU)+', '+str(sU)+', '+str(vU)+')')

    lastsu = sU

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
