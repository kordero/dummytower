import time
import BaseHTTPServer
import cgi
import ssl
import json
import urlparse
from api import TowerApi

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 45130

class TowerServer(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self):
    content_len = int(self.headers.getheader('content-length', 0))
    body = self.rfile.read(content_len)
    remote_address = self.client_address

    if self.path == '/api':
      length = int(self.headers['Content-Length'])
      data = urlparse.parse_qs(body)
      if not 'action' in data:
        # action not defined
        self.send_response(404)
      else:
        api = TowerApi()
        ret = api.run(data, remote_address)
        if ret:
          # running API action succeded
          self.send_response(200)
        else:
          # something went wrong when running API action
          self.send_response(400)
    elif self.path == '/webhook':
      #
      # here is were we should point GH json webhooks to
      #
      # payload = json.loads(body)
      #repository = payload['repository']['full_name']
      #if repository == 'owner/repository':
      #  dep = Deployment()
      #  dep.run(payload['ref'], remote_address)
      #  self.send_response(200)
      #  self.send_header("Content-type", "text/html")
      #  self.end_headers()
      #else:
      #  self.send_response(404)
      self.send_response(200)
    else:
      self.send_response(404)

    self.end_headers()

if __name__ == '__main__':
  httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), TowerServer)
  httpd.socket = ssl.wrap_socket(httpd.socket, certfile='towerserver.crt', server_side=True, keyfile='towerserver.key')
  print time.asctime(), "TowerServer Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "TowerServer Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)