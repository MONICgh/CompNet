import socket
import random

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
    socket.IPPROTO_UDP
)
server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_BROADCAST,
    1
)
server.bind(('', 1234))

while True:
    message, address = server.recvfrom(1024)
    if random.randint(0, 99) < 20:
        print('Package lost!', end='\n\n')
    else:
        server.sendto(message.upper(), address)
        print('Package sent!', end='\n\n')