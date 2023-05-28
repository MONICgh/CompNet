import tkinter
import socket
from random import randbytes
from datetime import datetime

MODE = 'UDP' # or 'UDP'
IP = '127.0.0.1'
PORT = 9876
ADDRESS = (IP, PORT)

def button_pressed():
    button_send['text'] = 'Sending...'
    root.after(1, send_time)

def client_started(address=ADDRESS, timeout=None):
    if MODE == 'UDP':
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
            )
    else:
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
            )
        client.connect(address)
    client.settimeout(timeout)
    return client

def packege_get(num, sz):
    packs = []
    for i in range(1, num + 1):
        ref = '#'
        package = ref + str(num) + ref + str(i) + ref
        package = package.encode('ascii')
        rand_size = sz - len(package) - 26
        if rand_size < 0:
            raise Exception('')
        package += randbytes(rand_size)
        packs.append(package)
    return packs

def send_time():

    def timing(servcon, address, num, size=1024):
        packages = packege_get(num, size)
        time_prefix = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').encode('ascii')
        
        def help(servcon, message, address):
            if MODE == 'UDP':
                servcon.sendto(message, address)
            else:
                servcon.send(message)

        for package in packages:
            help(servcon, time_prefix + package, address)

    address = (in_ip.get(), int(in_port.get()))
    num = int(in_count_paskeg.get())
    client = client_started(address)
    timing(client, address, num)
    button_send['text'] = 'Send'


root = tkinter.Tk()
if MODE == 'UDP':
    root.title = 'UDP'
else:
    root.title = 'TCP'

tkinter.Label(text='IP:').grid(row=0, column=0, sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='PORT:').grid(row=1, column=0, sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='Number of packets:').grid(row=2, column=0, sticky=tkinter.W, pady=5, padx=5)

in_ip = tkinter.Entry()
in_ip.insert(0, IP)
in_ip.grid(row=0, column=1, padx=5)

in_port = tkinter.Entry()
in_port.insert(0, str(PORT))
in_port.grid(row=1, column=1)

in_count_paskeg = tkinter.Entry()
in_count_paskeg.insert(0, str(5))
in_count_paskeg.grid(row=2, column=1)

button_send = tkinter.Button(text='Send', command=button_pressed, activebackground = "green")
button_send.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

root.mainloop()