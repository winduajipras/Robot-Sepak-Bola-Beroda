import socket
UDP_IP = ""
UDP_PORT = 3838
paketdata = 'anam'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.sendto(paketdata,(UDP_IP, UDP_PORT))
print "Socket OK"
