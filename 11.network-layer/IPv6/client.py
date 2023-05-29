import socket
 
host = '0000:0000:0000:0000:0000:0000:0000:0001' 
port = 1234

def echo_client(): 
    sock = socket.socket(
        socket.AF_INET6,
        socket.SOCK_STREAM
    )
    
    s = input()

    sock.connect((host, port)) 
    sock.sendall(s.encode('utf-8'))
    data = sock.recv(1024) 
    print(data.decode())
    sock.close()

echo_client() 
