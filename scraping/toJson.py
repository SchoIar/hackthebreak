import json
import os
import time
import random

class toJson():

    def __init__(self, selectedField, filename):
        self.selectedFields = selectedField
        self.filename = filename
        ''' data = {"job-list": [{}]}
        with open(filename, 'w') as file:
            json.dump(data, file)'''
    
    def reset_file(self):
        data = {"job-list": [{}]}
        with open(self.filename, 'w') as file:
            json.dump(data, file)
        
    def read_json(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def write_json(self):
        with open(self.filename, 'r+') as file:
            data = self.read_json()
            data['job-list'].append(self.selectedFields)
            file.seek(0)
            json.dump(data, file, indent = 2)

if(__name__ == "__main__"):
    toJson(selectedField={'A':'B'},filename='jobs.json').write_json()