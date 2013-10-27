import SocketServer
import os
import re
import threading

class MP3Server (SocketServer.TCPServer):

    ServedFiles = []
    AcceptedExtension = frozenset(['mp3', 'wav', 'ogg'])
    
    def __init__(self, server_address, RequestHandlerClass, SoundObj, DocRoot):
        SocketServer.TCPServer.__init__(self,
                                        server_address,
                                        RequestHandlerClass,
                                        bind_and_activate = False)
        self.allow_reuse_address = True
        self.server_bind()
        self.server_activate()

        # Setting SoundObj e DocRoot, the handler needs them
        self.SoundObj = SoundObj
        self.DocRoot = DocRoot

        # Changing to DocRoot directory
        os.chdir(self.DocRoot)

        # Loading files
        self.refreshServed()
    
    # Overriding method to add some print line
    def serve_forever(self, poll_interval=0.5):
        print "Server's listening on port %d." % (self.server_address[1])
        print "It's serving the folder %s." % (self.DocRoot)
        SocketServer.TCPServer.serve_forever(self, poll_interval=0.5)

    def refreshServed(self):
        drlen = len(self.DocRoot)
        self.ServedFiles = []
        for dir, subdir, files in os.walk(self.DocRoot):
            for f in files:
                ext = None
                try:
                    ext = f.rsplit('.', 1)[1]
                except Exception:
                    pass
                
                if ext != None and ext in self.AcceptedExtension:
                    self.ServedFiles.append(os.path.join(dir[drlen:], f))

        self.ServedFiles.sort()

