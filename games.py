import pandas as pd
import config.scrapr_config as CFG
from useful_functions import get_source


def get_pagination(league_id, league_name, season):
    """ Returns the number of game pages that exist for a league in a specific season
    """
    url = CFG.GAMES_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    pagination = soup.find_all("a", {"class": CFG.SEARCH_PAGINATION_BY_CLASS})[-1].get_text()
    return int(pagination)


def get_game_ids(league_id, league_name, season, page):
    """ Returns a list with all game IDs from a league, season and page number
    """
    url = CFG.GAMES_PATH.format(league_id, league_name, season) + "/" + str(page)
    soup = get_source(url)

    games = []
    for div in soup.find_all("div", {"class": CFG.SEARCH_GAMES_IDS_BY_CLASS}):
        for link in div.select("a"):
            if CFG.GAME_NAME in link['href']:
                games.append(link['href'].split("/")[CFG.ID_GAME_INDEX])
    return games


def get_game_details(game_id):
    """ returns a list with details (local_team, visit_team, match_date, local_score, visit_score)
        for a given game.
    """
    url = CFG.GAME_PATH.format(game_id)
    soup = get_source(url)

    teams = []
    for team in soup.find_all('a', class_=CFG.SEARCH_GAME_TEAMS_BY_CLASS):
        teams.append(team['href'].split("/")[3])
    local_team, visit_team = teams

    span_info = []
    for div in soup.find_all("div", {"class": CFG.SEARCH_GAME_RESULT_BY_CLASS}):
        for span in div.select('span'):
            span_info.append(span.get_text())

    match_date, teams, status = span_info
    local_score, visit_score = teams.split(" - ")

    headers_team_stats = ["MIN", "2M-2A", "3M-3A", "FG%", "1M-1A", "1%", "Or",
                          "Dr", "Reb", "Ast", "Stl", "Blk", "Fo", "Pts", "Ef"]
    player_stats, count = {}, 0
    for table_team in ["1", "2"]:
        if table_team == "1":
            team_game_id = game_id+'l'
        else:
            team_game_id = game_id + 'v'

        for tr in soup.find("div", class_="home-game__content__team-stats__content-team-"+table_team).select('tbody tr'):
            player_id = tr.select("td a")[0]['href'].split("/")[3]
            stats = []
            for td in tr.find_all("td", class_="right"):
                stats.append(td.get_text())
            table_rows = dict(zip(headers_team_stats, stats))
            table_rows["player_id"] = player_id
            table_rows["team_game_id"] = team_game_id
            player_stats[count] = table_rows
            count += 1

    game_info = {'game_date': match_date}
    team_games = {game_id+'l': {'game_no': game_id,
                                'team_no': local_team,
                                'score': local_score,
                                'win': local_score > visit_score,
                                'home': True},
                  game_id+'v': {'game_no': game_id,
                                'team_no': visit_team,
                                'score': visit_score,
                                'win': visit_score > local_score,
                                'home': False}}

    return game_info, team_games, player_stats


# def get_games_from_league_and_season(league_id, league_name, season):
#     """ Returns a pandas data frame with all game results of a given league in a given season """
#
#     game_ids = []
#     print(f"Get all games in league {league_id},{league_name} from season {season}")
#     num_of_pages = get_pagination(league_id, season)
#     for i in range(1, num_of_pages):
#         game_ids += get_game_ids(league_id, season, i)
#
#     games = {}
#     count, len_all_games = 0, len(game_ids)
#     for game_id in game_ids:
#         count += 1
#         print(f"{count}/{len_all_games}. Game Id {game_id}...")
#         games[game_id] = get_game_details(game_id)
#
#     df_games = pd.DataFrame.from_dict(games, orient='index').reset_index()
#     df_games.columns = ["Id", "Local Team", "Visiting Team", "Date", "Local Score",
#                         "Visiting Score"]
#     df_games["League"] = league_id
#     df_games["Year"] = season
#
#     return df_games


def save_games(league_id, league_name, season):

    game_ids = []
    num_of_pages = get_pagination(league_id, league_name, season)
    for i in range(1, num_of_pages):
        game_ids += get_game_ids(league_id, league_name, season, i)

    games = {}
    teams_games = {}
    for game_id in game_ids:
        games_info, teams_game, player_stats = get_game_details(game_id)
        games[game_id] = games_info
        games[game_id]['league_id'] = league_id
        games[game_id]['season'] = season

        teams_games.update(teams_game)
        break

    print(teams_games)
    print(games)
    print(player_stats)
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
