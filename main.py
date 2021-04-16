#!/usr/bin/python

# Note: the algorothims were inspired by the geeksforgeeks.com python code

import time
import csv
import tkinter as tk
from tkinter import ttk

MEM_SIZE = 500

class proccessClass:
    def __init__(self, p_PID, p_size, p_time):
        self.PID   = p_PID
        self.size  = p_size
        self.TTL   = p_time
        self.alloc = -1
        self.box   = None

class memBlockClass:
    def __init__(self, p_allocFlag, p_size):
        self.allocFlag = p_allocFlag
        self.size      = p_size

# Update memBlocks array after a process is alloced
def allocMemBlocks(a_memBlocks, blockIndex, proc, a_plist):

    # Split alloced block into alloced and free segments
    allocSize = proc.size
    freeSize  = a_memBlocks[blockIndex].size - proc.size

    a_memBlocks[blockIndex].allocFlag = True
    a_memBlocks[blockIndex].size = allocSize

    if freeSize != 0:
        insertIndex = blockIndex + 1
        temp = memBlockClass(False, freeSize)
        a_memBlocks.insert(insertIndex, temp)
        for i in a_plist:
            if i.alloc >= blockIndex+1:
                i.alloc += 1;

# Update memBlocks array after a process is freed
def freeMemBlocks(canvas, f_memBlocks, proc, f_plist):

    # Remove block from canvas
    canvas.delete(proc.box)

    blockIndex = proc.alloc # Index of block being freed

    proc.alloc = -1     # Mark proc as free
    f_memBlocks[blockIndex].allocFlag = False     # Mark block as free

    # Determine if adjacent blocks should be merged
    leftIndex = blockIndex - 1
    mergeLeft = not f_memBlocks[leftIndex].allocFlag if leftIndex >= 0 else False

    rightIndex = blockIndex + 1
    mergeRight = not f_memBlocks[rightIndex].allocFlag if rightIndex < len(f_memBlocks) else False

    # Merge adjacent blocks
    if mergeRight:
        f_memBlocks[blockIndex].size += f_memBlocks[rightIndex].size
        f_memBlocks.pop(rightIndex)

        for i in f_plist:
            if i.alloc > rightIndex:
                i.alloc -= 1

    if mergeLeft:
        f_memBlocks[leftIndex].size += f_memBlocks[blockIndex].size
        f_memBlocks.pop(blockIndex)

        for i in f_plist:
            if i.alloc > blockIndex:
                i.alloc -= 1;

# Removes a TTL from a running proccess and reallocs the space if process is complete
def runProccess(canvas, r_memBlocks, r_plist):
    for obj in r_plist:
        if obj.alloc != -1:
            obj.TTL -= 1
            if obj.TTL <= 0:
                freeMemBlocks(canvas, r_memBlocks, obj, r_plist)

# blocks as per First fit algorithm
def firstFit(ff_memBlocks, m, proc, ff_plist):

    # Initially no block is assigned to any process

    # pick each process and find suitable blocks
    # according to its size ad assign to it
    for j in range(m):
        if ff_memBlocks[j].size >= proc.size and not ff_memBlocks[j].allocFlag:

            # allocate block j to p[i] process
            proc.alloc = j

            # Update memory allocation state
            allocMemBlocks(ff_memBlocks, j, proc, ff_plist)

            break

    if proc.alloc != -1:
        return 0
    else:
        return -1

def bestFit(bf_memBlocks, m, proc, bf_plist):

    # Find the best fit block for current process
    bestIdx = -1
    for j in range(m):
        if bf_memBlocks[j].size >= proc.size and not bf_memBlocks[j].allocFlag:
            if bestIdx == -1:
                bestIdx = j
            elif bf_memBlocks[bestIdx].size > bf_memBlocks[j].size:
                bestIdx = j

    # If we could find a block for current process
    if bestIdx != -1:

        # allocate block j to p[i] process
        proc.alloc = bestIdx

        # Update memory allocation state
        allocMemBlocks(bf_memBlocks, bestIdx, proc, bf_plist)

    if proc.alloc != -1:
        return 0
    else:
        return -1

def worstFit(wf_memBlocks, m, proc, wf_plist):

    # Find the worst fit block for current process
    wstIdx = -1
#    for j in range(m):
    for j in range(len(wf_memBlocks)):
        if wf_memBlocks[j].size >= proc.size and not wf_memBlocks[j].allocFlag:
            if wstIdx == -1:
                wstIdx = j
            elif wf_memBlocks[wstIdx].size < wf_memBlocks[j].size:
                wstIdx = j

    # If we could find a block for current process
    if wstIdx != -1:

        # allocate block j to p[i] process
        proc.alloc = wstIdx

        # Update memory allocation state
        allocMemBlocks(wf_memBlocks, wstIdx, proc, wf_plist)

    if proc.alloc != -1:
        return 0
    else:
        return -1

def start_CB(*proccess):
    global start_flag
    start_flag = 1

def exit_CB():
    root.destroy()

global start_flag
start_flag = 0

# Make window for GUI
root = tk.Tk()
root.geometry("900x800")
root.title("Dynamic Memory Allocation");

# Make canvas to draw blocks on
canvasOffset = 200
canvas = tk.Canvas(root, width=500, height=700, bd=0)
canvas.place(x=canvasOffset, y=0)

# Add blocks to canvas
barSpace  = 200
barTop    = 100
barWidth  = 75
barHeight = MEM_SIZE + barTop
bar1_x = 0
bar2_x = bar1_x + barSpace
bar3_x = bar2_x + barSpace

first_bar_bg = canvas.create_rectangle(bar1_x, barTop,
        bar1_x + barWidth, barHeight, fill='red')
