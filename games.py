import config.scrapr_config as cfg
import config.database_config as dbcfg
import players
from useful_functions import get_source, insert_rows, progress_bar, remove_existing_keys


def get_pagination(league_id, league_name, season):
    """ Returns the number of game pages that exist for a league in a specific season
    """
    url = cfg.GAMES_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    if soup is None:
        raise TypeError("The website is not responing in this moment.")  # TODO: corregir texto

    pagination = soup.find_all("a", {"class": cfg.SEARCH_PAGINATION_BY_CLASS})[-1].get_text()
    return int(pagination)


def get_game_ids(league_id, league_name, season, page):
    """ Returns a list with all game IDs from a league, season and page number
    """
    url = cfg.GAMES_PATH.format(league_id, league_name, season) + "/" + str(page)
    soup = get_source(url)

    if soup is None:
        raise TypeError("The website is not responing in this moment.")  # TODO: corregir texto

    games = []
    for div in soup.find_all("div", class_=cfg.SEARCH_GAMES_IDS_BY_CLASS):
        for link in div.select("a"):
            if cfg.GAME_NAME in link['href']:
                games.append(int(link['href'].split("/")[cfg.ID_GAME_INDEX]))
    return games


def get_game_details(game_id):
    """ returns a list with details (local_team, visit_team, match_date, local_score, visit_score)
        for a given game.
    """
    url = cfg.GAME_PATH.format(game_id)
    soup = get_source(url)

    if not soup:
        return None

    teams = []
    for team in soup.find_all('a', class_=cfg.SEARCH_GAME_TEAMS_BY_CLASS):
        teams.append(team['href'].split("/")[3])
    local_team, visit_team = teams

    span_info = []
    for div in soup.find_all("div", class_=cfg.SEARCH_GAME_RESULT_BY_CLASS):
        for span in div.select('span'):
            span_info.append(span.get_text())

    match_date, teams, status = span_info
    local_score, visit_score = teams.split(" - ")

    headers_team_stats = ["minuets", "2M-2A", "3M-3A", "FG%", "1M-1A", "1%", "o_r",
                          "dr", "reb", "ast", "stl", "blk", "fo", "pts", "eff"]
    player_stats = []
    for table_team in ["1", "2"]:
        if table_team == "1":
            team_game_id = str(game_id) + 'l'
        else:
            team_game_id = str(game_id) + 'v'

        for tr in soup.find("div", class_="home-game__content__team-stats__content-team-"+table_team).select('tbody tr'):
            player_id = tr.select("td a")[0]['href'].split("/")[3]
            stats = []
            for td in tr.find_all("td", class_="right"):
                stats.append(td.get_text())

            table_rows = dict(zip(headers_team_stats, stats))
            table_rows["2m"], table_rows["2a"] = table_rows["2M-2A"].split('-')
            table_rows["3m"], table_rows["3a"] = table_rows["3M-3A"].split('-')
            table_rows["1m"], table_rows["1a"] = table_rows["1M-1A"].split('-')

            delete_rows = ["FG%", "1%", "2M-2A", "3M-3A", "1M-1A", "reb"]
            for delete_row in delete_rows:
                del table_rows[delete_row]

            table_rows["player_no"] = int(player_id)
            table_rows["team_game_id"] = team_game_id
            player_stats.append(table_rows)

    game_info = {'game_date': match_date}
    team_games = {str(game_id)+'l': {'game_no': game_id,
                                     'team_no': local_team,
                                     'score': local_score,
                                     'win': local_score > visit_score,
                                     'home': True,
                                     'team_game_id': str(game_id)+'l'},
                  str(game_id)+'v': {'game_no': game_id,
                                     'team_no': visit_team,
                                     'score': visit_score,
                                     'win': visit_score > local_score,
                                     'home': False,
                                     'team_game_id': str(game_id)+'v'}}

    return game_info, team_games, player_stats


def save_games(league_id, league_name, season, connection, player_stats):
    if not cfg.SILENT_MODE:
        print("Save games...")

    game_ids = []
    num_of_pages = get_pagination(league_id, league_name, season)
    for i in range(1, num_of_pages):
        game_ids += get_game_ids(league_id, league_name, season, i)
    game_ids = remove_existing_keys(dbcfg.GAMES_TABLE_NAME, game_ids)

    if not cfg.SILENT_MODE:
        print("Get games list passed!")

    if len(game_ids) > 0:
        games = {}
        teams_games = {}
        player_stats_games = []
        len_games = len(game_ids)
        for index, game_id in enumerate(game_ids):
            result = get_game_details(game_id)
            if not result:
                continue

            games_info, teams_game, player_stats = result
            games[game_id] = games_info
            games[game_id]['league'] = league_id
            games[game_id]['season'] = season
            games[game_id]['game_no'] = game_id
            teams_games.update(teams_game)
            player_stats_games += player_stats

            if not cfg.SILENT_MODE:
                progress_bar(index+1, len_games, "Get games details")

        if not cfg.SILENT_MODE:
            print("\nGet games details list passed!")

        players_list = list(set([player_stat['player_no'] for player_stat in player_stats_games]))
        players.save_teams(players_list, connection)

        games_data_type = {
            'game_date': 'date',
            'league': 'int',
            'season': 'int',
            'game_no': 'int'
        }

        insert_rows(games, dbcfg.GAMES_TABLE_NAME, connection, data_types=games_data_type)
        insert_rows(teams_games, dbcfg.TEAM_GAMES_TABLE_NAME, connection)

        new_player_stats = {}
        for index, element in enumerate(player_stats_games):
            new_player_stats[index] = element

        insert_rows(new_player_stats, dbcfg.PLAYER_STATS_TABLE_NAME, connection)

    else:
        if not cfg.SILENT_MODE:
            print("No news games")
        else:
            pass


# ----- Tests -----


def test_get_games():
    """ Test functions:

    * get_pagination()

    * get_games_ids()

    * get_game_information()
    """
    assert get_pagination("3", "nba", 2020) == 11

    assert get_game_ids("3", "nba", 2020, 3) == ['645322', '645323', '645324', '645326', '645327', '645328', '645329',
                                         '645330', '645333', '645334', '645335', '645337', '645338', '645339',
                                         '645340', '645341', '645342', '645343', '645345', '645346', '645347',
                                         '645349', '645351', '645352', '645353', '645354', '645355', '645356',
                                         '645357', '645358', '645360', '645361', '645363', '645365', '645366',
                                         '645367', '645368', '645370', '645371', '645372', '645373', '645374',
                                         '645375', '645376', '645377', '645378', '645379', '645381', '645382',
                                         '645383', '645384', '645385', '645386', '645387', '645388', '645389',
                                         '645391', '645392', '645393']

    assert get_game_details(645322) == ['119', '113', 'Jan 13, 2021', '137', '134']

    assert get_game_details(645391) == ['114', '112', 'Jan 22, 2021', '106', '113']

    print('All tests passed!!')
#test_get_games()
