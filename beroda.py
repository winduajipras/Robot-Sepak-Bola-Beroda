#!/usr/bin/env python
 
# mengimpor modul socket
import socket
 
# menentukan alamat server
server_address = ('', 3838)
 
# ukuran buffer ketika menerima pesan
SIZE = 1024
 
# membuat objek socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# bind ke alamat server
s.bind(server_address)
print "Conction Done"
# mendengarkan koneksi dari client
s.listen(1)
 
# siap menerima pesan terus-menerus dari client
while 1:
	# menerima koneksi dari client
	client, client_address = s.accept()
 
	# menerima pesan dari client
	message = client.recv(SIZE)
 
	# jika tidak ada pesan, keluar dari while
	if not message:
		break
 
	# mengirimkan kembali pesan ke client
	client.send(message)
 
# menutup socket
s.close()
