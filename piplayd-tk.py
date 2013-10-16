#!/usr/bin/env python

import Tkinter
import threading

class StopButton (Tkinter.Canvas):

    STOP_COLOR = 'red'
    PADDING = 5

    def __init__(self, parent, width, height, command=None):
        Tkinter.Canvas.__init__(self, parent, borderwidth = 1,
                                relief = Tkinter.RAISED)

        self.configure(width = width, height = height)

        circle = (self.PADDING + 3, self.PADDING + 3,
                  width - self.PADDING, height - self.PADDING)

        self.create_oval(circle, fill = self.STOP_COLOR)

        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)

    def _on_press(self, event):
        self.configure(relief = Tkinter.SUNKEN)

    def _on_release(self, event):
        self.configure(relief = Tkinter.RAISED)

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
    text_P = Tkinter.Entry(f)
    
    # Setting buttons
    but_Stop = StopButton(f, BUT_WIDTH, BUT_HEIGHT)
    
    but_Start = Tkinter.Canvas(f, width = BUT_WIDTH, height = BUT_HEIGHT)
    triangle = 5, 5, BUT_WIDTH - 5, BUT_HEIGHT / 2, 5, BUT_HEIGHT - 5 
    but_Start.create_polygon(triangle, fill = START_COLOR) 
    
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
