import socket
UDP_IP = ''
UDP_PORT = 28097 #3838
paketdata = 'anam'
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))
#sock.sendto(paketdata,(UDP_IP, UDP_PORT))
print "Socket OK"
a=0
b=0
c=0
d=0
e=0
while 1:
    data, addr = sock.recvfrom(116)#116 jumlah bufffer
    if((data) and (len(data) == 116)):
        data = [ord(c) for c in data]
    print len(data)
    print "received message:", data
    print "data ke 9=",data[9]
    print "data ke 9=",data[16]
   
##    print "STATE="
##    print "Gol Biru = ",biru
##    print "Gol Merah = ",merah
        
    
##    data, addr = sock.recvfrom(116)#116 jumlah bufffer
##    if((data) and (len(data) == 116)):
##        data = [ord(c) for c in data]
##   
##    if data[9]==0:
##        a=a+1
##        if a==0:
##            a=0
##        print "initial"
##    if data[4]==7:
##       
##        b=b+1
##        if b==10:
##            b=0
##        print"ready"
##        
##    
##    if data[9]==2:
##        c=c+1
##        if c==10:
##            c=0
##        print"set"
##    
##    elif data[9]==3:d=d+1
##    elif data[9]==4:e=e+1
##    
    
   
    
    
    
