#!/usr/bin/env python

import Tkinter
import threading
import MP3Server
import tkSnack
import os

class ControlButton(Tkinter.Canvas):

    STOP_COLOR = 'red'
    PADDING = 5
    START_COLOR = 'green'
    OUTLINE_COLOR = 'black'

    def __init__(self, parent, width, height, btype = None, command = None):
        Tkinter.Canvas.__init__(self, parent, borderwidth = 1,
                                relief = Tkinter.RAISED,
                                width = width,
                                height = height)


        self.command = command

        if (btype == 'stop'):
            circle = (self.PADDING + 3, self.PADDING + 3,
                      width - self.PADDING, height - self.PADDING)

            self.create_oval(circle, fill = self.STOP_COLOR)
        elif (btype == 'start'):
            triangle = (self.PADDING + 3, self.PADDING + 3,
                        width - self.PADDING,
                        height / 2 + self.PADDING / 2,
                        self.PADDING + 3, height - self.PADDING)
            self.create_polygon(triangle,
								fill = self.START_COLOR,
								outline = self.OUTLINE_COLOR)


        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)

    def _on_press(self, event):
        self.configure(relief = Tkinter.SUNKEN)

    def _on_release(self, event):
        self.configure(relief = Tkinter.RAISED)
        self.command()
        

def main():

    DOCROOT_LABEL = 'Document root:'
    PORT_LABEL = 'Listen on port:'
    APPNAME = 'PIPlayD'
    TEXT_HEIGHT = 1
    MF_WIDTH = 400
    MF_HEIGHT = 150
    BUT_WIDTH = 30
    BUT_HEIGHT = 30
    START_COLOR = 'green'
    DEFAULT_PORT = '9580'
    server = None
    sndobj = None

    # Loading main window
    win = Tkinter.Tk(baseName = APPNAME)
    win.wm_title(APPNAME)

    # Setting main frame
    f = Tkinter.Frame(win, width = MF_WIDTH, height = MF_HEIGHT)
    f.pack_propagate(False)


    # Setting labels
    label_DocRoot = Tkinter.Label(f, text = DOCROOT_LABEL)
    label_Port = Tkinter.Label(f, text = PORT_LABEL)

    # Setting text areas
    text_DR = Tkinter.Entry(f)
    text_DR.insert(0, os.getcwd())
    text_P = Tkinter.Entry(f)
    text_P.insert(0, DEFAULT_PORT)

    # Handlers for buttons
    def stopServer():
        global server
        server.shutdown()
    
    def startServer():
		global server
		port = int(text_P.get())
		server = MP3Server.MP3Server(('', port),
                                     MP3Server.PlayerHandler,
                                     sndobj,
                                     text_DR.get())
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
    
    # Setting buttons
    but_Stop = ControlButton(f, BUT_WIDTH, BUT_HEIGHT, 'stop',
                             command = stopServer)
    but_Start = ControlButton(f, BUT_WIDTH, BUT_HEIGHT, 'start',
                              command = startServer)
    
    # Initilizing tkSnack
    tkSnack.initializeSnack(win)
    sndobj = tkSnack.Sound()

    # Designign layout
    f.grid()
    label_DocRoot.grid(row = 1, column = 1, sticky = Tkinter.W)
    text_DR.grid(row = 1, column = 2, sticky = Tkinter.W, columnspan = 2)
    label_Port.grid(row = 2, column = 1, sticky = Tkinter.W)
    text_P.grid(row = 2, column = 2, sticky = Tkinter.W, columnspan = 2)
    but_Stop.grid(row = 3, column = 2)
    but_Start.grid(row = 3, column = 3)
   

    win.mainloop()

if __name__ == '__main__':
    main()
