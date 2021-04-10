#!/usr/bin/python

import time
import numpy as np
import tkinter as tk
from tkinter import ttk

class proccessClass:
    def __init__(self, p_pID, p_size, p_time):
        self.pID  = p_pID
        self.size = p_size
        self.time = p_time

# blocks as per First fit algorithm
# This function was created by geeksforgeeks
#       https://www.geeksforgeeks.org/program-first-fit-algorithm-memory-management
def firstFit(blockSize, m, processSize, n):

    # Stores block id of the
    # block allocated to a process
    allocation = [-1] * n

    # Initially no block is assigned to any process

    # pick each process and find suitable blocks
    # according to its size ad assign to it
    for i in range(n):
        for j in range(m):
            if blockSize[j] >= processSize[i]:

                # allocate block j to p[i] process
                allocation[i] = j

                # Reduce available memory in this block.
                blockSize[j] -= processSize[i]

                break

    print(" Process No.\tProcess Size\tBlock no.")
    for i in range(n):
        print(" ", i + 1, "\t\t", processSize[i],
                          "\t\t", end = " ")
        if allocation[i] != -1:
            print(allocation[i] + 1)
        else:
            print("Not Allocated")

def draw_box(canvas, proc, x_offset, y):
    size = proc.size
    id = proc.pid
    y_offset = 100
    bar_width = 100
    box = canvas.create_rectangle(
                x_offset,
                y + y_offset,
                x_offset + bar_width,
                y + y_offset + size,
                fill="black"
            )
    label = tk.Label(root,
                text= "Proc " + id + "\nSize " + size
            )
    label.place(x = x_offset, y = y + y_offset)

def start_CB(*proccess):
    global start_flag
    start_flag = 1

#    processSize = np.random.randint(1,10001, 20)
#    blockSize =  np.random.radnint(1,10001, 20)

#    firstFit(blockSize, len(blockSize), processSize, len(processSize))

def exit_CB():
    root.destroy()
    global quit_flag
    quit_flag = 1

global start_flag
start_flag = 0

global quit_flag
quit_flag = 0

# Make window for GUI
root = tk.Tk()
root.geometry("900x800")
root.title("Dynamic Memory Allocation");

# Make canvas to draw blocks on
canvas = tk.Canvas(root, width=500, height=500)
canvas.place(x=200, y=0)

# Add blocks to canvas
first_bar_bg = canvas.create_rectangle(  0, 100, 100, 600, fill='red')
best_bar_bg  = canvas.create_rectangle(200, 100, 300, 600, fill='red')
worst_bar_bg = canvas.create_rectangle(400, 100, 500, 600, fill='red')

first_label = tk.Label(root, text="First\n  Next: ")
best_label  = tk.Label(root, text="Best\n  Next: ")
worst_label = tk.Label(root, text="  Worst\n  Next: ")
time_label  = tk.Label(root, text="Time: ")

first_label.place(x=200, y=500)
best_label.place(x=400, y=500)
worst_label.place(x=600, y=500)
time_label.place(x=400, y=600)
#time_label.place( relx=0.50, rely=0.90)

btnTop = 400
btnLeft = 20
btnSpace = 50

startBtn = tk.Button(root, text="Start", command=start_CB)
startBtn.place(x=btnLeft, y=btnTop)

stopBtn = tk.Button(root, text="Exit", command=exit_CB)
stopBtn.place(x=btnLeft, y=btnTop+btnSpace)

#create memory blocks
blockSize = [25,25,25,25,50,50,100,200]

#create the process list
plist = []
for i in range(20):
    plist.append(proccessClass(i+1,np.random.randint(1,201), np.random.randint(1,11)))
print("Initially create list")
print("---------------------")
for obj in plist:
    print(obj.pID, obj.size, obj.time)


count = 0
while 1:

    if quit_flag == 1:
        quit(0)

    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

    if start_flag == 1 and count < len(plist):

        ########################################
        # Do back end stuff here

#        firstFit(blockSize, len(blockSize), plist[0].size, 1)


        ########################################

        # Bar location values
        first_x  = 0
        best_x   = 200
        worst_x  = 400
        y_offset = 100

        # Display current memory allocation
#        for i in first_plist:
#            draw_box(canvas, first_x, y, i.size)

        if count == 1:
            draw_box(canvas, first_x, 100, 150)
        if count == 2:
            draw_box(canvas, best_x, 100, 100)
        if count == 3:
            draw_box(canvas, worst_x, 250, 50)

        # Increment time
        count = count + 1
        time.sleep(1)

