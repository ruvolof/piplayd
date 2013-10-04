#!/usr/bin/python

from Tkinter import *
import sys, getopt , os
import tkSnack as sndsys

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

    print "%d %s" % (port, docroot)

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

    playSong(args[0])

    mainloop()

if __name__ == "__main__":
    main()
