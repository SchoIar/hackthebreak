import json
import os
import time
import random
from linkedin_api import Linkedin
from dotenv import load_dotenv
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


jobPost = {
    "Job title": "Software Engineer",
    "Compensation": "100k/yr",
    "Tech stack": "Python, Bash",
    "Location": "Online",
    "Link": "Indeed.com/mylin"
}



"""jobs = []
for i in range(1,11):#scale this up later
    job = api.search_jobs(keywords='Developer', remote = True, limit = 1, offset = i)
    time.sleep(5*random.random() + 2)
    jobs.append(job)

for element in jobs:
    title = element['title']
    print(title)"""

jobs = api.search_jobs(keywords = 'Developer', remote = True, limit = 2, offset = 1)
for job in jobs:
    title = job['title']
    jobID = job['dashEntityUrn'].split(':')[-1]
    #jobDetails = api.get_job(jobID)
    jobLink = f'https://www.linkedin.com/jobs/view/{jobID}/'
    job = {
        "Job title":title,
        "Job link":jobLink
    }
    if(title.lower().find('software') == True or title.lower().find('engineer') == True or title.lower().find('qa') == True or title.lower().find('developer') == True):
        write_json(job)
    else:
        print(title)
        write_json(job)

