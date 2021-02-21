import requests
from bs4 import BeautifulSoup
import re
import random


def get_player_id_card(player_url):
    """ Returns a dictionary of player ID card:
        input: url to player page
        output: dictionary
        example : {'p_id': '74971', 'name': 'Deni Avdija', 'Date of birth': 'Jan 3, 2001',
                    'Height': '2m05 / 6-9', 'Position': 'SF','Nationality': 'Israeli',
                    'Draft': 'round 1, pick 9 (2020)'} """

    response = requests.get(player_url)
    if response.status_code != 200:
        return

    source = response.text
    soup = BeautifulSoup(source, 'lxml')

    id_card = soup.find('div', class_="home-player__card-identity__profil__card")

    p_id = player_url.split(r'/')[-1]
    name = id_card.find('h3', itemprop="name").text.strip()

    id_card_dict = {'p_id': p_id, 'name': name}

    for parag in id_card.find_all('p', class_='home-player__card-identity__profil__card__infos__entry'):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub('\s+', ' ', words[1])
        id_card_dict[key] = value

    return id_card_dict


def test_get_player_id_card(num_of_iteration):
    """ testing get_player_id_card_function:
        calling get_player_id_card() func with different urls and printing the output.
        if there is an error, it will be stored in a set and will be printed in the end. """

    LAST_PLAYER_ID = 229373
    PLAYER_PATH = 'https://www.proballers.com/basketball/player/'

    test_players = [random.randint(1, LAST_PLAYER_ID) for i in range(num_of_iteration)]

    lst_of_players = []
    set_of_errors = set()

    for i in test_players:

        player_url = PLAYER_PATH + str(i)

        try:
            player_id = get_player_id_card(player_url)
            if player_id:
                print(player_id)
                lst_of_players.append(player_id)
        except Exception as e:
            set_of_errors.add(str(e))

    if len(set_of_errors) > 0:
        print('here is all errors from this run :')
        for e in set_of_errors:
            print('--------------\n', e)
    else:
        print('\nno errors in test run !')


def main():
    NUM_OF_ITERATIONS = 20

    test_get_player_id_card(NUM_OF_ITERATIONS)


if __name__ == '__main__':
    main()
