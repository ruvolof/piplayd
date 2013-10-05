import SocketServer
import os

class MP3Server (SocketServer.TCPServer):
    
    def __init__(self, server_address, RequestHandlerClass, SoundObj, DocRoot):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

        # Setting SoundObj e DocRoot, the handler needs them
        self.SoundObj = SoundObj
        self.DocRoot = DocRoot

        # Changing to DocRoot directory
        os.chdir(self.DocRoot)
    
    # Overriding method to add some print line
    def serve_forever(self, poll_interval=0.5):
        print "Server's listening on port %d." % (self.server_address[1])
        print "It's serving the folder %s." % (self.DocRoot)
        SocketServer.TCPServer.serve_forever(self, poll_interval=0.5)

class PlayerHandler (SocketServer.BaseRequestHandler):

    # Constants
    MSGBUFF = 256
    MSG_PLAY = 'PLAY'
    MSG_AYPP = 'AREYOUPIPLAY'
    MSG_PAUSE= 'PAUSE'
    CODE_OK = '200 OK'
    CODE_IMPP = '220 YES I AM'
    CODE_NF = '404 NOT FOUND'
    CODE_ERR = '500 ERROR'
    CODE_UNKNOWN = '505 METHOD NOT IMPLEMENTED'

    def handle(self):
        command = 'dummy'
        # This is because recv returns an empty line on error
        while command != '':
            self.data = self.request.recv(self.MSGBUFF).strip()

            command = self.data
            snd = self.server.SoundObj
            
            # Parsing command
            if command != '':

                if command.find(self.MSG_PLAY) == 0:
                    song = command.split(' ', 1)[1]
                    if self.playSong(snd, song) == 0:
                        self.request.send(self.CODE_OK)
                    else:
                        self.request.send(self.CODE_NF)

                elif command.find(self.MSG_PAUSE) == 0:
                    if self.pauseSong(snd) == 0:
                        self.request.send(self.CODE_OK)
                    else:
                        self.request.send(self.CODE_ERR)

                elif command.find(self.MSG_AYPP) == 0:
                    self.request.send(self.CODE_IMPP)

                else:
                    print "Unknown command: %s" % (command)
                    self.request.send(self.CODE_UNKNOWN)

    
    def playSong(self, sndobj, path):
        sndobj.flush()

        try:
            sndobj.read(path)
        except Exception, err:
            print "Error %s" % (err)
            return 1
        
        sndobj.play()
        print "Now playing: %s" % (path)
        return 0

    def pauseSong(self, sndobj):
        try:
            sndobj.pause()
        except Exception, err:
            print "Error %s" % (err)
            return 1
        return 0
