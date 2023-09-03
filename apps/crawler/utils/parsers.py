from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlopen


class BS4:
    def __init__(self, url):
        self.url = url
        res = urlopen(self.url)
        html = res.read()
        self.soup = BeautifulSoup(html, "html.parser")

    def select(self, css_selector):
        return self.soup.select(css_selector)


class Selenium:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
    
    def close_driver(self):
        self.driver.quit()
    
        