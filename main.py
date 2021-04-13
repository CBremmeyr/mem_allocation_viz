#!/usr/bin/python

# Note: the algorothims were inspired by the geeksforgeeks.com python code

import time
import numpy as np
import tkinter as tk
from tkinter import ttk

class proccessClass:
    def __init__(self, p_PID, p_size, p_time):
        self.PID  = p_PID
        self.size = p_size
        self.TTL  = p_time
        self.alloc= -1
#Removes a TTL from a running proccess and reallocs the space if process is complete
def runProccess(blockSize, plist):
    for obj in plist:
        if obj.alloc > -1:
            obj.TTL -= 1
            if obj.TTL == 0:
                blockSize[obj.alloc] += obj.size
                obj.alloc = -1

# blocks as per First fit algorithm
def firstFit(blockSize, m, proc):

    # Initially no block is assigned to any process

    # pick each process and find suitable blocks
    # according to its size ad assign to it
    for j in range(m):
        if blockSize[j] >= proc.size:

            # allocate block j to p[i] process
            proc.alloc = j

            # Reduce available memory in this block.
            blockSize[j] -= proc.size

            break

    if proc.alloc != -1:
        return 0
    else:
        return -1

def bestFit(blockSize, m, proc):
      
    # Find the best fit block for
    # current process 
    bestIdx = -1
    for j in range(m):
        if blockSize[j] >= proc.size:
            if bestIdx == -1: 
                bestIdx = j 
            elif blockSize[bestIdx] > blockSize[j]: 
                bestIdx = j
  
    # If we could find a block for 
    # current process 
    if bestIdx != -1:
              
        # allocate block j to p[i] process 
        proc.alloc = bestIdx 
  
        # Reduce available memory in this block. 
        blockSize[bestIdx] -= proc.size
  
    if proc.alloc != -1: 
        return 0
    else:
        return -1

def worstFit(blockSize, m, proc):
      
          
    # Find the best fit block for 
    # current process 
    wstIdx = -1
    for j in range(m):
        if blockSize[j] >= proc.size:
            if wstIdx == -1: 
                wstIdx = j 
            elif blockSize[wstIdx] < blockSize[j]: 
                wstIdx = j
  
    # If we could find a block for 
    # current process 
    if wstIdx != -1:
              
        # allocate block j to p[i] process 
        proc.alloc = wstIdx 
  
        # Reduce available memory in this block. 
        blockSize[wstIdx] -= proc.size
    
    if proc.alloc != -1: 
        return 0
    else:
        return -1

def draw_box(canvas, proc, x_offset, y):
    size = proc.size
    id = proc.PID
    y_offset = 100
    bar_width = 100
    box = canvas.create_rectangle(
                x_offset,
                y + y_offset,
                x_offset + bar_width,
                y + y_offset + size,
                fill="white",
                width=5
            )
    label = tk.Label(root,
                text= "Proc " + str(id) + "\nSize " + str(size),
                font=("TkDefaultFont","5")
            )
    label.place(x = x_offset+200, y = y + y_offset)
    return (box, label)

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
canvas = tk.Canvas(root, width=500, height=500, bd=0)
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
blockSize = [25,50,25,100,25,50,25,200]

#create the process list
plist = []
for i in range(3):
    plist.append(proccessClass(i+1,np.random.randint(50,151), np.random.randint(1,11)))
print("Initially create list")
print("---------------------")
for obj in plist:
    print(obj.PID, obj.size, obj.TTL)


draw_list = []
count = 0

#initialize all three sims
plist_ff = plist.copy()
blocks_ff = blockSize.copy()
currProc_ff = 0

plist_bf = plist.copy()
blocks_bf = blockSize.copy()
currProc_bf = 0

plist_wf = plist.copy()
blocks_wf = blockSize.copy()
currProc_wf = 0

while 1:

    if quit_flag == 1:
        quit(0)

    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

    if start_flag == 1 and currProc_ff < len(plist) and currProc_bf < len(plist) and currProc_wf < len(plist):

        ########################################

        #--------------------------First Fit-----------------------------
        print_ff = 0

        runProccess(blocks_ff, plist_ff)
        if print_ff == 1:
            print("\nFirst Fit Block List")
            print("Before: ", end = "")
            print(blocks_ff);
        
        ret = firstFit(blocks_ff, len(blocks_ff), plist_ff[currProc_ff])
        if print_ff == 1:
            print(" Process No.\tProcess Size\tBlock no.")
            print(" ",plist_ff[currProc_ff].PID, "\t\t", plist_ff[currProc_ff].size, "\t\t", end = " ")
            if plist_ff[currProc_ff].alloc != -1:
                print(plist_ff[currProc_ff].alloc + 1)
            else:
                print("Not Allocated")
            print("After : ", end = "")
            print(blocks_ff)
        
        if ret == 0:
            currProc_ff += 1

        #--------------------------Best Fit-----------------------------
        print_bf = 0;

        runProccess(blocks_bf, plist_bf)
        if print_bf == 1:
            print("\nBest Fit Block List")
            print("Before: ", end = "")
            print(blocks_bf);
        
        ret = bestFit(blocks_bf, len(blocks_bf), plist_bf[currProc_bf])
        if print_bf == 1:
            print(" Process No.\tProcess Size\tBlock no.")
            print(" ",plist_bf[currProc_bf].PID, "\t\t", plist_bf[currProc_bf].size, "\t\t", end = " ")
            if plist_bf[currProc_rf].alloc != -1:
                print(plist_bf[currProc_bf].alloc + 1)
            else:
                print("Not Allocated")
            print("After : ", end = "")
            print(blocks_bf)

        if ret == 0:
            currProc_bf += 1

        #--------------------------Worst Fit-----------------------------
        print_wf = 0;
        
        runProccess(blocks_wf, plist_wf)
        if print_wf == 1:
            print("\nWorst Fit Block List")
            print("Before: ", end = "")
            print(blocks_wf);
        
        ret = worstFit(blocks_wf, len(blocks_wf), plist_bf[currProc_wf])
        if print_wf == 1:
            print(" Process No.\tProcess Size\tBlock no.")
            print(" ",plist_wf[currProc_wf].PID, "\t\t", plist_wf[currProc_wf].size, "\t\t", end = " ")
            if plist_wf[currProc_wf].alloc != -1:
                print(plist_wf[currProc_wf].alloc + 1)
            else:
                print("Not Allocated")
            print("After : ", end = "")
            print(blocks_wf)

        if ret == 0:
            currProc_wf += 1

        ########################################

        # Bar location values
        first_x  = 0
        best_x   = 200
        worst_x  = 400
        y_offset = 100

        # Delete drawn stuff
        for i in draw_list:
            canvas.delete(i[0])
            i[1].destroy()

        # Display current memory allocation
        for i in plist:
            offset = 0
            for j in range(i.alloc-1):
                offset += blockSize[j]
            draw_list.append(draw_box(canvas, i, first_x, offset))


        # Increment time
        count = count + 1
        root.update()
        time.sleep(1)

