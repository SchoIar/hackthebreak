from linkedInScraper import *
from indeedScraper import *
from toJson import *
class Scraper():
    def __init__(self):
        pass

    def scrapeIndeed(self, searchQuery):
        '''Calls the indeed scrapper & sends the data to the json file'''
        indeedJobs = indeedScraper().getJob(searchQuery)
        i = 0
        for i in range(0, len(indeedJobs)):
            toJson(selectedField=indeedJobs[i],filename="jobs.json",fieldname="job-list").write_json()
            i += 1

        return indeedJobs
        
    
    def scrapeLinkedIn(self):
        '''Scrapes LinkedIn for SWE related jobs'''
        load_dotenv()
        Password = os.getenv('PASSWORD')
        Email = os.getenv('EMAIL')
        api = Linkedin(Email, Password)
        LinkedInScraper = linkedInScraper()
        linkedInJobs = LinkedInScraper.findSWEJobs(api)
        i = 0
        for i in range(0, len(linkedInJobs)):
            toJson(selectedField=linkedInJobs[i],filename="jobs.json",fieldname="job-list").write_json()
            i += 1

        return linkedInJobs

if(__name__ == "__main__"):
    #linkedInScraper() 
    #toJson(indeedScraper('Software Developer').getJob(),'jobs.json','job-list')

    print(Scraper().scrapeIndeed('Software Developer'))
    print(Scraper().scrapeLinkedIn())

