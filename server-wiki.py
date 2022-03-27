#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import shutil
from datetime import datetime as dt


class ReqHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        backupsdir = os.path.join(self.directory, 'backups')
        src = os.path.join(self.directory, self.path[1:])
        dest = os.path.join(
            backupsdir,
            os.path.splitext(os.path.basename(self.path))[0] + "-" + dt.now().strftime("%Y%m%d-%H%M") + ".html")
        if not os.path.exists(backupsdir):
            os.mkdir(backupsdir)
        shutil.copyfile(src, dest)
        clen = int(self.headers.get('Content-Length'))
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(src, 'wb') as fout:
            fout.write(self.rfile.read(clen))
            fout.close()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Allow", "GET,HEAD,POST,OPTIONS,CONNECT,PUT,DAV,dav")
        self.send_header("x-api-access-type", "file")
        self.send_header("dav", "tw5/put")
        self.end_headers()

try:
    server = HTTPServer(("0.0.0.0", 88), ReqHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
