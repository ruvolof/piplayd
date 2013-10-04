#!/usr/bin/python

from Tkinter import *
import sys, getopt , os
import tkSnack as sndsys

def playSong(sndobj, path):
    sndobj.flush()
    sndobj.read(path)
    sndobj.play()
    print "Now playing: %s" % (path)

def main():
    # Catching command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    # default values
    port = 9580
    docroot = os.getcwd()

    # Parsing command line options
    for o, a in opts:
        if o == "-p":
            port = int(a)
        elif o == "-r":
            docroot = a
        else:
            assert False, "Unhandled option"

    # Creating Tk window for Snack
    win = Tk()

    # Initializing Snack
    sndsys.initializeSnack(win)

    # Withdrawing Tk window, we don't need it after initializeSnack()
    win.withdraw()

    # Initiliazing Sound object
    sndobj = sndsys.Sound()

    playSong(sndobj, args[0])

    mainloop()

if __name__ == "__main__":
    main()
