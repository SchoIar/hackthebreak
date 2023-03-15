from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def getJob(nameOfJob):
    nameOfJob = "Software Developer"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    #driver = webdriver.Chrome('./chromedriver')
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
    #TODO: Find button via xpath

    """driver.find_element(By.CSS_SELECTOR,"#filter-dateposted")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,"label.css-irr45f:nth-child(2)")#label.css-irr45f:nth-child(2)
    time.sleep(5)
    #.css-4of6ml
    driver.find_element(By.CSS_SELECTOR,".css-4of6ml")
    time.sleep(5)"""
    element = driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[1]')#button id="filter-dateposted"
    element.click()
    time.sleep(5)
    within24hours = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[1]/ul/li[1]/a')
    within24hours.click()
    time.sleep(5)
    currentUrl = driver.current_url
    time.sleep(5)
    #content = driver.find_elements(By.CLASS_NAME, 'resultContent')
    
    driver.close()



#get all jobs stored at class = resultContent

getJob('Software Developer')