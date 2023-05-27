import socket
import time
from datetime import datetime

PORT = 8765

def broadcaster():
    param = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP
    )
    param.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BROADCAST,
        1
    )

    while True:
        param.sendto(
            str(datetime.now()).encode('ascii'),
            ('255.255.255.255', PORT)
        )
        time.sleep(1)

broadcaster()