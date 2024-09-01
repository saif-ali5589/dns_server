import http.server
import socketserver
from config import PORT, DIRECTORY, HOST



class MyhttpRequestHanlder(http.server.SimpleHTTPRequestHandler):

    def do_GET(self) -> None:
        if self.path == '/a.html':
            self.path = '/a.html'
        elif self.path == '/b.html':
            self.path = '/b.html'

        return super().do_GET(self)
    
    def translate_path(self, path: str) -> str:
        return f"./{DIRECTORY}/{path}"
    

my_handler = MyhttpRequestHanlder

myserver = socketserver.TCPServer((HOST, PORT), MyhttpRequestHanlder)

print('tcp server is up!!!')

myserver.serve_forever()