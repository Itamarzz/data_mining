#TODO: choose a website : a lot of data, frequently updated, detailful data points
#create venv: requests, beautifulsoup4, parser (lxml / html5lib)
#TODO: web scraper: get data, print collected data to the screen
#TODO: verify conventions , structure, modularity of code (parameters according to future need)
#TODO: create public github repo
#TODO: README : what website, how did we solve the problem, how to run the code
#TODO: README : reuirements text

import requests
from bs4 import BeautifulSoup
import re
import validators
import pandas as pd

def get_league_urls():
    """ Returns a list of all league urls """

    source = requests.get('https://www.proballers.com/').text
    soup = BeautifulSoup(source, 'lxml')

    league_urls= []
    league_urls.append('https://www.proballers.com/basketball/league/177/euroleague') # euroleague is a standalone league

    for league in soup.find_all('a', href=re.compile(r"/basketball/league")):
        if validators.url(league['href']):
            league_urls.append(league['href'])

    return league_urls

def get_leagues_df(league_urls):
    """ Returns leagues table as a panda's data frame with the columns: id, name, url
        input : list of league urls """
        # TODO add Country of league and continent (america, wnba, europe etc.)

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
    print(leagues[['id', 'name']].head())


if __name__ == '__main__':
    main()



# Websites:
# Option 1: https://www.cbssports.com/nba/
# more options:
#     https://basketball.realgm.com/nba
#     https://www.nba.com/news
#     https://www.mmafighting.com/fight-results