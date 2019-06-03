#!/usr/bin/env python3.6

import socket

HOST = ''
PORT = 80 #Port listening -> (1023,65535]
BACK_LOG = 100

# socket.AF_INET -> Ipv4, socket.SOCK_STREAM -> TCP

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Associate the socket with a specific network interface and port number
    s.bind((HOST,PORT))
    s.listen(BACK_LOG)

    conn,addr = s.accept()
    with conn:
        print('Connected by',addr)
        while(True):
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


