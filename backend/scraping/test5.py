from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import pandas as pd
from datetime import date
from datetime import datetime
import time
import requests
import random

url = "https://www.kayak.com/flights/YYC-YVR/2022-11-14?sort=depart_a&fs=stops=0"
print("\n" + url)

chrome_options = webdriver.ChromeOptions()
agents = ["Firefox/63.0.3","Chrome/73.0.3683.68","Edge/16.16299"]
browser_choice = random.randint(0,2)
print("User agent: " + agents[(browser_choice%len(agents))])
chrome_options.add_argument('--user-agent=' + agents[(browser_choice%len(agents))] + '"')    
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
driver.implicitly_wait(20)
driver.get(url)

#Check if Kayak thinks that we're a bot
time.sleep(5) 
soup=BeautifulSoup(driver.page_source, 'lxml')

if soup.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
    print("Kayak thinks I'm a bot, which I am ... so let's wait a bit and try again")
    driver.close()
    time.sleep(20)
    exit()

time.sleep(20) #wait 20sec for the page to load

# soup=BeautifulSoup(driver.page_source, 'lxml')
# data = soup.find_all('div', attrs={'class': 'inner-grid keel-grid'})
urls = []
# traverse list
elements = driver.find_elements(By.TAG_NAME, "a")
for el in elements:
    urls.append(el.get_attribute("href"))

urls_clean = []
urls_clean_no_duplicates = []
final_urls = []
# for link in soup.find_all('a', href=True):
#     urls.append(link['href'])
for i in range(len(urls)):
    if urls[i] == None:
        continue
    if "javascript" in urls[i]:
        continue
    if "/book/" in urls[i]:
        urls_clean.append(urls[i])
        
for i in urls_clean:
  if i not in urls_clean_no_duplicates:
    urls_clean_no_duplicates.append(i)

for url in urls_clean_no_duplicates:
    print(url)
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(random.randint(3,8))
    print(driver.current_url)
    final_urls.append(driver.current_url)


print(final_urls)