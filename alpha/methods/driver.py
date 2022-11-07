import os
from selenium import webdriver

class Driver:
	def __init__(self):
		self.CHROME_OPTIONS = webdriver.ChromeOptions()
		self.CHROME_OPTIONS.binary_location = os.environ.get("chrome_bin")
		self.CHROME_OPTIONS.add_argument("--headless")
		self.CHROME_OPTIONS.add_argument("--disable-dev-shm-usage")
		self.CHROME_OPTIONS.add_argument("--no-sandbox")
	
	def load(self):
		driver_path = os.environ.get("chrome_driver_path")
		return webdriver.Chrome(executable_path=driver_path, chrome_options=self.CHROME_OPTIONS)

driver = Driver().load()