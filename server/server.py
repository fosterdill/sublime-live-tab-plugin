import sys
import signal
from LiveServer import LiveServer
from LiveHandler import LiveHandler

if __name__ == "__main__":

  HOST, PORT = "0.0.0.0", 9999
  server = LiveServer((HOST, PORT), LiveHandler)

  def signal_handler(signal, frame):
    print 'Server stopped.'
    server.running = False
    sys.exit(0)

  #Listen for keyboard interrupt
  signal.signal(signal.SIGINT, signal_handler)
  server.serve_forever()