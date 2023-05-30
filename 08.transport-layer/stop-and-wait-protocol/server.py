from common_part import *
from checksums_main import *


print("Choose command: send/receive")
create()
    
while True:

    command = input()

    if command == 'send':
        process_send(
            open(
                server_send,
                'rt',
                encoding='utf-8'
            ).read(),
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
            server_receive,
            'wt',
            encoding='utf-8'
        ).write(data)
        break
    
    print("Wrong input! Try again!")