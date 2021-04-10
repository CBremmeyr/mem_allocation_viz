#!/usr/bin/python

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("900x800")
root.title("Dynamic Memory Allocation");

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()
a = canvas.create_rectangle(0, 0, 100, 600, fill='red')
b = canvas.create_rectangle(200, 0, 300, 600, fill='red')
c = canvas.create_rectangle(400, 0, 500, 600, fill='red')

#first_text = tk.Text(root, padx=200)
#first_text.insert(tk.INSERT, "First")
#first_text.pack()

#best_text = tk.Text(root, padx=400)
#best_text.insert(tk.INSERT, "Best")
#best_text.pack()

worst_label = tk.Label(root, text="Worst")
worst_label.place(relx=0.68, rely=0.63)

#worst_text = tk.Text(root, height=1, width=5)
#worst_text.insert(tk.INSERT, "Worst")
#worst_text.place(x=400, y=600)
#worst_text.pack()

root.mainloop()

