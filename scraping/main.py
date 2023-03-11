import json
import os
from dotenv import load_dotenv
load_dotenv()
Password = os.getenv('PASSWORD')
Email = os.getenv('EMAIL')

def read_json(filename='jobs.json'):
    with open(filename, 'r') as file:
        return json.load(file)


print(read_json())
