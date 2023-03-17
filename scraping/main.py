from linkedInScraper import *
from indeedScraper import *
from toJson import *
class scraper():
    def __init__(self):
        pass

    def scrapeIndeed(self, searchQuery):
        indeedJobs = indeedScraper().getJob(searchQuery)
        i = 0
        for i in range(0, len(indeedJobs)):
            print(f'{indeedJobs[i]} \n')
            toJson(selectedField=indeedJobs[i],filename="jobs.json",fieldname="job-list").write_json()
            i += 1
        print(indeedJobs)

if(__name__ == "__main__"):
    #linkedInScraper() 
    #toJson(indeedScraper('Software Developer').getJob(),'jobs.json','job-list')
    scraper().scrapeIndeed('Software Developer')

    
