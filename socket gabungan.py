import socket
import cv2
import numpy as  np

UDP_IP = ''
UDP_PORT = 3838
paketdata = 'anam'
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))
#sock.sendto(paketdata,(UDP_IP, UDP_PORT))
print "Socket OK"
babul=0
lazu=0
merah=0
biru=0
rizal=0
while 1:
    
    data, addr = sock.recvfrom(116)#116 jumlah bufffer
    if((data) and (len(data) == 116)):
        data = [ord(c) for c in data]
##    print len(data)
#    print "received message:", data
##    print "data ke 9=",data[9]  
##    print "STATE="
##    print "Gol Biru = ",biru
##    print "Gol Merah = ",merah

    if data[4]==7:
        if data[9]==0:print "####### INITIAL #######"
        elif data[9]==1:print "READY"
        elif data[9]==2:#print "SET"
            minRadius = 20 ## radius minimal kontur bola dalam pixel
            sudut = 0
            bola = 0
            tendang = 0
            X = 0
            Y = 0

            cap = cv2.VideoCapture(0)  ## memanggil webcam
            while cv2.waitKey(1) !=27 and cap.isOpened():  ## tekan esc untuk keluar loop
                _, imgOriginal= cap.read()  ## membaca data pada webcam

                ## konversi video asli rgb ke hsv
                imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
                
                ## menentukan batas warna H=0-179 S=0-255 V=0-255
                imgThreshBall = cv2.inRange(imgHSV,(0, 128, 182), (12, 255, 255))#(0, 6, 132), (22, 255, 255)
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
                    if (convY>-150):  
                        tendang = 0
                    else:
                        tendang = 1


                ## memvisualisasikan lingkaran
                cv2.circle(imgOriginal, center, int(round(radius)), (0, 255, 0))

            cap.release()
            cv2.destroyAllWindows()

            
        elif data[9]==3:
            if data[11]==0:
                    if data[4]==7:
                        #print "PLAY KICK BIRU"
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
                        ##ser = serial.Serial('/dev/ttyUSB0', 9600)

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
                            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
                            
                            ## mendapatkan pixel kontur
                            contoursBall = cv2.findContours(imgThreshBall, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            contoursGoal = cv2.findContours(imgThreshGoal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            (imgField,contoursField,hierarcy)=cv2.findContours(imgThreshField, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

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
                            ##    ser.write(str(sudutBola)+","+str(bola)+","+str(siapTendang)+","+str(sudutGawang)+","+str(gawang)+";")
                                
                            ##menampikan video langsung 
                            cv2.imshow('imgOriginal', imgOriginal)  ## menampilkan window webcam
                            cv2.imshow('imgHasil', imgField)  ## menampilkan window hasil img prosesing

                        cap.release()
                        cv2.destroyAllWindows()
       
                        
            if data[11]==1:
                if data[4]==7:
                        print "PLAY KICK MERAH"
        elif data[9]==4:print "FINISH"
       # elif data[10]==1:print"play"
        

    elif data[4]==8:
        if data[7]==0:print "####### INITIAL #######"
        elif data[7]==1:print "READY"
        elif data[7]==2:#print "SET"
            minRadius = 20 ## radius minimal kontur bola dalam pixel
            sudut = 0
            bola = 0
            tendang = 0
            X = 0
            Y = 0

            cap = cv2.VideoCapture(0)  ## memanggil webcam
            while cv2.waitKey(1) !=27 and cap.isOpened():  ## tekan esc untuk keluar loop
                _, imgOriginal= cap.read()  ## membaca data pada webcam

                ## konversi video asli rgb ke hsv
                imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
                
                ## menentukan batas warna H=0-179 S=0-255 V=0-255
                imgThreshBall = cv2.inRange(imgHSV,(0, 128, 182), (12, 255, 255))#(0, 6, 132), (22, 255, 255)
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
                    if (convY>-150):  
                        tendang = 0
                    else:
                        tendang = 1

              
                ## memvisualisasikan lingkaran
                cv2.circle(imgOriginal, center, int(round(radius)), (0, 255, 0))

            cap.release()
            cv2.destroyAllWindows()

    

        elif data[7]==3:
            if data[11]==0:
                    if data[4]==7:
                        #print "PLAY KICK BIRU"
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
                        ##ser = serial.Serial('/dev/ttyUSB0', 9600)

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
                            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
                            
                            ## mendapatkan pixel kontur
                            contoursBall = cv2.findContours(imgThreshBall, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            contoursGoal = cv2.findContours(imgThreshGoal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            (imgField,contoursField,hierarcy)=cv2.findContours(imgThreshField, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

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
                            ##    ser.write(str(sudutBola)+","+str(bola)+","+str(siapTendang)+","+str(sudutGawang)+","+str(gawang)+";")
                                
                            ##menampikan video langsung 
                            cv2.imshow('imgOriginal', imgOriginal)  ## menampilkan window webcam
                            cv2.imshow('imgHasil', imgField)  ## menampilkan window hasil img prosesing

                        cap.release()
                        cv2.destroyAllWindows()
                        
                    
                        
            if data[11]==1:
                if data[4]==7:
                        print "PLAY KICK MERAH"
            
        elif data[7]==4:print "FINISH"
        #elif  data[10]==0:print"play"
       

    if data[26]<=30:
        if data[24]==5:print"pickup robot 1 biru"
    elif data[26]<=30:
        if data[24]==0:print"pickup robot 1 biru"

    if data[30]<=30:
        if data[28]==5:print "pickup robot 2 biru"
    elif data[30]<=30:
        if data[28]==0:print"pickup robot 2 biru"

    if data[74]<=30:
        if data[72]==5:print"pickup robot 1 merah"
    elif data[74]<=30:
        if data[72]==0:print"pickup robot 1 merah"

    if data[78]<=30:
        if data[76]==5:print"pickup robot 2 merah"
    elif data[78]<=30:
        if data[76]==0:print"pickup robot 2 merah"

    if data[71] > rizal:merah +=1
    if data[71] > babul:
        babul = data[71]
        for a in range(0, 5):
            print"gol merah"

    elif data[20] > lazu :
        if data[4]==8:
            lazu =data[20]
            for a in range(0, 5):
                print "gol biru"
    
   
        
#state/kondisi ada di data ke 9 jadi perubahannya cuma 1-4 aja
#1= initial, 2= Ready, 3=Set dst
#Tugas analisis data yang lain yang blum terdetesi

##    if data[71] > rizal:print "GOL MERAH"   #Gool data[71]Merah, data[20]Biru patokan data[4]=8
##    elif data[20] > lazu  :
##        if data[4]==8: print "GOL BIRU"     #Urutannya jangan di rubah... perubahan data tempatkan di ahir

##    if data[71] > rizal:merah+=1            #Ini untuk mencetak skor sementara :)
##    elif data[20] > lazu :
##        if data[4]==8: biru+=1
##
##    if data[71] > babul: babul = data[71]  #Ini untuk perubahan data jangan di rubah urutnnya ok bang :)
##    elif data[20] > lazu :
##        if data[4]==8: lazu =data[20]



##    if data[7]==1: 
##        if data[4]==8:print "DROPPED BALL"
##    
##
##    if data[9]==0:print "####### INITIAL #######"
##    elif data[9]==1:print "READY"
##    elif data[9]==2:print "SET"
##    elif data[9]==3:print "PLAY"
##    elif data[9]==4:print "FINISH"
##    else:
##        break

    
    
    #Langsung ke SET Aja gak usah pakek initial dan ready GAK PENTING
#panjang data 116 jadi pakek buffer yang sama aja biar gak banyak loss

