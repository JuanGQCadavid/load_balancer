from http.server import BaseHTTPRequestHandler, HTTPServer
import queue, time,requests

class round_robbin_class:
    def __init__(self):
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

class myHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        response = self.handle_http(200, self.path, self.requestline)
        self.wfile.write(response)

    def getURLtoSend(self):
        
        ip,port = self.server.round_robbin.getServer()

        msg = self.requestline
        msg = msg.split(" ")
        URL = "http://" + ip +":" + str(port) + msg[1]
        
        print('!'*67)
        print(URL)
        print('!'*67)

        return URL

    def do_POST(self):
        print('-'*8)
        URL = self.getURLtoSend()
        print(URL)
        
        print('-'*8)
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        post_data = (post_data.decode('utf-8')).split('&')
        data_dict = {}

        for data in post_data:
            data = data.split('=')
            data_dict[data[0]] = data[1]

        r = requests.post(URL, data_dict)
        result = r.text

        self.send_response(200)
        self.end_headers()

        response =  bytes(result, 'UTF-8')

        self.wfile.write(response)


    def handle_http(self, status_code, path,requestline):
        #server_ip,server_port = self.getServer()

        print('-'*8)
        URL = self.getURLtoSend()
        print(URL)
        
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 

        result = r.text
        msg = requestline.split(" ")

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

class http_server:
    def __init__(self,round_robbin):
        HOST_NAME = 'localhost'
        PORT_NUMBER = 9000

        app = HTTPServer((HOST_NAME, PORT_NUMBER), myHandler)
        app.round_robbin = round_robbin

        print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))

        try:
            app.serve_forever()
        except KeyboardInterrupt:
            pass

        app.server_close()
        print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

class main:
    def __init__(self):
        self.round_robbin = round_robbin_class()
        self.server = http_server(self.round_robbin)

if __name__ == '__main__':
    m = main()
