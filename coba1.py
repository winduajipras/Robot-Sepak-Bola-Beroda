import cv2
import numpy as np
import serial
##import time

minRadius = 10
X = 0
Y = 0

cap = cv2.VideoCapture(0)
ser = serial.Serial('/dev/ttyUSB0',9600)   ## ganti USB0 sesuai dengan port arduino

while cv2.waitKey(1) !=27 and cap.isOpened():   ## tekan esc untuk keluar loop
    readFrame, imgOriginal = cap.read()

    ## konversi gambar asli ke HSV
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    ## menentukan batas warna
    imgThreshBall = cv2.inRange(imgHSV, (0, 92, 177), (16, 237, 255))

    ## filter efek penghalus
    ##imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 3)
    ##imgThresh = cv2.dilate(imgThresh, None, iterations = 1)

    ## mendapatkan nilai kontur
    imgContoursBall = imgThreshBall.copy()
    contoursBall = cv2.findContours(imgContoursBall, cv2.RETR_EXTERNAL, \
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    ## mencari kontur terbesar dan dirubah ke lingkaran
    center = None
    radius = 0
    if len(contoursBall) > 0:
        c = max(contoursBall, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X = int(M["m10"] / M["m00"])
            Y = int(M["m01"] / M["m00"])
            if radius < minRadius:
                center = None

    ## titik tengah camera
    intRows, intColumns = imgThreshBall.shape
    centerRows = intRows/2
    centerColumns = intColumns/2
    convX = X - centerColumns
    convY = centerRows - Y

    ## konversi pixel ke sudut
    sudut = (-convX - (-320)) * (25 - (-25)) / (320 - (-320)) + (-25)
                
    ## menampilkan ke python shell
    if center != None:
        print "(" + str(convX)+ ", " + str(convY)+ ")" + " D = " + str(round(radius))+ "        \ta = " + str(sudut)

    ## mengirim data ke arduino
        ser.write(str(sudut)+",")

    ## memvisualisasikan lingkaran
        cv2.circle(imgOriginal, center, int(round(radius)), (0, 255, 0))
        
    ## menampilkan video langsung
    cv2.imshow('imgOriginal', imgOriginal)
    ##cv2.imshow('imgControursBall', imgThreshBall)

cap.release()
cv2.destroyAllWindows()