class PlayerHandler (SocketServer.BaseRequestHandler):

    # Active list for easy retrieval
    Dirs = []
    Files = []
    ActiveList = []
    ActivePlaylist = []

    # Constants
    MSGBUFF = 256

    MSG_PLAY = 'PLAY'
    MSG_AYPP = 'AREYOUPIPLAY'
    MSG_PAUSE = 'PAUSE'
    MSG_RESUME = 'RESUME'
    MSG_LIST = 'LIST'
    MSG_SEARCH = 'SEARCH'
    MSG_PLAYLIST = 'PLAYLIST'

    CODE_OK = '200 OK\n'
    CODE_LISTSUCC = '210 LIST\n'
    CODE_IMPP = '250 YES I AM\n'
    CODE_FORBIDDEN = '403 FORBIDDEN\n'
    CODE_NF = '404 NOT FOUND\n'
    CODE_NOKEY = '420 NO KEY SPECIFIED\n'
    CODE_INVPL = '430 INVALID PLAYLIST\n'
    CODE_ERR = '500 INTERNAL ERROR\n'
    CODE_UNKNOWN = '505 METHOD NOT IMPLEMENTED\n'

    def handle(self):
        print "Got connection from ", self.client_address
        command = 'notempty'
        
        # socket.recv returns empty string on error
        while command != '':
            self.data = self.request.recv(self.MSGBUFF).strip()

            command = self.data
            snd = self.server.SoundObj
            
            # Parsing command
            if command != '':

                if self.checkMsg(command, self.MSG_PLAY):
                    if not self.startSong(snd, command):
                        self.request.send(self.CODE_OK)
                    else:
                        self.request.send(self.CODE_NF)

                elif self.checkMsg(command, self.MSG_PAUSE):
                    try:
                        snd.pause()
                        self.request.send(self.CODE_OK)
                    except Exception, err:
                        print "Errore ", err
                        self.request.send(self.CODE_ERR)

                elif self.checkMsg(command, self.MSG_RESUME):
                    try:
                        snd.play()
                        self.request.send(self.CODE_OK)
                    except Exception, err:
                        print "Errore ", err
                        self.request.send(self.CODE_ERR)

                elif self.checkMsg(command, self.MSG_AYPP):
                    self.request.send(self.CODE_IMPP)

                elif self.checkMsg(command, self.MSG_LIST):
                    rv = self.setActiveDir(command)
                    if rv ==  0:
                        self.request.send(self.createListMsg())
                    elif rv == 1:
                        self.request.send(self.CODE_NF)
                    elif rv == 2:
                        self.request.send(self.CODE_FORBIDDEN)

                elif self.checkMsg(command, self.MSG_SEARCH):
                    if not self.setActiveSearch(command):
                        self.request.send(self.createListMsg())
                    else:
                        self.request.send(self.CODE_NOKEY)

                elif self.checkMsg(command, self.MSG_PLAYLIST):
                    if self.startPlaylist(command):
                        self.request.send(self.CODE_OK)
                    else:
                        self.request.send(self.CODE_INVPL)
                else:
                    print "Unknown command: %s" % (command)
                    self.request.send(self.CODE_UNKNOWN)
    
    def startSong(self, sndobj, command):
        sndobj.flush()

        try:
            ref = command.split(' ', 1)[1]
        except Exception, err:
            print "Error ", err
            return 1

        if os.path.isfile(ref):
            try:
                sndobj.read(path)
            except Exception, err:
                print "Error ", err
                return 1
        elif ref.isdigit():
            try:
                ref = int(ref)
                sndobj.read(self.ActiveList[ref])
            except Exception, err:
                print "Error ", err
                return 1
        else:
            return 2
        
        sndobj.play()
        if not isinstance(ref, int):
            print "Now playing: ", ref
        else:
            print "Now playing: ", self.ActiveList[ref]
        return 0

    def setActiveDir(self, command):
        # Check for argument
        try:
            directory = os.path.join(os.getcwd(), command.split(' ', 1)[1])
        except Exception:
            directory = os.getcwd()

        # Flushing old entries
        self.flushActive()

        if os.path.isdir(directory):
            if self.checkIsSubdir(self.server.DocRoot, directory):
                for entry in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, entry)):
                        self.Files.append(os.path.join(directory, entry))
                    elif os.path.isdir(os.path.join(directory, entry)):
                        self.Dirs.append(os.path.join(directory, entry))
            else:
                return 2

        else:
            return 1

        self.Dirs.sort()
        self.Files.sort()
        self.ActiveList = self.Dirs + self.Files

        return 0

    def setActiveSearch(self, command):
        try:
            key = command.split(' ', 1)[1]
        except Exception:
            print "SEARCH: No key specified"
            return 1

        # Flushing old entries
        self.flushActive()

        self.server.refreshServed()

        for f in self.server.ServedFiles:
            if re.search(key, f, re.I):
                if os.path.isfile(f):
                    self.Files.append(f)
                elif os.path.isdir(f):
                    self.Dirs.append(f)

        self.Dirs.sort()
        self.Files.sort()
        self.ActiveList = self.Dirs + self.Files

        return 0
    
    def createListMsg(self):
        msg = self.CODE_LISTSUCC
        i = 0
        if self.ActiveList != []:
            for f in self.ActiveList:
                msg += str(i) + " - " + f + "\n"
                i += 1
        else:
            msg += "No match found\n"
        return msg
    
    def playLoop(self):
        sound = self.server.SoundObj

        for song in self.ActivePlaylist:
            valid = False
            sound.flush()
            try:
                sound.read(song)
                valid = True
            except Exception, err:
                print "Error", err

            if valid:
                try:
                    sound.play(blocking=True)
                except Exception, err:
                    print "Error", err


    def startPlaylist(self, command):
        files = 0
        self.ActivePlaylist = []
        args = command.split(' ');

        for a in args:
            if a.isdigit():
                try:
                    a = int(a)
                    if a < len(self.ActiveList): 
                        self.ActivePlaylist.append(self.ActiveList[a])
                        files += 1
                except Exception, err:
                    print "Error", err

        if files > 0:
            pl_thread = threading.Thread(target = self.playLoop)
            pl_thread.daemon = True
            pl_thread.start()
        
        return files

    def flushActive(self):
        self.Dirs = []
        self.Files = []
        self.ActiveList = []

    def checkIsSubdir(self, root, f):
        r = os.path.realpath(root)
        fp = os.path.realpath(f)

        return os.path.commonprefix([r, fp]) == r

    def checkMsg(self, string, msg):
        msg = msg.rstrip()
        return re.search(r'^%s\b' % msg, string, re.I)
