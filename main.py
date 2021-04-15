#!/usr/bin/python

# Note: the algorothims were inspired by the geeksforgeeks.com python code

import time
import numpy as np
import tkinter as tk
from tkinter import ttk

MEM_SIZE = 500

class proccessClass:
    def __init__(self, p_PID, p_size, p_time):
        self.PID  = p_PID
        self.size = p_size
        self.TTL  = p_time
        self.alloc= -1

class memBlockClass:
    def __init__(self, p_allocFlag, p_size):
        self.allocFlag = p_allocFlag
        self.size = p_size

# Update memBlocks array after a process is alloced
def allocMemBlocks(memBlocks, blockIndex, proc, plist):

    # Split alloced block into alloced and free segments
    allocSize = proc.size
    freeSize  = memBlocks[blockIndex].size - proc.size

    memBlocks[blockIndex].allocFlag = True
    memBlocks[blockIndex].size = allocSize

    if freeSize != 0:
        insertIndex = blockIndex + 1
        temp = memBlockClass(False, freeSize)
        memBlocks.insert(insertIndex, temp)
        for i in plist:
            if i.alloc >= blockIndex+1:
                i.alloc += 1;

# Update memBlocks array after a process is freed
def freeMemBlocks(canvas, memBlocks, proc, plist):

    # Remove block from canvas
    canvas.delete(memBlocks[proc.alloc].box)

    #DEBUG
#    print("freeMemBlocks()")
#    print("index: " + str(proc.alloc))
#    print("before:")
#    print("(allocFlag, size)")
#    for i in range(len(memBlocks)):
#        print("[", end="")
#        print(str(memBlocks[i].allocFlag) + ", " + str(memBlocks[i].size) + "]")

    blockIndex = proc.alloc                 # Index of block being freed

    proc.alloc = -1     # Mark proc as free
    memBlocks[blockIndex].allocFlag = False     # Mark block as free

    # Determine if adjacent blocks should be merged
    leftIndex = blockIndex - 1
    mergeLeft = not memBlocks[leftIndex].allocFlag if leftIndex >= 0 else False

    rightIndex = blockIndex + 1
    mergeRight = not memBlocks[rightIndex].allocFlag if rightIndex < len(memBlocks) else False

    # Merge adjacent blocks
    if mergeRight:

        #DEBUG
#        print("Merging w/ right")

        memBlocks[blockIndex].size += memBlocks[rightIndex].size
        memBlocks.pop(rightIndex)

        for i in plist:
            if i.alloc > rightIndex:
                i.alloc -= 1

    if mergeLeft:

        #DEBUG
#        print("Merging w/ left")

        memBlocks[leftIndex].size += memBlocks[blockIndex].size
        memBlocks.pop(blockIndex)

        for i in plist:
            if i.alloc > blockIndex:
                i.alloc -= 1;


    #DEBUG
#    print("after:")
#    print("(allocFlag, size)")
#    for i in range(len(memBlocks)):
#        print("[", end="")
#        print(str(memBlocks[i].allocFlag) + ", " + str(memBlocks[i].size) + "]")

# Removes a TTL from a running proccess and reallocs the space if process is complete
def runProccess(canvas, memBlocks, plist):
    for obj in plist:
        if obj.alloc > -1:
            obj.TTL -= 1
            if obj.TTL == 0:
#                memBlocks[obj.alloc] += obj.size
#                obj.alloc = -1
                freeMemBlocks(canvas, memBlocks, obj, plist)

# blocks as per First fit algorithm
def firstFit(memBlocks, m, proc, plist):

    # Initially no block is assigned to any process

    # pick each process and find suitable blocks
    # according to its size ad assign to it
    for j in range(m):
        if memBlocks[j].size >= proc.size and not memBlocks[j].allocFlag:

            # allocate block j to p[i] process
            proc.alloc = j

            # Update memory allocation state
            allocMemBlocks(memBlocks, j, proc, plist)

            break

    if proc.alloc != -1:
        return 0
    else:
        return -1

def bestFit(memBlocks, m, proc, plist):

    # Find the best fit block for
    # current process
    bestIdx = -1
    for j in range(m):
        if memBlocks[j].size >= proc.size and not memBlocks[j].allocFlag:
            if bestIdx == -1:
                bestIdx = j
            elif memBlocks[bestIdx].size > memBlocks[j].size:
                bestIdx = j

    # If we could find a block for
    # current process
    if bestIdx != -1:

        # allocate block j to p[i] process
        proc.alloc = bestIdx

        # Update memory allocation state
        allocMemBlocks(memBlocks, j, proc, plist)

    if proc.alloc != -1:
        return 0
    else:
        return -1

