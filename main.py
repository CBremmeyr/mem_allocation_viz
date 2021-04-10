#!/usr/bin/python

import time
import numpy as np
import tkinter as tk
from tkinter import ttk

# Function to allocate memory to
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

    print(" Process No. Process Size      Block no.")
    for i in range(n):
        print(" ", i + 1, "         ", processSize[i],
                          "         ", end = " ")
        if allocation[i] != -1:
            print(allocation[i] + 1)
        else:
            print("Not Allocated")

def start_CB(*proccess):
    global start_flag
    start_flag = 1

#    processSize = np.random.randint(1,10001, 20)
#    blockSize =  np.random.radnint(1,10001, 20)

#    firstFit(blockSize, len(blockSize), processSize, len(processSize))

def exit_CB():
    root.destroy()

global start_flag
start_flag = 0

# Make window for GUI
root = tk.Tk()
root.geometry("900x800")
root.title("Dynamic Memory Allocation");

# Make canvas to draw blocks on
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Add blocks to canvas
first_bar_bg = canvas.create_rectangle(  0, 0, 100, 600, fill='red')
best_bar_bg  = canvas.create_rectangle(200, 0, 300, 600, fill='red')
worst_bar_bg = canvas.create_rectangle(400, 0, 500, 600, fill='red')

# DEBUG: test drawing over other parts of the canvas
test_box = canvas.create_rectangle(0, 0, 100, 50, fill='black')

first_label = tk.Label(root, text="First\nNext: ")
best_label  = tk.Label(root, text="Best\nNext: ")
worst_label = tk.Label(root, text="Worst\nNext: ")
time_label  = tk.Label(root, text="Time: ")

first_label.place(relx=0.22, rely=0.63)
best_label.place( relx=0.44, rely=0.63)
worst_label.place(relx=0.66, rely=0.63)
time_label.place( relx=0.50, rely=0.90)

btnTop = 400
btnLeft = 20
btnSpace = 50

startBtn = tk.Button(root, text="Start", command=start_CB)
startBtn.place(x=btnLeft, y=btnTop)

stopBtn = tk.Button(root, text="Exit", command=exit_CB)
stopBtn.place(x=btnLeft, y=btnTop+btnSpace)

# Read in process sequence from file
file = open("process_seq.txt", 'r')
#print(file.readline())
str_seq = file.readline().split()
#print(str_seq)
proc_seq = [0] * len(str_seq)
for i in range(len(str_seq)):
    proc_seq[i] = int(str_seq[i])
print(proc_seq)

count = 0
while 1:
    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

    if start_flag == 1:

        ########################################
        # Do back end stuff here





        ########################################

        # Remove finished processes

        # Add new process

        # Update next process size for each catagory

        # Increment time
        count = count + 1
        time.sleep(1)

