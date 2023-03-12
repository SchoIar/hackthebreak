import json
import os
import time
import random
from linkedin_api import Linkedin
from dotenv import load_dotenv
import sys


load_dotenv()
Password = os.getenv('PASSWORD')
Email = os.getenv('EMAIL')

api = Linkedin(Email, Password)

data = {"job-list": [{}]}
with open('jobs.json', 'w') as file:
    json.dump(data, file)

def read_json(filename='jobs.json'):
    with open(filename, 'r') as file:
        return json.load(file)


def write_json(newData):
    with open('jobs.json', 'r+') as file:
        data = read_json()
        data['job-list'].append(newData)
        json.dump(data, file)

def searchJobs(numberOfSearches, keywordChosen, offsetNumber):
    jobs = api.search_jobs(keywordChosen, remote = 1, limit = \
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
        write_json(job)
    return True

for i in range(11,101):  
    searchJobs(1, "Software Developer", i)
    time.sleep(1*random.random()+random.randint(1,5))
    searchJobs(1, "Software Engineer", i)
    time.sleep(1*random.random()+random.randint(1,5))
    searchJobs(1, "Software Intern", i)
    searchJobs(1, "SDET", i)
    time.sleep(1*random.random()+random.randint(1,5))
    searchJobs(1, "Software Co-op", i)
    time.sleep(1*random.random()+random.randint(1,5))
    searchJobs(1, "Junior Developer", i)
    time.sleep(1*random.random()+random.randint(1,5))
#assert(searchJobs(3, "Software Developer") == True)



