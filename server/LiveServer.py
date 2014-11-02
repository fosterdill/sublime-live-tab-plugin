import SocketServer

class LiveServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer, object):
  def __init__(self, *args, **kargs):
    self.connections = {}
    self.running = True
    super(LiveServer, self).__init__(*args, **kargs)