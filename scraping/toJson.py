import json
import os
import time
import random
class toJson():
    """Appends selected Fieldname to specified filename, under selected field """

    def __init__(self, selectedField, filename, fieldname):
        self.selectedFields = selectedField
        self.filename = filename
        self.fieldname = fieldname

    def reset_file(self):
        data = {"job-list": []}
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def read_json(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def write_json(self):
        with open(self.filename, 'r+') as file:
            data = self.read_json()
            data[self.fieldname].append(self.selectedFields)
            file.seek(0)
            json.dump(data, file, indent=3)

if (__name__ == "__main__"):
    # toJson(selectedField={'A':'B'},filename='jobs.json',fieldname='job-list').reset_file() #clear file
    toJson(selectedField={'A': 'B'}, filename='jobs.json',
           fieldname='job-list').write_json()