def worstFit(memBlocks, m, proc, plist):

    # Find the best fit block for
    # current process
    wstIdx = -1
    for j in range(m):
        if memBlocks[j].size >= proc.size and not memBlocks[j].size:
            if wstIdx == -1:
                wstIdx = j
            elif memBlocks[wstIdx].size < memBlocks[j].size:
                wstIdx = j

    # If we could find a block for
    # current process
    if wstIdx != -1:

        # allocate block j to p[i] process
        proc.alloc = wstIdx

        # Update memory allocation state
        allocMemBlocks(memBlocks, j, proc, plist)

    if proc.alloc != -1:
        return 0
    else:
        return -1

def start_CB(*proccess):
    global start_flag
    start_flag = 1

#    processSize = np.random.randint(1,10001, 20)
#    memBlocks =  np.random.radnint(1,10001, 20)

#    firstFit(memBlocks, len(memBlocks), processSize, len(processSize))

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
#time_label.place( relx=0.50, rely=0.90)

btnTop   = 400
btnLeft  = 20
btnSpace = 50

startBtn = tk.Button(root, text="Start", command=start_CB)
startBtn.place(x=btnLeft, y=btnTop)

stopBtn = tk.Button(root, text="Exit", command=exit_CB)
stopBtn.place(x=btnLeft, y=btnTop+btnSpace)

#------------------    GUI FUNCTIONS ----------------------#
def drawBox(canvas, barType, memBlocks, proc):

    if(barType == 1):
        pBox_x = bar1_x
    if(barType == 2):
        pBox_x = bar2_x
    if(barType == 3):
        pBox_x = bar3_x

    pBox_y = 0

    for i in range(proc.alloc):
        pBox_y += memBlocks[i].size

    pBox_size = proc.size

    #print("Y & size:", pBox_y, pBox_size)
    offSet = barTop + pBox_y
    return canvas.create_rectangle(pBox_x, offSet, pBox_x + barWidth,
            pBox_size + offSet, fill = 'blue')

#create memory blocks
#memBlocks = [25,50,25,100,25,50,25,200]
memBlocks = [memBlockClass(False, MEM_SIZE)]

offSet = barTop
for i in range(len(memBlocks)):
    canvas.create_rectangle(bar1_x, offSet, bar1_x + barWidth,
            1+offSet, fill = 'black')
    canvas.create_rectangle(bar2_x, offSet, bar2_x + barWidth,
            1+offSet, fill = 'black')
    canvas.create_rectangle(bar3_x, offSet, bar3_x + barWidth,
            1+offSet, fill = 'black')
    offSet += memBlocks[i].size


#create the process list
plist = []
for i in range(3):
    plist.append(proccessClass(i+1,np.random.randint(1,151), np.random.randint(1,5)))
print("Initially create list")
print("---------------------")
for obj in plist:
    print(obj.PID, obj.size, obj.TTL)


draw_list = []
count = 0

#initialize all three sims
plist_ff = plist.copy()
blocks_ff = memBlocks.copy()
currProc_ff = 0

plist_bf = plist.copy()
blocks_bf = memBlocks.copy()
currProc_bf = 0

plist_wf = plist.copy()
blocks_wf = memBlocks.copy()
currProc_wf = 0

while 1:

    if quit_flag == 1:
        quit(0)

    try:
        time_label.config(text="Time: " + str(count))
        root.update()
    except:
        quit(0)

#    if start_flag == 1 and currProc_ff < len(plist) and currProc_bf < len(plist) and currProc_wf < len(plist):
    if start_flag == 1:

        ########################################

        #--------------------------First Fit-----------------------------

        #DEBUG
        print_ff = 1

        runProccess(canvas, blocks_ff, plist_ff)

        #DEBUG
        if print_ff == 1:
            print("\nFirst Fit Block List")
            print("Before: ", end = "")
#            print(blocks_ff);
            print("(allocFlag, size)")
            for i in range(len(blocks_ff)):
                print("[", end="")
                print(str(blocks_ff[i].allocFlag) + ", " + str(blocks_ff[i].size) + "]")


        if currProc_ff < len(plist):
            ret = firstFit(blocks_ff, len(blocks_ff), plist_ff[currProc_ff], plist_ff)

            #DEBUG
            if print_ff == 1:
                print(" Process No.\tProcess Size\tBlock no.")
                print(" ",plist_ff[currProc_ff].PID, "\t\t", plist_ff[currProc_ff].size, "\t\t", end = " ")
                if plist_ff[currProc_ff].alloc != -1:
                    print(plist_ff[currProc_ff].alloc + 1)
                else:
                    print("Not Allocated")
                print("After : ", end = "")
