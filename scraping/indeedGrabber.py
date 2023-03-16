from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

class indeedScraper():

    def __init__(self):
        pass

    def getJob(self, nameOfJob):
        '''Scrapes jobs from Indeed returning a list with their names.'''

        nameOfJob = "Software Developer"
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get("https://ca.indeed.com/?r=us")
        elem = driver.find_element(By.NAME, "q")
        elem.clear()
        elem.send_keys(nameOfJob)
        time.sleep(5)
        location = driver.find_element(By.NAME, "l")
        location.clear()
        #location.send_keys("Vancouver, BC")
        time.sleep(5)
        location.send_keys(Keys.RETURN)
        time.sleep(5)

        element = driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[1]')#button id="filter-dateposted"
        element.click()
        time.sleep(5)
        within24hours = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[1]/ul/li[1]/a')
        within24hours.click()
        time.sleep(5)
        currentUrl = driver.current_url
        print(currentUrl)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = soup.find_all("td",{"class":"resultContent"})
        for job in jobs:
            name = job.find("span")['title']
            company = job.find("span",{"class":"companyName"}).string
            location = job.find("div",{"class":"companyLocation"}).string
            linkID = job.a["data-jk"]
            link = 'https://ca.indeed.com/viewjob?jk=' + str(linkID)
            #https://ca.indeed.com/viewjob?jk=
            print(f'{name} at {company}, {location}, from {link}')#{link}')
        time.sleep(5)
        #content = driver.find_elements(By.CLASS_NAME, 'resultContent')
        
        driver.close()

if(__name__ == "__main__"):
    indeedScraper().getJob('Software Developer')