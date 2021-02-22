import requests
from bs4 import BeautifulSoup
import re
import random
import pandas as pd


def get_source(player_url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(player_url)
    if response.status_code != 200:
        return

    source = response.text
    soup = BeautifulSoup(source, 'lxml')

    return soup


def get_player_details(soup):
    """ Returns a dictionary wtith details about player.
        input: soup object of source ('lxml')
        output: dictionary """

    id_card = soup.find('div', class_="home-player__card-identity__profil__card")

    name = id_card.find('h3', itemprop="name").text.strip()

    id_card_dict = {'name': name}

    for parag in id_card.find_all('p', class_='home-player__card-identity__profil__card__infos__entry'):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub('\s+', ' ', words[1])
        id_card_dict[key] = value

    return id_card_dict


def get_id_card(player_url):
    """ Returns a dictionary of player ID card:
        input: url to player page
        output: dictionary
        example : {'p_id': '74971', 'name': 'Deni Avdija', 'Date of birth': 'Jan 3, 2001',
                    'Height': '2m05 / 6-9', 'Position': 'SF','Nationality': 'Israeli',
                    'Draft': 'round 1, pick 9 (2020)'} """

    soup = get_source(player_url)
    if not soup:
        return
    id_card = get_player_details(soup)
    p_id = re.findall("player/([0-9]{1,10})", player_url)[0]
    id_card['id'] = p_id

    return id_card


def get_players_df(lst_of_urls):
    """ Returns pandas data frame of players id card.
        input: list of urls """

    players_df = pd.DataFrame(columns=['id', 'name', 'Date of birth', 'Height', 'Position',
                                       'Nationality', 'Draft', 'University', 'Social'])

    i = 0

    for url in lst_of_urls:
        id_card = get_id_card(url)

        if id_card:
            print('adding to df:')
            print(id_card)
            players_df.loc[i] = id_card
            i += 1

    return (players_df)


# ---------Tests -----------

def test_get_id_card_single():
    """test single input to test_get_id_card function """

    test_url = 'https://www.proballers.com/basketball/player/74971'
    test_card = {'name': 'Deni Avdija', 'Date of birth': 'Jan 3, 2001', 'Height': '2m05 / 6-9', 'Position': 'SF',
                 'Nationality': 'Israeli', 'Draft': 'round 1, pick 9 (2020)', 'id': '74971'}
    print(test_card)
    assert get_id_card(test_url) == test_card
    print('single test for get_id_card passed!')


def test_get_players_df(num_of_iteration):
    """ testing get_player_id_card_function:
        calling get_player_id_card() func with different urls and printing the output.
        if there is an error, it will be stored in a set and will be printed in the end. """

    LAST_PLAYER_ID = 229373
    PLAYER_PATH = 'https://www.proballers.com/basketball/player/'

    test_players = [random.randint(1, LAST_PLAYER_ID) for i in range(num_of_iteration)]

    set_of_errors = set()
    list_of_errors_p_id = []
    set_of_columns = set()

    for p_id in test_players:
        player_url = [PLAYER_PATH + str(p_id)]
        try:
            df = get_players_df(player_url)
            set_of_columns = set_of_columns.union(set(df.columns))
        except Exception as e:
            set_of_errors.add(str(e))
            list_of_errors_p_id.append(p_id)

    if len(set_of_errors) > 0:
        print('here is all errors from this run :')
        for e in set_of_errors:
            print('--------------\n', e)
        print('players IDs which got error:\n', list_of_errors_p_id)
    else:
        print('\nno errors in test run !')

    assert set_of_columns == {'id', 'name', 'Date of birth', 'Height', 'Position', 'Nationality', 'Draft', 'University',
                              'Social'}


# test_get_id_card_single()
# test_get_players_df(5)

def main():
    LAST_PLAYER_ID = 229373
    PLAYER_PATH = 'https://www.proballers.com/basketball/player/'

    player_urls = [PLAYER_PATH + str(p_id) for p_id in range(1, LAST_PLAYER_ID, 1000)]
    players_df = get_players_df(player_urls)

    print(players_df)


if __name__ == '__main__':
    main()
