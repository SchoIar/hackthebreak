import json
import os
import time
import random
from linkedin_api import Linkedin
from dotenv import load_dotenv
import sys

class Scrape():
    def __init__(self, api):
        self.api = api
        
    def read_json(self, filename='jobs.json'):
        with open(filename, 'r') as file:
            return json.load(file)

    def write_json(self, newData):
        with open('jobs.json', 'r+') as file:
            data = self.read_json()
            data['job-list'].append(newData)
            json.dump(data, file)

    def searchJobs(self, apiChosen, numberOfSearches, keywordChosen, offsetNumber):
        jobs = apiChosen.search_jobs(keywordChosen, remote = 1, limit = \
                            numberOfSearches, offset = offsetNumber)
        for job in jobs:
            title = job['title']
            jobID = job['dashEntityUrn'].split(':')[-1] 
            location = job['formattedLocation']
            #jobDetails = api.get_job(jobID)
            jobLink = f'https://www.linkedin.com/jobs/view/{jobID}/'
            job = {
                "Job title":title,
                "Job link":jobLink,
                "Location":location
            }
            print(f"{title} : {jobID} : {location}")
            self.write_json(job)
        

    def findSWEJobs(self, apiChosen):
        listOfJobs = ["Software Developer","Software Engineer", "Software Intern","SDET","Developer Intern","Software co-op","Junior Developer"] 
        for i in range(11,101):
            
            for element in listOfJobs:
                self.searchJobs(apiChosen, 1, element, i)
                time.sleep(1*random.randint(1,5)+2)
    
if(__name__ == "__main__"):
    load_dotenv()
    Password = os.getenv('PASSWORD')
    Email = os.getenv('EMAIL')
    api = Linkedin(Email, Password)
    data = {"job-list": [{}]}
    with open('jobs.json', 'w') as file:
        json.dump(data, file)

    scraper = Scrape(api)
    scraper.findSWEJobs(api)
    
    