#                print(blocks_ff)
                print("(allocFlag, size)")
                for i in range(len(blocks_ff)):
                    print("[", end="")
                    print(str(blocks_ff[i].allocFlag) + ", " + str(blocks_ff[i].size) + "]")


            if ret == 0:
#                drawBox(canvas, 1, blocks_ff, plist_ff[currProc_ff])
                blocks_ff[plist_ff[currProc_ff].alloc].box = drawBox(canvas, 1, blocks_ff, plist_ff[currProc_ff])
                currProc_ff += 1

        #--------------------------Best Fit-----------------------------
        print_bf = 1

        runProccess(canvas, blocks_bf, plist_bf)
        if print_bf == 1:
            print("\nBest Fit Block List")
            print("Before: ", end = "")
#            print(blocks_bf);
            print("(allocFlag, size)")
            for i in range(len(blocks_bf)):
                print("[", end="")
                print(str(blocks_bf[i].allocFlag) + ", " + str(blocks_bf[i].size) + "]")
            print("Best Fit P List")
            print("Before: ", end="")
            for i in range(len(plist_bf)):
                print(plist_bf[i].alloc)


        if currProc_bf < len(plist):
            ret = bestFit(blocks_bf, len(blocks_bf), plist_bf[currProc_bf], plist_bf)
            if print_bf == 1:
                print(" Process No.\tProcess Size\tBlock no.")
                print(" ",plist_bf[currProc_bf].PID, "\t\t", plist_bf[currProc_bf].size, "\t\t", end = " ")
                if plist_bf[currProc_bf].alloc != -1:
                    print(plist_bf[currProc_bf].alloc + 1)
                else:
                    print("Not Allocated")
                print("After : ", end = "")
#                print(blocks_bf)
            print("(allocFlag, size)")
            for i in range(len(blocks_bf)):
                print("[", end="")
                print(str(blocks_bf[i].allocFlag) + ", " + str(blocks_bf[i].size) + "]")

            print("Best Fit P List")
            print("After: ", end="")
            for i in range(len(plist_bf)):
                print(plist_bf[i].alloc)

            if ret == 0:
#                drawBox(canvas, 2, blocks_bf, plist_bf[currProc_bf])

                #DEBUG
#                x = plist_bf[currProc_bf].alloc
#                print(plist_bf[currProc_bf])
#                print("x: " + str(x))
#                print(blocks_bf[x].size)
#                blocks_bf[x].box = drawBox(canvas, 2, blocks_bf, plist_bf[currProc_bf])
                blocks_bf[plist_bf[currProc_bf].alloc].box = drawBox(canvas, 2, blocks_bf, plist_bf[currProc_bf])
                currProc_bf += 1

        #--------------------------Worst Fit-----------------------------
#        print_wf = 0;
#
#        runProccess(canvas, blocks_wf, plist_wf)
#        if print_wf == 1:
#            print("\nWorst Fit Block List")
#            print("Before: ", end = "")
#            print(blocks_wf);
#
#        if currProc_wf < len(plist):
#            ret = worstFit(blocks_wf, len(blocks_wf), plist_wf[currProc_wf], plist_wf)
#            if print_wf == 1:
#                print(" Process No.\tProcess Size\tBlock no.")
#                print(" ",plist_wf[currProc_wf].PID, "\t\t", plist_wf[currProc_wf].size, "\t\t", end = " ")
#                if plist_wf[currProc_wf].alloc != -1:
#                    print(plist_wf[currProc_wf].alloc + 1)
#                else:
#                    print("Not Allocated")
#                print("After : ", end = "")
#                print(blocks_wf)
#
#            if ret == 0:
##                drawBox(canvas, 3, blocks_wf, plist_wf[currProc_wf])
#                blocks_wf[plist_wf[currProc_wf].alloc].box = drawBox(canvas, 3, blocks_wf, plist_wf[currProc_wf])
#                currProc_wf += 1

        ########################################


#        # Bar location values
#        first_x  = 0
#        best_x   = 200
#       worst_x  = 400
#       y_offset = 100
#
#       # Delete drawn stuff
#       for i in draw_list:
#           canvas.delete(i[0])
#           i[1].destroy()
#
#       # Display current memory allocation
#       for i in plist:
#           offset = 0
#           for j in range(i.alloc-1):
#               offset += memBlocks[j]
#           draw_list.append(draw_box(canvas, i, first_x, offset))


        # Increment time
        count = count + 1
        root.update()
        time.sleep(1)

