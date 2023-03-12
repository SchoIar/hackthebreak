"""
A simple TCP server program to handle all the http requests to the server
"""

import socketserver
import threading
import json
import re
import os
import time
import db.SQLManager
from datetime import date
from datetime import timedelta

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
            #checks if the path is for the job listings
            if(path == "/JobQuery"):
                #reads the json from the request
                jsoncontent = json.loads(Content)

                #finds all teh job ids that match the search conditions
                jobIDs = searchJobs(jsoncontent["keywords"], jsoncontent["location"], self.server.Database)

                print("num of matchs: " + str(len(jobIDs)))

                #creates an empty job list
                Jobs = []

                #for each job in the jobIDs list
                for j in jobIDs:
                    #creates a json job entry for the job from the job list
                    Jobs.append(generatejob(j, self.server.Database))


                #converts the jobs list into a json string
                jsonOut = json.dumps(Jobs)

                print("raw json:\n" + jsonOut)

                binout = b"HTTP/1.1 200 success\r\n"
                binout += b"Content-Type: application/json\r\n"
                binout += b"Content-Length: " + str(len(jsonOut)).encode() + b"\r\n\r\n"
                binout += jsonOut.encode()

                self.wfile.write(binout)
                

            #checks if the request is for the userdata
            elif(path == "/userdata"):
                #reads the content of the request and converts it to a json
                jsonContent = json.loads(Content)

                #creates a json to store whether or not the user exists
                outputJson = {}

                #records whether or not that user exists and stores it in teh database
                outputJson["exists"] = self.server.Database.userExists(jsonContent["username"])

                #checks if this account exists
                if(outputJson["exists"]):
                    #checks if the password matches whats in the database
                    if(jsonContent["password"] == self.server.Database.getUserInfo(jsonContent["username"], "pw")):
                        #reads the xp, last application date, and username from database
                        outputJson["xp"] = self.server.Database.getUserInfo(jsonContent["username"], "xp")
                        outputJson["username"] = jsonContent["username"]
                        outputJson["lastApp"] = str(self.server.Database.getUserInfo(jsonContent["username"], "lastapp"))

                        if(isDateValid(self.server.Database.getUserInfo(jsonContent["username"], "lastapp"))):
                            outputJson["streak"] = self.server.Database.getUserInfo(jsonContent["username"], "streak")
                        else:
                            #since it has been too long since their last login resets streak
                            self.server.Database.removeStreak(outputJson["username"])
                            #returns streak 0
                            outputJson["streak"] = 0


                    else:
                        #writes that permission was denied
                        self.wfile.write(b"HTTP/1.1 403 permission denied\r\n")

                        return

                else:
                    if(jsonContent["create"]):
                        self.server.Database.newUser(jsonContent["username"], jsonContent["password"])

                        outputJson["streak"] = 0
                        outputJson["xp"] = 0
                        outputJson["username"] = jsonContent["username"]
                        outputJson["lastApp"] = str(self.server.Database.getUserInfo(jsonContent["username"], "lastapp"))

                    else: 
                        #sets the other values to empty strings/0
                        outputJson["streak"] = -1
                        outputJson["xp"] = -1
                        outputJson["lastApp"] = "2000-01-01"
                        outputJson["username"] = ""

                #dumps the dictionary to a raw json string
                rawOutJson = json.dumps(outputJson).encode()

                print("raw json:\n" + rawOutJson.decode())

                #sets up the output data
                binoutput = b'HTTP/1.1 200 success\r\n'
                binoutput += b'Content-Type: Appliation/json\r\n'
                binoutput += b'Content-Length: ' + str(len(rawOutJson)).encode() + b'\r\n\r\n'
                binoutput += rawOutJson

                #sends the output data
                self.wfile.write(binoutput)

            elif(path == "/increaseXP"):
                 #reads the content of the request and converts it to a json
                jsonContent = json.loads(Content)

                if(jsonContent["password"] == self.server.Database.getUserInfo(jsonContent["username"], "pw")):
                    #addds the specifed amount of xp to the user account
                    self.server.Database.addXp(jsonContent["username"], jsonContent["xp"])

                    #reads the date the user last applied for a job
                    datestr = self.server.Database.getUserInfo(jsonContent["username"], "lastapp")

                    #checks if the date is not the current date
                    if(not isDateCurrent(datestr)):
                        #increase the length of the streak and resets the lastapp day
                        self.server.Database.increaseStreak(jsonContent["username"])

                    #writes the the xp was added successfully
                    self.wfile.write(b'HTTP/1.1 200 success')

                else:
                    
                    #write that premission was denied
                    self.wfile.write(b'HTTP/1.1 403 premission denied')


                    
#searchs all the jobs and returns a list of jobs that matc  
def searchJobs(keywords, location, database):
    matchingJobs = []

    for job in database.getAllJobs():
        #checks if the job title contains the keywords
        if(keywords in job[1]):
            #checks if the job location contains the location value
            if(location in database.getJobInfo(job[0], "location")):
                #adds the job id to the results
                matchingJobs.append(job[0])
    
    return matchingJobs

def generatejob(id, database):

    #creates an empty dictionary fro the job
    returnJob = {}

    #attaches the data within the dictionary
    returnJob["link"] = database.getJobInfo(id, "link")
    returnJob["title"] = database.getJobInfo(id, "title")
    returnJob["location"] = database.getJobInfo(id, "location")

    #returns the dictionary
    return returnJob

def isDateValid(dbDate):
    if(dbDate != None):

        return(date.today() > (dbDate + timedelta(days=1)))
        """print("testing date: " + dbDate)
        dbDate = int(dbDate.replace('-',''))
        today = int(str(date.today()).replace('-',''))
        if(today + 1 > dbDate):
            return True
        else:
            return False"""
    else:
        return False
    
def isDateCurrent(dbDate):
    if(dbDate != None):
        return (date.today() == dbDate)
        """print("testing date: " + dbDate)
        dbDate = int(dbDate.replace('-',''))
        today = int(str(date.today()).replace('-',''))
        if(today == dbDate):
            return True
        else:
            return False"""
    else:
        return True


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

        #opens the mysql database
        self.Database = db.SQLManager.SQLManager()

        #starts the thread
        ServerThread.start()

    def stopServer(self):
        #stops the current server loop
        self.shutdown()

        #waits for the server thread to close
        self.ServerThread.join()

        #closes the mysql database
        self.Database.close()

        #finializes the server close
        self.server_close()


if(__name__ == "__main__"):

    srvr = JobServer(("localhost", 8080), JobServerHandler)

    srvr.startServer()

    #print(srvr.Database.getAllJobs())

    try:
        time.sleep(10000)
    except:
        pass

    srvr.stopServer()