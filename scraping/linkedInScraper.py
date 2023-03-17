import json
import os
import time
import random
from linkedin_api import Linkedin
from dotenv import load_dotenv
from toJson import *


class linkedInScraper():
    def __init__(self):
        pass

    def searchJobs(self, apiChosen, numberOfSearches, keywordChosen, offsetNumber):
        jobs = apiChosen.search_jobs(
            keywordChosen, remote=1, limit=numberOfSearches, offset=offsetNumber)
        for job in jobs:
            title = job['title']
            jobID = job['dashEntityUrn'].split(':')[-1]
            location = job['formattedLocation']
            #jobDetails = api.get_job(jobID)
            jobLink = f'https://www.linkedin.com/jobs/view/{jobID}/'

            job = {"Job Title": title,
                   "Company": ' ',
                   "Location": location,
                   "Link": jobLink, }
            print(f"{title} : {jobID} : {location}")
            # self.write_json(job)
            toJson(selectedField=job, filename='jobs.json',
                   fieldname='job-list').write_json()

    def findSWEJobs(self, apiChosen):
        listOfJobs = ["Software Developer", "Software Engineer", "Software Intern",
                      "SDET", "Developer Intern", "Software co-op", "Junior Developer"]
        for i in range(11, 101):

            for element in listOfJobs:
                self.searchJobs(apiChosen, 1, element, i)
                time.sleep(1*random.randint(1, 5)+2)


if (__name__ == "__main__"):
    load_dotenv()
    Password = os.getenv('PASSWORD')
    Email = os.getenv('EMAIL')
    api = Linkedin(Email, Password)
    scraper = linkedInScraper()
    scraper.findSWEJobs(api)
