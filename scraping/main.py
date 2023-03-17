from linkedInScraper import *
from indeedScraper import *
from toJson import *
class scraper():
    def __init__():
        pass

if(__name__ == "__main__"):
    #linkedInScraper() 
    #toJson(indeedScraper('Software Developer').getJob(),'jobs.json','job-list')
    indeedScraper('Software Engineer').getJob('Software Developer')
    print('done')
    
