import os
from selenium import webdriver
from .commands import commands
from .system import system
from .responses import responses

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.binary_location = os.environ.get("chrome_bin")
CHROME_OPTIONS.add_argument("--headless")
CHROME_OPTIONS.add_argument("--disable-dev-shm-usage")
CHROME_OPTIONS.add_argument("--no-sandbox")
DRIVER = webdriver.Chrome(executable_path=os.environ.get('chrome_driver_path'), chrome_options=CHROME_OPTIONS)