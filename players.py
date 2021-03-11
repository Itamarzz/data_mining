import requests
from bs4 import BeautifulSoup
import re


PLAYER_PROFILE_CLASS = "home-player__card-identity__profil__card"
PLAYER_INFO_CLASS = 'home-player__card-identity__profil__card__infos__entry'
PLAYER_PATH = 'https://www.proballers.com/basketball/player/'
LAST_PLAYER_ID = 229373


def get_source(player_url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(player_url)

    if response.status_code == 200:
        source = response.text
        soup = BeautifulSoup(source, 'lxml')

        return soup


def get_player_details(soup):
    """ Returns a dictionary with details about player.
        input: soup object of source ('lxml')
        output: dictionary """

    id_card = soup.find('div', class_= PLAYER_PROFILE_CLASS)

    name = id_card.find('h3', itemprop="name").text.strip()

    id_card_dict = {'name': name}

    for parag in id_card.find_all('p', class_= PLAYER_INFO_CLASS):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub('\s+', ' ', words[1])
        id_card_dict[key] = value

    id_card_dict['Height'] = get_height_in_meters(id_card_dict['Height'])

    return id_card_dict


def get_player_info_dict(lst_of_ids):
    """ Returns list of player id cards. where each id card is represented by a dictionary
    """

    player_info_dict = {}

    for player_id in lst_of_ids :
        url = PLAYER_PATH + str(player_id)
        soup = get_source(url)

        if not soup:
            continue

        player_info = get_player_details(soup)
        player_info_dict[player_id] = player_info

    return player_info_dict


def get_height_in_meters(height):
    """ convert height string to float
    """

    height_meters = height.split(" / ")[0]
    height_meters = height_meters.replace('m', '.')

    return float(height_meters)





############## TESTS #####################

# test run on some range:

# lst_of_ids = [x for x in range(1, LAST_PLAYER_ID, 17532)]
#
# player_info_dict = get_player_info_dict(lst_of_ids)
#
# print(player_info_dict)


# ---------Tests -----------

# def test_get_id_card_single():
#     """test single input to test_get_id_card function """
#
#     test_url = 'https://www.proballers.com/basketball/player/74971'
#     test_card = {'name': 'Deni Avdija', 'Date of birth': 'Jan 3, 2001', 'Height': 2.05, 'Position': 'SF',
#                  'Nationality': 'Israeli', 'Draft': 'round 1, pick 9 (2020)', 'id': '74971'}
#     print(test_card)
#     assert get_id_card(test_url) == test_card
#     print('single test for get_id_card passed!')


# def test_get_players_df(num_of_iteration):
#     """ testing get_player_id_card_function:
#         calling get_player_id_card() func with different urls and printing the output.
#         if there is an error, it will be stored in a set and will be printed in the end. """
#
#     LAST_PLAYER_ID = 229373
#     PLAYER_PATH = 'https://www.proballers.com/basketball/player/'
#
#     test_players = [random.randint(1, LAST_PLAYER_ID) for i in range(num_of_iteration)]
#
#     set_of_errors = set()
#     list_of_errors_p_id = []
#     set_of_columns = set()
#
#     for p_id in test_players:
#         player_url = [PLAYER_PATH + str(p_id)]
#         try:
#             df = get_players_df(player_url)
#             set_of_columns = set_of_columns.union(set(df.columns))
#         except Exception as e:
#             set_of_errors.add(str(e))
#             list_of_errors_p_id.append(p_id)
#
#     if len(set_of_errors) > 0:
#         print('here is all errors from this run :')
#         for e in set_of_errors:
#             print('--------------\n', e)
#         print('players IDs which got error:\n', list_of_errors_p_id)
#     else:
#         print('\nno errors in test run !')
#
#     assert set_of_columns == {'id', 'name', 'Date of birth', 'Height', 'Position', 'Nationality', 'Draft', 'University',
#                               'Social'}

