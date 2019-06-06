# import the socketserver module of Python

import socketserver
import requests


# Create a Request Handler

# In this TCP server case - the request handler is derived from StreamRequestHandler

class MyTCPRequestHandler(socketserver.StreamRequestHandler):

 

# handle() method will be called once per connection

    

    def handle(self):
        print('-'*8)
        # Receive and print the data received from client

        print("Recieved one request from {}".format(self.client_address[0]))

        msg = (self.rfile.readline().strip()).decode('utf-8')

        msg = msg.split(" ")

        URL = "http://3.84.69.127:80" + msg[1]
        print(URL)
        
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 

        result = r.text

        print('*'*8)
        print(msg)
        print(result)

 

       

        # Send some data to client

        self.wfile.write(result.encode())

            

# Create a TCP Server instance

aServer = socketserver.TCPServer(("127.0.0.1", 9090), MyTCPRequestHandler)

 

# Listen for ever

aServer.serve_forever()