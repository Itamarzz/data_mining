import requests
import json
import time
import config.scrapr_config as cfg
import config.api_config as apicfg
import tqdm as tq
import logging


def set_logger():
    """ set scraper module logger
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(apicfg.LOG_FILE)
    file_handler.setFormatter(apicfg.MAIN_FORMATTER)

    logger.addHandler(file_handler)

    return logger


def get_source(url):
    """ Returns a json object with the source of given url """

    response = requests.request("GET", url)
    if response.status_code not in [500, 200]:
        return None

    count_retries = 0
    while response.status_code == 500:
        count_retries += 1
        time.sleep(1)
        response = requests.get(url)
        if count_retries == cfg.MAX_RETRIES:
            api_logger.warning(f"api endpoint not found: {url}, response status code {response.status_code}")

    data = json.loads(response.text)

    return data


def get_data_player_scraper(players):
    """Returns a dict with player name and player id """

    players_list = {value["name"]: value["player_no"] for key, value in players.items()}
    return players_list


def get_data_player_api(data):
    """Returns a dict after join two columns in two columns """

    players_api_list = {values[apicfg.API_CREATE_NAME_1] + " " +
                        values[apicfg.API_CREATE_NAME_2]: values[apicfg.API_NBA_PLAYER_ID] for values in data}
    return players_api_list


def inner_join_dict(dict1, dict2):
    """Returns a dict after delete players who are not in the scrapper"""

    dict_result = {}
    for key in dict1.keys():
        if key in dict2.keys():
            dict_result[dict2[key]] = dict1[key]
        else:
            api_logger.warning(f'player {key} was not found')
    return dict_result


def get_player_details(data, season):
    """Returns a dict with player details"""

    player_detail_dict = [value[apicfg.API_NBA_PLAYERS_INFO_KEY] for value in data
                          if value[apicfg.API_NBA_SEASON_YEAR] == int(season)]

    if player_detail_dict:
        player_detail = {key: player_detail_dict[0][key] for key in player_detail_dict[0].keys()
                         & apicfg.API_NBA_PLAYERS_INFO_COLUMNS}
        return player_detail
    else:
        api_logger.warning(f'player was not found in api')
        return None


def get_players_info(players_api_ids, season):
    """Returns a dict with all player details"""

    players_dict = {}

    for player_no, player_api_id in tq.tqdm(players_api_ids.items()):
        url = apicfg.NBA_URL_PLAYER_API.format(season, player_api_id)
        data = get_source(url)

        try:
            player_info = get_player_details(data[apicfg.API_NBA_PLAYERS_JSON_KEY_1][apicfg.API_NBA_PLAYERS_JSON_KEY_2]
                                             [apicfg.API_NBA_PLAYERS_JSON_KEY_3][apicfg.API_NBA_PLAYERS_JSON_KEY_4]
                                             [apicfg.API_NBA_PLAYERS_JSON_KEY_5], season)

        except AttributeError:
            api_logger.warning(f'player id {player_no} was not found in api')
            continue
        if player_info:
            player_info["season"] = season
            player_info['player_no'] = player_no
            players_dict[player_no] = player_info

    return players_dict


def get_player_ids_data(season, players):
    """Returns a dict with player ids included in api and scraper"""

    url = apicfg.NBA_URL_TEAMS_API.format(season)
    data = get_source(url)

    players_ids_scraper = get_data_player_scraper(players)
    players_ids_api = get_data_player_api(data[apicfg.API_NBA_JSON_KEY_1][apicfg.API_NBA_JSON_KEY_2])
    players_ids = inner_join_dict(players_ids_api, players_ids_scraper)

    return players_ids


def nba_api(season, players):
    """ Returns a dictionary where key is a table names and values are dictionaries with
        nba api information
    """

    player_ids = get_player_ids_data(season, players)
    players_info = get_players_info(player_ids, season)

    data = {"player_summary_season": players_info}
    return data


LEAGUES_API = {
    "nba": nba_api
}


def api(league, season, players):
    """ Returns a dictionary corresponding api. For the moment, just nba
    """
    api_logger.info(f'api process is finished')
    data = LEAGUES_API[league](season, players)
    return data


api_logger = set_logger()
