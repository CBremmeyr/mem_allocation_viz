#!/usr/bin/python

#import tkinter
#top = tkinter.Tk()
#top.mainloop()

from tkinter import *
root = Tk()
root.geometry("900x800")
canvas = Canvas(root, width=500, height=600)
canvas.pack()
a = canvas.create_rectangle(0, 0, 100, 600, fill='red')
b = canvas.create_rectangle(200, 0, 300, 600, fill='red')
c = canvas.create_rectangle(400, 0, 500, 600, fill='red')
#canvas.move(a, 20, 20)

root.mainloop()
