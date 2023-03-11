"""
A simple TCP server program to handle all the http requests to the server
"""

import socketserver
import threading
import json
import re
import os

class JobServerHandler(socketserver.StreamRequestHandler):

    def handle(self):
        #reads the main header off the request
        Header = self.rfile.readline().decode()

        #creates a list of the optional headers included in the request
        OptionalHeaders = ""

        #creates a varaible to store each line as it is read 
        line = self.rfile.readline().decode()

        #loops until all optional headers have been read
        while(line != "\r\n"):
            #adds the header to the option headers string
            OptionalHeaders = OptionalHeaders + line
            #reads the next line
            line = self.rfile.readline().decode()

        #print(OptionalHeaders)

        #creates a variable to store the content of the request and sets it to ""
        Content = ""

        #attempts to find the content length of the any attached content
        contentLengths = re.findall(r'^Content-Length: (\d*)$', OptionalHeaders)

        if(len(contentLengths) > 0):
            #reads the first occurenct of content length and converts it to an int for processing
            contentLength = int(contentLengths[0])

            print(contentLength)
            
            #reads the content attached to the http request
            Content = self.rfile.read(contentLength).decode()

        else:
            print("no content attached")

        #reads the path the request is attempting to get from
        path = "." + re.findall(r'^.* (.*) ', Header)[0]

        #checks if this is a get request
        if(Header[0:3] == "GET"):
            #checks that the path is not an icon request
            if(path != "./favicon.ico"):
                #prints the path
                print(path)

                #checks if an HTML file exists at that location
                if(os.path.isfile(path + "\Index.htm")):
                    #opens the found html file
                    HTMLfile  = open(path + "\Index.htm")

                    #reads teh html from the file
                    HTMLReturn = HTMLfile.read()

                    #closes the html file
                    HTMLfile.close()

                    #writes the reutrn header (200 since the file was found marks the return as html and the length as the length of the text)
                    returnHeader = "HTTP/1.1 200 success\r\nContent-Type: text/html\r\nContent-Length: " + str(len(HTMLReturn))

                    #writes the html return
                    self.wfile.write((returnHeader + HTMLReturn).encode())

                else:
                    #writes a return
                    self.wfile.write(b"HTTP/1.1 404 file not found\r\n\r\nFile Not Found")

            else:
                print("icon request")

                self.wfile.write(b"HTTP/1.1 200 success\r\n\r\nthis worked?")




        #self.wfile.write(b"HTTP/1.1 200 success\r\n\r\nthis worked?")

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