best_bar_bg  = canvas.create_rectangle(bar2_x, barTop,
        bar2_x + barWidth, barHeight, fill='red')
worst_bar_bg = canvas.create_rectangle(bar3_x, barTop,
        bar3_x + barWidth, barHeight, fill='red')

first_label = tk.Label(root, text="First\n  Next: ")
best_label  = tk.Label(root, text="Best\n  Next: ")
worst_label = tk.Label(root, text="  Worst\n  Next: ")
time_label  = tk.Label(root, text="Time: ")

first_label.place(x=bar1_x + canvasOffset + 5, y=barHeight + 10)
best_label.place( x=bar2_x + canvasOffset + 5, y=barHeight + 10)
worst_label.place(x=bar3_x + canvasOffset + 5, y=barHeight + 10)


# Add remaining Elements to root
time_label.place( x=400, y=700)

btnTop   = 400
btnLeft  = 20
btnSpace = 50

startBtn = tk.Button(root, text="Start", command=start_CB)
startBtn.place(x=btnLeft, y=btnTop)

stopBtn = tk.Button(root, text="Exit", command=exit_CB)
stopBtn.place(x=btnLeft, y=btnTop+btnSpace)

#------------------ GUI FUNCTIONS ----------------------#
def drawBox(canvas, barType, d_memBlocks, proc):

    if(barType == 1):
        pBox_x = bar1_x
    if(barType == 2):
        pBox_x = bar2_x
    if(barType == 3):
        pBox_x = bar3_x

    pBox_y = 0

    for i in range(proc.alloc):
        pBox_y += d_memBlocks[i].size
    pBox_size = proc.size
    offSet = barTop + pBox_y
    proc.box = canvas.create_rectangle(pBox_x, offSet, pBox_x + barWidth,
            pBox_size + offSet, fill = 'blue')

# Make background rectangles for memory spaces
canvas.create_rectangle(bar1_x, barTop, bar1_x + barWidth, 1+barTop, fill = 'black')
canvas.create_rectangle(bar2_x, barTop, bar2_x + barWidth, 1+barTop, fill = 'black')
canvas.create_rectangle(bar3_x, barTop, bar3_x + barWidth, 1+barTop, fill = 'black')

# Load process sequence from csv file
plist_ff = []
plist_bf = []
plist_wf = []
csvFile = open("proc_seq.csv")
csvReader = csv.reader(csvFile, )
for row in csvReader:
    if row[0][0] == '#':
        continue

    pid  = int(row[0])
    size = int(row[1])
    ttl  = int(row[2])

    plist_ff.append(proccessClass(pid, size, ttl))
    plist_bf.append(proccessClass(pid, size, ttl))
    plist_wf.append(proccessClass(pid, size, ttl))

print("Initially create list")
print("---------------------")
for obj in plist_ff:
    print(obj.PID, obj.size, obj.TTL)


count = 0

# Initialize all three sims
blocks_ff = []
blocks_ff.append(memBlockClass(False, MEM_SIZE))
currProc_ff = 0

blocks_bf = []
blocks_bf.append(memBlockClass(False, MEM_SIZE))
currProc_bf = 0

blocks_wf = []
blocks_wf.append(memBlockClass(False, MEM_SIZE))
currProc_wf = 0

while 1:

    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

    # Wait for start button to be pressed to start sim
    if start_flag == 1:

        ########################################

        #--------------------------First Fit-----------------------------
        nextProc_ff = currProc_ff + 1
        if nextProc_ff < len(plist_ff):
            try:
                first_label.config(text="First\n  Next: "+str(plist_ff[nextProc_ff].size))
            except:
                quit(0)
        else:
            try:
                first_label.config(text="First\n  Next: ")
            except:
                quit(0)

        runProccess(canvas, blocks_ff, plist_ff)

        if currProc_ff < len(plist_ff):
            ret_ff = firstFit(blocks_ff, len(blocks_ff), plist_ff[currProc_ff], plist_ff)
            if ret_ff == 0:
                drawBox(canvas, 1, blocks_ff, plist_ff[currProc_ff])
                currProc_ff += 1

        #--------------------------Best Fit-----------------------------
        nextProc_bf = currProc_bf + 1
        if nextProc_bf < len(plist_bf):
            try:
                best_label.config(text="Best\n  Next: "+str(plist_bf[nextProc_bf].size))
            except:
                quit(0)
        else:
            try:
                best_label.config(text="Best\n  Next: ")
            except:
                quit(0)

        runProccess(canvas, blocks_bf, plist_bf)

        if currProc_bf < len(plist_bf):
            ret_bf = bestFit(blocks_bf, len(blocks_bf), plist_bf[currProc_bf], plist_bf)
            if ret_bf == 0:
                drawBox(canvas, 2, blocks_bf, plist_bf[currProc_bf])
                currProc_bf += 1

        #--------------------------Worst Fit-----------------------------
        nextProc_wf = currProc_wf + 1
        if nextProc_wf < len(plist_wf):
            try:
                worst_label.config(text="  Worst\n  Next: "+str(plist_wf[nextProc_wf].size))
            except:
                quit(0)
        else:
            try:
                worst_label.config(text="  Worst\n  Next: ")
            except:
                quit(0)

        runProccess(canvas, blocks_wf, plist_wf)
        if currProc_wf < len(plist_wf):
            ret_wf = worstFit(blocks_wf, len(blocks_wf), plist_wf[currProc_wf], plist_wf)
            if ret_wf == 0:
                drawBox(canvas, 3, blocks_wf, plist_wf[currProc_wf])
                currProc_wf += 1

        ########################################

        # Increment time
        count = count + 1
        try:
            root.update()
        except:
            quit(0)

        time.sleep(1)

