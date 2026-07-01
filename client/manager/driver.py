from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os

class Driver:
  options = webdriver.ChromeOptions()

  def __init__(self):
    chrome_bin = os.environ.get("chrome_bin")
    if chrome_bin:
      self.options.binary_location = chrome_bin

    self.options.add_argument("--headless")
    self.options.add_argument("--disable-dev-shm-usage")
    self.options.add_argument("--no-sandbox")

  def load(self):
    path = os.environ.get("chrome_driver_path")
    service = Service(executable_path=path) if path else Service()
    return webdriver.Chrome(service=service, options=self.options)
