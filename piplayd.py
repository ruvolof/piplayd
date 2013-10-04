#!/usr/bin/python

from Tkinter import *
import sys, getopt 
import tkSnack as sndsys

def main():
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

if __name__ == "__main__":
    main()
