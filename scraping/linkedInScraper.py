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
        jobList = []
        jobs = apiChosen.search_jobs(
            keywordChosen, remote=1, limit=numberOfSearches, offset=offsetNumber)
        for job in jobs:
            companyURNid = job['companyDetails'].get('company').split(':')[-1]
            #URN id for company [number]
            companyInfo = apiChosen.get_company(companyURNid)
            #print(companyInfo['title'])
            companyLink = companyInfo['url'].split('company/')
            companyName = companyLink[1].capitalize().replace('-',' ')
            title = job['title']

            
            jobID = job['dashEntityUrn'].split(':')[-1]
            location = job['formattedLocation']
            #jobDetails = api.get_job(jobID)
            jobLink = f'https://www.linkedin.com/jobs/view/{jobID}/'

            job = {"Job Title": title,
                    "Company": companyName,
                    "Location": location,
                    "Link": jobLink, }
            #print(job)

            jobList.append(job)

        return jobList

    def findSWEJobs(self, apiChosen):
        listOfJobs = ["Software Developer", "Software Engineer", "Software Intern",
                      "SDET", "Developer Intern", "Software co-op", "Junior Developer"]
        jobsList = []
        for i in range(1, 101):
        
            for element in listOfJobs:
                jobsList.append(self.searchJobs(apiChosen, 1, element, i))
                time.sleep(1*random.randint(1, 5)+2)

        return jobsList

if (__name__ == "__main__"):
    load_dotenv()
    Password = os.getenv('PASSWORD')
    Email = os.getenv('EMAIL')
    api = Linkedin(Email, Password)
    scraper = linkedInScraper()
    scraper.findSWEJobs(api)
