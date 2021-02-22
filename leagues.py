import requests
from bs4 import BeautifulSoup
import re
import validators
import pandas as pd


def get_league_urls():
    """ Returns a list of all league urls """

    source = requests.get('https://www.proballers.com/').text
    soup = BeautifulSoup(source, 'lxml')

    league_urls = []

    for league in soup.find_all('a', href=re.compile(r"/basketball/league")):
        if validators.url(league['href']):
            league_urls.append(league['href'])

    return league_urls


def get_leagues_df(league_urls):
    """ Returns leagues table as a pandas` data frame with the columns: id, name, url
        input : list of league urls
        output: pandas data frame"""

    leagues = pd.DataFrame(columns = ['id', 'name', 'url'])
    for i in range(len(league_urls)):
        league = league_urls[i]
        league_name = league.split(r'/')[-1]
        league_id = league.split(r'/')[-2]
        leagues.loc[i] = (league_id, league_name, league)

    return leagues


def main():
    league_urls = get_league_urls()
    leagues = get_leagues_df(league_urls)
    print(leagues.sample(6))


if __name__ == '__main__':
    main()
