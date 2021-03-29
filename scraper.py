import requests
import config.scrapr_config as cfg
from bs4 import BeautifulSoup
import time
import tqdm as tq
from config import database_config as dbcfg
import database as db
import re
import pandas as pd


# usful functions

def get_source(url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(url)
    if response.status_code not in [500, 200]:
        return None

    count_retries = 0
    while response.status_code == 500:
        count_retries += 1
        time.sleep(1)
        response = requests.get(url)
        if count_retries == cfg.MAX_RETRIES:
            return None

    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_keys_from_table(table):
    """ returns df as a result of sql select query
    """

    sql = f"SELECT * FROM {table}"
    con = db.connect_sql()
    db.execute_sql("USE proballers", con)
    df = pd.read_sql(sql, con)
    if len(df) == 0:
        return []
    return df.iloc[:, 0].tolist()


def remove_existing_keys(table, keys):
    """ returns list of keys that do not already exist in the database
    """

    lst_db = get_keys_from_table(table)
    new_lst = [key for key in keys if key not in lst_db]

    return new_lst


def get_pagination(soup):
    """ Returns the number of  sub-pages of a given page as a soup instance
    """

    pages = soup.find_all("a", {"class": cfg.SEARCH_PAGINATION_BY_CLASS})[-1].get_text()

    return int(pages)


# seasons

def get_seasons_list(league_id, league_name):
    """ Returns a list of available seasons for league
    """

    soup = get_source(cfg.TEAMS_PATH.format(league_id, league_name, 0))
    seasons = []
    for div in soup.find_all("div", {"class": "card card-body"}):
        for link in div.select("a"):
            seasons.append(link['href'].split("/")[5])
    return seasons


# Leagues

def get_leagues():
    """ Returns a dictionary of all available leagues for scrapping from the Proballers website
        where league_id is the key and league_name is the value.
    """

    soup = get_source(cfg.URL_ALL_LEAGUES)
    leagues_dict = {}
    for league in soup.find_all('a', {"title": cfg.SEARCH_LINK_BY_TITLE}):
        url = league.get('href').split("/")
        leagues_dict[url[cfg.ID_LEAGUE_INDEX]] = url[cfg.NAME_LEAGUE_INDEX]

    return leagues_dict


# teams

def get_teams_per_season(soup):
    """ Returns list of team IDs that participated in a specific league and season,
        given a soup instance of the league and season webpage.
    """

    team_ids = []
    for link in soup.find_all('a', class_=cfg.SEARCH_TEAM_BY_CLASS):
        team_ids.append(int(link['href'].split("/")[cfg.ID_TEAM_INDEX]))

    return team_ids


def get_team_details(soup):
    """Returns a dictionary with team details (name, country)
        for a given soup instance of team page.
    """

    team_description = soup.find('div', class_=cfg.SEARCH_TEAM_INFO_BY_CLASS)
    team_name = soup.find(class_=cfg.SEARCH_TEAM_NAME_BY_CLASS).get_text()
    team_country = team_description.find('p').get_text().split("\n")[cfg.COUNTRY_TEAM_INDEX]
    team = {"name": team_name, "country": team_country}

    return team


def teams_scraper(league_id, league_name, season):
    """ Returns a dictionary of teams which participated in a given league and season.
        format: {team_id: {team_id : id, team_name: name, country: country}}
    """

    url = cfg.TEAMS_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    if not soup:
        raise TypeError("The website is not responding in this moment. \
                        Try again in few minutes or try different league")

    team_ids = get_teams_per_season(soup)
    team_ids = remove_existing_keys(dbcfg.TEAMS_TABLE_NAME, team_ids)

    teams_dict = {}
    for team_id in tq.tqdm(team_ids):
        url = cfg.TEAM_PATH.format(team_id)
        soup = get_source(url)

        if not soup:
            continue

        team = get_team_details(soup)
        team["team_no"] = team_id
        teams_dict[team_id] = team

    return teams_dict


# Players

def get_player_details(soup):
    """ Returns a dictionary with details about player.
        input: soup object of source ('lxml')
        output: dictionary """

    id_card = soup.find('div', class_=cfg.PLAYER_PROFILE_CLASS)

    name = id_card.find('h3', itemprop="name").text.strip()

    id_card_dict = {'name': name}

    for parag in id_card.find_all('p', class_=cfg.PLAYER_INFO_CLASS):
        words = [w.strip() for w in parag.text.split(':')]
        key = words[0]
        value = re.sub(r'\s+', ' ', words[1])
        id_card_dict[key] = value

    return id_card_dict


def get_player_dict(player_info):
    """Retruns a dictionary with relevant player info and renamed field
    """

    player_dict = {"name": player_info["name"],
                   "date_of_birth": player_info["Date of birth"],
                   "height": player_info["Height"],
                   "position": player_info["Position"],
                   "nationality": player_info["Nationality"]}

    return player_dict


def players_scraper(player_ids):
    """ Returns a dictionary of player id cards. where each id card is represented by a dictionary
    """

    player_ids = remove_existing_keys(dbcfg.PLAYERS_TABLE_NAME, player_ids)

    players_dict = {}

    for player_id in tq.tqdm(player_ids):
        url = cfg.PLAYER_PATH.format(player_id)
        soup = get_source(url)

        try:
            player_info = get_player_details(soup)
        except AttributeError:
            continue
        player_dict = get_player_dict(player_info)
        player_dict['player_no'] = player_id
        players_dict[player_id] = player_dict

    return players_dict


# Games

def get_game_ids_in_page(soup):
    """ Returns a list of game IDs of league, season and page number
        from given instance of soup of page.
    """

    games = []
    for div in soup.find_all("div", class_=cfg.SEARCH_GAMES_IDS_BY_CLASS):
        for link in div.select("a"):
            if cfg.GAME_NAME in link['href']:
                games.append(int(link['href'].split("/")[cfg.ID_GAME_INDEX]))

    return games


def get_game_ids(league_id, league_name, season, pages):
    """ Returns a list of all game IDs that have been played in given league and season
    """

    game_ids = []

    for page in range(1, pages + 1):
        url = cfg.GAMES_PATH.format(league_id, league_name, season) + "/" + str(page)
        soup = get_source(url)
        if not soup:
            raise TypeError("The website is not responding in this moment. \
                            Try again in few minutes or try different league")

        game_ids_in_page = get_game_ids_in_page(soup)
        game_ids += game_ids_in_page

    return game_ids


def get_team_game_details(soup):
    """ Returns a dictionary with general information about game:
        scores, teams etc.
    """

    game = {}
    teams = []
    for team in soup.find_all('a', class_=cfg.SEARCH_GAME_TEAMS_BY_CLASS):
        teams.append(team['href'].split("/")[3])
    local_team, visit_team = teams

    span_info = []
    for div in soup.find_all("div", class_=cfg.SEARCH_GAME_RESULT_BY_CLASS):
        for span in div.select('span'):
            span_info.append(span.get_text())

    match_date, scores, status = span_info
    local_score, visit_score = scores.split(" - ")

    game['local_team'] = local_team
    game['visit_team'] = visit_team
    game['match_date'] = match_date
    game['local_score'] = local_score
    game['visit_score'] = visit_score

    return game


def get_team_game_dict(game, game_id):
    """Returns a dictionary where the key is team_game_id and the value is
            a dictionary with details about team in game: score, win or lose, etc."""

    local_team = {'game_no': game_id, 'team_no': game['local_team'], 'score': game['local_score'],
                  'win': game['local_score'] > game['visit_score'], 'home': True,
                  'team_game_id': str(game_id) + 'l'}

    visit_team = {'game_no': game_id, 'team_no': game['visit_team'], 'score': game['visit_score'],
                  'win': game['visit_score'] > game['local_score'], 'home': False,
                  'team_game_id': str(game_id) + 'v'}

    team_games = {str(game_id) + 'l': local_team, str(game_id) + 'v': visit_team}

    return team_games


def get_game_stats_details(game_id, soup):
    """Returns a list of dictionaries where each dictionary represent player stats from game
    """

    player_stats = []

    for table_team in ["1", "2"]:
        for tr in soup.find("div", class_="home-game__content__team-stats__content-team-" + table_team).select(
                'tbody tr'):
            player_id = tr.select("td a")[0]['href'].split("/")[3]
            stats = []

            for td in tr.find_all("td", class_="right"):
                stats.append(td.get_text())

            if table_team == "1":
                team_game_id = str(game_id) + 'l'
            else:
                team_game_id = str(game_id) + 'v'

            player_row = get_player_stats_dictionary(stats)
            player_row["player_no"] = int(player_id)
            player_row["team_game_id"] = team_game_id
            player_stats.append(player_row)

    return player_stats


def get_player_stats_dictionary(stats):
    """ Return a dictionary of player stats from a row in the team stats given as a list.
    """

    plyar_stats = dict(zip(cfg.HEADERS_TEAM_STATS, stats))
    plyar_stats["2m"], plyar_stats["2a"] = plyar_stats["2M-2A"].split('-')
    plyar_stats["3m"], plyar_stats["3a"] = plyar_stats["3M-3A"].split('-')
    plyar_stats["1m"], plyar_stats["1a"] = plyar_stats["1M-1A"].split('-')

    return plyar_stats


def get_game_details(game_id):
    """ returns details of one game, given game id:
        1. game info: dictionary with general info of the game: date etc.
        2. team games: dictionary where the key is team_game_id and the value is
            a dictionary with details about team in game: score, win or lose, etc.
        3. player stats: list of dictionary where each dictionary represents player stats in the game
    """
    url = cfg.GAME_PATH.format(game_id)
    soup = get_source(url)

    if not soup:
        return None

    game = get_team_game_details(soup)
    team_games = get_team_game_dict(game, game_id)
    player_stats = get_game_stats_details(game_id, soup)
    game_info = {'game_date': game['match_date']}

    return game_info, team_games, player_stats


def get_game_dict(league_id, season, game_id, games_info):
    """ Returns a dictionary with games info """

    games_info['league'] = league_id
    games_info['season'] = season
    games_info['game_no'] = game_id

    return games_info


def games_scraper(league_id, league_name, season, game_limit):
    """Returns a dictionary of games played in league and season
    """

    url = cfg.GAMES_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    if not soup:
        raise TypeError("The website is not responding in this moment. \
                        Try again in few minutes or try different league")

    pages = get_pagination(soup)
    game_ids = get_game_ids(league_id, league_name, season, pages)
    game_ids = remove_existing_keys(dbcfg.GAMES_TABLE_NAME, game_ids)

    if game_limit <= len(game_ids):
        game_ids = game_ids[: game_limit]

    games = {}
    teams_games = {}
    player_stats = []

    for game_id in tq.tqdm(game_ids):
        result = get_game_details(game_id)
        if not result:
            continue

        games_info, team_games, player_stats_in_game = result

        games[game_id] = get_game_dict(league_id, season, game_id, games_info)
        teams_games.update(team_games)
        player_stats += player_stats_in_game

    return games, team_games, player_stats


def scraper(league_no, league_name, season, games_limit=cfg.GAME_LIMIT):
    """ scrape something """

    teams = teams_scraper(league_no, league_name, season)
    games, team_games, player_stats = games_scraper(league_no, league_name, season, games_limit)
    player_ids = set([player['player_no'] for player in player_stats])
    player_ids = remove_existing_keys('players', player_ids)
    players = players_scraper(player_ids)

    return teams, games, team_games, player_stats, players

r = scraper(177, 'euroleague', 2006, 5)
for a in r:
    print('#####################')
    print(a)