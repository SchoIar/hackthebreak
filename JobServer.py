"""
A simple TCP server program to handle all the http requests to the server
"""

import socketserver
import threading
import json
import re
import os
import time

class JobServerHandler(socketserver.StreamRequestHandler):

    def handle(self):
        #reads the main header off the request
        Header = self.rfile.readline().decode()

        #creates a list of the optional headers included in the request
        OptionalHeaders = ""

        print(Header)
        #creates a varaible to store each line as it is read 
        line = self.rfile.readline().decode()

        #loops until all optional headers have been read
        while(line != "\r\n"):
            #adds the header to the option headers string
            OptionalHeaders = OptionalHeaders + line
            #reads the next line
            line = self.rfile.readline().decode()

        print(OptionalHeaders)

        print("response findings: \n")

        #creates a variable to store the content of the request and sets it to ""
        Content = ""

        #attempts to find the content length of the any attached content
        contentLengths = re.findall(r'Content-Length: (\d*)', OptionalHeaders)

        if(len(contentLengths) > 0):
            #reads the first occurenct of content length and converts it to an int for processing
            contentLength = int(contentLengths[0])

            print(contentLength)
            
            #reads the content attached to the http request
            Content = self.rfile.read(contentLength).decode()

            print(Content)

        else:
            print("no content attached")

        #reads the path the request is attempting to get from
        path = re.findall(r'^.* (.*) ', Header)[0]

        #checks if this is a get request
        if(Header[0:3] == "GET"):
            #checks that the path is not an icon request
            if(path != "/favicon.ico"):
                #prints the path
                print(path)

                #checks if the path ends with .css or .js
                if(path[-4:] != ".css" and path[-3:] != ".js" and path[-4:] != ".jpg"):
                    #adds /index.html to the end of the file
                    path = path + "/Index.html"

                #checks if an HTML file exists at that location
                if(os.path.isfile("./website" + path)):

                    #opens the found html file
                    returnfile  = open("./website" + path, mode="rb")

                    #reads teh content from the file
                    ContentReturn = returnfile.read()

                    #closes the html file
                    returnfile.close()

                    returnContentType = ""

                    if(path[-4:] == ".css"):
                        returnContentType = "Content-Type: text/css\r\n"

                    elif(path[-3:] == ".js"):

                        returnContentType = "Content-Type: application/javascript\r\n"

                    elif(path[-4:] == ".jpg"):

                        returnContentType = "Content-Type: image\jpeg"

                    else:
                        returnContentType = "Content-Type: text/html\r\n"

                    #writes the reutrn header (200 since the file was found marks the return as html and the length as the length of the text)
                    returnHeader = "HTTP/1.1 200 success\r\n" + returnContentType + "Content-Length: " + str(len(ContentReturn))

                    print("replaing with header:\n" + returnHeader)

                    #writes the html return
                    self.wfile.write((returnHeader + "\r\n\r\n").encode() + ContentReturn)

                else:
                    print("file at " + path + " not found")
                    #writes a return
                    self.wfile.write(b"HTTP/1.1 404 file not found\r\n\r\nFile Not Found")

            else:
                print("icon request")

                IconFile = open("./website/favicon.ico", mode="rb")

                binIcon = IconFile.read()

                IconFile.close()

                self.wfile.write(b"HTTP/1.1 200 success\r\n" \
                            + b"Content-Type: image/x-icon\r\nContent-Length: " + str(len(binIcon)).encode()\
                            +b"\r\n\r\n" + binIcon)

        #checks if this is a posts request    
        elif(Header[0:4] == "POST"):
            if(path == "/JobQuery"):
                self.wfile.write(b"HTTP/1.1 200 success\r\n" \
                            + b"Content-Type: application/json\r\n"\
                            + b"Content-Length: 19\r\n\r\n"\
                            + b'{"yourMom": "Large"}')




        #self.wfile.write(b"HTTP/1.1 200 success\r\n\r\nthis worked?")

class JobServer(socketserver.TCPServer):
    #stores a link to the database program for users and jobData
    Database = ""

    #stores the thread the server is running on
    ServerThread = ""

    def runServer(self):
        self.serve_forever()

        print("server closed")

    def startServer(self):
        #creates a thread for the server to run on
        ServerThread = threading.Thread(target=self.runServer, name="ServerThreadName")

        ServerThread.start()

    def stopServer(self):
        #stops the current server loop
        self.shutdown()

        #waits for the server thread to close
        self.ServerThread.join

        #finializes the server close
        self.server_close()


if(__name__ == "__main__"):

    srvr = JobServer(("localhost", 8080), JobServerHandler)

    srvr.startServer()

    try:
        time.sleep(10000)
    except:
        pass

    srvr.stopServer()