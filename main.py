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
canvas.place(x=200, y=0)

# Add blocks to canvas
first_bar_bg = canvas.create_rectangle(  0, 100, 100, 600, fill='red')
best_bar_bg  = canvas.create_rectangle(200, 100, 300, 600, fill='red')
worst_bar_bg = canvas.create_rectangle(400, 100, 500, 600, fill='red')

# DEBUG: test drawing over other parts of the canvas
test_box = canvas.create_rectangle(0, 100, 200, 50, fill='black')

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

# Read in process sequence from file
file = open("process_seq.txt", 'r')
#print(file.readline())
str_seq = file.readline().split()
#print(str_seq)
proc_seq = [0] * len(str_seq)
for i in range(len(str_seq)):
    proc_seq[i] = int(str_seq[i])
print(proc_seq)

#create memory blocks
blockSize = [5,10,15,20]

#create the process list
plist = []
for i in range(20):
    plist.append(proccessClass(i+1,np.random.randint(1,1001), np.random.randint(1,10)))
print("Initially create list")
print("---------------------")
for obj in plist:
    print(obj.pID, obj.size, obj.time)


count = 0
while 1:
    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

    if start_flag == 1 and count < len(plist):

        ########################################
        # Do back end stuff here

        firstFit(blockSize, len(blockSize), plist[0].size, 1)


        ########################################

        # Remove finished processes

        # Add new process

        # Update next process size for each catagory

        # Increment time
        count = count + 1
        time.sleep(1)

