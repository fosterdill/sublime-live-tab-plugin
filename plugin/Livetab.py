import socket
import sys
import sublime
import sublime_plugin
import _thread as thread

HOST = "localhost"
PORT = 9999

sock       = None
session_id = None
view       = None
edit       = None

class LivetabCommand(sublime_plugin.TextCommand):
  def _open_tab(self, file_name):
    return (file_name if self.window.open_file(file_name) else self.new_file())

  def run(self, edit_param, session_id_param, file_name=None):
    global session_id, view, edit
    session_id = session_id
    view = self._open_tab(file_name)
    edit = edit_param


class LiveListener(sublime_plugin.EventListener, object):
  def on_modified(self, modified_view):
    if (sock and view.id() == modified_view.id):
      sock.sendall(modified_view.substr(sublime.Region(0, modified_view.size())))

  def _connect(self):
      global sock
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((HOST, PORT))
      sock.sendall('session-{}'.format(session_id))
      session_state = sock.recv(1024)

  def _handle_session(self, session_state):
    getattr(self, 'on' + session_state.capitalize() + 'State')

  def onNewState(self):
    global sock
    sock.sendall()
    thread.start_new_thread(self._change_listener)

  def onLiveState(self):
    thread.start_new_thread(self._change_listener)

  def onDeadState(self):
    pass

  def _change_listener(self):
    global sock, view

    while True:
      data = sock.recv(1024)
      view.replace(edit, view.substr(sublime.Region(0, view.size())), data)

  def on_load(self, loaded_view):
    if (view.id == loaded_view.id()):
      session_state = self._connect()
      self._handle_session(session_state, loaded_view)

  def on_new(self, new_view):
    if (view.id == new_view.id()):
      session_state = self._connect()
      self._handle_session(session_state, new_view)