#!/usr/bin/python

import Tkinter
import sys
import getopt
import os
import threading
import tkSnack
import MP3Server
import signal

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
    docroot = os.getenv('HOME')

    # Parsing command line options
    for o, a in opts:
        if o == "-p":
            port = int(a)
        elif o == "-r":
            docroot = a
        else:
            assert False, "Unhandled option"

    # Registering signal handler
    def sigint_handler(signal, frame):
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    # Creating Tk window for Snack
    win = Tkinter.Tk()

    # Initializing Snack
    tkSnack.initializeSnack(win)

    # Withdrawing Tk window, we don't need it after initializeSnack()
    win.withdraw()
    
    # Initiliazing Sound object
    sndobj = tkSnack.Sound()

    # Starting server thread
    server = MP3Server.MP3Server(('', port),
                                MP3Server.PlayerHandler,
                                sndobj,
                                docroot)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Dummy function to interrupt mainloop in order to handle signal
    int_for_signal(win)

    win.mainloop()

if __name__ == "__main__":
    main()
