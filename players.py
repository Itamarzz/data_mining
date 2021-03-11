import re
import config.scrapr_config as cfg
from useful_functions import get_source

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

    id_card_dict['Height'] = get_height_in_meters(id_card_dict['Height'])

    return id_card_dict


def get_player_info_dict(lst_of_ids):
    """ Returns list of player id cards. where each id card is represented by a dictionary
    """

    player_info_dict = {}

    for player_id in lst_of_ids:
        url = cfg.PLAYER_PATH.format(player_id)
        soup = get_source(url)

        player_info = get_player_details(soup)
        player_info_dict[player_id] = {"player_on": player_id,
                                       "name": player_info["name"],
                                       "date_of_birth": player_info["Date of birth"],
                                       "height": player_info["Height"],
                                       "position": player_info["Position"],
                                       "nationality": player_info["Nationality"]}

        player_info_dict[player_id]['player_on'] = player_id

    return player_info_dict


def get_height_in_meters(height):
    """ convert height string to float
    """

    height_meters = height.split(" / ")[0]
    height_meters = height_meters.replace('m', '.')

    return float(height_meters)

