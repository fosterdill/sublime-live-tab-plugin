import SocketServer
from random import random
import pickle

class LiveHandler(SocketServer.BaseRequestHandler, object):
  def _generate_ip_key(self):
    return self.client_address[0] + '-' + str(int(random() * 1000000))

  def handle(self):
    self._id = self._generate_ip_key()

    while self.server.running:
      data = self.request.recv(2048)
      sessions = self.server.sessions

      if (not data):
        break

      parsed_data = pickle.loads(data)
      session_id = parsed_data['session_id']

      if (session_id in self.server.sessions):
        if (self._id in self.server.sessions[session_id]):
          sessions[session_id]['text'] = parsed_data['text']
          for handler_id in sessions[session_id]:
            if (handler_id != 'text' and handler_id != self._id):
              data = pickle.dumps(parsed_data, protocol = 2)
              sessions[session_id][handler_id](data)
        else:
          self.server.sessions[session_id][self._id] = self.request.sendall
          self.request.sendall(pickle.dumps({'text': sessions[session_id]['text']}, protocol = 2))

      else:
        data = pickle.dumps(parsed_data, protocol = 2)
        self.server.sessions[session_id] = {'text': parsed_data['text'], self._id: self.request.sendall}


    del self.server.sessions[session_id][self._id]
    print("{} closed connection.".format(self.client_address[0]))