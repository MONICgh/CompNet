from socket import *

def start_scan(ip, MIN = 0, MAX = 2**15 - 1):
    for port in range(MIN, MAX + 1):
        socket_con = socket(
            AF_INET,
            SOCK_STREAM
        )
        socket_con.settimeout(0.3)
        AI_NUMERICSERV = socket_con.connect_ex((ip, port))
        print(port)
        if AI_NUMERICSERV == 0:
            socket_con.close()
            print(f"Port open: {port}")

address = input("range (IP, min, max): ")
print(start_scan(address))