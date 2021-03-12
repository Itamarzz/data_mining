import re
import numpy as np
import config.scrapr_config as cfg
import config.database_config as dbcfg
from useful_functions import get_source, insert_rows, progress_bar, remove_existing_keys

PLAYER_PROFILE_CLASS = "home-player__card-identity__profil__card"
PLAYER_INFO_CLASS = 'home-player__card-identity__profil__card__infos__entry'


def get_player_details(soup):
    
    """ Returns a dictionary with details about player.
        input: soup object of source ('lxml')
        output: dictionary """

    id_card = soup.find('div', class_=PLAYER_PROFILE_CLASS)

    name = id_card.find('h3', itemprop="name").text.strip()

    id_card_dict = {'name': name}

    for parag in id_card.find_all('p', class_=PLAYER_INFO_CLASS):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub('\s+', ' ', words[1])
        id_card_dict[key] = value

    if '-' == id_card_dict['Height'].strip():
        id_card_dict['Height'] = np.nan
    else:
        id_card_dict['Height'] = get_height_in_meters(id_card_dict['Height'])

    return id_card_dict


def get_player_info_dict(lst_of_ids):
    
    """ Returns list of player id cards. where each id card is represented by a dictionary
    """

    player_info_dict = {}

    for player_id in lst_of_ids:
        url = cfg.PLAYER_PATH.format(player_id)
        soup = get_source(url)

        if not soup:
            continue

        player_info = get_player_details(soup)
        player_info_dict[player_id] = {"player_no": player_id,
                                       "name": player_info["name"],
                                       "date_of_birth": player_info["Date of birth"],
                                       "height": player_info["Height"],
                                       "position": player_info["Position"],
                                       "nationality": player_info["Nationality"]}

    return player_info_dict


def get_height_in_meters(height):
    
    """ convert height string to float
    """

    height_meters = height.split(" / ")[0]
    height_meters = height_meters.replace('m', '.')

    return float(height_meters)


def save_teams(players_id, connection, chunk_size):
    """ insert to database. scrapped date into the teams table
    """
    
    if not cfg.SILENT_MODE:
        print("Save players...")

    players_id = remove_existing_keys(dbcfg.PLAYERS_TABLE_NAME, players_id)
    players_details = get_player_info_dict(players_id)

    if len(players_details) > 0:
        if not cfg.SILENT_MODE:
            print("Get players details list passed!")

        data_type = {
            'player_no': 'int',
            'name': 'str',
            'date_of_birth': 'date',
            'height': 'float',
            'position': 'str',
            'nationality': 'str'
        }
        insert_rows(players_details, dbcfg.PLAYERS_TABLE_NAME, connection, chunk_size, data_types=data_type)
        if not cfg.SILENT_MODE:
            print("Insert players rows passed!")

    else:
        if not cfg.SILENT_MODE:
            print("Not news players")
        else:
            pass
