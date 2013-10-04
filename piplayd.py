#!/usr/bin/python

from Tkinter import *
import tkSnack as sndsys
import sys
from time import sleep

# Creating Tk window for Snack
win = Tk()

# Initializing Snack
sndsys.initializeSnack(win)

# Withdrawing Tk window, we don't need it after initializeSnack()
win.withdraw()

# Initiliazing Sound object
mp3 = sndsys.Sound()

def playSong(path):
    mp3.flush()
    mp3.read(path)
    mp3.play()
    print "Now playing: %s" % (path)

playSong(sys.argv[1])

mainloop()
