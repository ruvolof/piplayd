import SocketServer
import socket
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
    MSG_PAUSE = 'PAUSE'
    MSG_RESUME = 'RESUME'

    CODE_OK = '200 OK'
    CODE_IMPP = '220 YES I AM'
    CODE_NF = '404 NOT FOUND'
    CODE_ERR = '500 ERROR'
    CODE_UNKNOWN = '505 METHOD NOT IMPLEMENTED'

    def handle(self):
        print "Got connection from ", self.client_address

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
                    if not self.startSong(snd, song):
                        self.request.send(self.CODE_OK)
                    else:
                        self.request.send(self.CODE_NF)

                elif command.find(self.MSG_PAUSE) == 0:
                    try:
                        snd.pause()
                        self.request.send(self.CODE_OK)
                    except Exception, err:
                        print "Errore ", err
                        self.request.send(self.CODE_ERR)

                elif command.find(self.MSG_RESUME) == 0:
                    try:
                        snd.play()
                        self.request.send(self.CODE_OK)
                    except Exception, err:
                        print "Errore ", err
                        self.request.send(self.CODE_ERR)

                elif command.find(self.MSG_AYPP) == 0:
                    self.request.send(self.CODE_IMPP)

                else:
                    print "Unknown command: %s" % (command)
                    self.request.send(self.CODE_UNKNOWN)

    def finish(self):
        self.request.shutdown(socket.SHUT_RDWR)
        self.request.close()

    
    def startSong(self, sndobj, path):
        sndobj.flush()

        if os.path.isfile(path):
            try:
                sndobj.read(path)
            except Exception, err:
                print "Error %s" % (err)
                return 1
        else:
            return 2
        
        sndobj.play()
        print "Now playing: %s" % (path)
        return 0
