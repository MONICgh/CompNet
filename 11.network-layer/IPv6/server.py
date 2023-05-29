
import socket

host = '0000:0000:0000:0000:0000:0000:0000:0001'
port = 1234

def echo_server():
    sock = socket.socket(
        socket.AF_INET6, 
        socket.SOCK_STREAM,
        0
    )
    sock.setsockopt(
        socket.SOL_SOCKET, 
        socket.SO_REUSEADDR,
        1
    )
    
    sock.bind((host, port))
    sock.listen(5) 
    while True: 
        client, address = sock.accept() 
        data = client.recv(2048) 
        if data:
            client.send(str.upper(data.decode()).encode('utf-8'))
        client.close() 

echo_server()

