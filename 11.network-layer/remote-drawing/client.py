import socket

from tkinter import Tk, Canvas

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
client.connect(('localhost', 8765))

root = Tk()
canvas = Canvas(
    root,
    width = 600,
    height = 800,
    bg='white'
)

def drawing(event):
    canvas.create_oval(
        event.x,
        event.y,
        event.x + 1,
        event.y + 1,
        fill='black'
    )
    client.send(f'{event.x} {event.y}'.encode('ascii'))


canvas.bind('<B1-Motion>', drawing)
canvas.pack()
root.mainloop()

