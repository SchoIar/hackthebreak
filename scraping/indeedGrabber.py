from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver = webdriver.Chrome('./chromedriver')
driver.get("https://ca.indeed.com/?r=us")
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("Software developer")
time.sleep(5)
location = driver.find_element(By.NAME, "l")
location.clear()
#location.send_keys("Vancouver, BC")
time.sleep(5)
location.send_keys(Keys.RETURN)
time.sleep(5)
#TODO: Find button via xpath
driver.find_element(By.CSS_SELECTOR,"#filter-dateposted")
time.sleep(5)
driver.find_element(By.CSS_SELECTOR,"label.css-irr45f:nth-child(2)")#label.css-irr45f:nth-child(2)
time.sleep(5)
#.css-4of6ml
driver.find_element(By.CSS_SELECTOR,".css-4of6ml")
time.sleep(5)
time.sleep(5)
driver.close()