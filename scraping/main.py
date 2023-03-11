import json
import os
from dotenv import load_dotenv
load_dotenv()
Password = os.getenv('PASSWORD')
Email = os.getenv('EMAIL')

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

jobPost = {\
"Job title":"Software Engineer",
"Compensation":"100k/yr",
"Tech stack":"Python, Bash",
"Location":"Online",
"Link":"Indeed.com/mylin"
    }
     
write_json(jobPost)


