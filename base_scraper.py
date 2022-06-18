import csv
import requests
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class scrapper_pure(metaclass=ABCMeta):
    """
    this class contains only basic mathhod that may be needed for general web scarping,
    pasre_json : must be implemented in all
    """
    def __init__(self,url = None):
        self.url = url
        self.data = None
    def make_request(self):

        return requests.get(self.url)

    def read_in_json(self,response,key):

        jsonFile = response.json()
        self.data = self.parse_json(jsonFile,jsonFile[key])

class scrapper_sel(metaclass=ABCMeta):
    def __init__(self, driver_path = '/usr/bin/chromedriver', ):
        self.DRIVER_PATH = driver_path
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(options = self.options, executable_path=self.DRIVER_PATH)

    def fetch_site(self, url):
        page = self.driver.get(url)

