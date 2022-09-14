# https://docs.python.org/zh-cn/2.7/library/signal.html?highlight=signal
# https://docs.python.org/zh-cn/2.7/library/basehttpserver.html

import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json, signal

def signalHandler(signum, frame):
    print('Signal handler called with signal', signum)
    Request.signalValue = signum
 
class Request(BaseHTTPRequestHandler):
    signalValue = 0

    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())
 
    def do_GET(self):
        print(self.requestline)
        responseCode = 200
        if self.path == '/health' and self.signalValue == 15 :
            responseCode = 500
        
        data = {
            'signal_value': self.signalValue,
            'response_code': responseCode,
            'request_url': self.path,
            'commnad': 'kill -TERM ' + str(os.getpid()),
            'host_name': os.uname()[1]
        }
        self.send_response(responseCode)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    host = ('', 9000)
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    # server.serve_forever()
    # server.server_activate()
    signal.signal(signal.SIGTERM, signalHandler)
    server.serve_forever()