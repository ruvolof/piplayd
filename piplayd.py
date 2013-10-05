#!/usr/bin/python

from Tkinter import *
import sys, getopt , os, threading, socket, errno
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

    accepted = True
    while accepted:
        try:
            clientsocket, address = serversocket.accept()
        except Exception, err:
            accepted = False
            print "Error %s" % (err)
        
        if accepted:
            received = True
            while received:
                try:
                    command = clientsocket.recv(MSGBUF)
                except Exception, err:
                    received = False
                    print "Error %s" % (err)

                if command == '':
                    received = False
                    print "Client disconnected."
            
                # Checking command
                if received:
                    command = command.rstrip()

                    if command.find('PLAY') == 0:
                        song = command.split(' ', 1)[1]
                        playSong(sndobj, song)
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
    
def int_for_signal(tkObject):
	tkObject.after(1000, int_for_signal, tkObject)

def main():
    # Catching command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    # Default values 
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
    server = threading.Thread(target=runServer, args=(port, docroot, sndobj))
    server.daemon = True
    server.start()
    
    # Dummy function to interrupt mainloop in order to handle signal
    int_for_signal(win)

    mainloop()

if __name__ == "__main__":
    main()
