import cv2
import numpy as  np
import serial
import time

minRadius = 10 ## radius minimal kontur bola dalam pixel
sudut = 0
bola = 0
tendang = 0
X = 0
Y = 0

cap = cv2.VideoCapture(0)  ## memanggil webcam
##ser = serial.Serial('/dev/ttyUSB0', 9600)

while cv2.waitKey(1) !=27 and cap.isOpened():  ## tekan esc untuk keluar loop
    readFrame, imgOriginal = cap.read()  ## membaca data pada webcam

    ## konversi video asli rgb ke hsv
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    ## menentukan batas warna H=0-179 S=0-255 V=0-255
    imgThreshBall = cv2.inRange(imgHSV, (0, 196, 71), (16, 255, 255))

    imgThreshBall = cv2.GaussianBlur(imgThreshBall, (3, 3), 3)
    
    ## mendapatkan pixel kontur
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
               
    ## jika mendeteksi bola menampilkan ke python shell
    if center != None:
        print "x dan y(" + str(convX)+ "," + str(convY)+ ")" + " \tDiameter=" + str(round(radius))+ "     \tSudut" + str(sudut) 
        bola = 1
        if (convY>-80):  
            tendang = 0
        else:
            tendang = 1
    else:
        bola = 0


    ## mengirim data ke arduino
    ##ser.write(str(sudut)+","+str(bola)+","+str(tendang)+";")
    #time.sleep(0.01)
    


    ## memvisualisasikan lingkaran
    cv2.circle(imgOriginal, center, int(round(radius)), (0, 255, 0))

    ##menampikan video langsung 
    cv2.imshow('imgOriginal', imgOriginal)  ## menampilkan window webcam
   ## cv2.imshow('imgHasil', imgThreshBall)  ## menampilkan window hasil img prosesing


cap.release()
##cv2.waitKey(1)
cv2.destroyAllWindows()
