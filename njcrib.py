import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import csv

url = "http://www.njcrib.com/PolicyCoverage/Search"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

# driver = webdriver.Chrome()

delay = 5

def scrape(name):
  driver.get(url)
  time.sleep(1)

  username = driver.find_element_by_name('EmployerName')
  username.clear()
  username.send_keys(name)

  date = driver.find_element_by_name('DateOfAccident')
  date.clear()
  date.send_keys("01/01/2019")

  button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//form/button")))
  button.click()

  try:
    a_tag = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//tbody//a")))
  except TimeoutException:
    return None

  print(a_tag.get_attribute('href'))

  a_url = a_tag.get_attribute('href')

  driver.get(a_url)

  return [
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]/td[2]"))).text,
    driver.find_element_by_xpath("//tbody/tr[2]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[3]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[4]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[5]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[6]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[7]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[8]/td[2]").text,
    driver.find_element_by_xpath("//tbody/tr[9]/td[2]").text
  ]


with open('names.csv', errors='ignore') as file:
  reader = csv.reader(file)
  headers = next(reader)

  with open('result.csv', 'w') as csvfile:
    autowriter = csv.writer(csvfile, delimiter ='|')
    autowriter.writerow(["Insured's First 10 Names", "Insured's Address", "Insurer", "Issuing Office", "Coverage ID", "Policy Number", "Policy Period", "NJ Sole Proprietors Cov", "Canc/Rein Exist"])
    for row in reader:
      name = row[0]
      start = time.time()
      if scrape(name) is None:
        continue
      autowriter.writerow(scrape(name))
      print(time.time() - start)

