from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('./chromedriver')
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
driver.close()