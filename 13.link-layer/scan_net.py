import scapy.all as scapy
import socket

def search_ip (users):
    for num, user in enumerate(users):
        if num == 0:
            print("OTHER:")
        print(f'{"":25}{user["ip"]:25}{user["mac"]:25}{user["name"]}')

print(f'{"":25}{"IP":25}{"MAC":25}{"NAME"}')

list_ip = socket.gethostbyname_ex(socket.gethostname())[-1]

def get_packet(ip):
    return scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst = ip + '/24')

for ip in list_ip:

    req = scapy.srp(get_packet(ip), timeout=3, verbose=0)
    if len(req) == 0:
        continue
    res_req = req[0]
    if len(res_req) == 0:
        continue

    users = []
    for non, data in res_req:
        try:
            name = socket.gethostbyaddr(data.psrc)[0]
        except socket.herror:
            name = ''

        if data.psrc == ip:
            print("YOUR:")
            print(f'{"":25}{ip:25}{data.hwsrc:25}{name}')
        else:
            users.append({
                'ip': data.psrc,
                'mac': data.hwsrc,
                'name': name
            })
    
    search_ip(users)