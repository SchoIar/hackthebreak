"""
A simple TCP server program to handle all the http requests to the server
"""

import socketserver
import threading
import json

class JobServerHandler(socketserver.StreamRequestHandler):

    def handle(self):
        self.wfile.write(b"this worked?")

class JobServer(socketserver.TCPServer):
    #stores a link to the database program for users and jobData
    Database = ""

if(__name__ == "__main__"):
    srvr = JobServer(("localhost", 8080), JobServerHandler)

    try:
        srvr.serve_forever()
    except:
        pass

    srvr.server_close()