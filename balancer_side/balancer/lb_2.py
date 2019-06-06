import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import queue
import requests

HOST_NAME = 'localhost'
PORT_NUMBER = 9000


class MyHandler(BaseHTTPRequestHandler):


    def balancer_init(self):
        server_farm = {'server_1':{'ip':'3.84.69.127','port':80},
               'server_2':{'ip':'3.84.69.127', 'port':5000}}
        self.servers_queue = self.startQueue(server_farm)
        return
    
    def startQueue(self,servers):
        print("Starting Server's queue")
        local_queue = queue.Queue(maxsize=len(servers))

        for server in servers.values():
            print('Putting ', server,'on queue')
            local_queue.put(server)
        print('Done')
        return local_queue
    
    def getServer(self):
        server_to_send = self.servers_queue.get()

        server_ip = server_to_send['ip']
        server_port = server_to_send['port']

        print('Routing to', server_ip,':',server_port)

        self.servers_queue.put(server_to_send)

        return server_ip,server_port



    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.respond({'status': 200})

    def handle_http(self, status_code, path,requestline):
        #server_ip,server_port = self.getServer()
        print('-'*8)

        msg = requestline
        print(msg)

        msg = msg.split(" ")
        URL = "http://3.84.69.127:80" + msg[1]
        print(URL)
        
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 

        result = r.text

        print('*'*8)
        print(msg)
        print(result)

        type_of_content = msg[1].split('.')
        print(type_of_content)

        if(len(type_of_content)> 1):
            if(type_of_content[1] == 'css'):
                type_of_content = 'text/css'
            else:
                type_of_content = 'text/html'
        else:
            type_of_content = 'text/html'

        self.send_response(status_code)
        
        self.send_header('Content-type', type_of_content)
        self.end_headers()

        return bytes(result, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path, self.requestline)
        self.wfile.write(response)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))