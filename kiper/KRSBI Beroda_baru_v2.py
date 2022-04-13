import cv2
import numpy as  np
import serial

minRadiusBall = 20 ## radius minimal kontur bola dalam pixel
bola = 0
siapTendang = 0
xBall = 0
yBall = 0

cap = cv2.VideoCapture(0)  ## memanggil webcam
ser = serial.Serial('/dev/ttyUSB0', 9600)

while cv2.waitKey(1) !=27 and cap.isOpened():  ## tekan esc untuk keluar loop
    readFrame, imgOriginal = cap.read()  ## membaca data pada webcam

    ## konversi video asli rgb ke hsv
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    ## menentukan batas wearna H=0-179 S=0-255 V=0-255
    imgThreshBall = cv2.inRange(imgHSV, (0, 154, 63), (13, 255, 255))
               
    ## mendapatkan pixel kontur
    contoursBall = cv2.findContours(imgThreshBall, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    ## titik tengah camera
    intRows, intColumns = imgThreshBall.shape
    centerRows = intRows/2
    centerColumns = intColumns/2
            
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
            if radiusBall < minRadiusBall:
                centerBall = None

    if centerBall != None:
        bola = 1
        if (yBall>-80):  
            siapTendang = 0
        else:
            siapTendang = 1
    else:
        bola = 0
    
    ## konversi pixel ke sudut
    sudutBola = (-xBall - (-320)) * (25 - (-25)) / (320 - (-320)) + (-25)

    ## jika mendeteksi bola menampilkan ke python shell
    print str(bola)+" sBola = "+str(sudutBola)+"\tsTendang = "+str(siapTendang)\
          +"\tRadius = "+str(round(radiusBall))

    ## mengirim data ke arduino
    ser.write(str(sudutBola)+","+str(bola)+","+str(siapTendang)+","+str(radiusBall)+";")


cap.release()
cv2.destroyAllWindows()
