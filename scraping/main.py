import json
import os
from dotenv import load_dotenv
load_dotenv()
Password = os.getenv('PASSWORD')
Email = os.getenv('EMAIL')

def read_json(filename='jobs.json'):
    with open(filename, 'r') as file:
        return json.load(file)

def write_json(data,filename='jobs.json'):
    with open(filename, 'w') as file:
        compiledData = read_json()
        compiledData["job-list"].append((data))
        json.dump(compiledData, file)


write_json()
print(read_json())

