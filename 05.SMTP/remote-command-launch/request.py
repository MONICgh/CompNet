import socket

PORT = 8760

request = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
request.connect(('localhost', PORT))
request.send(input('distant command: ').encode('ascii'))

print(request.recv(1024).decode('CP866'))