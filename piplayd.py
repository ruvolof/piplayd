#!/usr/bin/python

from Tkinter import *
import sys, getopt , os, thread, socket, errno
import tkSnack as sndsys

MSGBUF = 256

def runServer(port, docroot, sndobj):
    # Changing DocRoot
    if docroot != os.getcwd():
        os.chdir(docroot)
    
    # Opening socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen(1)

    print "Server listening on port %d." % (port)
    print "It's serving the folder %s." % (docroot)

    while True:
        clientsocket, address = serversocket.accept()
        command, msg = clientsocket.recv(MSGBUF).rstrip().split(' ', 1)
        
        # Checking command
        if command == "PLAY":
            playSong(sndobj, msg)
        else:
            print "Unrecognized command"

def playSong(sndobj, path):
    sndobj.flush()

    try:
        sndobj.read(path)
    except Exception, err:
        print "Error %s" % (err)
        return 1
    
    sndobj.play()
    print "Now playing: %s" % (path)
    return 0

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

    # Starting server thread
    thread.start_new_thread(runServer, (port, docroot, sndobj))
    
    mainloop()

if __name__ == "__main__":
    main()
