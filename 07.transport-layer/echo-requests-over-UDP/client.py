import socket
from datetime import datetime

get_p = 0
lost_p = 0
max_rtt = 0
min_rtt = 10**10
sum_rtt = 0

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
    socket.IPPROTO_UDP
)
client.settimeout(1.0)

for num in range(10):
    send_time = datetime.now()
    print('Ping #' + str(num + 1) + ',  ' + send_time.strftime('%H:%M:%S.%f'))
    message = 'abacaba'
    client.sendto(message.encode('ascii'), ('127.0.0.1', 1234))

    try:
        message, _ = client.recvfrom(1024)
        get_time = datetime.now()
        print(message.decode('ascii'))
        get_p += 1
        max_rtt = max((get_time - send_time).microseconds, max_rtt)
        min_rtt = min((get_time - send_time).microseconds, min_rtt)
        sum_rtt += (get_time - send_time).microseconds
        print('Maximum =', max_rtt, end=', ')
        print('Minimum =', min_rtt, end=', ')
        print('Average =', sum_rtt // (get_p + lost_p))
        print('Lost:', int(lost_p / (get_p + lost_p) * 100), end='%\n\n')


    except socket.timeout:
        print('Request timed out', end='\n\n')
        lost_p += 1