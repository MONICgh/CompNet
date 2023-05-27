import socket

PORT = 8765

def client():
    param = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP
    )
    param.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    param.bind(('', PORT))

    while True:
        time, *_ = param.recvfrom(2^10)
        print(time)

client()