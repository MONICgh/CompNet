import socket
import subprocess

PORT = 8760

req = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
req.bind(('localhost', PORT))
req.listen()

def get_request():
    while True:
        request, *_ = req.accept()
        request.send(subprocess.check_output(request.recv(1024).decode('ascii')))
        request.close()

get_request()