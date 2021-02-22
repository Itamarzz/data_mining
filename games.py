import pandas as pd
from useful_functions import get_source

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba', 100028: 'basketball-champions-league-americas'}
SCHEDULE_PATH = ROOT + "/basketball/league/{}/{}/{}/schedule"
GAME_PATH = ROOT + "/basketball/game/{}"


def get_pagination(league_id, season):
    """ Returns the number of game pages that exist for a league in a specific season
    """
    url = SCHEDULE_PATH.format(league_id, LEAGUES[league_id], season)
    soup = get_source(url)

    pagination = []
    for div in soup.find_all("a", {"class": "pagination-link"}):
        pagination.append(int(div.get_text()))
    return int(max(pagination))


def get_game_ids(league_id, season, page):
    """ Returns a list with all game IDs from a league, season and page number
    """
    url = SCHEDULE_PATH.format(league_id, LEAGUES[league_id], season) + "/" + str(page)
    soup = get_source(url)

    games = []
    for div in soup.find_all("div", {"class": "home-league__schedule__content__tables__content"}):
        for link in div.select("a"):
            if 'game' in link['href']:
                games.append(link['href'].split("/")[3])
    return games


def get_game_details(game_id):
    """ returns a list with details (local_team, visit_team, match_date, local_score, visit_score)
        for a given game.
    """
    url = GAME_PATH.format(game_id)
    soup = get_source(url)

    teams = []
    for team in soup.find_all('a', class_="home-game__content__result__final-score__team__picture"):
        teams.append(team['href'].split("/")[3])
    local_team, visit_team = teams

    span_info = []
    for div in soup.select('div.home-game__content__result__final-score__score'):
        for span in div.select('span'):
            span_info.append(span.get_text())
    match_date, results, status = span_info
    local_score, visit_score = results.split(" - ")
    return [local_team, visit_team, match_date, local_score, visit_score]


def get_games_from_league_and_season(league_id, season):
    """ Returns a pandas data grame with all game results of a given league in a given season """

    game_ids = []
    print(f"Get all games in league {league_id},{LEAGUES[league_id]} from season {season}")
    num_of_pages = get_pagination(league_id, season)
    for i in range(1, num_of_pages):
        game_ids += get_game_ids(league_id, season, i)

    games = {}
    count, len_all_games = 0, len(game_ids)
    for game_id in game_ids:
        count += 1
        print(f"{count}/{len_all_games}. Game Id {game_id}...")
        games[game_id] = [league_id, season] + get_game_details(game_id)

    df_games = pd.DataFrame.from_dict(games, orient='index').reset_index()
    df_games.columns = ["Id", "League", "Year", "Local Team", "Visiting Team", "Date", "Local Score",
                        "Visiting Score"]
    return df_games

#----- Tests -----

def test_get_games():
    """ Test functions:

    * get_pagination()

    * get_games_ids()

    * get_game_information()
    """
    assert get_pagination(3, 2020) == 8

    assert get_game_ids(3, 2020, 3) == ['645322', '645323', '645324', '645326', '645327', '645328', '645329',
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
# test_get_games()

def main():

    LEAGUE_ID = 100028 # sample league_id
    SEASON = 2019

    df_games = get_games_from_league_and_season(LEAGUE_ID, SEASON)
    print(df_games.sample(5))

if __name__ == '__main__':
    main()
