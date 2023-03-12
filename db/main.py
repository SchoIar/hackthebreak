import json
import os
import time
import random
from linkedin_api import Linkedin
from dotenv import load_dotenv
from SQLManager import SQLManager


load_dotenv()
Password = os.getenv('PASSWORD')
Email = os.getenv('EMAIL')
api = Linkedin(Email, Password)
sql = SQLManager()

def searchJobs(numberOfSearches, keywordChosen, offsetNumber):
    jobs = api.search_jobs(keywordChosen, remote = 1, limit = \
                           numberOfSearches, offset = offsetNumber)
    for job in jobs:
        title = job['title']
        jobID = job['dashEntityUrn'].split(':')[-1] 
        location = job['formattedLocation']
        jobLink = f'https://www.linkedin.com/jobs/view/{jobID}/'

        sql.newJob(str(jobID), jobLink, title, location)
        
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



