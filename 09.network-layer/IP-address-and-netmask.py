import psutil

name, address, port = None, None, None
for _name, data in psutil.net_if_addrs().items():
    for item in data:
        if item.address.startswith("192"):
            name, address, port = _name, item.address, item.netmask

if port is None:
    exit(1)

print(f"Address: {address}\nPort: {port}\nName {name}")