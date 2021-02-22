import requests
import pandas as pd
from bs4 import BeautifulSoup
from useful_functions import get_all_seasons
from datetime import date

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba', 100028: 'basketball-champions-league-americas'}
SCHEDULES_PATH = ROOT+"/basketball/league/{}/{}/{}/schedule"
SCHEDULE_PATH = ROOT+"/basketball/game/{}"


def get_pagination(league_id, season):
    """ This function returns the number of pages that the league has about games league_id in the season.
    """
    url = SCHEDULES_PATH.format(league_id, LEAGUES[league_id], season)
    response = requests.get(url)
    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination = []
    for div in soup.find_all("a", {"class": "pagination-link"}):
        pagination.append(int(div.get_text()))
    return int(max(pagination))


def get_games_ids(league_id, season, page):
    """ This function returns all the games id of a league for a specific season given a page
    """
    url = SCHEDULES_PATH.format(league_id, LEAGUES[league_id], season) + "/" + str(page)
    response = requests.get(url)
    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    games = []
    for div in soup.find_all("div", {"class": "home-league__schedule__content__tables__content"}):
        for link in div.select("a"):
            if 'game' in link['href']:
                games.append(link['href'].split("/")[3])
    return games


def get_game_information(game_id):
    """EThis function returns information about the game game_id
    """
    url = SCHEDULE_PATH.format(game_id)
    response = requests.get(url)
    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
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


def get_all_games_information_from_league_and_season(league_id, season):
    all_games = []
    print(f"Get all matches in league {league_id},{LEAGUES[league_id]} and season {season}")
    for i in range(1, get_pagination(league_id, season)):
        all_games += get_games_ids(league_id, season, i)

    all_games_with_info = {}
    count, len_all_games = 0, len(all_games)
    for game_id in all_games:
        count += 1
        print(f"{count}/{len_all_games}. Game Id {game_id}...")
        all_games_with_info[game_id] = [league_id, season] + get_game_information(game_id)

    df_games = pd.DataFrame.from_dict(all_games_with_info, orient='index').reset_index()
    df_games.columns = ["Id", "League", "Year", "Local Team", "Visiting Team", "Date", "Local Score",
                        "Visiting Score"]
    return df_games


def main():
    """ Test functions:

    * get_pagination()

    * get_games_ids()

    * get_game_information()
    """
    assert get_pagination(3, 2020) == 8
    assert get_games_ids(3, 2020, 3) == ['645322', '645323', '645324', '645326', '645327', '645328', '645329',
                                         '645330', '645333', '645334', '645335', '645337', '645338', '645339',
                                         '645340', '645341', '645342', '645343', '645345', '645346', '645347',
                                         '645349', '645351', '645352', '645353', '645354', '645355', '645356',
                                         '645357', '645358', '645360', '645361', '645363', '645365', '645366',
                                         '645367', '645368', '645370', '645371', '645372', '645373', '645374',
                                         '645375', '645376', '645377', '645378', '645379', '645381', '645382',
                                         '645383', '645384', '645385', '645386', '645387', '645388', '645389',
                                         '645391', '645392', '645393']
    assert get_game_information(645322) == ['119', '113', 'Jan 13, 2021', '137', '134']
    assert get_game_information(645391) == ['114', '112', 'Jan 22, 2021', '106', '113']
    df_games = get_all_games_information_from_league_and_season(100028, 2019)
    print(df_games.head())
    print('All tests passed!!')


if __name__ == '__main__':
    main()
