import SocketServer
import os

class MP3Server (SocketServer.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, SoundObj, DocRoot):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.SoundObj = SoundObj
        self.DocRoot = DocRoot

        # Changing to DocRoot directory
        os.chdir(self.DocRoot)
    
    def serve_forever(self, poll_interval=0.5):
        print "Server's listening on port %d." % (self.server_address[1])
        print "It's serving the folder %s." % (self.DocRoot)
        SocketServer.TCPServer.serve_forever(self, poll_interval=0.5)

class PlayerHandler (SocketServer.BaseRequestHandler):

    MSGBUFF = 256
    command = 'dummy'

    def handle(self):
        while self.command != '':
            self.data = self.request.recv(self.MSGBUFF).strip()

            self.command = self.data
            snd = self.server.SoundObj

            if self.command != '':
                if self.command.find('PLAY') == 0:
                    song = self.command.split(' ', 1)[1]
                    self.playSong(snd, song)
                else:
                    print "Unknown command: %s" % (self.command)

    
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
            
