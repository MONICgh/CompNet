import socket

from random import randint
from checksums_main import *

HOST = '127.0.0.1'
PORT = 1236

client_send = 'csend'
client_receive = 'crecv'
server_send = 'send'
server_receive = 'recv'

pad = 2 + 1000
file_size = 2048
step_size = 1000

def pack_lost():
    return randint(1, 100) < 30

def create():
    data = 'A' * file_size
    open(
        server_send,
        'wt',
        encoding='utf-8'
    ).write(data)
    open(
        client_send,
        'wt',
        encoding='utf-8'
    ).write(data)



def process_send(data, host, port, timeout):

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP
    )
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    s.settimeout(timeout)
    print('Connect')

    wait_ACK = 1
    for i in range(0, len(data), step_size):

        wait_ACK = 1 - wait_ACK

        encoded_data = data[i:i + step_size].encode(encoding='utf-8')
        get_checksum = checksum(bytes([wait_ACK]) + encoded_data)
        modified_data = bytes([get_checksum]) + bytes([wait_ACK]) + encoded_data

        while True:
            s.sendto(modified_data, (host, port))
            try:
                print(f'State ACK: {wait_ACK} sent')
                if pack_lost():
                    if s.recvfrom(5)[0] == bytes([get_checksum]) + bytes([wait_ACK]) + b'ACK':
                        print(f'State ACK: {wait_ACK} received')
                        break
                else:
                    raise socket.timeout()
            except socket.timeout:
                print('Timeout')
                continue


def process_receive(size, _host, _port, timeout):
    
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP
    )
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    s.settimeout(timeout)
    s.bind((_host, _port))
    print('Connect')

    wait_ACK = 0
    out = []

    while size > 0:
        try:
            response = s.recvfrom(pad)
            response_wait_ACK = response[0][1]
            response_data = response[0][2:].decode()

            if pack_lost():
                if response_wait_ACK == wait_ACK:
                    if not check_checksum(response[0]):
                        print('Wrong checksum!')
                        continue

                    wait_ACK = 1 - wait_ACK
                    out.append(response_data)

                    print(f'State resp ACK: {response_wait_ACK}')
                    size = size - len(response_data)

                s.sendto(
                    bytes([checksum(bytes([response_wait_ACK]) + b'ACK')])\
                    + bytes([response_wait_ACK])\
                    + b'ACK', response[1]
                )
                print(f'State ACK: {wait_ACK} sent')
            else:
                raise socket.timeout()
            
        except socket.timeout:
            print('Timeout')
            continue

    return ''.join(out)
