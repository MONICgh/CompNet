import tkinter
import socket
from math import inf
from datetime import datetime

MODE = 'UDP' # or 'TCP'
MIL = 10**6

IP = '127.0.0.1'
PORT = 9876
ADDRESS = (IP, PORT)
BATCH_SIZE = 1024

def button_pressed():
    recv_button['text'] = 'Receipt...'
    root.after(1, recv)

def packeges_parsing(pack):
    time_prefix, num, curr_batch, *_ = pack.split(b'#')
    return datetime.strptime(
        time_prefix.decode('ascii'),
        '%Y-%m-%d %H:%M:%S.%f'
        ), int(
        num.decode('ascii')
        ), int(
        curr_batch.decode('ascii')
        )


def use_recv(servcon):
    if MODE == 'UDP':
        return servcon.recvfrom(BATCH_SIZE)
    else:
        return servcon.recv(BATCH_SIZE), None


def start_server(_bind=ADDRESS):
    if MODE == 'UDP':
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(_bind)
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(_bind)
    return server

def conn(server):
    if MODE == 'UDP':
        return server
    else:
        server.listen()
        connection, _ = server.accept()
        return connection

def recv():
    ip = ip_entry.get()
    port = int(port_entry.get())
    address = (ip, port)

    server = start_server(address)
    servcon = conn(server)

    _set = set()
    num = inf
    send = None
    last = None
    started = False

    try:
        while len(_set) < num:
            send, num, curr_batch = packeges_parsing(use_recv(servcon)[0])
            last = datetime.now()
            _set.add(curr_batch)
            if not started:
                servcon.settimeout(3)
                started = True
    except socket.timeout:
        pass

    delta = last - send
    delta = MIL * delta.seconds + delta.microseconds
    speed = BATCH_SIZE * len(_set) / delta

    pack_label['text'] = f'{len(_set)} / {num}'
    time_label['text'] = f'{delta / MIL} c'
    speed_label['text'] = '%.6f МБ/c' % speed

    recv_button['text'] = 'Receipt'


root = tkinter.Tk()
if MODE == 'UDP':
    root.title = 'UDP'
else:
    root.title = 'TCP'


tkinter.Label(text='IP:').grid(sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='PORT:').grid(row=1, column=0, sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='Number of packets received:').grid(row=2, column=0, sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='Time:').grid(row=3, column=0, sticky=tkinter.W, pady=5, padx=5)
tkinter.Label(text='Speed:').grid(row=4, column=0, sticky=tkinter.W, pady=5, padx=5)

ip_entry = tkinter.Entry()
ip_entry.insert(0, IP)
ip_entry.grid(row=0, column=1, padx=5)

port_entry = tkinter.Entry()
port_entry.insert(0, str(PORT))
port_entry.grid(row=1, column=1)

pack_label = tkinter.Label(text='-')
time_label = tkinter.Label(text='-')
speed_label = tkinter.Label(text='-')
recv_button = tkinter.Button(text='Get', command=button_pressed, activebackground = "green")

pack_label.grid(row=2, column=1, sticky=tkinter.W, padx=5)
time_label.grid(row=3, column=1, sticky=tkinter.W, padx=5)
speed_label.grid(row=4, column=1, sticky=tkinter.W, padx=5)
recv_button.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

root.mainloop()