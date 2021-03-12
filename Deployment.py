import requests
from bs4 import BeautifulSoup
import re
import random
import pandas as pd
import sys

TOP_250_URL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
IMDB_URL = 'https://www.imdb.com'


def get_source(url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(url)

    if response.status_code != 200:
        print('the following url was not found:')
        print(url)
        sys.exit(1)

    source = response.text
    soup = BeautifulSoup(source, 'lxml')

    return soup


def get_title_urls(soup):
    """ Returns a list in which each element is a dictionary that represent title with values of name and url
    """

    titles = []

    for title in soup.find_all('td', class_="titleColumn"):
        name = title.a.text
        title_url = title.a['href']
        full_title_url = IMDB_URL + title_url
        titles.append({'name' : name, 'url' : full_title_url})

    return titles

def get_directors(titles):
    """ Return list of titles where each title is a dictionary. this function adds to each dictionary a list of directors as value.
    """

    for title in titles:
        directors = []
        soup = get_source(title['url'])
        credits = soup.find('div', class_= 'credit_summary_item')

        for cred in credits.find_all('a', ):
            director = cred.text
            directors.append(director)

        title['directors'] = directors

    return titles

def main():

    top_250_soup = get_source(TOP_250_URL)
    titles = get_title_urls(top_250_soup)
    titles = get_directors(titles)

    for i, title in enumerate(titles):
        print(i,'.',title['name'],'-',', '.join(title['directors']))

if __name__ == '__main__':
    main()
