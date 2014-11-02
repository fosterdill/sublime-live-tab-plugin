import socket
import sys
import sublime
import sublime_plugin
import thread
import random
import pickle
import time
from functools import partial



HOST = "54.187.58.214"
# 54.187.58.214
PORT = 9992
CLIENT = 'client'
SERVER = 'server'

sessions = {}

#global helpers

def all_region(view):
  return sublime.Region(0, view.size())

def view_text(view):
  return view.substr(all_region(view))

class SessionState:
  def __init__(self):
    self._state = {}
    self._source_callbacks = {}

  def set(self, source, kargs):
    for key in kargs:
      self._state[key] = kargs[key]

    self._source_callbacks[source](self._state)

  def on_change(self, source, callback):
    self._source_callbacks[source] = callback


class Connection:
  def __init__(self, host, port, callback):
    self._callback = callback
    self._host = host
    self._port = port
    self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def send(self, state):
    self._sock.sendall(pickle.dumps(state, protocol = 2))

  def connect(self):
    # if (not self._sock.connect((self._host, self._port))):
    #   raise ConnectionError(host = self._host, port = self._port)
    self._sock.connect((self._host, self._port))

    thread.start_new_thread(self._connection_listener, ())

  def _connection_listener(self):
    while True:
      data = self._sock.recv(4096)
      if (data):
        self._callback(pickle.loads(data))


class ReplaceCommand(sublime_plugin.TextCommand):
  def run(self, edit, string):
    self.view.replace(edit, all_region(self.view), string)

class LivetabCommand(sublime_plugin.TextCommand):
  def run(self, edit, session_id = None):
    global sessions
    session = Session(self.view, edit, session_id)
    sessions[self.view.id()] = session
    print("Success! Session: " + str(session.id()))
    



class LivetabListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    global sessions
    session = view.id() in sessions and sessions[view.id()]

    if (session):
      text = view_text(view)
      session.set_state(CLIENT, { 'text': text })


class StateHandlers:

  def handle_server_state(self, state, view, edit):
    self._changing = True
    def anon():
      view.run_command('replace', {'string': state['text']})
    sublime.set_timeout(anon, 0)

  def handle_client_state(self, state, view, connection, session_id):
    if (self._changing):
      self._changing = False
    else:
      connection.send({ 'session_id': session_id, 'text': view_text(view)})


class Session(StateHandlers):
  def __init__(self, view, edit, session_id):
    self._state = SessionState()
    self._view = view
    self._edit = edit
    self._id = session_id
    self._changing = False

    on_data = partial(self.set_state, SERVER)
    self._connection = Connection(HOST, PORT, on_data)

    self._state.on_change(
      SERVER,
      partial(
        self._handle_state,
        SERVER,
        view = view,
        edit = edit ))
    self._state.on_change(
      CLIENT,
      partial(
        self._handle_state,
        CLIENT,
        session_id = self._id,
        connection = self._connection,
        view = self._view ))

    self._connection.connect()
    self._connection.send({'session_id': self.id(), 'text': view_text(view)})

  def id(self):
    self._id = self._id or random.getrandbits(128)
    return self._id

  def set_state(self, source, state):
    self._state.set(source, state)

  def _handle_state(self, source, state, **kargs):
    getattr(self, 'handle_' + source + '_state')(state, **kargs)