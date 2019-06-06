import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import queue

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
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path,requestline):
        server_ip,server_port = self.getServer()
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        <p>Request: {}</p>
        <p>to: {}:{}</p>
        </body></html>
        '''.format(requestline,server_ip,server_port)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path, self.requestline)
        self.wfile.write(response)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    httpd.balancer_init()
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))