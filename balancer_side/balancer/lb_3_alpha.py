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

    def getURLtoSend(self):
        
        ip,port = self.server.round_robbin.getServer()

        msg = self.requestline
        print(msg)
        msg = msg.split(" ")
        URL = "http://" + ip +":" + str(port) + msg[1]
        
        print('!'*67)
        print(URL)
        print('!'*67)

        return URL

    def sendRequest(self,URL, data_dict = None):
        if data_dict == None:
            r = requests.get(URL)
        else:
            r = requests.post(URL, data_dict)
        result = r.text

        self.send_response(200)
        self.end_headers()

        response =  bytes(result, 'UTF-8')
        
        return response

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

        response = self.sendRequest(URL,data_dict)

        self.wfile.write(response)

    def do_GET(self):
        print('-'*8)
        URL = self.getURLtoSend()
        print(URL)
        print('-'*8)

        response = self.sendRequest(URL)

        self.wfile.write(response)



class http_server:
    def __init__(self,round_robbin):
        HOST_NAME = ''
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
