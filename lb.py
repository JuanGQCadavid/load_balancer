#!/usr/bin/env python3.6

import socket
import queue
HOST = 'localhost'
PORT = 8001 #Port listening -> (1023,65535]
BACK_LOG = 100
MAX_BUFFER = 65507 #https://es.stackoverflow.com/questions/43482/python-socket-como-recibir-todos-los-datos-con-socket-recv

server_farm = {'server_1':{'ip':'3.84.69.127','port':8080},
               'server_2':{'ip':'3.84.69.127', 'port':5000}
              }
# socket.AF_INET -> Ipv4, socket.SOCK_STREAM -> TCP

def main():

    servers_queue = startQueue(server_farm)
    global_socket = setup_load_balancer()

    round_robin(servers_queue,global_socket)

def setup_load_balancer():
    print('Setting up socket')
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind((HOST,PORT))
    print('Done')
    return local_socket

def startQueue(servers):
    print("Starting Server's queue")
    local_queue = queue.Queue(maxsize=len(server_farm))

    for server in servers.values():
        print('Putting ', server,'on queue')
        local_queue.put(server)
    print('Done')
    return local_queue

def round_robin(servers_queue,global_socket):
    global_socket.listen(BACK_LOG)
    while True:
        conn,addr = global_socket.accept()
        print('Connected by', addr)

        msg = b''
        while True:
            data = conn.recv(1024)
            msg += data
            if data[len(data)-1] == 10:
                break
        message = msg.decode("utf-8") 

        print('-'*50)
        print(message)
        #Send the data
        server_to_send = servers_queue.get()

        server_ip = server_to_send['ip']
        server_port = server_to_send['port']

        socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_to_server.connect((server_ip, server_port))
        socket_to_server.sendall(msg)
        
        response = b''
        while True:
            data = socket_to_server.recv(1024)
            response += data
            if data[len(data)-1] == 10:
                break
        message = response.decode("utf-8") 

        print(message)
        print('-'*50)

        conn.sendall(response)
        conn.close()
        socket_to_server.close()
        
        #add again the server
        servers_queue.put(server_to_send)




    pass



if __name__ == '__main__':
    main()

