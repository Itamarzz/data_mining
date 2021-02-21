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
from dateutil.parser import parse

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


def get_player_id_card(player_url):
    """ Returns a dictionary of player ID card:
        input: url to player page
        output: dictionary
        example : {'id': '74971', 'name': 'Deni Avdija', 'Date of birth': 'Jan 3, 2001',
                'Height': '2m05 / 6-9', 'Position': 'SF','Nationality': 'Israeli',
                'Draft': 'round 1, pick 9 (2020)'} """

    source = requests.get(player_url).text
    soup = BeautifulSoup(source, 'lxml')

    id_card = soup.find('div', class_="home-player__card-identity__profil__card")

    id = player_url.split(r'/')[-2]
    name = id_card.find('h3', itemprop = "name").text.strip()

    id_card_dict ={'id' : id, 'name' : name}

    for parag in id_card.find_all('p', class_ = 'home-player__card-identity__profil__card__infos__entry'):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub('\s+',' ',words[1])
        id_card_dict[key] = value

    return id_card_dict

def get_player_id_dict(id_card):
    """ receives player_id_card as a dictionary with raw data
        returns : dictionary after setting suitable data type for each value """
    id_dict = {}
    id_dict['id'] = int(id_card['id'])
    id_dict['name'] = id_card['name']
    id_dict['date_of_birth'] = parse(id_card['Date of birth']).date()
    id_dict['height'] = get_height_meters(id_card['Height'])
    id_dict['position'] = id_card['Position']
    id_dict['position'] = id_card['Position']
    id_dict['nationality'] = id_card['Nationality']
    id_dict['draft'] = id_card['Draft']

    return id_dict

def get_height_meters(height):
    """ Returns height in meters as a float.
        input: string of height in meters and feet
        output: float """

    height_m = height.split(' / ')[0]
    height_m = height_m.replace('m', '.')
    height_m = float(height_m)

    return  height_m


def main():
#     league_urls = get_league_urls()
#     leagues = get_leagues_df(league_urls)
#     print(leagues[['id', 'name']].head())
    test_player_url = 'https://www.proballers.com/basketball/player/74971/deni-avdija'
    test_player_url = 'https://www.proballers.com/basketball/player/19067'
    test_player_id = get_player_id_card(test_player_url)
    print(test_player_id)

#
#
if __name__ == '__main__':
    main()



# Websites:
# Option 1: https://www.cbssports.com/nba/
# more options:
#     https://basketball.realgm.com/nba
#     https://www.nba.com/news
#     https://www.mmafighting.com/fight-results