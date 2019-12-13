import requests
from bs4 import BeautifulSoup

import pandas

#url = input('SENT FROM USER REQUEST')
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
