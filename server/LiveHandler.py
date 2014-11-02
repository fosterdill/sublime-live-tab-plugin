import SocketServer
from random import random

class LiveHandler(SocketServer.BaseRequestHandler, object):
  def _generate_ip_key(self):
    return self.client_address[0] + '-' + str(int(random() * 1000000))

  def handle(self):
    self.ip_key = self._generate_ip_key()
    self.server.connections[self.ip_key] = self.request.sendall

    while self.server.running:
      data = self.request.recv(1024)
      connections = self.server.connections

      if (not data):
        break

      for ip_key in connections:
        connections[ip_key]("{} says: {} ".format(self.ip_key, data))

    print("{} closed connection.".format(self.client_address[0]))