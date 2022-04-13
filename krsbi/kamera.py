import cv2
import numpy as  np
import serial

minRadiusBall = 10 ## radius minimal kontur bola dalam pixel
minRadiusGoal = 10
bola = 0
gawang = 0
tendang = 0
siapTendang = 0
xBall = 0
yBall = 0
xGoal = 0
yGoal = 0
approx = 0

cap = cv2.VideoCapture(0)  ## memanggil webcam
ser = serial.Serial('/dev/ttyUSB0', 9600)

while cv2.waitKey(1) !=27 and cap.isOpened():  ## tekan esc untuk keluar loop
    readFrame, imgOriginal = cap.read()  ## membaca data pada webcam

    ## konversi video asli rgb ke hsv
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    ## menentukan batas warna H=0-179 S=0-255 V=0-255
    imgThreshBall = cv2.inRange(imgHSV, (0, 196, 71), (16, 255, 255))
    imgThreshGoal = cv2.inRange(imgHSV, (107, 154, 124), (121, 255, 255))
    imgThreshField = cv2.inRange(imgHSV, (66, 96, 99), (99, 255, 255))
    
    ## filter
    imgThreshBall = cv2.GaussianBlur(imgThreshBall, (3, 3), 3)
    imgThreshGoal = cv2.GaussianBlur(imgThreshGoal, (3, 3), 3)
    imgThreshField = cv2.GaussianBlur(imgThreshField, (3, 3), 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    
    ## mendapatkan pixel kontur
    contoursBall = cv2.findContours(imgThreshBall, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contoursGoal = cv2.findContours(imgThreshGoal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contoursField = cv2.findContours(imgThreshField, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #(imgField,contoursField,hierarcy)=cv2.findContours(imgThreshField, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    ## titik tengah camera
    intRows, intColumns = imgThreshBall.shape
    centerRows = intRows/2
    centerColumns = intColumns/2

    ## mencari kontur terbesar dan dirbuah ke polygon
    if len(contoursField) > 0:
        cf = max(contoursField, key=cv2.contourArea)
        epsilon = 0.009*cv2.arcLength(cf,True)
        approx = cv2.approxPolyDP(cf,epsilon,True)
        cv2.drawContours(imgOriginal, [approx], 0, (0, 255, 0), 2)
        
    ## mencari kontur terbesar dan dirubah ke persegi
    centerGoal = None
    radiusGoal = 0
    if len(contoursGoal) >0:
        cg = max(contoursGoal, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cg)
        M1 = cv2.moments(cg)
        if M1["m00"]>0:
            centerGoal = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
            X = int(M1["m10"] / M1["m00"])
            Y = int(M1["m01"] / M1["m00"])
            xGoal = X - centerColumns
            yGoal = centerRows - Y
            #deteksi gawang dilapangan atau tidak
            if cv2.pointPolygonTest(approx,(x+w/2,y+h*1.1),False) == 1:
                gawang = 1
            else:
                gawang = 0
            if w < minRadiusGoal or h <minRadiusGoal:
                centerGoal = None
            
    ## mencari kontur terbesar dan dirubah ke lingkaran
    centerBall = None
    radiusBall = 0
    if len(contoursBall) > 0:
        c = max(contoursBall, key=cv2.contourArea)
        ((x, y), radiusBall) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            centerBall = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X = int(M["m10"] / M["m00"])
            Y = int(M["m01"] / M["m00"])
            xBall = X-centerColumns
            yBall = centerRows - Y
            ##deteksi bola dilapangan atau tidak
            if cv2.pointPolygonTest(approx,(X, Y+radiusBall*1.5),False) == 1 or cv2.pointPolygonTest(approx,(X, Y-radiusBall),False) == 1 or cv2.pointPolygonTest(approx,(X+radiusBall, Y),False) == 1 or cv2.pointPolygonTest(approx,(X-radiusBall, Y),False) == 1:
                bola = 1
                if (yBall>-80):  
                    siapTendang = 0
                else:
                    siapTendang = 1
            else:
                bola = 0
            if radiusBall < minRadiusBall:
                center = None
    
    ## konversi pixel ke sudut
    sudutBola = (-xBall - (-320)) * (25 - (-25)) / (320 - (-320)) + (-25)
    sudutGawang = (-xGoal - (-320)) * (25 - (-25)) / (320 - (-320)) + (-25) 

    ## jika mendeteksi bola menampilkan ke python shell
    print str(bola)+" sBola = "+str(sudutBola)+"\t"+str(gawang)+" sGawang = "+ str(sudutGawang)+"\tsTendang = "+str(siapTendang)+"\ttendang = "+str(tendang)

    ## mengirim data ke arduino
    ser.write(str(sudutBola)+","+str(bola)+","+str(siapTendang)+","+str(sudutGawang)+","+str(gawang)+";")
    
    ##menampikan video langsung 
    #cv2.imshow('imgOriginal', imgOriginal)  ## menampilkan window webcam
    #cv2.imshow('imgHasil', imgField)  ## menampilkan window hasil img prosesing


cap.release()
cv2.destroyAllWindows()
