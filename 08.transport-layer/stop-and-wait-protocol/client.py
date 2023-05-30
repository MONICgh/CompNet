from common_part import *
from checksums_main import *

print("Choose command: send/receive")

while True:

    command = input()

    if command == 'send':
        file_data = open(
            client_send,
            'rt',
            encoding='utf-8'
        ).read()
        process_send(
            file_data,
            HOST,
            PORT,
            1
        )

        print('Data sent')
        break

    elif command == 'receive':

        print('Specify file size:')
        size = int(input())
        data = process_receive(
            size,
            HOST, 
            PORT,
            1
        )

        print(f'Data recieved: {len(data)}')
        open(
            client_receive,
            'wt',
            encoding='utf-8'
        ).write(data)
        break

    print("Wrong input! Try again!")