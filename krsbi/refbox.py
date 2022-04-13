import socket

UDP_IP = ''
UDP_PORT = 3838
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))
print "Socket OK"
babul=0
lazu=0
merah=0
biru=0
rizal=0

a=0
b=0
c=0    

while (True):
    data, addr = sock.recvfrom(116)#116 jumlah bufffer
    if((data) and (len(data) == 116)):
        data = [ord(c) for c in data]
    #print (data)

    if data[4]==7:
        if data[9]==0:print "####### INITIAL #######"
        elif data[9]==1:print "READY"
        elif data[9]==2:print "SET"
        elif data[9]==3:
            if data[11]==0:
                from play import play     #ambil data dari kamera.py
                #print "PLAY KICK BIRU"
                       
            if data[11]==1:
                print "PLAY KICK MERAH"              
        elif data[9]==4:print "FINISH"        

    elif data[4]==8:
        if data[7]==0:print "####### INITIAL #######"
        elif data[7]==1:print "READY"
        elif data[7]==2:print "SET"
        elif data[7]==3:
            if data[9]==0:
                from play import play      #ambil data dari kamera.py
                #print "PLAY KICK BIRU"
                       
            if data[9]==1:
                print "PLAY KICK MERAH"    
        elif data[7]==4:print "FINISH"

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
