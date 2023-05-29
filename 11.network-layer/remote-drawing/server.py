import socket

from threading import Thread
from tkinter import Tk, Canvas
from queue import Queue, Empty


def server_listning():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    server.bind(('localhost', 8765))
    server.listen()

    con, _ = server.accept()
    while True:
        res = con.recv(1024).decode('ascii').split(' ')
        if len(res) < 2:
            return
        queue.put((
            int(res[0]),
            int(res[1])
        ))


queue = Queue(0)
thread_ = Thread(target = server_listning)
thread_.start()

root = Tk()
canvas = Canvas(
    root,
    width = 600,
    height = 800,
    bg = 'pink'
)
canvas.pack()

def drawing():
    try:
        coords = queue.get_nowait()
        x, y = coords
        canvas.create_oval(
            x,
            y,
            x + 1,
            y + 1,
            fill='black'
        )
    except Empty:
        pass
    root.after(1, drawing)

root.after(1, drawing)
root.mainloop()