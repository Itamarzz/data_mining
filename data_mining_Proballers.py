#TODO: choose a website : a lot of data, frequently updated, detailful data points
#create venv: requests, beautifulsoup4, parser (lxml / html5lib)
#TODO: web scraper: get data, print collected data to the screen
#TODO: verify conventions , structure, modularity of code (parameters according to future need)
#TODO: create public github repo
#TODO: README : what website, how did we solve the problem, how to run the code
#TODO: README : reuirements text

import requests
from bs4 import BeautifulSoup


url = 'https://www.proballers.com/'
r = requests.get(url)
r.status_code
r.status_code == requests.codes.OK
requests.codes['temporary_redirect']
requests.codes.teapot
requests.codes['o/']






# Websites:
# Option 1: https://www.cbssports.com/nba/
# more options:
#     https://basketball.realgm.com/nba
#     https://www.nba.com/news
#     https://www.mmafighting.com/fight-results